import re

with open('src/components/AdminPortal.tsx', 'r') as f:
    content = f.read()

# 1. Add Bell icon if missing
if 'BellRing' not in content:
    content = content.replace('BadgeCheck,', 'BadgeCheck, BellRing,')

# 2. Add New Order Notification State
state_injection = """
  const [newOrderAlert, setNewOrderAlert] = useState<Order | null>(null);
  const previousOrdersCountRef = useRef<number>(orders?.length || 0);

  useEffect(() => {
    if (!orders) return;
    if (orders.length > previousOrdersCountRef.current) {
      const recentPendingOrder = [...orders]
        .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
        .find(o => o.status === 'Pending' && (new Date().getTime() - new Date(o.createdAt).getTime() < 5 * 60 * 1000));
        
      if (recentPendingOrder) {
        setNewOrderAlert(recentPendingOrder);
        triggerHaptic('success');
        
        // Modern bell notification sound
        const audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3');
        audio.play().catch(e => console.warn('Audio play failed:', e));
        
        // Auto dismiss after 15s
        setTimeout(() => setNewOrderAlert(null), 15000);
      }
    }
    previousOrdersCountRef.current = orders.length;
  }, [orders]);
"""

if 'const [newOrderAlert' not in content:
    content = content.replace("const [crmToast, setCrmToast] = useState<string | null>(null);", "const [crmToast, setCrmToast] = useState<string | null>(null);\n" + state_injection)

# 3. Add Notification UI at the end of the file
ui_injection = """
      {/* New Order Notification Alert */}
      <AnimatePresence>
        {newOrderAlert && (
          <motion.div
            initial={{ opacity: 0, y: -50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, y: -20, transition: { duration: 0.2 } }}
            className={`fixed top-6 right-6 z-[9999] p-4 rounded-2xl shadow-2xl border flex items-start gap-4 max-w-sm ${isDark ? 'bg-slate-900 border-blue-500/30 shadow-blue-900/20' : 'bg-white border-blue-200 shadow-blue-500/10'}`}
          >
            <div className="w-10 h-10 rounded-full bg-blue-500/20 text-blue-500 flex items-center justify-center shrink-0">
              <BellRing className="w-5 h-5 animate-pulse" />
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-sm mb-1">New Order Received!</h4>
              <p className={`text-xs mb-2 ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
                {newOrderAlert.customerInfo.name} just placed an order for {newOrderAlert.items.reduce((a, c) => a + c.quantity, 0)} items.
              </p>
              <div className="flex gap-2">
                <button 
                  onClick={() => {
                    setActiveTab('orders');
                    setNewOrderAlert(null);
                  }}
                  className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg transition-colors cursor-pointer"
                >
                  View Order
                </button>
                <button 
                  onClick={() => setNewOrderAlert(null)}
                  className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors cursor-pointer ${isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}
                >
                  Dismiss
                </button>
              </div>
            </div>
            <button onClick={() => setNewOrderAlert(null)} className={`absolute top-2 right-2 p-1 rounded-full ${isDark ? 'text-slate-500 hover:text-slate-300 hover:bg-slate-800' : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'} cursor-pointer`}>
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>
"""

if 'New Order Notification Alert' not in content:
    content = content.replace("    </div>\n  );\n};", ui_injection + "\n    </div>\n  );\n};")

with open('src/components/AdminPortal.tsx', 'w') as f:
    f.write(content)

print("Patched AdminPortal.tsx")
