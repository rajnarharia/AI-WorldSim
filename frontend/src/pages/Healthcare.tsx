import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Heart, Activity, Thermometer } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function Healthcare() {
    const [data, setData] = useState<any>(null);
    useEffect(() => { axios.get(`${API_BASE_URL}/dashboards/healthcare`).then(res => setData(res.data)) }, []);
    if (!data) return <div className="animate-pulse">Loading...</div>;

    return (
        <div className="space-y-6 animate-in fade-in">
            <header>
                <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><Heart className="text-rose-600"/> Healthcare & Vitality</h1>
                <p className="text-slate-500 mt-1">Agent well-being, sickness rates, and healthcare utilization.</p>
            </header>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Avg Population Health</h3>
                    <div className="text-4xl font-black text-rose-600">{data.average_health?.toFixed(1) || 0}%</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Currently Sick</h3>
                    <div className="text-4xl font-black text-slate-800">{data.sick_agents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Hospital Visits</h3>
                    <div className="text-4xl font-black text-slate-800">{data.hospital_visits || 0}</div>
                </div>
            </div>
        </div>
    );
}
