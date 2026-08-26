import re

with open('src/components/CategoryProductsPreviewModal.tsx', 'r') as f:
    content = f.read()

# Add props
content = content.replace("  onEditFullProduct: (product: Product) => void;", "  onEditFullProduct: (product: Product) => void;\n  onDuplicateProduct?: (product: Product) => void;")
content = content.replace("  onEditFullProduct,\n", "  onEditFullProduct,\n  onDuplicateProduct,\n")

if "Copy," not in content:
    content = content.replace("Edit,", "Edit,\n  Copy,")

# Grid duplicate
grid_btn = """<button
                        type="button"
                        onClick={() => {
                          onClose();
                          if (onDuplicateProduct) onDuplicateProduct(product);
                        }}
                        className="flex-1 py-1.5 px-3 rounded-xl text-xs font-bold bg-emerald-600/10 hover:bg-emerald-600 text-emerald-600 hover:text-white dark:text-emerald-400 dark:hover:text-white transition-all flex items-center justify-center gap-1.5 shadow-sm active:scale-95"
                        title="Duplicate Product"
                      >
                        <Copy className="w-3.5 h-3.5" />
                        <span>Duplicate</span>
                      </button>
                      <button"""
content = content.replace("""<button
                        type="button"
                        onClick={() => {
                          onClose();
                          onEditFullProduct(product);""", grid_btn + """
                        type="button"
                        onClick={() => {
                          onClose();
                          onEditFullProduct(product);""")

list_btn = """<button
                              type="button"
                              onClick={() => {
                                onClose();
                                if (onDuplicateProduct) onDuplicateProduct(product);
                              }}
                              className="p-1.5 rounded-lg bg-emerald-600/10 hover:bg-emerald-600 text-emerald-600 hover:text-white transition-all"
                              title="Duplicate Product"
                            >
                              <Copy className="w-3.5 h-3.5" />
                            </button>
                            <button"""

content = content.replace("""<button
                              type="button"
                              onClick={() => {
                                onClose();
                                onEditFullProduct(product);""", list_btn + """
                              type="button"
                              onClick={() => {
                                onClose();
                                onEditFullProduct(product);""")

with open('src/components/CategoryProductsPreviewModal.tsx', 'w') as f:
    f.write(content)
