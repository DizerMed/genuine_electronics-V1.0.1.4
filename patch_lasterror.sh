sed -i 's/const remainingQueue: PendingSyncItem\[\] = \[\];/let lastError: string | undefined = undefined;\n    const remainingQueue: PendingSyncItem[] = [];/g' src/lib/useSupabase.ts
