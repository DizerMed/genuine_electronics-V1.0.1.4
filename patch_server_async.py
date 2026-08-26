import re

with open("server.ts", "r") as f:
    content = f.read()

# Make the catchall route async
content = content.replace("app.get('*', (req, res, next) => {", "app.get('*', async (req, res, next) => {")

# Update the product search logic
old_logic = """const targetId = decodeURIComponent(productMatch[1]).toLowerCase();
      const productsList = Object.values(memoryStore['products'] || {});
      const product = productsList.find((p: any) => p.id.toLowerCase() === targetId || (p.sku && p.sku.toLowerCase() === targetId));
      if (product) {"""

new_logic = """const targetId = decodeURIComponent(productMatch[1]).toLowerCase();
      const productsList = Object.values(memoryStore['products'] || {});
      let product = productsList.find((p: any) => p.id.toLowerCase() === targetId || (p.sku && p.sku.toLowerCase() === targetId));
      
      if (!product) {
        const supabase = getSupabaseAdmin();
        if (supabase) {
          try {
            // First try by ID if it looks like a UUID
            let query = supabase.from('products').select('*');
            if (targetId.length > 20) {
              query = query.eq('id', targetId);
            } else {
              query = query.ilike('sku', targetId);
            }
            const { data } = await query.maybeSingle();
            if (data) {
              product = normalizeFromSupabase('products', data);
            }
          } catch (e) {
            console.error('Error fetching product for OG tags', e);
          }
        }
      }

      if (product) {"""

content = content.replace(old_logic, new_logic)

with open("server.ts", "w") as f:
    f.write(content)
