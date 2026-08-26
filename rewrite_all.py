import re

with open('src/lib/useSupabase.ts', 'r') as f:
    content = f.read()

# Replace the beginning
content = re.sub(
    r"let isSyncingOfflineQueue = false;\nexport async function processOfflineSyncQueue\(\) \{\n  if \(isSyncingOfflineQueue\) return;\n  const queue = getOfflineQueue\(\);\n  if \(queue\.length === 0 \|\| !navigator\.onLine\) return;\n\n  isSyncingOfflineQueue = true;\n  try \{",
    r"let syncPromise: Promise<void> | null = null;\nexport async function processOfflineSyncQueue(): Promise<void> {\n  if (syncPromise) return syncPromise;\n  syncPromise = (async () => {\n    const queue = getOfflineQueue();\n    if (queue.length === 0 || !navigator.onLine) return;\n    try {",
    content
)

# And replace the end
content = re.sub(
    r"  \} finally \{\n    isSyncingOfflineQueue = false;\n  \}\n\}",
    r"  } finally {\n    syncPromise = null;\n  }\n})();\n  return syncPromise;\n}",
    content
)

# Also fix the missing isSyncingOfflineQueue without the empty line
content = re.sub(
    r"let isSyncingOfflineQueue = false;\nexport async function processOfflineSyncQueue\(\) \{\n  if \(isSyncingOfflineQueue\) return;\n  const queue = getOfflineQueue\(\);\n  if \(queue\.length === 0 \|\| !navigator\.onLine\) return;\n  isSyncingOfflineQueue = true;\n  try \{",
    r"let syncPromise: Promise<void> | null = null;\nexport async function processOfflineSyncQueue(): Promise<void> {\n  if (syncPromise) return syncPromise;\n  syncPromise = (async () => {\n    const queue = getOfflineQueue();\n    if (queue.length === 0 || !navigator.onLine) return;\n    try {",
    content
)

# Fix the end if it has extra braces from my previous messed up patch
content = re.sub(
    r"  \} finally \{\n    syncPromise = null;\n  \}\n\}\)\(\);\n  return syncPromise;\n\}",
    r"  } finally {\n    syncPromise = null;\n  }\n})();\n  return syncPromise;\n}",
    content
)

with open('src/lib/useSupabase.ts', 'w') as f:
    f.write(content)

