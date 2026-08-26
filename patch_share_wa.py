import re

with open('src/components/ProductDetailPage.tsx', 'r') as f:
    content = f.read()

# 1. Update handleCopyShare
old_handle = """  const handleCopyShare = () => {
    const shareableUrl = `${window.location.origin}${productPath}`;
    navigator.clipboard.writeText(shareableUrl);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2500);
  };"""

new_handle = """  const handleCopyShare = async () => {
    const shareableUrl = `${window.location.origin}${productPath}`;
    if (navigator.share) {
      try {
        await navigator.share({
          title: product.name,
          text: `Check out ${product.name} on Genuine Electronics Trust`,
          url: shareableUrl,
        });
        return;
      } catch (err) {
        // user cancelled or failed, fallback to clipboard
      }
    }
    navigator.clipboard.writeText(shareableUrl);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2500);
  };"""

content = content.replace(old_handle, new_handle)

# 2. Update out-of-stock contact seller (desktop view)
old_oos_1 = """                    const msg = `Hello, I'm inquiring about the out-of-stock product: ${product.name} (SKU: ${product.sku || product.barcode || 'N/A'}). When will it be available?`;
                    window.open(`https://wa.me/255768929203?text=${encodeURIComponent(msg)}`, '_blank');"""

new_oos_1 = """                    const msg = `Hello, I'm inquiring about the out-of-stock product: ${product.name} (SKU: ${product.sku || product.barcode || 'N/A'}). When will it be available?\\n\\nProduct Link: ${window.location.origin}${productPath}`;
                    window.open(`https://wa.me/255768929203?text=${encodeURIComponent(msg)}`, '_blank');"""
content = content.replace(old_oos_1, new_oos_1)

# 3. Update out-of-stock contact seller (sticky bottom bar)
old_oos_2 = """                    const msg = `Hello, I'm inquiring about the out-of-stock product: ${product.name} (SKU: ${product.sku || product.barcode || 'N/A'}). When will it be available?`;
                    window.open(`https://wa.me/255768929203?text=${encodeURIComponent(msg)}`, '_blank');"""

# Wait, they are exactly the same. Let's see how many occurrences.
content = content.replace(old_oos_1, new_oos_1) # This should replace all if they are exactly the same string.
print("OOS Replacements:", content.count(new_oos_1))

# 4. Update order directly via WhatsApp
old_order = """                  onClick={() => {
                    window.open(`https://wa.me/255768929203?text=${encodeURIComponent(
                      `Hi Genuine Electronics Trust! I want to order ${product.name} (Qty: ${selectedQuantity}, SKU: ${product.sku}) priced at ${formatTZS(product.price * selectedQuantity)}.`
                    )}`, '_blank', 'noreferrer');
                  }}"""

new_order = """                  onClick={() => {
                    const msg = `Hi Genuine Electronics Trust! I want to order ${product.name} (Qty: ${selectedQuantity}, SKU: ${product.sku}) priced at ${formatTZS(product.price * selectedQuantity)}.\\n\\nProduct Link: ${window.location.origin}${productPath}`;
                    window.open(`https://wa.me/255768929203?text=${encodeURIComponent(msg)}`, '_blank', 'noreferrer');
                  }}"""

content = content.replace(old_order, new_order)
print("Order Replacement:", content.count(new_order))

with open('src/components/ProductDetailPage.tsx', 'w') as f:
    f.write(content)

