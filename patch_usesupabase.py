import re

with open('src/lib/useSupabase.ts', 'r') as f:
    content = f.read()

# 1. Update PendingSyncItem
content = re.sub(
    r"type: 'ADD' \| 'UPDATE' \| 'DELETE';",
    r"type: 'ADD' | 'UPDATE' | 'DELETE' | 'STOCK_ADJUST';\n  _syncState?: 'NEW' | 'DIRTY';\n  _lastSyncedAt?: string;\n  _localUpdatedAt?: string;\n  _baseSnapshot?: any;",
    content
)

# 2. Update processOfflineSyncQueue
new_sync_logic = """  isSyncingOfflineQueue = true;
  try {
    // Phase 1: PULL changes & tombstones (deletions) from server to purge local zombies
    const uniqueTables = Array.from(new Set(queue.map(q => q.tableName)));
    const deletedIdsByTable = new Set<string>();

    for (const tbl of uniqueTables) {
      try {
        const lastSyncKey = `ge_last_sync_${tbl}`;
        const lastSyncTime = localStorage.getItem(lastSyncKey) || '';
        const pullRes = await fetch(`/api/sync/pull?collection=${encodeURIComponent(tbl)}${lastSyncTime ? `&since=${encodeURIComponent(lastSyncTime)}` : ''}`);
        
        if (pullRes.ok) {
          const pullData = await pullRes.json();
          const cacheKey = `ge_cache_${tbl}`;
          const localCacheRaw = localStorage.getItem(cacheKey);
          let localCache: any[] = localCacheRaw ? JSON.parse(localCacheRaw) : [];

          if (Array.isArray(pullData.deletedIds) && pullData.deletedIds.length > 0) {
            pullData.deletedIds.forEach((d: { id: string }) => {
              deletedIdsByTable.add(`${tbl}:${d.id}`);
              localCache = localCache.filter(item => item.id !== d.id);
            });
          }

          if (Array.isArray(pullData.updatedItems) && pullData.updatedItems.length > 0) {
            pullData.updatedItems.forEach((serverItem: any) => {
              const idx = localCache.findIndex(l => l.id === serverItem.id);
              if (idx >= 0) {
                localCache[idx] = { ...serverItem, _syncState: 'SYNCED', _lastSyncedAt: serverItem.updatedAt || pullData.serverTime };
              } else {
                localCache.push({ ...serverItem, _syncState: 'SYNCED', _lastSyncedAt: serverItem.updatedAt || pullData.serverTime });
              }
            });
          }

          localStorage.setItem(cacheKey, JSON.stringify(localCache));
          if (pullData.serverTime) {
            localStorage.setItem(lastSyncKey, pullData.serverTime);
          }
        }
      } catch (pullErr) {
        console.warn(`[Sync Engine] Could not execute PULL phase for ${tbl}:`, pullErr);
      }
    }

    notifySyncStatus({
      type: 'syncing',
      message: `Syncing ${queue.length > 0 ? queue.length + ' ' : ''}validated offline changes to database`
    });

    const remainingQueue: PendingSyncItem[] = [];

    for (const syncTask of queue) {
      if (deletedIdsByTable.has(`${syncTask.tableName}:${syncTask.id}`) && syncTask.type !== 'DELETE') {
        continue;
      }

      try {
        let res: Response | null = null;
        let lastError: string | undefined = undefined;
        
        const payload = {
          ...syncTask.item,
          _lastSyncedAt: syncTask._lastSyncedAt,
          _localUpdatedAt: syncTask._localUpdatedAt
        };

        if (syncTask.type === 'ADD') {
          res = await fetch(`/api/data/${syncTask.tableName}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        } else if (syncTask.type === 'UPDATE') {
          res = await fetch(`/api/data/${syncTask.tableName}/${syncTask.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
        } else if (syncTask.type === 'DELETE') {
          res = await fetch(`/api/data/${syncTask.tableName}/${syncTask.id}`, {
            method: 'DELETE'
          });
        } else if (syncTask.type === 'STOCK_ADJUST') {
          res = await fetch('/api/inventory/adjust', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              adjustments: Array.isArray(syncTask.item) ? syncTask.item : [syncTask.item]
            })
          });
        } else {
          continue;
        }

        if (res.ok) {
          try {
            const cacheKey = `ge_cache_${syncTask.tableName}`;
            const localCacheRaw = localStorage.getItem(cacheKey);
            if (localCacheRaw) {
              const localCache: any[] = JSON.parse(localCacheRaw);
              const updatedCache = localCache.map(i => i.id === syncTask.id ? { ...i, _syncState: 'SYNCED', _lastSyncedAt: new Date().toISOString() } : i);
              localStorage.setItem(cacheKey, JSON.stringify(updatedCache));
            }
          } catch {}
        } else if (res.status === 409) {
          try {
            const cacheKey = `ge_cache_${syncTask.tableName}`;
            const localRaw = localStorage.getItem(cacheKey);
            if (localRaw) {
              const list = JSON.parse(localRaw);
              const filtered = list.filter((i: any) => i.id !== syncTask.id);
              localStorage.setItem(cacheKey, JSON.stringify(filtered));
            }
          } catch {}
        } else {
          const errText = await res.text().catch(() => 'Unknown error');
          let errJson: any = { error: errText };
          try { errJson = JSON.parse(errText); } catch(e) {}
          lastError = errJson.error || errJson.supabaseError || `HTTP ${res.status}`;
          if (res.status !== 400 || !errJson.error?.includes('Invalid collection')) {
            remainingQueue.push({ ...syncTask, error: lastError, attempts: (syncTask.attempts || 0) + 1 });
          }
        }
      } catch (err: any) {
        remainingQueue.push({ ...syncTask, error: err?.message || 'Network error', attempts: (syncTask.attempts || 0) + 1 });
      }
    }
"""

