import os
import textwrap

base_dir = r'c:\Users\welcome\OneDrive\Desktop\AI WorldSim\frontend\src'
dirs = ['components', 'pages', 'charts', 'simulation', 'agents', 'experiments', 'analytics', 'services', 'hooks', 'types', 'utils']
for d in dirs: os.makedirs(os.path.join(base_dir, d), exist_ok=True)

with open(os.path.join(base_dir, 'components', 'Layout.tsx'), 'w') as f:
    f.write(textwrap.dedent('''\
        import React from 'react';
        import { Link, useLocation } from 'react-router-dom';
        import { Activity, Map, Users, DollarSign, BookOpen, Heart, MessageSquare, Shield, FileText, BarChart2, FlaskConical, LayoutDashboard, Settings } from 'lucide-react';
        import SimulationControls from './SimulationControls';

        const navItems = [
            { name: 'Overview', path: '/', icon: LayoutDashboard },
            { name: 'Live Simulation', path: '/simulation', icon: Map },
            { name: 'AI Agents', path: '/agents', icon: Users },
            { name: 'Economy', path: '/economy', icon: DollarSign },
            { name: 'Education', path: '/education', icon: BookOpen },
            { name: 'Healthcare', path: '/healthcare', icon: Heart },
            { name: 'Social', path: '/social', icon: MessageSquare },
            { name: 'Safety & Gov', path: '/safety', icon: Shield },
            { name: 'Event Logs', path: '/events', icon: FileText },
            { name: 'Analytics', path: '/analytics', icon: BarChart2 },
            { name: 'Experiments', path: '/experiments', icon: FlaskConical },
            { name: 'Final Report', path: '/report', icon: FileText }
        ];

        export default function Layout({ children }: { children: React.ReactNode }) {
            const location = useLocation();
            
            return (
                <div className="flex h-screen bg-slate-50 text-slate-800 font-sans">
                    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col shadow-xl z-20">
                        <div className="p-6 pb-2">
                            <h1 className="text-2xl font-black text-white flex items-center gap-2">
                                <Activity className="text-indigo-500" /> WorldSim
                            </h1>
                            <p className="text-[10px] text-slate-500 mt-2 uppercase tracking-widest font-bold">Research Platform</p>
                        </div>
                        <nav className="flex-1 overflow-y-auto py-4 space-y-1 px-3 custom-scrollbar mt-4">
                            {navItems.map(item => {
                                const Icon = item.icon;
                                const active = location.pathname === item.path;
                                return (
                                    <Link key={item.name} to={item.path} 
                                        className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${active ? 'bg-indigo-600 text-white font-medium shadow-md shadow-indigo-900/50' : 'hover:bg-slate-800 hover:text-white'}`}>
                                        <Icon size={18} className={active ? 'text-indigo-200' : 'text-slate-500'} />
                                        {item.name}
                                    </Link>
                                )
                            })}
                        </nav>
                    </aside>
                    <div className="flex-1 flex flex-col min-w-0 bg-slate-50 relative">
                        <header className="bg-white border-b border-slate-200 h-16 flex items-center px-6 shrink-0 z-10 shadow-sm justify-end">
                            <SimulationControls />
                        </header>
                        <main className="flex-1 overflow-auto p-8 relative">
                            <div className="max-w-7xl mx-auto h-full">
                                {children}
                            </div>
                        </main>
                    </div>
                </div>
            );
        }
    '''))

