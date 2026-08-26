with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

old_deals = """              <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 sm:gap-6 lg:gap-8">
                {shuffledProducts
                  .filter(p => p.isOnOffer || (p.originalPrice && p.originalPrice > p.price))
                  .map((product) => {"""
new_deals = """              <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 sm:gap-6 lg:gap-8">
                {shuffledProducts
                  .filter(p => p.isOnOffer || (p.originalPrice && p.originalPrice > p.price))
                  .slice(0, 10)
                  .map((product) => {"""
content = content.replace(old_deals, new_deals)
with open('src/components/ClientShop.tsx', 'w') as f:
    f.write(content)
