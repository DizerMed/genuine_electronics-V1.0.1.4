import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { 
  Users, 
  Search, 
  Eye, 
  ShoppingCart, 
  TrendingUp, 
  Filter, 
  Calendar, 
  Smartphone, 
  Monitor, 
  Tablet, 
  RotateCw, 
  Download, 
  Trash2, 
  AlertCircle, 
  CheckCircle2, 
  Clock, 
  ArrowUpRight, 
  Sparkles, 
  Layers, 
  MessageSquare, 
  HelpCircle,
  X,
  ChevronRight,
  UserCheck,
  Globe,
  Radio
} from 'lucide-react';
import { Product, VisitorLog, VisitorAnalyticsSummary, VisitorInteractionType, formatToGMT3 } from '../types';
import { fetchVisitorSummary, fetchVisitorLogs, triggerVisitorLogsCleanup, exportVisitorLogsToCSV } from '../lib/visitorTrackingService';
import { VisitorActivityHeatmap } from './VisitorActivityHeatmap';
import { TopViewedProductsBreakdown } from './TopViewedProductsBreakdown';

interface AdminVisitorAnalyticsProps {
  products: Product[];
  categories?: any[];
}

export const AdminVisitorAnalytics: React.FC<AdminVisitorAnalyticsProps> = ({
  products = [],
  categories = []
}) => {
  // Timeframe and Filters State
  const [timeframe, setTimeframe] = useState<'today' | 'yesterday' | '7days' | '30days' | '60days'>('30days');
  const [selectedProductId, setSelectedProductId] = useState<string>('ALL');
  const [selectedInteraction, setSelectedInteraction] = useState<VisitorInteractionType | 'ALL'>('ALL');
  const [selectedDevice, setSelectedDevice] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [customStartDate, setCustomStartDate] = useState<string>('');
  const [customEndDate, setCustomEndDate] = useState<string>('');

  // Data State
  const [summary, setSummary] = useState<VisitorAnalyticsSummary | null>(null);
  const [logs, setLogs] = useState<VisitorLog[]>([]);
  const [totalLogsCount, setTotalLogsCount] = useState<number>(0);
  const [isLoadingSummary, setIsLoadingSummary] = useState<boolean>(true);
  const [isLoadingLogs, setIsLoadingLogs] = useState<boolean>(true);
  const [isCleaning, setIsCleaning] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<{ type: 'success' | 'error' | 'info'; text: string } | null>(null);

  // Selected Visitor Journey Modal
  const [selectedVisitorId, setSelectedVisitorId] = useState<string | null>(null);

  // Load Analytics Summary
  const loadSummary = useCallback(async () => {
    setIsLoadingSummary(true);
    try {
      const data = await fetchVisitorSummary(timeframe);
      setSummary(data);
    } catch (err: any) {
      console.error('Error fetching visitor summary:', err);
    } finally {
      setIsLoadingSummary(false);
    }
  }, [timeframe]);

  // Load Filtered Visitor Logs
  const loadLogs = useCallback(async () => {
    setIsLoadingLogs(true);
    try {
      const data = await fetchVisitorLogs({
        timeframe,
        productId: selectedProductId !== 'ALL' ? selectedProductId : undefined,
        interactionType: selectedInteraction !== 'ALL' ? selectedInteraction : undefined,
        deviceType: selectedDevice !== 'ALL' ? selectedDevice : undefined,
        searchQuery: searchQuery.trim() || undefined,
        startDate: customStartDate || undefined,
        endDate: customEndDate || undefined,
        limit: 300
      });
      setLogs(data.logs || []);
      setTotalLogsCount(data.total || 0);
    } catch (err: any) {
      console.error('Error fetching visitor logs:', err);
    } finally {
      setIsLoadingLogs(false);
    }
  }, [timeframe, selectedProductId, selectedInteraction, selectedDevice, searchQuery, customStartDate, customEndDate]);

  // Initial Load and on Filter Change
  useEffect(() => {
    loadSummary();
  }, [loadSummary]);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadLogs();
    }, 250);
    return () => clearTimeout(timer);
  }, [loadLogs]);

  // Handle Manual Purge of Logs Older Than 60 Days (2-Month Retention Spec)
  const handlePurgeLogs = async () => {
    if (!window.confirm('Are you sure you want to purge visitor logs older than 60 days (2 months)? This will free up database space while preserving recent traffic data.')) {
      return;
    }
    setIsCleaning(true);
    try {
      const result = await triggerVisitorLogsCleanup(60);
      setStatusMessage({
        type: 'success',
        text: `Cleanup successful: ${result.deletedCount} expired logs (older than 2 months) were purged.`
      });
      await Promise.all([loadSummary(), loadLogs()]);
    } catch (err: any) {
      setStatusMessage({
        type: 'error',
        text: `Cleanup failed: ${err.message || 'Error executing retention purge'}`
      });
    } finally {
      setIsCleaning(false);
      setTimeout(() => setStatusMessage(null), 5000);
    }
  };

  // Handle CSV Export
  const handleExportCSV = () => {
    if (logs.length === 0) {
      alert('No visitor logs to export with current filters.');
      return;
    }
    exportVisitorLogsToCSV(logs, `genuine_visitor_analytics_${timeframe}_${new Date().toISOString().substring(0, 10)}.csv`);
  };

  // Quick helper to filter by a specific product from the top product table
  const handleQuickFilterProduct = (productId: string) => {
    setSelectedProductId(productId);
    window.scrollTo({ top: 750, behavior: 'smooth' });
  };

  // Quick helper to filter by a specific search keyword from top searches
  const handleQuickFilterSearch = (keyword: string) => {
    setSearchQuery(keyword);
    setSelectedInteraction('SEARCH');
    window.scrollTo({ top: 750, behavior: 'smooth' });
  };

  // Find active product details for banner
  const activeSelectedProduct = useMemo(() => {
    if (!selectedProductId || selectedProductId === 'ALL') return null;
    return products.find(p => p.id === selectedProductId) || null;
  }, [selectedProductId, products]);

  // Selected Visitor Journey events
  const visitorJourneyLogs = useMemo(() => {
    if (!selectedVisitorId) return [];
    return logs
      .filter(l => l.visitorId === selectedVisitorId)
      .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
  }, [selectedVisitorId, logs]);

  // Format interaction badge
  const renderInteractionBadge = (type: VisitorInteractionType) => {
    switch (type) {
      case 'PRODUCT_VIEW':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200/80"><Eye className="w-3 h-3 text-blue-600" /> Product View</span>;
      case 'SEARCH':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200/80"><Search className="w-3 h-3 text-amber-600" /> Search</span>;
      case 'ADD_TO_CART':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/80"><ShoppingCart className="w-3 h-3 text-emerald-600" /> Add to Cart</span>;
      case 'REMOVE_FROM_CART':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200/80">Remove Cart</span>;
      case 'EXPRESS_BUY_OPEN':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200/80"><Sparkles className="w-3 h-3 text-indigo-600" /> Express Buy</span>;
      case 'CHECKOUT_INITIATED':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 border border-purple-200/80">Checkout</span>;
      case 'ORDER_PLACED':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-teal-50 text-teal-800 border border-teal-200/80"><CheckCircle2 className="w-3 h-3 text-teal-600" /> Order Placed</span>;
      case 'CATEGORY_FILTER':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200"><Layers className="w-3 h-3 text-slate-500" /> Category</span>;
      case 'BRAND_FILTER':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-zinc-100 text-zinc-700 border border-zinc-200">Brand</span>;
      case 'WHATSAPP_CLICK':
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-700 border border-green-200/80"><MessageSquare className="w-3 h-3 text-green-600" /> WhatsApp</span>;
      case 'PAGE_VIEW':
      default:
        return <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700 border border-gray-200"><Globe className="w-3 h-3 text-gray-500" /> Page Visit</span>;
    }
  };

  // Device icon helper
  const renderDeviceIcon = (device?: string) => {
    if (device === 'Mobile') return <Smartphone className="w-3.5 h-3.5 text-slate-500" />;
    if (device === 'Tablet') return <Tablet className="w-3.5 h-3.5 text-slate-500" />;
    return <Monitor className="w-3.5 h-3.5 text-slate-500" />;
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header & Retention Notice */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-5 sm:p-6 shadow-sm">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-xl bg-blue-600/10 border border-blue-200 flex items-center justify-center text-blue-600">
                <Users className="w-5 h-5" />
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
                  Visitor & Interaction Analytics
                </h1>
                <p className="text-sm text-slate-500">
                  Track real visitor count, searched keywords, product views, and buyer journeys in real-time.
                </p>
              </div>
            </div>
          </div>

          {/* Action Bar */}
          <div className="flex flex-wrap items-center gap-2.5">
            {/* Timeframe selector */}
            <div className="flex items-center bg-slate-100/80 p-1 rounded-xl border border-slate-200/60 text-xs font-medium text-slate-600">
              <button
                type="button"
                onClick={() => setTimeframe('today')}
                className={`px-3 py-1.5 rounded-lg transition-all ${timeframe === 'today' ? 'bg-white text-blue-600 shadow-sm font-semibold' : 'hover:text-slate-900'}`}
              >
                Today
              </button>
              <button
                type="button"
                onClick={() => setTimeframe('7days')}
                className={`px-3 py-1.5 rounded-lg transition-all ${timeframe === '7days' ? 'bg-white text-blue-600 shadow-sm font-semibold' : 'hover:text-slate-900'}`}
              >
                7 Days
              </button>
              <button
                type="button"
                onClick={() => setTimeframe('30days')}
                className={`px-3 py-1.5 rounded-lg transition-all ${timeframe === '30days' ? 'bg-white text-blue-600 shadow-sm font-semibold' : 'hover:text-slate-900'}`}
              >
                30 Days
              </button>
              <button
                type="button"
                onClick={() => setTimeframe('60days')}
                className={`px-3 py-1.5 rounded-lg transition-all ${timeframe === '60days' ? 'bg-white text-blue-600 shadow-sm font-semibold' : 'hover:text-slate-900'}`}
              >
                60 Days (Max)
              </button>
            </div>

            {/* Refresh Button */}
            <button
              type="button"
              onClick={() => { loadSummary(); loadLogs(); }}
              disabled={isLoadingSummary || isLoadingLogs}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors"
              title="Refresh Analytics Data"
            >
              <RotateCw className={`w-3.5 h-3.5 ${isLoadingSummary || isLoadingLogs ? 'animate-spin text-blue-600' : ''}`} />
              Refresh
            </button>

            {/* Export CSV */}
            <button
              type="button"
              onClick={handleExportCSV}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-slate-900 hover:bg-slate-800 text-white transition-colors shadow-sm"
              title="Export Current Log Results to CSV"
            >
              <Download className="w-3.5 h-3.5" />
              Export CSV
            </button>

            {/* Purge 60+ Days Button */}
            <button
              type="button"
              onClick={handlePurgeLogs}
              disabled={isCleaning}
              className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 transition-colors"
              title="Purge logs older than 60 days to save space"
            >
              <Trash2 className="w-3.5 h-3.5" />
              {isCleaning ? 'Purging...' : 'Purge 60d+ Logs'}
            </button>
          </div>
        </div>

        {/* 2-Month Retention Banner */}
        <div className="mt-4 pt-3 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 font-medium border border-emerald-200/60">
              <CheckCircle2 className="w-3 h-3 text-emerald-600" />
              2-Month Max Retention Active
            </span>
            <span>Logs persist for 60 days maximum and auto-purge to save database space.</span>
          </div>
          <div className="text-slate-400">
            Total stored logs: <strong className="text-slate-700">{summary?.retentionInfo?.totalLogsStored || totalLogsCount}</strong> records
          </div>
        </div>
      </div>

      {/* Status Feedback Toast */}
      {statusMessage && (
        <div className={`p-4 rounded-xl text-sm font-medium flex items-center gap-2 ${
          statusMessage.type === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-rose-50 text-rose-800 border border-rose-200'
        }`}>
          {statusMessage.type === 'success' ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <AlertCircle className="w-4 h-4 text-rose-600" />}
          {statusMessage.text}
        </div>
      )}

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Unique Visitors */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Unique Visitors</span>
            <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl sm:text-3xl font-bold text-slate-900">
              {summary?.uniqueVisitors ?? 0}
            </span>
            <span className="text-xs text-slate-500 font-medium">in window</span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Today: <strong className="text-slate-800">{summary?.uniqueVisitorsToday ?? 0}</strong></span>
            <span>This Week: <strong className="text-slate-800">{summary?.uniqueVisitorsWeek ?? 0}</strong></span>
          </div>
        </div>

        {/* Card 2: Live Visitors & Traffic */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Live Active (15m)</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Radio className="w-4 h-4 animate-pulse" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl sm:text-3xl font-bold text-emerald-600 flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500 animate-ping inline-block" />
              {summary?.liveVisitors15m ?? 0}
            </span>
            <span className="text-xs text-slate-500 font-medium">browsing now</span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Total Visits: <strong className="text-slate-800">{summary?.totalVisits ?? 0}</strong></span>
            <span className="text-emerald-700 font-medium">Real-time sync</span>
          </div>
        </div>

        {/* Card 3: Product Views & Searches */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Products Browsed</span>
            <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
              <Eye className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl sm:text-3xl font-bold text-slate-900">
              {summary?.totalProductViews ?? 0}
            </span>
            <span className="text-xs text-slate-500 font-medium">product views</span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Searches Logged: <strong className="text-amber-700">{summary?.totalSearches ?? 0}</strong></span>
            <span>Add to Cart: <strong className="text-emerald-700">{summary?.totalCartAdds ?? 0}</strong></span>
          </div>
        </div>

        {/* Card 4: Conversion & Buyer Needs */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">View-to-Cart Conversion</span>
            <div className="w-8 h-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-2xl sm:text-3xl font-bold text-purple-700">
              {summary?.conversionRate ?? 0}%
            </span>
            <span className="text-xs text-slate-500 font-medium">conversion rate</span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Cart &rarr; Order: <strong className="text-slate-800">{summary?.cartToOrderRate ?? 0}%</strong></span>
            <span>Orders: <strong className="text-slate-800">{summary?.totalOrdersPlaced ?? 0}</strong></span>
          </div>
        </div>
      </div>

      {/* Visitor Activity Heatmap Section (Peak Hours, Peak Days & Server Load Optimization) */}
      <VisitorActivityHeatmap 
        heatmapData={summary?.activityHeatmap}
        timeframe={timeframe}
        onTimeframeChange={setTimeframe}
        isDark={false}
      />

      {/* Deep Insights Leaderboards: Top Searched Keywords & Most Viewed Products */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Top Search Queries Leaderboard */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 sm:p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
                  <Search className="w-3.5 h-3.5" />
                </div>
                <h3 className="text-base font-bold text-slate-900">Top Search Queries</h3>
              </div>
              <span className="text-xs text-slate-400">Buyer Demand Evaluation</span>
            </div>

            {summary?.topSearches && summary.topSearches.length > 0 ? (
              <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
                {summary.topSearches.slice(0, 8).map((s, idx) => (
                  <div 
                    key={idx}
                    className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 hover:bg-amber-50/50 border border-slate-100 transition-colors group cursor-pointer"
                    onClick={() => handleQuickFilterSearch(s.query)}
                    title={`Click to filter logs for "${s.query}"`}
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <span className="w-5 h-5 rounded-md bg-white border border-slate-200 text-[10px] font-bold text-slate-600 flex items-center justify-center">
                        #{idx + 1}
                      </span>
                      <span className="text-sm font-semibold text-slate-800 truncate group-hover:text-amber-700">
                        {s.query}
                      </span>
                    </div>
                    <div className="flex items-center gap-3 text-xs shrink-0">
                      <span className="font-semibold text-slate-900 bg-white px-2 py-0.5 rounded-md border border-slate-200">
                        {s.count} searches
                      </span>
                      <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-amber-600 group-hover:translate-x-0.5 transition-all" />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-12 text-center text-sm text-slate-400">
                No search queries recorded in this timeframe yet.
              </div>
            )}
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 text-xs text-slate-500 flex items-center justify-between">
            <span>Tip: Click any query to view matching visitor interaction logs below.</span>
          </div>
        </div>

        {/* Right: Top Viewed Products with Search-Query Correlation & Trending Badges */}
        <TopViewedProductsBreakdown
          products={summary?.topProducts || []}
          onSelectProduct={handleQuickFilterProduct}
          onSelectSearchQuery={handleQuickFilterSearch}
          isDark={false}
        />
      </div>

      {/* Device & Daily Trend Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Device Distribution */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
            <Smartphone className="w-4 h-4 text-slate-500" />
            Device Distribution
          </h3>
          <div className="space-y-3">
            {(summary?.deviceBreakdown || []).map((dev) => (
              <div key={dev.device} className="space-y-1">
                <div className="flex justify-between text-xs font-semibold text-slate-700">
                  <span className="flex items-center gap-1.5">
                    {renderDeviceIcon(dev.device)}
                    {dev.device}
                  </span>
                  <span>{dev.count} ({dev.percentage}%)</span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${
                      dev.device === 'Mobile' ? 'bg-blue-600' : dev.device === 'Desktop' ? 'bg-indigo-600' : 'bg-slate-500'
                    }`}
                    style={{ width: `${Math.max(4, dev.percentage)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Product Categories Breakdown */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
            <Layers className="w-4 h-4 text-slate-500" />
            Category Interest Breakdown
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {(summary?.topCategories || []).slice(0, 8).map((cat) => (
              <div key={cat.category} className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <p className="text-xs font-semibold text-slate-900 truncate">{cat.category}</p>
                <p className="text-lg font-bold text-blue-600 mt-1">{cat.count}</p>
                <p className="text-[11px] text-slate-400">{cat.percentage}% of views</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* =========================================================================
          FILTERS BY PRODUCT VIEWED & INTERACTIONS (USER SPECIFICATION)
          ========================================================================= */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-5 sm:p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Filter className="w-4 h-4 text-blue-600" />
              Filter Visitor Activity Logs
            </h2>
            <p className="text-xs text-slate-500">
              Filter by specific product viewed, customer search term, or interaction type.
            </p>
          </div>

          {/* Clear Filters Button */}
          {(selectedProductId !== 'ALL' || selectedInteraction !== 'ALL' || selectedDevice !== 'ALL' || searchQuery) && (
            <button
              type="button"
              onClick={() => {
                setSelectedProductId('ALL');
                setSelectedInteraction('ALL');
                setSelectedDevice('ALL');
                setSearchQuery('');
              }}
              className="inline-flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-800 bg-blue-50 px-2.5 py-1 rounded-lg self-start sm:self-auto"
            >
              <X className="w-3.5 h-3.5" />
              Reset All Filters
            </button>
          )}
        </div>

        {/* Filter Controls Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {/* 1. FILTER BY PRODUCT VIEWED (Searchable Dropdown) */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Filter by Product Viewed
            </label>
            <select
              value={selectedProductId}
              onChange={(e) => setSelectedProductId(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 text-xs rounded-xl px-3 py-2.5 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium"
            >
              <option value="ALL">📦 All Products ({products.length})</option>
              {products.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name.length > 40 ? p.name.substring(0, 40) + '...' : p.name} — TZS {(p.price || 0).toLocaleString()}
                </option>
              ))}
            </select>
          </div>

          {/* 2. FILTER BY INTERACTION TYPE */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Filter by Interaction
            </label>
            <select
              value={selectedInteraction}
              onChange={(e) => setSelectedInteraction(e.target.value as any)}
              className="w-full bg-slate-50 border border-slate-200 text-xs rounded-xl px-3 py-2.5 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium"
            >
              <option value="ALL">⚡ All Interactions</option>
              <option value="PRODUCT_VIEW">👁️ Product Views</option>
              <option value="SEARCH">🔍 Searches Logged</option>
              <option value="ADD_TO_CART">🛒 Add to Cart</option>
              <option value="EXPRESS_BUY_OPEN">⚡ Express Buy Click</option>
              <option value="CHECKOUT_INITIATED">💳 Checkout Initiated</option>
              <option value="ORDER_PLACED">✅ Orders Placed</option>
              <option value="WHATSAPP_CLICK">💬 WhatsApp Inquiries</option>
              <option value="CATEGORY_FILTER">🗂️ Category Filters</option>
              <option value="PAGE_VIEW">🌐 Page Visits</option>
            </select>
          </div>

          {/* 3. FILTER BY DEVICE */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Device Type
            </label>
            <select
              value={selectedDevice}
              onChange={(e) => setSelectedDevice(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 text-xs rounded-xl px-3 py-2.5 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium"
            >
              <option value="ALL">📱 All Devices</option>
              <option value="Mobile">Mobile Phone</option>
              <option value="Desktop">Desktop / Laptop</option>
              <option value="Tablet">Tablet</option>
            </select>
          </div>

          {/* 4. KEYWORD & SEARCH FILTER */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Search Query / Visitor ID
            </label>
            <div className="relative">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search keyword, visitor ID, email..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 text-xs rounded-xl pl-8 pr-3 py-2 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  className="absolute right-2.5 top-2.5 text-slate-400 hover:text-slate-600"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Selected Product Banner Indicator */}
        {activeSelectedProduct && (
          <div className="p-3 rounded-xl bg-blue-50/80 border border-blue-200 flex items-center justify-between gap-3">
            <div className="flex items-center gap-3 min-w-0">
              {activeSelectedProduct.image && (
                <img 
                  src={activeSelectedProduct.image} 
                  alt={activeSelectedProduct.name} 
                  className="w-10 h-10 rounded-lg object-contain bg-white border border-blue-200 p-0.5 shrink-0" 
                  referrerPolicy="no-referrer"
                />
              )}
              <div className="min-w-0">
                <p className="text-xs font-bold text-blue-950 truncate">
                  Filtered by Product: {activeSelectedProduct.name}
                </p>
                <p className="text-[11px] text-blue-700">
                  Category: {activeSelectedProduct.category} • Price: TZS {(activeSelectedProduct.price || 0).toLocaleString()} • Stock: {activeSelectedProduct.stock}
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setSelectedProductId('ALL')}
              className="text-xs font-semibold text-blue-700 hover:text-blue-900 bg-white px-2.5 py-1 rounded-lg border border-blue-200 shadow-2xs shrink-0"
            >
              Clear Product Filter
            </button>
          </div>
        )}
      </div>

      {/* =========================================================================
          DETAILED VISITOR LOGS ACTIVITY TABLE
          ========================================================================= */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="p-4 sm:p-5 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-bold text-slate-900">
              Real Visitor Interaction Stream
            </h3>
            <span className="text-xs font-semibold bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">
              Showing {logs.length} of {totalLogsCount} logs
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Recorded in chronological order (East Africa Time - GMT+3)
          </p>
        </div>

        {isLoadingLogs ? (
          <div className="py-20 text-center">
            <RotateCw className="w-6 h-6 animate-spin text-blue-600 mx-auto mb-2" />
            <p className="text-xs font-medium text-slate-500">Loading visitor logs...</p>
          </div>
        ) : logs.length === 0 ? (
          <div className="py-16 text-center text-slate-500">
            <AlertCircle className="w-8 h-8 text-slate-300 mx-auto mb-2" />
            <p className="text-sm font-semibold text-slate-800">No Visitor Logs Found</p>
            <p className="text-xs text-slate-400 mt-1">
              Try adjusting your filter criteria or timeframe above.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-100">
                  <th className="py-3 px-4">Time (EAT)</th>
                  <th className="py-3 px-4">Visitor & Session</th>
                  <th className="py-3 px-4">Interaction</th>
                  <th className="py-3 px-4">Target Details</th>
                  <th className="py-3 px-4">Device & Browser</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50/60 transition-colors">
                    {/* Timestamp */}
                    <td className="py-3 px-4 whitespace-nowrap text-slate-600 font-mono text-[11px]">
                      {formatToGMT3(log.createdAt)}
                    </td>

                    {/* Visitor ID & User */}
                    <td className="py-3 px-4">
                      <div className="font-mono text-[11px] text-slate-800 font-semibold truncate max-w-[140px]" title={log.visitorId}>
                        {log.visitorId.slice(0, 16)}...
                      </div>
                      {log.userEmail ? (
                        <span className="text-[10px] text-blue-600 font-medium block truncate max-w-[140px]" title={log.userEmail}>
                          {log.userName || log.userEmail}
                        </span>
                      ) : (
                        <span className="text-[10px] text-slate-400">Anonymous Visitor</span>
                      )}
                    </td>

                    {/* Interaction Type Badge */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      {renderInteractionBadge(log.interactionType)}
                    </td>

                    {/* Target Details (Product or Search Query) */}
                    <td className="py-3 px-4">
                      {log.interactionType === 'SEARCH' ? (
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-slate-900 bg-amber-50 text-amber-900 px-2 py-0.5 rounded border border-amber-200">
                            "{log.searchQuery}"
                          </span>
                          <span className="text-[10px] text-slate-400">
                            ({log.searchResultsCount || 0} results)
                          </span>
                        </div>
                      ) : log.productName ? (
                        <div className="flex items-center gap-2 min-w-0 max-w-[280px]">
                          {log.productImage && (
                            <img 
                              src={log.productImage} 
                              alt={log.productName} 
                              className="w-7 h-7 rounded object-contain bg-white border border-slate-200 p-0.5 shrink-0" 
                              referrerPolicy="no-referrer"
                            />
                          )}
                          <div className="min-w-0">
                            <span className="font-semibold text-slate-900 truncate block text-[11px]" title={log.productName}>
                              {log.productName}
                            </span>
                            <span className="text-[10px] text-slate-500">
                              {log.productCategory || 'General'} • TZS {(log.productPrice || 0).toLocaleString()}
                            </span>
                          </div>
                        </div>
                      ) : log.categoryFilter ? (
                        <span className="text-slate-700 font-medium">Category: <strong>{log.categoryFilter}</strong></span>
                      ) : (
                        <span className="text-slate-500 truncate block max-w-[200px]" title={log.pageUrl}>
                          {log.pageUrl || '/'}
                        </span>
                      )}
                    </td>

                    {/* Device & Browser */}
                    <td className="py-3 px-4 whitespace-nowrap">
                      <div className="flex items-center gap-1.5 text-slate-700 font-medium">
                        {renderDeviceIcon(log.deviceType)}
                        <span>{log.deviceType || 'Desktop'}</span>
                      </div>
                      <span className="text-[10px] text-slate-400 block">
                        {log.browser || 'Browser'} • {log.os || 'OS'}
                      </span>
                    </td>

                    {/* Actions: View Journey */}
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <button
                        type="button"
                        onClick={() => setSelectedVisitorId(log.visitorId)}
                        className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-600 hover:text-blue-800 bg-blue-50/80 hover:bg-blue-100 px-2.5 py-1 rounded-lg transition-colors"
                      >
                        Journey
                        <ChevronRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* =========================================================================
          VISITOR JOURNEY MODAL / DRAWER
          ========================================================================= */}
      {selectedVisitorId && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-slate-200 w-full max-w-2xl max-h-[85vh] shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            {/* Modal Header */}
            <div className="p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-sm">
                  <UserCheck className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">
                    Visitor Journey Timeline
                  </h3>
                  <p className="text-xs text-slate-500 font-mono">
                    ID: {selectedVisitorId}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setSelectedVisitorId(null)}
                className="w-8 h-8 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 flex items-center justify-center transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body: Chronological Journey Steps */}
            <div className="p-6 overflow-y-auto space-y-4">
              <p className="text-xs text-slate-500">
                Step-by-step chronology of this visitor's searches, viewed products, and cart actions:
              </p>

              {visitorJourneyLogs.length === 0 ? (
                <div className="py-8 text-center text-xs text-slate-400">
                  No detailed steps found for this visitor in the current cached query.
                </div>
              ) : (
                <div className="relative pl-6 border-l-2 border-blue-200 space-y-6">
                  {visitorJourneyLogs.map((step, idx) => (
                    <div key={step.id} className="relative group">
                      {/* Timeline node */}
                      <div className="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-white border-2 border-blue-600 flex items-center justify-center">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                      </div>

                      <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 space-y-1.5">
                        <div className="flex items-center justify-between text-xs">
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-slate-500">Step {idx + 1}</span>
                            {renderInteractionBadge(step.interactionType)}
                          </div>
                          <span className="text-[11px] font-mono text-slate-400">
                            {formatToGMT3(step.createdAt)}
                          </span>
                        </div>

                        {step.productName && (
                          <div className="flex items-center gap-2 pt-1">
                            {step.productImage && (
                              <img 
                                src={step.productImage} 
                                alt={step.productName} 
                                className="w-8 h-8 rounded object-contain bg-white border border-slate-200 p-0.5" 
                                referrerPolicy="no-referrer"
                              />
                            )}
                            <div>
                              <p className="text-xs font-semibold text-slate-900">{step.productName}</p>
                              <p className="text-[11px] text-slate-500">TZS {(step.productPrice || 0).toLocaleString()}</p>
                            </div>
                          </div>
                        )}

                        {step.searchQuery && (
                          <p className="text-xs text-slate-800">
                            Searched: <strong className="text-amber-800">"{step.searchQuery}"</strong> ({step.searchResultsCount || 0} results)
                          </p>
                        )}

                        {step.categoryFilter && (
                          <p className="text-xs text-slate-700">
                            Selected Category: <strong>{step.categoryFilter}</strong>
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end">
              <button
                type="button"
                onClick={() => setSelectedVisitorId(null)}
                className="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-900 text-white hover:bg-slate-800 transition-colors"
              >
                Close Journey
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
