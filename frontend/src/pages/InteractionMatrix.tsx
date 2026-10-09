import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ArrowRightLeft, Target } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function InteractionMatrix() {
    const [matrix, setMatrix] = useState<any>(null);

    useEffect(() => {
        // Find latest experiment
        axios.get(`${API_BASE_URL}/experiments`).then(async res => {
            if(res.data && res.data.length > 0) {
                const latestExpId = res.data[res.data.length-1].id;
                const mRes = await axios.get(`${API_BASE_URL}/experiments/${latestExpId}/cross-model-interactions`);
                setMatrix(mRes.data);
            } else {
                setMatrix({});
            }
        }).catch(() => setMatrix({}));
    }, []);

    if (!matrix) return <div className="animate-pulse">Loading matrix...</div>;

    const models = ['Model A', 'Model B', 'Model C'];

    return (
        <div className="space-y-6 animate-in fade-in">
            <header>
                <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><ArrowRightLeft className="text-emerald-600"/> Interaction Matrix</h1>
                <p className="text-slate-500 mt-1">Cross-model interaction tracking.</p>
            </header>

            <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
                <div className="flex gap-4 mb-4">
                    <div className="w-24"></div>
                    {models.map(m => <div key={'col'+m} className="flex-1 text-center font-bold text-slate-500 text-sm tracking-widest uppercase">TO {m}</div>)}
                </div>
                {models.map(src => (
                    <div key={'row'+src} className="flex gap-4 mb-4 items-center">
                        <div className="w-24 font-bold text-slate-500 text-sm tracking-widest uppercase text-right pr-4">FROM {src}</div>
                        {models.map(tgt => {
                            const val = matrix[src]?.[tgt] || 0;
                            return (
                                <div key={src+tgt} className="flex-1 bg-slate-50 border border-slate-200 rounded-xl p-4 text-center cursor-pointer hover:bg-indigo-50 hover:border-indigo-200 transition-colors group">
                                    <div className="text-3xl font-black text-slate-800 group-hover:text-indigo-600">{val}</div>
                                    <div className="text-[10px] uppercase font-bold text-slate-400 mt-1">Interactions</div>
                                </div>
                            );
                        })}
                    </div>
                ))}
            </div>
            
            <div className="bg-slate-900 p-8 rounded-2xl text-white">
                <h3 className="font-bold text-emerald-400 mb-4 flex items-center gap-2"><Target/> Shared World Verification</h3>
                <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">If non-zero values appear in off-diagonal cells (e.g. Model A to Model B), it proves agents are participating in ONE shared world, buying products, conversing, and cooperating across architectural boundaries.</p>
            </div>
        </div>
    );
}
