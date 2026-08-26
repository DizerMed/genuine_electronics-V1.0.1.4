import re

with open("src/components/ClientShop.tsx", "r") as f:
    content = f.read()

old_render = """      {window.location.pathname.startsWith('/product/') && !selectedProduct && products.length === 0 ? ("""

new_render = """      {window.location.pathname.startsWith('/product/') && !selectedProduct ? ("""

content = content.replace(old_render, new_render)

with open("src/components/ClientShop.tsx", "w") as f:
    f.write(content)
