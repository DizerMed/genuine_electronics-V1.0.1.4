import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "<AuthScreen \n                      theme={effectiveClientTheme}",
    "<Suspense fallback={<div className=\"flex-1 flex items-center justify-center p-12\"><div className=\"w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin\"></div></div>}><AuthScreen \n                      theme={effectiveClientTheme}"
)

content = content.replace(
    "<AuthScreen \n                theme={effectiveAdminTheme}",
    "<Suspense fallback={<div className=\"flex-1 flex items-center justify-center p-12\"><div className=\"w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin\"></div></div>}><AuthScreen \n                theme={effectiveAdminTheme}"
)

# And close the suspense
content = content.replace(
    "setIsAuthModalOpen(false);\n                      }}\n                    />",
    "setIsAuthModalOpen(false);\n                      }}\n                    /></Suspense>"
)

content = content.replace(
    "setCurrentView('client');\n                }}\n              />",
    "setCurrentView('client');\n                }}\n              /></Suspense>"
)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("AuthScreen Suspense applied.")
