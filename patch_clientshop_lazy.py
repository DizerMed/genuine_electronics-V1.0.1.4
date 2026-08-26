import re

with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

# Add Suspense and lazy
content = content.replace("import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';",
                          "import React, { useState, useEffect, useMemo, useRef, useCallback, lazy, Suspense } from 'react';")

# Remove static imports
imports_to_remove = [
    "import { ProductDetailPage } from './ProductDetailPage';",
    "import { InvoicePrintModal } from './InvoicePrintModal';",
    "import { POSReceiptModal } from './POSReceiptModal';",
    "import { ProductCompareModal, CompareFloatingBar } from './ProductCompareModal';",
    "import { ExpressBuyDrawer } from './ExpressBuyDrawer';",
    "import { ReceiptVerificationModal } from './ReceiptVerificationModal';",
    "import { ReviewForm } from './ReviewForm';"
]

for imp in imports_to_remove:
    content = content.replace(imp, "")

# Add lazy imports below the other imports
lazy_imports = """
const ProductDetailPage = lazy(() => import('./ProductDetailPage').then(m => ({ default: m.ProductDetailPage })));
const InvoicePrintModal = lazy(() => import('./InvoicePrintModal').then(m => ({ default: m.InvoicePrintModal })));
const POSReceiptModal = lazy(() => import('./POSReceiptModal').then(m => ({ default: m.POSReceiptModal })));
const ProductCompareModal = lazy(() => import('./ProductCompareModal').then(m => ({ default: m.ProductCompareModal })));
const CompareFloatingBar = lazy(() => import('./ProductCompareModal').then(m => ({ default: m.CompareFloatingBar })));
const ExpressBuyDrawer = lazy(() => import('./ExpressBuyDrawer').then(m => ({ default: m.ExpressBuyDrawer })));
const ReceiptVerificationModal = lazy(() => import('./ReceiptVerificationModal').then(m => ({ default: m.ReceiptVerificationModal })));
const ReviewForm = lazy(() => import('./ReviewForm').then(m => ({ default: m.ReviewForm })));
"""

if "const ProductDetailPage = lazy" not in content:
    # insert before export const ClientShop
    content = content.replace("export const ClientShop", lazy_imports + "\nexport const ClientShop")

# Wrap components in Suspense where used
tags_to_wrap = [
    'ProductDetailPage',
    'InvoicePrintModal',
    'POSReceiptModal',
    'ProductCompareModal',
    'CompareFloatingBar',
    'ExpressBuyDrawer',
    'ReceiptVerificationModal',
    'ReviewForm'
]

# We must be careful because regex on HTML/JSX tags is tricky, 
# but since these are distinct component names we can do `<Component ... />` or `<Component ... >...</Component>`
for tag in tags_to_wrap:
    # Match self-closing and block tags
    # Since these are modals, they are typically self-closing or simple. 
    # Let's just use a simple string replacement approach where possible or regex.
    # Actually, simpler regex: find `<TagName ` or `<TagName>` and wrap it? That's too risky.
    pass

# We will just write a custom replacer in python
def wrap_with_suspense(html, tag_name):
    # This regex is a bit complex but let's try to match the component tags
    # assuming they are properly nested and not nested inside themselves
    # e.g. <ReviewForm ... />
    pattern = r'(<' + tag_name + r'[^>]*?/>)'
    html = re.sub(pattern, r'<Suspense fallback={null}>\1</Suspense>', html)
    
    # Check if there are non-self-closing tags
    pattern2 = r'(<' + tag_name + r'[^>]*?>.*?</' + tag_name + r'>)'
    html = re.sub(pattern2, r'<Suspense fallback={null}>\1</Suspense>', html, flags=re.DOTALL)
    
    return html

for tag in tags_to_wrap:
    content = wrap_with_suspense(content, tag)

with open('src/components/ClientShop.tsx', 'w') as f:
    f.write(content)

print("Lazy loading applied to ClientShop.")
