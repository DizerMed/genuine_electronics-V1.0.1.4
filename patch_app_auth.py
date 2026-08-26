import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = re.sub(
    r'(<AuthScreen[^>]*/>)',
    r'<Suspense fallback={<div className="flex-1 flex items-center justify-center p-12"><div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div></div>}>\1</Suspense>',
    content,
    flags=re.DOTALL
)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("AuthScreen Suspense applied.")
