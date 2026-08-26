import re

with open('src/components/CategoryProductsPreviewModal.tsx', 'r') as f:
    content = f.read()

# Add the Duplicate button for Grid view (before Full Edit)
duplicate_btn_grid = """
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          if (onDuplicateProduct) onDuplicateProduct(product);
                        }}
                        className="flex-1 py-1.5 px-3 rounded-xl text-xs font-bold bg-emerald-600/10 hover:bg-emerald-600 text-emerald-600 hover:text-white dark:text-emerald-400 dark:hover:text-white transition-all flex items-center justify-center gap-1.5 shadow-sm active:scale-95"
                        title="Duplicate Product"
                      >
                        <Copy className="w-3.5 h-3.5" />
                        <span>Duplicate</span>
                      </button>
"""
# Find the start of the full edit button in grid view
full_edit_start = content.find("<button", content.find("onEditFullProduct(product);") - 150)
if full_edit_start != -1:
    # insert duplicate button before full edit button
    content = content[:full_edit_start] + duplicate_btn_grid + content[full_edit_start:]

# Find the start of the full edit button in list view
full_edit_start2 = content.find("<button", content.rfind("onEditFullProduct(product);") - 150)
duplicate_btn_list = """
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                if (onDuplicateProduct) onDuplicateProduct(product);
                              }}
                              className="p-1.5 rounded-lg bg-emerald-600/10 hover:bg-emerald-600 text-emerald-600 hover:text-white transition-all"
                              title="Duplicate Product"
                            >
                              <Copy className="w-3.5 h-3.5" />
                            </button>
"""
if full_edit_start2 != -1 and full_edit_start2 != full_edit_start:
    content = content[:full_edit_start2] + duplicate_btn_list + content[full_edit_start2:]

with open('src/components/CategoryProductsPreviewModal.tsx', 'w') as f:
    f.write(content)
