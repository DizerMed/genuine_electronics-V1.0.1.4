with open('src/components/CategoryProductsPreviewModal.tsx', 'r') as f:
    content = f.read()

duplicate_btn_grid = """
                      <button
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
content = content.replace('                      <button', duplicate_btn_grid, 1)

duplicate_btn_list = """
                            <button
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
content = content.replace('                            <button', duplicate_btn_list, 1)

with open('src/components/CategoryProductsPreviewModal.tsx', 'w') as f:
    f.write(content)
