import React, { useState } from 'react';
import axios from 'axios';
import { FlaskConical, Play, CheckCircle2, ChevronRight, Activity } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function Experiments() {
    const [running, setRunning] = useState(false);
    const [comparison, setComparison] = useState<any>(null);

    const runExp = async () => {
        try {
            setRunning(true);
            const createRes = await axios.post(`${API_BASE_URL}/metrics/experiments?name=Model_Comparison&population=30&runs=3&duration_days=2`);
            const expId = createRes.data.id;
            await axios.post(`${API_BASE_URL}/metrics/experiments/${expId}/run`);
            const compRes = await axios.get(`${API_BASE_URL}/metrics/experiments/${expId}/comparison`);
            setComparison(compRes.data);
        } catch (err) {
            console.error(err);
        } finally {
            setRunning(false);
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <header className="flex justify-between items-end border-b border-slate-200 pb-6">
                <div>
                    <h1 className="text-3xl font-black text-slate-800">Experiment Runner</h1>
                    <p className="text-slate-500 mt-1">Execute parallel deterministic simulations to compare AI model behaviour.</p>
                </div>
                <button 
                    onClick={runExp} 
                    disabled={running} 
                    className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-white shadow-lg transition-all ${running ? 'bg-slate-400 cursor-not-allowed' : 'bg-teal-600 hover:bg-teal-700 hover:scale-[1.02] active:scale-[0.98] shadow-teal-600/30'}`}
                >
                    {running ? <Activity size={18} className="animate-spin" /> : <Play size={18} />}
                    {running ? 'EXECUTING SIMULATIONS...' : 'RUN EXPERIMENT'}
                </button>
            </header>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                        <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2"><FlaskConical size={18} className="text-teal-600"/> Configuration</h3>
                        <div className="space-y-3">
                            <div className="flex justify-between border-b border-slate-100 pb-2"><span className="text-slate-500 text-sm">Models</span><span className="font-bold text-slate-700 text-sm">A, B, C</span></div>
                            <div className="flex justify-between border-b border-slate-100 pb-2"><span className="text-slate-500 text-sm">Population</span><span className="font-bold text-slate-700 text-sm">30</span></div>
                            <div className="flex justify-between border-b border-slate-100 pb-2"><span className="text-slate-500 text-sm">Runs</span><span className="font-bold text-slate-700 text-sm">3 (Different Seeds)</span></div>
                            <div className="flex justify-between"><span className="text-slate-500 text-sm">Duration</span><span className="font-bold text-slate-700 text-sm">2 Simulation Days</span></div>
                        </div>
                    </div>
                    
                    <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                        <h3 className="font-bold mb-3 flex items-center gap-2 text-teal-400"><CheckCircle2 size={18}/> Initial Conditions</h3>
                        <p className="text-sm text-slate-400 leading-relaxed">
                            For fair comparison, the database is wiped and the exact same agents, locations, funds, and needs are spawned deterministically for every run.
                        </p>
                    </div>
                </div>
                
                <div className="lg:col-span-2">
                    {running && (
                        <div className="h-full min-h-[300px] flex flex-col items-center justify-center bg-white border border-slate-200 rounded-2xl shadow-sm">
                            <div className="w-16 h-16 border-4 border-teal-100 border-t-teal-600 rounded-full animate-spin mb-6"></div>
                            <h3 className="text-xl font-bold text-slate-800">Running Parallel Universes</h3>
                            <p className="text-slate-500 mt-2 text-center max-w-sm">Generating identical worlds, evaluating AI models, and aggregating time-series metrics...</p>
                        </div>
                    )}
                    
                    {comparison && !running && (
                        <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden animate-in slide-in-from-bottom-8 duration-500">
                            <div className="bg-slate-50 p-6 border-b border-slate-200">
                                <h3 className="text-lg font-bold text-slate-800">Aggregated Metric Results</h3>
                                <p className="text-xs font-semibold text-slate-500 uppercase tracking-widest mt-1">Mean across all simulation runs</p>
                            </div>
                            <div className="p-0">
                                <table className="min-w-full text-left">
                                    <thead className="bg-white border-b border-slate-200">
                                        <tr>
                                            <th className="py-4 px-6 text-xs font-bold text-slate-400 uppercase tracking-widest">Metric</th>
                                            <th className="py-4 px-6 text-xs font-bold text-slate-800 uppercase tracking-widest bg-emerald-50">Model A <span className="font-normal text-slate-500 lowercase ml-1">(Rule-Based)</span></th>
                                            <th className="py-4 px-6 text-xs font-bold text-slate-800 uppercase tracking-widest bg-blue-50">Model B <span className="font-normal text-slate-500 lowercase ml-1">(LLM-1)</span></th>
                                            <th className="py-4 px-6 text-xs font-bold text-slate-800 uppercase tracking-widest bg-purple-50">Model C <span className="font-normal text-slate-500 lowercase ml-1">(LLM-2)</span></th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100">
                                        {Object.keys(comparison).map((metricName, idx) => (
                                            <tr key={metricName} className="hover:bg-slate-50 transition-colors">
                                                <td className="py-4 px-6 font-bold text-slate-700 capitalize flex items-center gap-2"><ChevronRight size={14} className="text-slate-300"/> {metricName.replace(/_/g, ' ')}</td>
                                                <td className="py-4 px-6 font-mono text-emerald-700 bg-emerald-50/30">{comparison[metricName]['Model A']?.mean ?? 'N/A'}</td>
                                                <td className="py-4 px-6 font-mono text-blue-700 bg-blue-50/30">{comparison[metricName]['Model B']?.mean ?? 'N/A'}</td>
                                                <td className="py-4 px-6 font-mono text-purple-700 bg-purple-50/30">{comparison[metricName]['Model C']?.mean ?? 'N/A'}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}
                    
                    {!comparison && !running && (
                        <div className="h-full min-h-[300px] flex flex-col items-center justify-center bg-slate-50 border border-slate-200 border-dashed rounded-2xl text-center px-8">
                            <FlaskConical size={48} className="text-slate-300 mb-4" />
                            <h3 className="text-lg font-bold text-slate-600">No Experiment Results</h3>
                            <p className="text-slate-400 mt-2 text-sm max-w-sm">Click "Run Experiment" to execute simulations across all 3 AI models and view comparative metrics.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
