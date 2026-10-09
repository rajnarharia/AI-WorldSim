import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Users, Search, Filter } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function AgentsList() {
    const [world, setWorld] = useState<any>(null);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        axios.get(`${API_BASE_URL}/simulation/world`).then(res => setWorld(res.data));
    }, []);

    if (!world) return <div className="animate-pulse font-medium text-slate-500">Loading agents database...</div>;

    const filtered = Object.values(world.agents).filter((a: any) => 
        a.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        a.model_type.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <header className="flex justify-between items-end pb-6 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><Users className="text-indigo-600"/> AI Agents Directory</h1>
                    <p className="text-slate-500 mt-1">Inspect individual simulated agent state, goals, and history.</p>
                </div>
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18}/>
                    <input 
                        type="text" 
                        placeholder="Search agents by name or model..." 
                        className="pl-10 pr-4 py-2 bg-white border border-slate-300 rounded-lg w-72 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 shadow-sm"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </header>
            
            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="min-w-full text-left text-sm">
                        <thead className="bg-slate-50 border-b border-slate-200 text-xs uppercase tracking-widest font-bold text-slate-500">
                            <tr>
                                <th className="py-4 px-6">ID</th>
                                <th className="py-4 px-6">Name</th>
                                <th className="py-4 px-6">Model Architecture</th>
                                <th className="py-4 px-6 text-right">Age</th>
                                <th className="py-4 px-6 text-right">Funds</th>
                                <th className="py-4 px-6 text-right">Health</th>
                                <th className="py-4 px-6">Current Location</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {filtered.map((a: any) => (
                                <tr key={a.id} className="hover:bg-indigo-50/50 cursor-pointer transition-colors">
                                    <td className="py-3 px-6 font-mono text-slate-400">#{String(a.id).padStart(3, '0')}</td>
                                    <td className="py-3 px-6 font-bold text-slate-800">{a.name}</td>
                                    <td className="py-3 px-6">
                                        <span className={`px-2.5 py-1 rounded text-xs font-bold ${
                                            a.model_type === 'Model A' ? 'bg-emerald-100 text-emerald-700' :
                                            a.model_type === 'Model B' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'
                                        }`}>
                                            {a.model_type}
                                        </span>
                                    </td>
                                    <td className="py-3 px-6 text-right text-slate-600">{a.age} yrs</td>
                                    <td className="py-3 px-6 text-right font-mono font-bold text-emerald-600">${a.money?.toFixed(2)}</td>
                                    <td className="py-3 px-6 text-right">
                                        <div className="flex items-center justify-end gap-2">
                                            <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                                <div className="h-full bg-rose-500" style={{width: `${a.health || 0}%`}}></div>
                                            </div>
                                            <span className="font-mono text-xs text-slate-500">{a.health?.toFixed(0) || 0}</span>
                                        </div>
                                    </td>
                                    <td className="py-3 px-6 text-slate-600 truncate max-w-[150px]">
                                        {(Object.values(world.locations).find((l:any) => l.id === a.current_location_id) as any)?.name || 'Unknown'}
                                    </td>
                                </tr>
                            ))}
                            {filtered.length === 0 && (
                                <tr>
                                    <td colSpan={7} className="py-12 text-center text-slate-400">
                                        No agents found matching your criteria.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
