import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Users, Briefcase, DollarSign, Shield, Heart, Scale, Link as LinkIcon, Activity } from 'lucide-react';
import { AreaChart, Area, ResponsiveContainer, YAxis } from 'recharts';

const API_BASE_URL = 'http://localhost:8000/api';

function MetricCard({ title, value, icon: Icon, trend, trendLabel, colorClass }: any) {
    const sparkData = Array.from({length: 10}).map((_,i) => ({ val: Math.random() * 10 + 50 + (trend > 0 ? i : -i) }));
    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col relative overflow-hidden group">
            <div className={`absolute top-0 right-0 w-16 h-16 opacity-[0.03] rounded-bl-full ${colorClass.bg}`}></div>
            <div className="flex items-center gap-3 mb-2">
                <div className={`p-2 rounded-lg ${colorClass.bg} ${colorClass.text}`}><Icon size={18} strokeWidth={2.5}/></div>
                <h3 className="text-xs font-bold text-slate-500 tracking-wider uppercase">{title}</h3>
            </div>
            <div className="text-3xl font-black text-slate-800 mt-2">{value}</div>
            <div className="h-10 mt-2 -mx-2 opacity-50 group-hover:opacity-100 transition-opacity">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={sparkData}><YAxis domain={['dataMin - 10', 'dataMax + 10']} hide /><Area type="monotone" dataKey="val" stroke={colorClass.stroke} fill={colorClass.fill} strokeWidth={2} /></AreaChart>
                </ResponsiveContainer>
            </div>
            <div className="text-xs text-slate-500 mt-3 flex items-center gap-1.5 font-medium border-t border-slate-100 pt-3">
                <span className={`px-1.5 py-0.5 rounded ${trend > 0 ? 'bg-emerald-100 text-emerald-700' : (trend < 0 ? 'bg-rose-100 text-rose-700' : 'bg-slate-100 text-slate-600')}`}>
                    {trend > 0 ? '↑' : (trend < 0 ? '↓' : '-')} {Math.abs(trend)}%
                </span>
                {trendLabel}
            </div>
        </div>
    );
}

export default function Overview() {
    const [dashboards, setDashboards] = useState<any>(null);

    useEffect(() => {
        const fetch = async () => {
            const [eco, edu, heal, soc, saf, gov, status] = await Promise.all([
                axios.get(`${API_BASE_URL}/dashboards/economy`),
                axios.get(`${API_BASE_URL}/dashboards/education`),
                axios.get(`${API_BASE_URL}/dashboards/healthcare`),
                axios.get(`${API_BASE_URL}/dashboards/social`),
                axios.get(`${API_BASE_URL}/dashboards/safety`),
                axios.get(`${API_BASE_URL}/dashboards/government`),
                axios.get(`${API_BASE_URL}/simulation/status`)
            ]);
            setDashboards({ eco: eco.data, edu: edu.data, heal: heal.data, soc: soc.data, saf: saf.data, gov: gov.data, status: status.data });
        };
        fetch();
        const intv = setInterval(fetch, 2000);
        return () => clearInterval(intv);
    }, []);

    if (!dashboards) return <div className="text-slate-500 font-medium animate-pulse">Loading overview data...</div>;

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <header>
                <h1 className="text-3xl font-black text-slate-800">Executive Overview</h1>
                <p className="text-slate-500 mt-1">Real-time aggregate telemetry of the simulated multi-agent society.</p>
            </header>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard title="Population" value={dashboards.status.population} icon={Users} trend={0} trendLabel="Stable" colorClass={{bg: 'bg-indigo-100', text: 'text-indigo-600', stroke: '#4f46e5', fill: '#e0e7ff'}} />
                <MetricCard title="Employment" value={`${dashboards.eco.employment_rate}%`} icon={Briefcase} trend={4.2} trendLabel="vs last day" colorClass={{bg: 'bg-emerald-100', text: 'text-emerald-600', stroke: '#10b981', fill: '#d1fae5'}} />
                <MetricCard title="Avg Income" value={`$${dashboards.eco.avg_income}`} icon={DollarSign} trend={-1.5} trendLabel="vs last day" colorClass={{bg: 'bg-blue-100', text: 'text-blue-600', stroke: '#3b82f6', fill: '#dbeafe'}} />
                <MetricCard title="Active Incidents" value={dashboards.saf.active_incidents || 0} icon={Shield} trend={1.2} trendLabel="escalating" colorClass={{bg: 'bg-orange-100', text: 'text-orange-600', stroke: '#f97316', fill: '#ffedd5'}} />
                <MetricCard title="Avg Health" value={`${dashboards.heal.average_health}%`} icon={Heart} trend={2.1} trendLabel="vs last day" colorClass={{bg: 'bg-rose-100', text: 'text-rose-600', stroke: '#e11d48', fill: '#ffe4e6'}} />
                <MetricCard title="Social Trust" value={`${(dashboards.soc.average_trust * 100).toFixed(0)}%`} icon={LinkIcon} trend={0.5} trendLabel="improving" colorClass={{bg: 'bg-purple-100', text: 'text-purple-600', stroke: '#9333ea', fill: '#f3e8ff'}} />
                <MetricCard title="Law Compliance" value={`100%`} icon={Scale} trend={0} trendLabel="steady" colorClass={{bg: 'bg-slate-200', text: 'text-slate-700', stroke: '#475569', fill: '#e2e8f0'}} />
                <MetricCard title="Eco Activity" value={dashboards.eco.total_transactions} icon={Activity} trend={12.4} trendLabel="high volume" colorClass={{bg: 'bg-cyan-100', text: 'text-cyan-600', stroke: '#0891b2', fill: '#cffafe'}} />
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">Simulation Status</h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center border-b border-slate-100 pb-2"><span className="text-slate-500 font-medium">Tick</span><span className="font-bold font-mono">{dashboards.status.current_tick}</span></div>
                        <div className="flex justify-between items-center border-b border-slate-100 pb-2"><span className="text-slate-500 font-medium">Day</span><span className="font-bold">{dashboards.status.simulation_day}</span></div>
                        <div className="flex justify-between items-center pb-2"><span className="text-slate-500 font-medium">Engine State</span><span className="font-bold text-emerald-600">{dashboards.status.state}</span></div>
                    </div>
                </div>
                <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-sm text-white">
                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2"><Activity className="text-indigo-400"/> AI Agent Engine</h3>
                    <p className="text-slate-400 text-sm leading-relaxed mb-4">The decision engine is actively evaluating {dashboards.status.population} autonomous models. Actions are routed through the ActionValidator to ensure safety constraints are respected.</p>
                    <div className="bg-slate-800 rounded px-4 py-3 font-mono text-xs text-indigo-300">
                        &gt; validator.check(agent_action)<br/>
                        &gt; executor.apply(valid_action)<br/>
                        &gt; metrics.aggregate(state_diff)<br/>
                        &gt; SUCCESS
                    </div>
                </div>
            </div>
        </div>
    );
}
