import re

with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

# InvoicePrintModal
content = re.sub(
    r'(<InvoicePrintModal[^>]*isClientView=\{true\}\s*/>)',
    r'<Suspense fallback={null}>\1</Suspense>',
    content
)

# POSReceiptModal
content = re.sub(
    r'(<POSReceiptModal[^>]*/>)',
    r'<Suspense fallback={null}>\1</Suspense>',
    content
)

# CompareFloatingBar
content = re.sub(
    r'(<CompareFloatingBar[^>]*/>)',
    r'<Suspense fallback={null}>\1</Suspense>',
    content
)

# ProductCompareModal
content = re.sub(
    r'(<ProductCompareModal[^>]*/>)',
    r'<Suspense fallback={null}>\1</Suspense>',
    content
)

# ExpressBuyDrawer
content = re.sub(
    r'(<ExpressBuyDrawer[^>]*/>)',
    r'<Suspense fallback={null}>\1</Suspense>',
    content
)

# ReceiptVerificationModal
content = re.sub(
    r'(<ReceiptVerificationModal[^>]*/>)',
    r'<Suspense fallback={null}>\1</Suspense>',
    content
)

# ProductDetailPage (this one is NOT self closing or has complex stuff, let's look at how we can wrap it)
# We can wrap it by finding `<ProductDetailPage` and `          onCategorySelect={` because it's long.
# Actually, the simplest is to find `) : selectedProduct ? (` and replace with `) : selectedProduct ? ( <Suspense fallback={<div className="flex-1 flex items-center justify-center"><div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div></div>}>`
# and find the corresponding `/>` for `ProductDetailPage`. Wait, I think `ProductDetailPage` is self-closing `/>` at the very end of its props.
# Let's check if `ProductDetailPage` has `/>` at the end.
