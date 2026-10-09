import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Shield, Scale, AlertTriangle, Building } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function SafetyGov() {
    const [saf, setSaf] = useState<any>(null);
    const [gov, setGov] = useState<any>(null);
    useEffect(() => { 
        Promise.all([
            axios.get(`${API_BASE_URL}/dashboards/safety`),
            axios.get(`${API_BASE_URL}/dashboards/government`)
        ]).then(([s, g]) => { setSaf(s.data); setGov(g.data); }).catch(e => {
            console.error(e);
            setSaf({});
            setGov({});
        });
    }, []);

    if (!saf || !gov) return <div className="animate-pulse">Loading...</div>;

    return (
        <div className="space-y-8 animate-in fade-in">
            <header>
                <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><Shield className="text-orange-600"/> Safety & Governance</h1>
                <p className="text-slate-500 mt-1">Incident tracking, law enforcement, and government policy metrics.</p>
            </header>
            
            <h2 className="text-xl font-bold text-slate-800 border-b border-slate-200 pb-2">Public Safety</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-[10px] mb-2">Total Incidents</h3>
                    <div className="text-3xl font-black text-orange-600">{saf.total_incidents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-[10px] mb-2">Active</h3>
                    <div className="text-3xl font-black text-orange-600">{saf.active_incidents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-[10px] mb-2">Resolved</h3>
                    <div className="text-3xl font-black text-emerald-600">{saf.resolved_incidents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-[10px] mb-2">Police Resp Time</h3>
                    <div className="text-3xl font-black text-slate-800">{saf.avg_response_time || 0} <span className="text-sm">ticks</span></div>
                </div>
            </div>

            <h2 className="text-xl font-bold text-slate-800 border-b border-slate-200 pb-2 mt-8">Government Administration</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                    <h3 className="font-bold text-slate-400 uppercase tracking-widest text-[10px] mb-2">Treasury Funds</h3>
                    <div className="text-3xl font-black text-emerald-400">${gov.government_funds?.toFixed(2) || '0.00'}</div>
                </div>
                <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                    <h3 className="font-bold text-slate-400 uppercase tracking-widest text-[10px] mb-2">Tax Rate</h3>
                    <div className="text-3xl font-black text-white">{gov.tax_rate || 0}%</div>
                </div>
                <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                    <h3 className="font-bold text-slate-400 uppercase tracking-widest text-[10px] mb-2">Healthcare Budget</h3>
                    <div className="text-3xl font-black text-white">${gov.healthcare_budget || 0}</div>
                </div>
                <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                    <h3 className="font-bold text-slate-400 uppercase tracking-widest text-[10px] mb-2">Police Effectiveness</h3>
                    <div className="text-3xl font-black text-white">{((gov.police_effectiveness||0)*100).toFixed(0)}%</div>
                </div>
            </div>
        </div>
    );
}
