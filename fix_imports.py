with open('src/components/AdminPortal.tsx', 'r') as f:
    content = f.read()

content = content.replace('import { Bell, ', 'import { ')

if 'import { Bell' not in content:
    content = content.replace("import { BellRing", "import { Bell, BellRing")

with open('src/components/AdminPortal.tsx', 'w') as f:
    f.write(content)

print("Fixed imports.")
