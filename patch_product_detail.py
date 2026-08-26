import re

with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    ") : selectedProduct ? (",
    ") : selectedProduct ? ( <Suspense fallback={<div className=\"flex-1 flex items-center justify-center py-24\"><div className=\"w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin\"></div></div>}>"
)

content = content.replace(
    "isInCompare={compareProducts.some((p) => p.id === selectedProduct.id)}\n          categoriesList={categoriesList}\n        />\n      ) : (",
    "isInCompare={compareProducts.some((p) => p.id === selectedProduct.id)}\n          categoriesList={categoriesList}\n        /></Suspense>\n      ) : ("
)

with open('src/components/ClientShop.tsx', 'w') as f:
    f.write(content)

print("ProductDetailPage Suspense applied.")
