import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { MessageSquare, Users, Link as LinkIcon } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function Social() {
    const [data, setData] = useState<any>(null);
    useEffect(() => { axios.get(`${API_BASE_URL}/dashboards/social`).then(res => setData(res.data)) }, []);
    if (!data) return <div className="animate-pulse">Loading...</div>;

    return (
        <div className="space-y-6 animate-in fade-in">
            <header>
                <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><MessageSquare className="text-purple-600"/> Social Dynamics</h1>
                <p className="text-slate-500 mt-1">Inter-agent relationships, cooperation rates, and societal trust.</p>
            </header>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Average Trust</h3>
                    <div className="text-4xl font-black text-purple-600">{((data.average_trust||0) * 100).toFixed(0)}%</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Cooperation Rate</h3>
                    <div className="text-4xl font-black text-purple-600">{((data.average_cooperation||0) * 100).toFixed(0)}%</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Active Relationships</h3>
                    <div className="text-4xl font-black text-slate-800">{data.total_relationships || 0}</div>
                </div>
            </div>
        </div>
    );
}
