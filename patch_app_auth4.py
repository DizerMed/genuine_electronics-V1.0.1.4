with open('src/App.tsx', 'r') as f:
    content = f.read()

text1 = """                      onCancel={() => {
                        setIsAuthModalOpen(false);
                        setSessionExpiredNotice(null);
                      }}
                    />"""

text2 = """                onCancel={() => {
                  setCurrentView('client');
                  setSessionExpiredNotice(null);
                }}
              />"""

content = content.replace(text1, text1 + "</Suspense>")
content = content.replace(text2, text2 + "</Suspense>")

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("AuthScreen Suspense closing tags applied via EXACT replace.")
