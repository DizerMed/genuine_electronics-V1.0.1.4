import re

with open('src/components/AdminPortal.tsx', 'r') as f:
    content = f.read()

bell_code = """
            <button
              type="button"
              onClick={() => {
                setActiveTab('orders');
              }}
              title="View Pending Orders"
              className={`relative p-2 md:hidden sm:flex rounded-xl border text-xs font-semibold flex items-center justify-center transition-all ${
                isDark 
                  ? 'border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800' 
                  : 'border-slate-200 text-slate-700 hover:text-slate-900 hover:bg-slate-100 shadow-xs'
              }`}
            >
              <Bell className="w-4 h-4 text-amber-500" />
              {(orders?.filter(o => o.status === 'Pending').length || 0) > 0 && (
                <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-red-500 text-white text-[9px] font-bold flex items-center justify-center rounded-full shadow-sm animate-pulse">
                  {(orders?.filter(o => o.status === 'Pending').length || 0) > 9 ? '9+' : (orders?.filter(o => o.status === 'Pending').length || 0)}
                </span>
              )}
            </button>
"""

# Let's add Bell to lucide-react imports if not there
if 'Bell,' not in content and ' Bell ' not in content:
    content = content.replace('BellRing,', 'Bell, BellRing,')
    content = content.replace('import { ', 'import { Bell, ')

# Inject the bell before the "Jump to Client Storefront App" button
content = content.replace(
    "{onSwitchToClient && (",
    bell_code + "\n            {onSwitchToClient && ("
)

with open('src/components/AdminPortal.tsx', 'w') as f:
    f.write(content)

print("Added bell.")
