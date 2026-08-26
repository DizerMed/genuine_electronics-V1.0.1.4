sed -i 's/  } finally {/  } catch (syncErr) { console.error(syncErr); } finally {/g' src/lib/useSupabase.ts
