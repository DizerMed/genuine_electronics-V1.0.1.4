import os
import re

def replace_in_file(filepath, pattern, replacement):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        new_content = re.sub(pattern, replacement, content)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

# ExpressBuyDrawer
replace_in_file(
    'src/components/ExpressBuyDrawer.tsx', 
    r'\s*\|\s*<span>VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}</span>', 
    ''
)
replace_in_file(
    'src/components/ExpressBuyDrawer.tsx', 
    r'<span>VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}</span>\s*\|?', 
    ''
)


# InvoiceGenerator
replace_in_file(
    'src/components/InvoiceGenerator.tsx',
    r'\s*\|\s*VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}',
    ''
)

# POSZReportModal
replace_in_file(
    'src/components/POSZReportModal.tsx',
    r'\s*\|\s*VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}',
    ''
)

# Footer
replace_in_file(
    'src/components/Footer.tsx',
    r'\s*\|\s*VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}',
    ''
)

# ReceiptVerificationModal
replace_in_file(
    'src/components/ReceiptVerificationModal.tsx',
    r'\s*\|\s*<span>VRN: \{store\?.vrn \|\| \'[^\']+\'\}</span>',
    ''
)
replace_in_file(
    'src/components/ReceiptVerificationModal.tsx',
    r'<span>VRN: \{store\?.vrn \|\| \'[^\']+\'\}</span>\s*\|?',
    ''
)


# POSReceiptModal
replace_in_file(
    'src/components/POSReceiptModal.tsx',
    r'\s*\|\s*VRN: \$\{storeSettings\?.vrn \|\| \'[^\']+\'\}',
    ''
)
replace_in_file(
    'src/components/POSReceiptModal.tsx',
    r'\s*\|\s*<span>VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}</span>',
    ''
)
replace_in_file(
    'src/components/POSReceiptModal.tsx',
    r'<span>VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}</span>\s*\|?',
    ''
)


# ClientShop
replace_in_file(
    'src/components/ClientShop.tsx',
    r'\s*\|\s*<span>VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}</span>',
    ''
)
replace_in_file(
    'src/components/ClientShop.tsx',
    r'<span>VRN: \{storeSettings\?.vrn \|\| \'[^\']+\'\}</span>\s*\|?',
    ''
)

