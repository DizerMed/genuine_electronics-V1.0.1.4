import re

with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

if "import { ImageWithSkeleton }" not in content:
    content = content.replace("import { Breadcrumb, BreadcrumbItem } from './Breadcrumb';", "import { Breadcrumb, BreadcrumbItem } from './Breadcrumb';\nimport { ImageWithSkeleton } from './ImageWithSkeleton';")

# 1. State for visible items
if "const [visibleProductsCount, setVisibleProductsCount]" not in content:
    content = content.replace(
        "const [cart, setCart] = useState<CartItem[]>([]);",
        "const [cart, setCart] = useState<CartItem[]>([]);\n  const [visibleProductsCount, setVisibleProductsCount] = useState(12);"
    )

# 2. Reset visible count on filter/search change
reset_effect = """  useEffect(() => {
    setVisibleProductsCount(12);
  }, [searchTerm, selectedCategory, selectedBrand, dealFilter]);"""
if reset_effect not in content:
    content = content.replace(
        "const [cart, setCart] = useState<CartItem[]>([]);",
        f"const [cart, setCart] = useState<CartItem[]>([]);\n{reset_effect}"
    )

# 3. Replace images
# First img at 1304
old_img1 = '<img src={product.image} alt={product.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />'
new_img1 = '<ImageWithSkeleton src={product.image} alt={product.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 transition-opacity" wrapperClassName="absolute inset-0" />'
content = content.replace(old_img1, new_img1)

# Second img at 1476
old_img2 = """                        <img
                          src={product.image}
                          alt={product.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />"""
new_img2 = """                        <ImageWithSkeleton
                          src={product.image}
                          alt={product.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 transition-opacity"
                          wrapperClassName="absolute inset-0"
                        />"""
content = content.replace(old_img2, new_img2)

# 4. Map only visible products
old_map = "{filteredProducts.map((product) => {"
new_map = "{filteredProducts.slice(0, visibleProductsCount).map((product) => {"
if new_map not in content:
    content = content.replace(old_map, new_map)

# 5. Add "Load More" button
old_end_map = """                    </motion.div>
                  );
                })}
                </AnimatePresence>
              </motion.div>"""
new_end_map = """                    </motion.div>
                  );
                })}
                </AnimatePresence>
              </motion.div>
              {filteredProducts.length > visibleProductsCount && (
                <div className="mt-8 flex justify-center">
                  <button
                    onClick={() => setVisibleProductsCount(prev => prev + 12)}
                    className="bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 px-6 py-3 rounded-xl font-bold transition-colors flex items-center gap-2"
                  >
                    <RefreshCw className="w-4 h-4" /> Load More Products
                  </button>
                </div>
              )}"""
if "Load More Products" not in content:
    content = content.replace(old_end_map, new_end_map)


with open('src/components/ClientShop.tsx', 'w') as f:
    f.write(content)
