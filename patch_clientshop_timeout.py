import re

with open("src/components/ClientShop.tsx", "r") as f:
    content = f.read()

old_state = """  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);"""
new_state = """  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [deepLinkFailed, setDeepLinkFailed] = useState(false);"""

content = content.replace(old_state, new_state)

old_effect = """      // 3. Reset product state if navigating to root/home
      if (!targetId && !categoryMatch && (pathname === '/' || pathname === '')) {
        setSelectedProduct(null);
      }
    };

    handleUrlRouting();"""

new_effect = """      // 3. Reset product state if navigating to root/home
      if (!targetId && !categoryMatch && (pathname === '/' || pathname === '')) {
        setSelectedProduct(null);
      }
      
      // Handle timeout for deep links
      if (targetId && !selectedProduct) {
        setTimeout(() => setDeepLinkFailed(true), 4000);
      }
    };

    handleUrlRouting();"""

content = content.replace(old_effect, new_effect)

old_render = """      {window.location.pathname.startsWith('/product/') && !selectedProduct ? ("""
new_render = """      {window.location.pathname.startsWith('/product/') && !selectedProduct && !deepLinkFailed ? ("""

content = content.replace(old_render, new_render)

with open("src/components/ClientShop.tsx", "w") as f:
    f.write(content)
