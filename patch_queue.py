import re

with open('src/lib/useSupabase.ts', 'r') as f:
    content = f.read()

replacement = """
  const queue = getOfflineQueue();
  queue.push({
    id: `stock-adj-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
    tableName: 'products',
    type: 'STOCK_ADJUST',
    item: adjustments,
    attempts: 0
  });
  saveOfflineQueue(queue);
}
"""

content = re.sub(
    r"  addToOfflineQueue\(\{[\s\S]*?\}\);",
    replacement,
    content
)

with open('src/lib/useSupabase.ts', 'w') as f:
    f.write(content)

