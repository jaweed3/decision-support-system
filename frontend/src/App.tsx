import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Cpu, Database, Zap, Search, MessageSquare, Monitor, CheckCircle, ArrowRightLeft, TrendingUp, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// API Configuration
const API_URL = 'http://localhost:8000';

interface Laptop {
  id: number;
  model_name: string;
  brand: string;
  price: number;
  used_price: number;
  ram_gb: number;
  ssd_gb: number;
  spec_score: number;
  no_of_cores: number;
  topsis_score: number;
  rank: number;
}

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Laptop[]>([]);
  const [aiSummary, setAiSummary] = useState('');
  const [viewMode, setViewMode] = useState<'new' | 'used'>('new');

  const handleConsult = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    setResults([]);
    try {
      const response = await axios.post(`${API_URL}/consult?query=${encodeURIComponent(query)}`);
      setResults(response.data.recommendations);
      setAiSummary(response.data.ai_summary);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-slate-200 p-4 md:p-8 font-sans selection:bg-primary/30">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/5 blur-[120px] rounded-full"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/5 blur-[120px] rounded-full"></div>
      </div>

      {/* Header */}
      <header className="max-w-7xl mx-auto mb-12 flex flex-col md:flex-row justify-between items-center gap-6">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-4"
        >
          <div className="p-3 bg-gradient-to-br from-primary to-secondary rounded-2xl shadow-neon group">
            <Zap className="text-slate-950 group-hover:scale-110 transition-transform" size={28} />
          </div>
          <div>
            <h1 className="text-4xl font-black tracking-tighter neon-text bg-clip-text text-transparent bg-gradient-to-r from-primary to-white">NEON-DECISION</h1>
            <p className="text-[10px] text-primary tracking-[0.3em] uppercase font-bold opacity-80">Advanced AI Hardware Advisor</p>
          </div>
        </motion.div>
        
        <div className="flex bg-slate-900/50 p-1 rounded-xl border border-slate-800 backdrop-blur-md">
          <button 
            onClick={() => setViewMode('new')}
            className={`px-6 py-2 rounded-lg text-sm font-bold transition-all ${viewMode === 'new' ? 'bg-primary text-slate-950 shadow-neon' : 'text-slate-400 hover:text-white'}`}
          >
            NEW UNITS
          </button>
          <button 
            onClick={() => setViewMode('used')}
            className={`px-6 py-2 rounded-lg text-sm font-bold transition-all ${viewMode === 'used' ? 'bg-accent text-white shadow-[0_0_15px_rgba(244,114,182,0.4)]' : 'text-slate-400 hover:text-white'}`}
          >
            USED / PRE-OWNED
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto">
        {/* Terminal Input */}
        <section className="mb-16">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass neon-border rounded-2xl p-8 shadow-2xl relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <Search size={120} />
            </div>
            <div className="flex items-center gap-3 mb-6 text-primary font-mono text-sm">
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
              <span className="tracking-widest">NEURAL_INTERFACE_v2.0: ACTIVE</span>
            </div>
            <form onSubmit={handleConsult} className="relative z-10">
              <div className="flex flex-col md:flex-row gap-4">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Describe your needs (e.g., 'Video editing laptop under 20k with 16GB RAM')"
                  className="flex-1 bg-slate-950/80 border border-slate-700 rounded-xl py-5 px-6 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all text-xl font-medium placeholder:text-slate-600"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="md:w-48 bg-gradient-to-r from-primary to-cyan-400 text-slate-950 font-black rounded-xl hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-3 disabled:opacity-50 shadow-neon py-5"
                >
                  {loading ? (
                    <div className="w-6 h-6 border-4 border-slate-950/30 border-t-slate-950 rounded-full animate-spin"></div>
                  ) : (
                    <>
                      <Zap size={20} />
                      <span>ANALYZING</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </motion.div>
        </section>

        <AnimatePresence>
          {results.length > 0 && (
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
              {/* AI Insight Side Panel */}
              <motion.div
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                className="lg:col-span-1 space-y-6"
              >
                <div className="glass border-secondary/30 rounded-2xl p-6 relative overflow-hidden group">
                  <div className="absolute -right-4 -top-4 w-24 h-24 bg-secondary/10 rounded-full blur-2xl group-hover:bg-secondary/20 transition-all"></div>
                  <h2 className="text-lg font-black mb-4 flex items-center gap-3 text-secondary tracking-tighter">
                    <MessageSquare size={22} />
                    AI VERDICT
                  </h2>
                  <div className="relative">
                    <div className="absolute -left-3 top-0 bottom-0 w-1 bg-gradient-to-b from-secondary to-transparent rounded-full opacity-50"></div>
                    <p className="text-slate-300 leading-relaxed text-sm font-medium pl-4 italic">
                      "{aiSummary}"
                    </p>
                  </div>
                  
                  <div className="mt-8 space-y-4">
                    <div className="p-4 bg-slate-900/50 rounded-xl border border-slate-800">
                      <div className="flex items-center gap-2 text-xs font-bold text-slate-400 mb-2">
                        <TrendingUp size={14} />
                        EFFICIENCY RATING
                      </div>
                      <div className="text-2xl font-black text-white tracking-tighter">98.4%</div>
                    </div>
                  </div>
                </div>

                <div className="glass border-slate-800 rounded-2xl p-6">
                  <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
                    <Database size={14} />
                    ALGO_WEIGHTS
                  </h3>
                  <div className="space-y-6">
                    {[
                      { label: 'PRICE', value: 30, color: 'bg-primary' },
                      { label: 'PERFORMANCE', value: 40, color: 'bg-secondary' },
                      { label: 'DURABILITY', value: 30, color: 'bg-accent' },
                    ].map((item) => (
                      <div key={item.label}>
                        <div className="flex justify-between text-[10px] font-black mb-2 tracking-widest uppercase">
                          <span className="text-slate-400">{item.label}</span>
                          <span className="text-white">{item.value}%</span>
                        </div>
                        <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                          <motion.div 
                            initial={{ width: 0 }}
                            animate={{ width: `${item.value}%` }}
                            transition={{ duration: 1, ease: "easeOut" }}
                            className={`${item.color} h-full`}
                          ></motion.div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>

              {/* Main Results Grid */}
              <div className="lg:col-span-3">
                <div className="flex items-center justify-between mb-8">
                  <h2 className="text-2xl font-black flex items-center gap-3 tracking-tighter">
                    <div className={`p-1.5 rounded-lg ${viewMode === 'new' ? 'bg-primary/20' : 'bg-accent/20'}`}>
                      <CheckCircle className={viewMode === 'new' ? 'text-primary' : 'text-accent'} size={24} />
                    </div>
                    {viewMode === 'new' ? 'RECOMMENDED NEW UNITS' : 'VALUE USED ALTERNATIVES'}
                  </h2>
                  <div className="text-xs font-mono text-slate-500">
                    MATCHED_RECORDS: {results.length}
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {results.map((laptop, idx) => (
                    <motion.div
                      key={laptop.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className={`glass border-slate-800 rounded-3xl p-6 hover:translate-y-[-4px] transition-all group relative overflow-hidden ${idx === 0 ? 'ring-2 ring-primary/30 bg-primary/5' : ''}`}
                    >
                      {idx === 0 && (
                        <div className="absolute top-0 right-0 px-4 py-1 bg-primary text-slate-950 text-[10px] font-black uppercase tracking-widest rounded-bl-xl shadow-neon">
                          Best Match
                        </div>
                      )}
                      
                      <div className="flex justify-between items-start mb-6">
                        <div>
                          <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">{laptop.brand}</p>
                          <h3 className="text-lg font-bold leading-tight group-hover:text-primary transition-colors pr-8">{laptop.model_name}</h3>
                        </div>
                        <div className="flex flex-col items-end">
                           <div className="text-2xl font-black text-white tracking-tighter">
                              ₹{(viewMode === 'new' ? laptop.price : laptop.used_price).toLocaleString()}
                           </div>
                           <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                              {viewMode === 'new' ? 'Market Price' : 'Approx. Used'}
                           </p>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3 mb-6">
                        <div className="bg-slate-900/80 rounded-2xl p-3 border border-slate-800/50 flex items-center gap-3">
                          <Cpu size={16} className="text-primary" />
                          <div>
                            <p className="text-[10px] text-slate-500 font-bold uppercase">CPU Cores</p>
                            <p className="text-sm font-bold text-white">{laptop.no_of_cores}</p>
                          </div>
                        </div>
                        <div className="bg-slate-900/80 rounded-2xl p-3 border border-slate-800/50 flex items-center gap-3">
                          <Database size={16} className="text-secondary" />
                          <div>
                            <p className="text-[10px] text-slate-500 font-bold uppercase">Memory</p>
                            <p className="text-sm font-bold text-white">{laptop.ram_gb}GB</p>
                          </div>
                        </div>
                        <div className="bg-slate-900/80 rounded-2xl p-3 border border-slate-800/50 flex items-center gap-3">
                          <Monitor size={16} className="text-accent" />
                          <div>
                            <p className="text-[10px] text-slate-500 font-bold uppercase">Storage</p>
                            <p className="text-sm font-bold text-white">{laptop.ssd_gb}GB</p>
                          </div>
                        </div>
                        <div className="bg-slate-900/80 rounded-2xl p-3 border border-slate-800/50 flex items-center gap-3">
                          <Zap size={16} className="text-yellow-400" />
                          <div>
                            <p className="text-[10px] text-slate-500 font-bold uppercase">Score</p>
                            <p className="text-sm font-bold text-white">{laptop.spec_score}</p>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-4 border-t border-slate-800">
                        <div className="flex items-center gap-2">
                           <div className="w-10 h-2 bg-slate-800 rounded-full overflow-hidden">
                              <div className="bg-primary h-full" style={{ width: `${laptop.topsis_score * 100}%` }}></div>
                           </div>
                           <span className="text-[10px] font-mono text-slate-400">Ci: {laptop.topsis_score.toFixed(4)}</span>
                        </div>
                        <button className="text-[10px] font-black text-primary hover:text-white uppercase tracking-widest flex items-center gap-1 transition-colors">
                          View Details <ArrowRightLeft size={10} />
                        </button>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </AnimatePresence>

        {/* Placeholder for Initial State */}
        {!results.length && !loading && (
           <motion.div 
             initial={{ opacity: 0 }}
             animate={{ opacity: 1 }}
             className="text-center py-20"
           >
              <div className="w-20 h-20 bg-slate-900 rounded-3xl border border-slate-800 flex items-center justify-center mx-auto mb-6">
                <Monitor size={40} className="text-slate-700" />
              </div>
              <h3 className="text-xl font-bold text-slate-500 mb-2 tracking-tight">Awaiting Neural Input</h3>
              <p className="text-sm text-slate-600 max-w-xs mx-auto">Describe your dream laptop or budget constraints to begin the AI analysis.</p>
           </motion.div>
        )}
      </main>

      {/* Footer Info */}
      <footer className="max-w-7xl mx-auto mt-32 py-12 border-t border-slate-900/50 flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="text-[10px] font-black text-slate-600 uppercase tracking-[0.3em]">
          NEON DECISION // 2026_PROTOCOL_ALPHA
        </div>
        <div className="flex gap-8 text-[10px] font-black text-slate-500 uppercase tracking-widest">
           <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-500/50 animate-pulse"></div>
              SERVER_ONLINE
           </div>
           <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary/50"></div>
              TOPSIS_ACTIVE
           </div>
           <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-secondary/50"></div>
              GEMINI_AI_CONNECTED
           </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
