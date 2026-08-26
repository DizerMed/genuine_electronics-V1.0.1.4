import re

with open("server.ts", "r") as f:
    content = f.read()

replacement_logic = """    if (req.path.startsWith('/api/') || req.path.startsWith('/static/') || req.path.includes('.')) {
      return next();
    }

    let ogTags = '';
    const productMatch = req.path.match(/^\\/product\\/([^\\/]+)/);
    if (productMatch && productMatch[1]) {
      const targetId = decodeURIComponent(productMatch[1]).toLowerCase();
      const productsList = Object.values(memoryStore['products'] || {});
      const product = productsList.find((p: any) => p.id.toLowerCase() === targetId || (p.sku && p.sku.toLowerCase() === targetId));
      if (product) {
        const storeName = memoryStore['settings']?.['main']?.storeName || 'Genuine Electronics Trust';
        const priceFormatted = `TZS ${Number(product.price).toLocaleString()}`;
        const title = `${product.name} | ${product.brand || 'Genuine'} - ${priceFormatted} | ${storeName}`;
        const description = `Nunua ${product.name} kwa ${priceFormatted} Tanzania. 100% Genuine, Free Delivery Dar es Salaam.`;
        const image = product.image || 'https://ukwkseawcdwbpsjnwrut.supabase.co/storage/v1/object/public/genuine_electronics/Genuine%20Electronics%203D%2002.png';
        
        ogTags = `
    <!-- Dynamic Open Graph & Social Sharing Card -->
    <meta property="og:type" content="product" />
    <meta property="og:site_name" content="${storeName}" />
    <meta property="og:title" content="${title.replace(/"/g, '&quot;')}" />
    <meta property="og:description" content="${description.replace(/"/g, '&quot;')}" />
    <meta property="og:url" content="https://${req.get('host')}${req.originalUrl}" />
    <meta property="og:image" content="${image}" />
    <meta property="og:image:width" content="800" />
    <meta property="og:image:height" content="800" />
    <meta property="og:image:alt" content="${product.name.replace(/"/g, '&quot;')}" />
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="${title.replace(/"/g, '&quot;')}" />
    <meta name="twitter:description" content="${description.replace(/"/g, '&quot;')}" />
    <meta name="twitter:image" content="${image}" />`;
      }
    }
"""

content = content.replace("app.get('*', (req, res) => {", f"app.get('*', (req, res, next) => {{\n{replacement_logic}")

replacement_send = """let html = fs.readFileSync(path.join(distPath, 'index.html'), 'utf-8');
      if (ogTags) {
        html = html.replace(/<!-- Open Graph & Social Sharing Card -->[\\s\\S]*?<!-- Twitter Card -->[\\s\\S]*?<link rel="preconnect"/, `${ogTags}\\n    <link rel="preconnect"`);
      }
      res.send(html);"""

content = content.replace("res.sendFile(path.join(distPath, 'index.html'));", replacement_send)

with open("server.ts", "w") as f:
    f.write(content)
