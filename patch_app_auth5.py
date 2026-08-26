import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Look for exactly:
#                }}
#               />
#             )
#           )}
# and replace with:
#                }}
#               /></Suspense>
#             )
#           )}

content = re.sub(
    r'(setCurrentView\(\'client\'\);\s+setSessionExpiredNotice\(null\);\s+\}\}\s+/>)',
    r'\1</Suspense>',
    content
)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("AuthScreen Suspense closing tags applied via EXACT replace.")
