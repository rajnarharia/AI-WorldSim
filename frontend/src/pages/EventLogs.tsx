import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FileText, Search } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function EventLogs() {
    const [events, setEvents] = useState<any[]>([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        axios.get(`${API_BASE_URL}/simulation/events?limit=200`).then(res => setEvents(res.data)).catch(e => setEvents([]));
    }, []);

    const filtered = events.filter((e: any) => 
        e.event_type?.toLowerCase().includes(searchTerm.toLowerCase()) || 
        e.action?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        e.reason?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="space-y-6 animate-in fade-in">
            <header className="flex justify-between items-end pb-6 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><FileText className="text-slate-600"/> Global Event Logs</h1>
                    <p className="text-slate-500 mt-1">Searchable chronological history of all macro simulation events.</p>
                </div>
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18}/>
                    <input 
                        type="text" 
                        placeholder="Search events..." 
                        className="pl-10 pr-4 py-2 bg-white border border-slate-300 rounded-lg w-72 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </header>
            
            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
                <table className="min-w-full text-left text-sm">
                    <thead className="bg-slate-50 border-b border-slate-200 text-xs uppercase tracking-widest font-bold text-slate-500">
                        <tr>
                            <th className="py-4 px-6">Tick</th>
                            <th className="py-4 px-6">Event Type</th>
                            <th className="py-4 px-6">Agent</th>
                            <th className="py-4 px-6">Action & Reason</th>
                            <th className="py-4 px-6">Outcome</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {filtered.map((e: any) => (
                            <tr key={e.id} className="hover:bg-slate-50 transition-colors">
                                <td className="py-3 px-6 font-mono text-slate-400">{e.tick}</td>
                                <td className="py-3 px-6 font-bold text-indigo-700">{e.event_type}</td>
                                <td className="py-3 px-6 font-medium text-slate-600">ID: {e.agent_id}</td>
                                <td className="py-3 px-6 text-slate-600">
                                    <div className="font-bold text-slate-800">{e.action}</div>
                                    <div className="text-xs italic mt-1 text-slate-500">{e.reason}</div>
                                </td>
                                <td className="py-3 px-6">
                                    <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-widest ${e.outcome === 'SUCCESS' || e.outcome === 'Valid' ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-600'}`}>{e.outcome}</span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
