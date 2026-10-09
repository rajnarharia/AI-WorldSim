import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Play, Pause, Square, SkipForward, RefreshCw } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function SimulationControls() {
    const [status, setStatus] = useState<any>(null);

    const fetchStatus = async () => {
        try {
            const res = await axios.get(`${API_BASE_URL}/simulation/status`);
            setStatus(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 1000);
        return () => clearInterval(interval);
    }, []);

    const action = async (cmd: string) => {
        await axios.post(`${API_BASE_URL}/simulation/control`, { action: cmd });
        fetchStatus();
    };

    if (!status) return <div className="text-sm text-slate-500 animate-pulse font-medium">Connecting to Simulation Engine...</div>;

    return (
        <div className="flex items-center gap-6">
            <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200 shadow-inner">
                <button onClick={() => action('start')} className={`p-1.5 rounded-md transition-all ${status.state === 'RUNNING' ? 'bg-white shadow-sm text-emerald-600 font-bold' : 'text-slate-500 hover:bg-slate-200'}`} title="Start"><Play size={16} /></button>
                <button onClick={() => action('pause')} className={`p-1.5 rounded-md transition-all ${status.state === 'PAUSED' ? 'bg-white shadow-sm text-orange-600 font-bold' : 'text-slate-500 hover:bg-slate-200'}`} title="Pause"><Pause size={16} /></button>
                <button onClick={() => action('stop')} className="p-1.5 rounded-md text-slate-500 hover:bg-slate-200 hover:text-rose-600" title="Stop"><Square size={16} /></button>
                <div className="w-px h-5 bg-slate-300 mx-1"></div>
                <button onClick={() => action('next_tick')} className="p-1.5 rounded-md text-slate-500 hover:bg-slate-200 hover:text-indigo-600" title="Next Tick"><SkipForward size={16} /></button>
                <button onClick={() => action('reset')} className="p-1.5 rounded-md text-slate-500 hover:bg-slate-200 hover:text-rose-600" title="Reset"><RefreshCw size={16} /></button>
            </div>
            <div className="flex flex-col border-l border-slate-200 pl-6">
                <span className={`text-xs font-black uppercase tracking-widest ${status.state === 'RUNNING' ? 'text-emerald-600' : (status.state === 'PAUSED' ? 'text-orange-500' : 'text-rose-500')}`}>
                    {status.state}
                </span>
                <span className="text-sm font-semibold text-slate-700 mt-0.5">Day {status.simulation_day} <span className="text-slate-400 mx-1">•</span> {status.simulation_time}</span>
            </div>
            <div className="text-xs font-medium text-slate-500 bg-slate-100 px-3 py-1.5 rounded-md border border-slate-200">
                Tick <span className="text-slate-700 font-bold">{status.current_tick}</span> <span className="mx-2 text-slate-300">|</span> Speed <span className="text-slate-700 font-bold">{status.speed}x</span>
            </div>
        </div>
    );
}
