import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# The missing closing Suspense tags for AuthScreen
# Let's find exactly the AuthScreen in client and admin.
# 1. Client side AuthScreen:
content = re.sub(
    r'(<Suspense[^>]*><AuthScreen[^>]*theme=\{effectiveClientTheme\}.*?/>)',
    r'\1</Suspense>',
    content,
    flags=re.DOTALL
)

# 2. Admin side AuthScreen:
content = re.sub(
    r'(<Suspense[^>]*><AuthScreen[^>]*theme=\{effectiveAdminTheme\}.*?/>)',
    r'\1</Suspense>',
    content,
    flags=re.DOTALL
)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("AuthScreen Suspense closing tags applied.")
