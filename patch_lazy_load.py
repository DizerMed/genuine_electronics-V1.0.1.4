import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add Suspense and lazy
content = content.replace("import React, { useState, useEffect, useMemo, useCallback } from 'react';",
                          "import React, { useState, useEffect, useMemo, useCallback, lazy, Suspense } from 'react';")

# Remove static imports
imports_to_remove = [
    "import { AdminPortal as AdminApp } from './components/AdminPortal';",
    "import { AuthScreen } from './components/AuthScreen';",
    "import { AIChatWidget } from './components/AIChatWidget';",
    "import { InstallPwaBanner } from './components/InstallPwaBanner';",
    "import { Footer } from './components/Footer';",
    "import { ClientProfileModal } from './components/ClientProfileModal';"
]

for imp in imports_to_remove:
    content = content.replace(imp, "")

# Add lazy imports below the other imports
lazy_imports = """
const AdminApp = lazy(() => import('./components/AdminPortal').then(m => ({ default: m.AdminPortal })));
const AuthScreen = lazy(() => import('./components/AuthScreen').then(m => ({ default: m.AuthScreen })));
const AIChatWidget = lazy(() => import('./components/AIChatWidget').then(m => ({ default: m.AIChatWidget })));
const InstallPwaBanner = lazy(() => import('./components/InstallPwaBanner').then(m => ({ default: m.InstallPwaBanner })));
const Footer = lazy(() => import('./components/Footer').then(m => ({ default: m.Footer })));
const ClientProfileModal = lazy(() => import('./components/ClientProfileModal').then(m => ({ default: m.ClientProfileModal })));
"""

if "const AdminApp = lazy" not in content:
    content = content.replace("export default function App() {", lazy_imports + "\nexport default function App() {")

# Wrap components in Suspense where used
content = content.replace("<Footer categoriesList={categories} storeSettings={storeSettings} />",
                          "<Suspense fallback={null}><Footer categoriesList={categories} storeSettings={storeSettings} /></Suspense>")

content = content.replace("<AIChatWidget />",
                          "<Suspense fallback={null}><AIChatWidget /></Suspense>")

content = content.replace("<InstallPwaBanner />",
                          "<Suspense fallback={null}><InstallPwaBanner /></Suspense>")

content = re.sub(r'(<ClientProfileModal[^>]*/>)', r'<Suspense fallback={null}>\1</Suspense>', content)

# For AdminApp, AuthScreen, we can just wrap the main blocks or they might be conditionally rendered.
# AuthScreen is rendered as: <AuthScreen isOpen={isAuthModalOpen} ... />
content = re.sub(r'(<AuthScreen[^>]*/>)', r'<Suspense fallback={null}>\1</Suspense>', content)

# AdminApp is a bit more complex, it has many props.
admin_app_regex = re.compile(r'(<AdminApp.*?/>)', re.DOTALL)
content = admin_app_regex.sub(r'<Suspense fallback={<div className="flex-1 flex items-center justify-center p-12"><div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div></div>}>\1</Suspense>', content)

with open('src/App.tsx', 'w') as f:
    f.write(content)

print("Lazy loading applied.")
