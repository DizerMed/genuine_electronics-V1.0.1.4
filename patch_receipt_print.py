import re

with open('src/components/ReceiptVerificationModal.tsx', 'r') as f:
    content = f.read()

style_injection = """
      {/* Dedicated Printer-Friendly CSS for exact receipt alignment and stamp positioning */}
      <style>{`
        @media print {
          @page {
            margin: 0;
            size: auto;
          }
          *, *::before, *::after {
            color: #000000 !important;
            border-color: #000000 !important;
            text-shadow: none !important;
            box-shadow: none !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
          body {
            background-color: #ffffff !important;
            color: #000000 !important;
            margin: 0 !important;
            padding: 0 !important;
          }
          body * {
            visibility: hidden;
          }
          .printable-invoice-root, .printable-invoice-root * {
            visibility: visible;
            color: #000000 !important;
            border-color: #000000 !important;
          }
          
          /* Ensures Authentic Blue Ink Stamp keeps its exact color & tilt when printing to color printers/PDFs */
          .printable-invoice-root .official-stamp,
          .printable-invoice-root .official-stamp * {
            color: #0033a0 !important;
            border-color: #0033a0 !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
          
          .printable-invoice-root {
            position: absolute;
            left: 50% !important;
            top: 0 !important;
            transform: translateX(-50%) !important;
            width: ${paperWidth === '58mm' ? '58mm' : '80mm'} !important;
            max-width: 100% !important;
            margin: 0 auto !important;
            padding: 5mm !important;
            background: #ffffff !important;
            color: #000000 !important;
            font-family: 'Courier Prime', Consolas, 'Courier New', 'Roboto Mono', monospace !important;
            font-weight: 700 !important;
            font-size: ${paperWidth === '58mm' ? '10px' : '12px'} !important;
            line-height: 1.2 !important;
            box-shadow: none !important;
            border: none !important;
            border-radius: 0 !important;
          }
          .no-print {
            display: none !important;
          }
        }
      `}</style>
"""

# Only insert if not already present
if 'Dedicated Printer-Friendly CSS for exact receipt alignment' not in content:
    # We will insert it right after the main <div className="fixed inset-0 z-50 ...">
    target_str = '<div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-2 sm:p-4 overflow-y-auto">'
    if target_str in content:
        content = content.replace(target_str, target_str + '\n' + style_injection)
    else:
        print("Could not find target div!")

with open('src/components/ReceiptVerificationModal.tsx', 'w') as f:
    f.write(content)

print("Patched ReceiptVerificationModal.tsx")
