import re

with open('src/components/AdminPortal.tsx', 'r') as f:
    content = f.read()

# Add unreadCount state
if 'const [unreadCount, setUnreadCount] = useState(0);' not in content:
    content = content.replace(
        "const [newOrderAlert, setNewOrderAlert] = useState<Order | null>(null);",
        "const [newOrderAlert, setNewOrderAlert] = useState<Order | null>(null);\n  const [unreadCount, setUnreadCount] = useState(0);"
    )

# Replace the useEffect block for previousOrdersCountRef
old_use_effect = """  const previousOrdersCountRef = useRef<number>(orders?.length || 0);

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
  }, [orders]);"""

new_use_effect = """  // Clear unread count when viewing orders
  useEffect(() => {
    if (activeTab === 'orders') {
      setUnreadCount(0);
    }
  }, [activeTab]);

  // Real-time listener for New Orders via SSE
  useEffect(() => {
    const handleLiveEvent = (e: any) => {
      const payload = e.detail;
      if (
        payload &&
        payload.type === 'COLLECTION_UPDATE' &&
        (payload.collection === 'orders' || payload.collection === 'Orders') &&
        payload.action === 'ADD'
      ) {
        const newOrder = payload.item;
        if (newOrder) {
          setNewOrderAlert(newOrder);
          
          setUnreadCount(prev => prev + 1);
          
          triggerHaptic('success');
          
          // Modern bell notification sound
          const audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3');
          audio.play().catch(err => console.warn('Audio play failed:', err));
          
          // Auto dismiss after 15s
          setTimeout(() => setNewOrderAlert(null), 15000);
        }
      }
    };
    
    window.addEventListener('cloud-live-event', handleLiveEvent);
    return () => window.removeEventListener('cloud-live-event', handleLiveEvent);
  }, []);"""

if 'const previousOrdersCountRef =' in content:
    content = content.replace(old_use_effect, new_use_effect)

# Update the Bell icon counter
old_bell_counter = """              <Bell className="w-4 h-4 text-amber-500" />
              {(orders?.filter(o => o.status === 'Pending').length || 0) > 0 && (
                <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-red-500 text-white text-[9px] font-bold flex items-center justify-center rounded-full shadow-sm animate-pulse">
                  {(orders?.filter(o => o.status === 'Pending').length || 0) > 9 ? '9+' : (orders?.filter(o => o.status === 'Pending').length || 0)}
                </span>
              )}"""

new_bell_counter = """              <Bell className={`w-4 h-4 ${unreadCount > 0 ? 'text-amber-500 animate-pulse' : 'text-slate-400'}`} />
              {unreadCount > 0 && (
                <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-red-500 text-white text-[9px] font-bold flex items-center justify-center rounded-full shadow-sm">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              )}"""

if '<Bell className="w-4 h-4 text-amber-500" />' in content:
    content = content.replace(old_bell_counter, new_bell_counter)

# Wait, is there another place where the Bell is used? In the Sidebar maybe?
old_sidebar_bell = """                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ml-auto ${
                  isDark ? 'bg-red-500/20 text-red-400' : 'bg-red-100 text-red-600'
                }`}>
                  {orders.filter(o => o.status === 'Pending').length}
                </span>"""
new_sidebar_bell = """                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ml-auto ${
                  isDark ? 'bg-red-500/20 text-red-400' : 'bg-red-100 text-red-600'
                }`}>
                  {unreadCount > 0 ? unreadCount : orders?.filter(o => o.status === 'Pending').length || 0}
                </span>"""
# We don't necessarily have to touch the sidebar bell if it's fine showing total pending.
# The user specifically complained about the notification counter (which is usually the top bell).

with open('src/components/AdminPortal.tsx', 'w') as f:
    f.write(content)

print("Patched.")
