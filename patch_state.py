with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "const isDark = theme === 'dark';",
    "const isDark = theme === 'dark';\n  const [visibleProductsCount, setVisibleProductsCount] = useState(12);"
)

reset_effect = """  useEffect(() => {
    setVisibleProductsCount(12);
  }, [searchTerm, selectedCategory, selectedBrand, dealFilter]);"""
content = content.replace(
    "const [selectedCategory, setSelectedCategory] = useState<Category>('All');",
    f"const [selectedCategory, setSelectedCategory] = useState<Category>('All');\n{reset_effect}"
)

with open('src/components/ClientShop.tsx', 'w') as f:
    f.write(content)
