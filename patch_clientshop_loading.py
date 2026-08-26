import re

with open("src/components/ClientShop.tsx", "r") as f:
    content = f.read()

old_render = """  return (
    <div id="home" className="min-h-screen bg-slate-50 dark:bg-slate-900 pb-24" style={{ fontFamily: storeSettings?.fontFamily || 'inherit' }}>
      {selectedProduct ? ("""

new_render = """  return (
    <div id="home" className="min-h-screen bg-slate-50 dark:bg-slate-900 pb-24" style={{ fontFamily: storeSettings?.fontFamily || 'inherit' }}>
      {window.location.pathname.startsWith('/product/') && !selectedProduct && products.length === 0 ? (
        <div className="flex flex-col items-center justify-center min-h-[60vh] pt-20">
          <div className="w-12 h-12 border-4 border-blue-600/30 border-t-blue-600 rounded-full animate-spin"></div>
          <p className="mt-4 text-slate-500 font-medium">Loading product details...</p>
        </div>
      ) : selectedProduct ? ("""

content = content.replace(old_render, new_render)

with open("src/components/ClientShop.tsx", "w") as f:
    f.write(content)
