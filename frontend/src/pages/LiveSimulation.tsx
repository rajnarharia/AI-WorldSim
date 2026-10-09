import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Activity, Target, Brain, Briefcase, Heart, Zap, Crosshair } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

function AgentInspector({ agent, onClose }: any) {
    if (!agent) return null;
    return (
        <div className="absolute top-4 right-4 w-96 bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl border border-slate-200 z-50 overflow-hidden flex flex-col max-h-[90%] animate-in slide-in-from-right-8 duration-300">
            <div className="bg-slate-900 p-5 text-white flex justify-between items-start">
                <div>
                    <h3 className="font-black text-xl flex items-center gap-2">{agent.name} <span className="text-xs font-bold px-2 py-0.5 rounded bg-indigo-500 text-white uppercase tracking-wider">{agent.model_type}</span></h3>
                    <p className="text-slate-400 text-sm mt-1 flex items-center gap-1"><Briefcase size={14}/> {agent.job_id ? `Employed (Job #${agent.job_id})` : 'Unemployed'}</p>
                </div>
                <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors bg-slate-800 p-1.5 rounded-md">X</button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-5 space-y-6">
                <div>
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 border-b border-slate-100 pb-1 flex items-center gap-2"><Activity size={14}/> Vitals & State</h4>
                    <div className="grid grid-cols-2 gap-3">
                        <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <p className="text-xs text-slate-500 font-medium flex items-center gap-1"><Heart size={12}/> Health</p>
                            <p className="text-lg font-black text-rose-600 mt-1">{agent.health?.toFixed(1) || 0}</p>
                        </div>
                        <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <p className="text-xs text-slate-500 font-medium flex items-center gap-1"><Zap size={12}/> Energy</p>
                            <p className="text-lg font-black text-amber-500 mt-1">{agent.energy?.toFixed(1) || 0}</p>
                        </div>
                        <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 col-span-2">
                            <p className="text-xs text-slate-500 font-medium flex items-center gap-1"><Target size={12}/> Funds</p>
                            <p className="text-2xl font-black text-emerald-600 mt-1">${agent.money?.toFixed(2) || '0.00'}</p>
                        </div>
                    </div>
                </div>
                <div>
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 border-b border-slate-100 pb-1 flex items-center gap-2"><Crosshair size={14}/> Needs Profile</h4>
                    <div className="space-y-2">
                        {['need_rest', 'need_money', 'need_social', 'need_health'].map(need => (
                            <div key={need} className="flex items-center gap-3">
                                <span className="text-xs font-semibold text-slate-600 w-20 capitalize">{need.replace('need_','')}</span>
                                <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                                    <div className="h-full bg-indigo-500 rounded-full" style={{width: `${agent[need]}%`}}></div>
                                </div>
                                <span className="text-xs font-mono text-slate-500">{agent[need]?.toFixed(0)}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default function LiveSimulation() {
    const [world, setWorld] = useState<any>(null);
    const [decisions, setDecisions] = useState<any[]>([]);
    const [inspectAgent, setInspectAgent] = useState<any>(null);
    const [modelFilter, setModelFilter] = useState<string>('ALL');

    useEffect(() => {
        const fetch = async () => {
            const [w, d] = await Promise.all([
                axios.get(`${API_BASE_URL}/simulation/world`),
                axios.get(`${API_BASE_URL}/simulation/decisions?limit=25`)
            ]);
            setWorld(w.data);
            setDecisions(d.data);
        };
        fetch();
        const intv = setInterval(fetch, 1000);
        return () => clearInterval(intv);
    }, []);

    if (!world) return <div className="animate-pulse font-medium text-slate-500">Connecting to shared world state...</div>;

    const filteredAgents = modelFilter === 'ALL' ? Object.values(world.agents) : Object.values(world.agents).filter((a:any) => a.model_type === modelFilter);

    return (
        <div className="h-[calc(100vh-8rem)] flex flex-col gap-6 animate-in fade-in duration-500">
            <header className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-black text-slate-800">Shared World Experiment</h1>
                    <p className="text-slate-500 mt-1">One Shared World. Multiple AI Architectures. Real-time visualization.</p>
                </div>
                <div className="flex gap-2 bg-slate-100 p-1 rounded-lg">
                    {['ALL', 'Model A', 'Model B', 'Model C'].map(m => (
                        <button key={m} onClick={() => setModelFilter(m)} className={`px-4 py-1.5 rounded-md text-sm font-bold transition-all ${modelFilter === m ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-700'}`}>{m}</button>
                    ))}
                </div>
            </header>
            
            <div className="flex gap-6 flex-1 min-h-0">
                <div className="flex-[2] bg-white border border-slate-200 rounded-2xl shadow-sm relative overflow-hidden bg-[#fafafa]">
                    <div className="absolute inset-0 opacity-[0.15] bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
                    {Object.values(world.locations).map((loc: any) => (
                        <div key={loc.id} className="absolute w-28 h-28 bg-white border border-slate-200 rounded-xl shadow-sm flex items-center justify-center flex-col gap-2 transition-all z-10" style={{left: loc.pos_x, top: loc.pos_y}}>
                            <span className="text-2xl drop-shadow-sm">{loc.type === 'RESIDENTIAL' ? 'House' : (loc.type === 'COMMERCIAL' ? 'Shop' : 'Location')}</span>
                            <span className="text-xs font-bold text-slate-700 tracking-tight text-center px-2">{loc.name}</span>
                            <div className="text-[10px] text-slate-400 font-medium px-2 py-0.5 bg-slate-50 rounded-full">{loc.type}</div>
                        </div>
                    ))}
                    {filteredAgents.map((agent: any) => {
                        const loc: any = Object.values(world.locations).find((l:any) => l.id === agent.current_location_id);
                        if(!loc) return null;
                        const seed = agent.id * 17;
                        const randOffsetX = (seed % 60) - 30;
                        const randOffsetY = ((seed * 13) % 60) - 30;
                        const isSelected = inspectAgent?.id === agent.id;
                        return (
                            <div key={agent.id} onClick={() => setInspectAgent(agent)}
                                className={`absolute w-5 h-5 rounded-full border-2 cursor-pointer transition-all z-20 group ${isSelected ? 'bg-indigo-600 border-white shadow-[0_0_15px_rgba(79,70,229,0.6)] scale-125' : 'bg-blue-500 border-white shadow hover:scale-125'}`} 
                                style={{left: loc.pos_x + 56 + randOffsetX - 10, top: loc.pos_y + 56 + randOffsetY - 10}}>
                                <div className={`absolute -top-8 left-1/2 -translate-x-1/2 w-max bg-slate-900 text-white text-xs font-bold px-2 py-1 rounded shadow-lg pointer-events-none transition-opacity ${isSelected ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}>
                                    {agent.name}
                                </div>
                            </div>
                        )
                    })}
                    {inspectAgent && <AgentInspector agent={inspectAgent} onClose={() => setInspectAgent(null)} />}
                </div>
                
                <div className="flex-1 flex flex-col bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
                    <div className="bg-slate-50 p-4 border-b border-slate-200">
                        <h3 className="font-bold text-slate-800 flex items-center gap-2"><Activity size={18} className="text-indigo-500"/> Live AI Decision Stream</h3>
                    </div>
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
                        {decisions.map(d => (
                            <div key={d.id} className="text-sm bg-white border border-slate-200 rounded-xl p-4 shadow-sm relative overflow-hidden group">
                                <div className="absolute left-0 top-0 bottom-0 w-1 bg-indigo-500"></div>
                                <div className="flex justify-between items-center mb-2">
                                    <span className="font-black text-slate-800 flex items-center gap-1.5"><Brain size={14} className="text-indigo-500"/> Agent {d.agent_id}</span>
                                    <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 font-mono">{d.simulation_time_str}</span>
                                </div>
                                <div className="font-bold text-indigo-700 tracking-wide text-xs mb-2 bg-indigo-50 inline-block px-2 py-1 rounded border border-indigo-100">{d.selected_action}</div>
                                <div className="text-slate-600 text-xs leading-relaxed bg-slate-50 p-2.5 rounded-lg border border-slate-100 italic border-l-2 border-l-slate-300">"{d.reason}"</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
