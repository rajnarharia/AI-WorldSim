import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart2, Info, Activity } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function Analytics() {
    const [defs, setDefs] = useState<any>(null);

    useEffect(() => {
        axios.get(`${API_BASE_URL}/metrics/definitions`).then(res => setDefs(res.data));
    }, []);

    if (!defs) return <div className="animate-pulse font-medium text-slate-500">Loading metrics engine...</div>;

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <header>
                <h1 className="text-3xl font-black text-slate-800">Analytics Engine</h1>
                <p className="text-slate-500 mt-1">Formal metric definitions and traceability logic used by the simulation.</p>
            </header>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Object.keys(defs).map(m => (
                    <div key={m} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 group hover:border-indigo-300 transition-colors">
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <h3 className="font-bold text-slate-800 capitalize text-lg">{m.replace(/_/g, ' ')}</h3>
                                <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-600 bg-indigo-50 px-2 py-1 rounded-md mt-2 inline-block">
                                    {defs[m].category}
                                </span>
                            </div>
                            <div className="w-8 h-8 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:text-indigo-500 group-hover:bg-indigo-50 transition-colors">
                                <Activity size={16} />
                            </div>
                        </div>
                        
                        <p className="text-sm text-slate-600 leading-relaxed min-h-[40px]">{defs[m].description}</p>
                        
                        <div className="mt-6 bg-slate-50 p-4 rounded-lg border border-slate-100 relative">
                            <div className="absolute -top-3 left-4 bg-white px-2 text-xs font-bold text-slate-400 flex items-center gap-1"><Info size={12}/> FORMULA</div>
                            <code className="text-xs font-mono text-slate-700 break-all">{defs[m].formula}</code>
                            <div className="mt-3 text-xs font-bold text-slate-500 uppercase tracking-widest border-t border-slate-200 pt-3 flex justify-between">
                                <span>Unit</span>
                                <span className="text-indigo-600 bg-white px-2 border border-slate-200 rounded">{defs[m].unit}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            
            <div className="bg-slate-900 rounded-2xl p-8 text-white mt-8 shadow-xl">
                <h3 className="text-xl font-bold mb-4 text-white flex items-center gap-2"><BarChart2 className="text-indigo-400"/> Traceability Guarantee</h3>
                <p className="text-slate-400 leading-relaxed max-w-3xl">
                    Every metric calculated by the AI WorldSim Metrics Engine is strictly traceable to underlying database events and state mutations. 
                    No "intelligence scores" or random numbers are generated. All dashboards reflect actual simulation telemetry and mathematical aggregations.
                </p>
            </div>
        </div>
    );
}
