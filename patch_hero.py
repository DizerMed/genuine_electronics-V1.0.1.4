import re
with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

old_hero = """            <img
              src={storeSettings?.heroImage || "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=800"}
              alt="Hero Products"
              className="w-full h-auto max-h-[480px] object-contain drop-shadow-xl mx-auto"
            />"""

new_hero = """            <ImageWithSkeleton
              src={storeSettings?.heroImage || "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=800"}
              alt="Hero Products"
              className="w-full h-auto max-h-[480px] object-contain drop-shadow-xl mx-auto"
              wrapperClassName="w-full h-auto max-h-[480px] mx-auto bg-transparent"
            />"""
content = content.replace(old_hero, new_hero)

with open('src/components/ClientShop.tsx', 'w') as f:
    f.write(content)
