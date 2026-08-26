import re

with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

# For each tag, find where it starts and find the matching closing tag or self-closing
def wrap_tag(html, tag):
    # Find all occurrences of <tag
    idx = 0
    while True:
        idx = html.find(f'<{tag}', idx)
        if idx == -1:
            break
        
        # Now find the end of this tag by counting < and >
        # Wait, inside { } we can have < and >, but this is JSX, it's hard to parse perfectly without AST.
        # But for these specific modals, they usually end with /> and we can just search for />
        # Let's find the matching />
        # However, they might have arrow functions inside props: onChange={(e) => ...}
        # Let's just find the exact string to replace.
        idx += 1

tags = ['InvoicePrintModal', 'POSReceiptModal', 'ProductCompareModal', 'CompareFloatingBar', 'ExpressBuyDrawer', 'ReceiptVerificationModal', 'ReviewForm']

