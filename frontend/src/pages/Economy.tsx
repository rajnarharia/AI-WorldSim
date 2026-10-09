import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { DollarSign, Briefcase, Activity, TrendingUp, Building2, ShoppingCart } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const API_BASE_URL = 'http://localhost:8000/api';

export default function Economy() {
    const [eco, setEco] = useState<any>(null);

    useEffect(() => {
        axios.get(`${API_BASE_URL}/dashboards/economy`).then(res => setEco(res.data));
    }, []);

    if (!eco) return <div className="animate-pulse font-medium text-slate-500">Aggregating economic telemetry...</div>;

    const mockTimeSeries = Array.from({length: 24}).map((_, i) => ({
        time: `${i}:00`,
        employment: eco.employment_rate - 5 + Math.random() * 10,
        activity: eco.total_transactions - 100 + Math.random() * 200
    }));

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <header>
                <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><DollarSign className="text-emerald-600"/> Economic Analytics</h1>
                <p className="text-slate-500 mt-1">Deep dive into simulated macro-economic indicators, labor markets, and monetary velocity.</p>
            </header>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <div className="flex items-center justify-between mb-4"><h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs">Employment Rate</h3><Briefcase size={16} className="text-emerald-500"/></div>
                    <div className="text-4xl font-black text-slate-800">{eco.employment_rate}%</div>
                    <div className="mt-2 text-sm text-slate-500 font-medium">{eco.employed_count} active workers</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <div className="flex items-center justify-between mb-4"><h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs">Average Income</h3><DollarSign size={16} className="text-emerald-500"/></div>
                    <div className="text-4xl font-black text-slate-800">${eco.avg_income}</div>
                    <div className="mt-2 text-sm text-slate-500 font-medium">Per employed agent</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <div className="flex items-center justify-between mb-4"><h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs">Active Businesses</h3><Building2 size={16} className="text-emerald-500"/></div>
                    <div className="text-4xl font-black text-slate-800">{eco.business_count}</div>
                    <div className="mt-2 text-sm text-slate-500 font-medium">Corporate entities</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <div className="flex items-center justify-between mb-4"><h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs">Velocity (Tx)</h3><ShoppingCart size={16} className="text-emerald-500"/></div>
                    <div className="text-4xl font-black text-slate-800">{eco.total_transactions}</div>
                    <div className="mt-2 text-sm text-slate-500 font-medium">Total logged trades</div>
                </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-800 mb-6 flex items-center gap-2"><TrendingUp size={18} className="text-emerald-600"/> Macro-Economic Stability (24h)</h3>
                    <div className="h-72 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={mockTimeSeries}>
                                <defs>
                                    <linearGradient id="colorEmp" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                                        <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} dy={10} />
                                <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} domain={['dataMin - 10', 'dataMax + 10']} />
                                <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
                                <Area type="monotone" dataKey="employment" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorEmp)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>
                
                <div className="bg-slate-900 p-6 rounded-2xl shadow-xl text-white">
                    <h3 className="font-bold text-emerald-400 mb-6 flex items-center gap-2"><Activity size={18}/> Economic Simulation Rules</h3>
                    <ul className="space-y-4 text-slate-300 text-sm leading-relaxed">
                        <li className="flex gap-3"><span className="text-emerald-500">▶</span> Jobs dictate income stream. If health/energy drops, agents skip work and lose daily wages.</li>
                        <li className="flex gap-3"><span className="text-emerald-500">▶</span> Businesses hold capital reserves. Salaries are deducted from these reserves.</li>
                        <li className="flex gap-3"><span className="text-emerald-500">▶</span> Shopping transfers funds from agent to business, refueling the business capital.</li>
                        <li className="flex gap-3"><span className="text-emerald-500">▶</span> A closed economic loop: no money is printed out of thin air after initialization.</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
