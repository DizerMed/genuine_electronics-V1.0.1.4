import re

with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

old_block = """            ) : (
              <motion.div layout className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3 sm:gap-6">
                <AnimatePresence>
                {filteredProducts.slice(0, visibleProductsCount).map((product) => {"""

new_block = """            ) : (
              <div className="w-full flex flex-col gap-6">
              <motion.div layout className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3 sm:gap-6">
                <AnimatePresence>
                {filteredProducts.slice(0, visibleProductsCount).map((product) => {"""
content = content.replace(old_block, new_block)

old_end = """              </motion.div>
              {filteredProducts.length > visibleProductsCount && (
                <div className="mt-8 flex justify-center">"""

new_end = """              </motion.div>
              {filteredProducts.length > visibleProductsCount && (
                <div className="mt-8 flex justify-center">"""

content = content.replace(
"""              )}
            )}
          </>""",
"""              )}
              </div>
            )}
          </>""")

with open('src/components/ClientShop.tsx', 'w') as f:
    f.write(content)