with open(os.path.join(base_dir, 'components', 'SimulationControls.tsx'), 'w') as f:
    f.write(textwrap.dedent('''\
        import React, { useState, useEffect } from 'react';
        import axios from 'axios';
        import { Play, Pause, Square, SkipForward, RefreshCw } from 'lucide-react';

        const API_BASE_URL = 'http://localhost:8000/api';

        export default function SimulationControls() {
            const [status, setStatus] = useState<any>(null);

            const fetchStatus = async () => {
                try {
                    const res = await axios.get(`${API_BASE_URL}/simulation/status`);
                    setStatus(res.data);
                } catch (error) {
                    console.error(error);
                }
            };

            useEffect(() => {
                fetchStatus();
                const interval = setInterval(fetchStatus, 1000);
                return () => clearInterval(interval);
            }, []);

            const action = async (cmd: string) => {
                await axios.post(`${API_BASE_URL}/simulation/control`, { action: cmd });
                fetchStatus();
            };

            if (!status) return <div className="text-sm text-slate-500 animate-pulse font-medium">Connecting to Simulation Engine...</div>;

            return (
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 shadow-inner">
                        <button onClick={() => action('start')} className={`p-1.5 rounded-md transition-all ${status.state === 'RUNNING' ? 'bg-white shadow-sm text-emerald-600 font-bold' : 'text-slate-500 hover:bg-slate-200'}`} title="Start"><Play size={16} /></button>
                        <button onClick={() => action('pause')} className={`p-1.5 rounded-md transition-all ${status.state === 'PAUSED' ? 'bg-white shadow-sm text-orange-600 font-bold' : 'text-slate-500 hover:bg-slate-200'}`} title="Pause"><Pause size={16} /></button>
                        <button onClick={() => action('stop')} className="p-1.5 rounded-md text-slate-500 hover:bg-slate-200 hover:text-rose-600" title="Stop"><Square size={16} /></button>
                        <div className="w-px h-5 bg-slate-300 mx-1"></div>
                        <button onClick={() => action('next_tick')} className="p-1.5 rounded-md text-slate-500 hover:bg-slate-200 hover:text-indigo-600" title="Next Tick"><SkipForward size={16} /></button>
                        <button onClick={() => action('reset')} className="p-1.5 rounded-md text-slate-500 hover:bg-slate-200 hover:text-rose-600" title="Reset"><RefreshCw size={16} /></button>
                    </div>
                    <div className="flex flex-col border-l border-slate-200 pl-6">
                        <span className={`text-xs font-black uppercase tracking-widest ${status.state === 'RUNNING' ? 'text-emerald-600' : (status.state === 'PAUSED' ? 'text-orange-500' : 'text-rose-500')}`}>
                            {status.state}
                        </span>
                        <span className="text-sm font-semibold text-slate-700 mt-0.5">Day {status.simulation_day} <span className="text-slate-400 mx-1">•</span> {status.simulation_time}</span>
                    </div>
                    <div className="text-xs font-medium text-slate-500 bg-slate-100 px-3 py-1.5 rounded-md border border-slate-200">
                        Tick <span className="text-slate-700 font-bold">{status.current_tick}</span> <span className="mx-2 text-slate-300">|</span> Speed <span className="text-slate-700 font-bold">{status.speed}x</span>
                    </div>
                </div>
            );
        }
    '''))

with open(os.path.join(base_dir, 'App.tsx'), 'w', encoding='utf-8') as f:
    f.write(textwrap.dedent('''\
        import React from 'react';
        import { BrowserRouter, Routes, Route } from 'react-router-dom';
        import Layout from './components/Layout';
        import Overview from './pages/Overview';
        import LiveSimulation from './pages/LiveSimulation';
        import AgentsList from './pages/AgentsList';
        import Economy from './pages/Economy';
        import Analytics from './pages/Analytics';
        import Experiments from './pages/Experiments';

        function Placeholder({ title }: { title: string }) {
            return <div className="bg-white p-10 rounded-2xl shadow-sm border border-slate-200 max-w-3xl mx-auto mt-10 text-center">
                <div className="w-16 h-16 bg-indigo-50 text-indigo-500 rounded-full flex items-center justify-center mx-auto mb-6">
                    <span className="text-2xl font-bold">WIP</span>
                </div>
                <h2 className="text-2xl font-bold text-slate-800">{title}</h2>
                <p className="text-slate-500 mt-4 leading-relaxed">This module is part of the AI WorldSim Research Platform.<br/>The backend logic is fully integrated, and this UI panel is under active construction.</p>
            </div>;
        }

        export default function App() {
            return (
                <BrowserRouter>
                    <Layout>
                        <Routes>
                            <Route path="/" element={<Overview />} />
                            <Route path="/simulation" element={<LiveSimulation />} />
                            <Route path="/agents" element={<AgentsList />} />
                            <Route path="/economy" element={<Economy />} />
                            <Route path="/education" element={<Placeholder title="Education & Skills Dashboard" />} />
                            <Route path="/healthcare" element={<Placeholder title="Healthcare & Vitality Dashboard" />} />
                            <Route path="/social" element={<Placeholder title="Social Trust & Relationships" />} />
                            <Route path="/safety" element={<Placeholder title="Safety, Governance & Incidents" />} />
                            <Route path="/events" element={<Placeholder title="Global Event Logs" />} />
                            <Route path="/analytics" element={<Analytics />} />
                            <Route path="/experiments" element={<Experiments />} />
                            <Route path="/report" element={<Placeholder title="Final Evaluation Report" />} />
                        </Routes>
                    </Layout>
                </BrowserRouter>
            );
        }
    '''))

print('Base structure generated')