content = re.sub(
    r"  isSyncingOfflineQueue = true;\n  try \{\n    console\.log\(`Auto Sync Engine: Processing \$\{queue\.length\} pending offline items\.\.\.`\);\n.*?        \}\n      \} catch \(err: any\) \{\n.*?      \}\n    \}",
    new_sync_logic,
    content,
    flags=re.DOTALL
)

# 3. Add queueStockDelta after removeFromOfflineQueue
queue_stock_delta = """}

export function queueStockDelta(adjustments: { productId: string; delta: number; reason?: string; txId?: string }[]) {
  if (!adjustments || adjustments.length === 0) return;
  
  try {
    const cacheKey = 'ge_cache_products';
    const raw = localStorage.getItem(cacheKey);
    if (raw) {
      let list: any[] = JSON.parse(raw);
      adjustments.forEach(adj => {
        list = list.map((p: any) => {
          if (p.id === adj.productId) {
            const currentStock = Number(p.stock) || 0;
            return { ...p, stock: Math.max(0, currentStock + adj.delta), _syncState: 'DIRTY', _localUpdatedAt: new Date().toISOString() };
          }
          return p;
        });
      });
      localStorage.setItem(cacheKey, JSON.stringify(list));
    }
  } catch (err) {}

  addToOfflineQueue({
    id: `stock-adj-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
    tableName: 'products',
    type: 'STOCK_ADJUST',
    item: adjustments,
    timestamp: Date.now()
  });

  processOfflineSyncQueue();
}"""

content = re.sub(
    r"\}\n\n/\*\*\n \* Returns the current online status",
    queue_stock_delta + "\n\n/**\n * Returns the current online status",
    content
)

# 4. Modify addItem to flag as NEW
add_item = """    if (!isOnline()) {
      const raw = localStorage.getItem(CACHE_KEY);
      let list: any[] = raw ? JSON.parse(raw) : [];
      const localCreatedAt = new Date().toISOString();
      const newItemWithMeta = { ...item, id, _syncState: 'NEW', _localCreatedAt: localCreatedAt };
      const existingIndex = list.findIndex((i: any) => i.id === id);
      if (existingIndex >= 0) {
        list[existingIndex] = newItemWithMeta;
      } else {
        list = [newItemWithMeta, ...list];
      }
      localStorage.setItem(CACHE_KEY, JSON.stringify(list));
      setData(list as T[]);

      addToOfflineQueue({
        id,
        tableName,
        type: 'ADD',
        item,
        _syncState: 'NEW',
        _localUpdatedAt: localCreatedAt,
        timestamp: Date.now()
      });"""
      
content = re.sub(
    r"    if \(!isOnline\(\)\) \{\n      const raw = localStorage\.getItem\(CACHE_KEY\);\n      let list: any\[\] = raw \? JSON\.parse\(raw\) : \[\];\n      const existingIndex = list\.findIndex\(\(i: any\) => i\.id === id\);\n      if \(existingIndex >= 0\) \{\n        list\[existingIndex\] = item;\n      \} else \{\n        list = \[item, \.\.\.list\];\n      \}\n      localStorage\.setItem\(CACHE_KEY, JSON\.stringify\(list\)\);\n      setData\(list as T\[\]\);\n\n      addToOfflineQueue\(\{\n        id,\n        tableName,\n        type: 'ADD',\n        item,\n        timestamp: Date\.now\(\)\n      \}\);",
    add_item,
    content,
    flags=re.DOTALL
)

# 5. Modify updateItem to flag as DIRTY
update_item = """    if (!isOnline()) {
      const raw = localStorage.getItem(CACHE_KEY);
      let list: any[] = raw ? JSON.parse(raw) : [];
      const existingItem = list.find((i: any) => i.id === id);
      const lastSyncedAt = existingItem?._lastSyncedAt || existingItem?.updatedAt;
      const localUpdatedAt = new Date().toISOString();
      const newSyncState = existingItem?._syncState === 'NEW' ? 'NEW' : 'DIRTY';
      const updatedItemWithMeta = { ...existingItem, ...item, id, _syncState: newSyncState, _localUpdatedAt: localUpdatedAt };
      list = list.map((i: any) => i.id === id ? updatedItemWithMeta : i);
      localStorage.setItem(CACHE_KEY, JSON.stringify(list));
      setData(list as T[]);

      addToOfflineQueue({
        id,
        tableName,
        type: 'UPDATE',
        item: updatedItemWithMeta,
        _syncState: newSyncState,
        _lastSyncedAt: lastSyncedAt,
        _localUpdatedAt: localUpdatedAt,
        timestamp: Date.now()
      });"""

content = re.sub(
    r"    if \(!isOnline\(\)\) \{\n      const raw = localStorage\.getItem\(CACHE_KEY\);\n      let list: any\[\] = raw \? JSON\.parse\(raw\) : \[\];\n      const existingItem = list\.find\(\(i: any\) => i\.id === id\);\n      list = list\.map\(\(i: any\) => i\.id === id \? \{ \.\.\.i, \.\.\.item \} : i\);\n      localStorage\.setItem\(CACHE_KEY, JSON\.stringify\(list\)\);\n      setData\(list as T\[\]\);\n\n      addToOfflineQueue\(\{\n        id,\n        tableName,\n        type: 'UPDATE',\n        item,\n        timestamp: Date\.now\(\)\n      \}\);",
    update_item,
    content,
    flags=re.DOTALL
)

with open('src/lib/useSupabase.ts', 'w') as f:
    f.write(content)

