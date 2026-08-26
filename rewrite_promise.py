import re

with open('src/lib/useSupabase.ts', 'r') as f:
    content = f.read()

# Replace the beginning
content = re.sub(
    r"let syncPromise: Promise<void> \| null = null;\nexport async function processOfflineSyncQueue\(\): Promise<void> \{\n  if \(syncPromise\) return syncPromise;\n  syncPromise = \(async \(\) => \{\n  const queue = getOfflineQueue\(\);\n  if \(queue\.length === 0 \|\| !navigator\.onLine\) return;\n  try \{",
    r"let syncPromise: Promise<void> | null = null;\nexport async function processOfflineSyncQueue(): Promise<void> {\n  if (syncPromise) return syncPromise;\n  syncPromise = (async () => {\n    const queue = getOfflineQueue();\n    if (queue.length === 0 || !navigator.onLine) return;\n    try {",
    content
)

# And replace the end
content = re.sub(
    r"  \} finally \{\n    isSyncingOfflineQueue = false;\n  \}\n\}",
    r"  } finally {\n    syncPromise = null;\n  }\n})();\n  return syncPromise;\n}",
    content
)

with open('src/lib/useSupabase.ts', 'w') as f:
    f.write(content)

