import React, { useState, useEffect } from 'react';
import { FileText, Download, Play, AlertCircle } from 'lucide-react';

export default function FinalReport() {
    const [experiments, setExperiments] = useState<any[]>([]);
    const [selectedExpId, setSelectedExpId] = useState<number | ''>('');
    const [report, setReport] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetch('http://localhost:8000/api/experiments')
            .then(res => res.json())
            .then(data => setExperiments(data))
            .catch(err => console.error(err));
    }, []);

    const fetchReport = async (id: number) => {
        try {
            const res = await fetch(`http://localhost:8000/api/experiments/${id}/report`);
            if (res.ok) {
                const data = await res.json();
                setReport(data);
                setError(null);
            } else {
                setReport(null);
            }
        } catch (e) {
            setReport(null);
        }
    };

    useEffect(() => {
        if (selectedExpId) {
            fetchReport(selectedExpId as number);
        } else {
            setReport(null);
        }
    }, [selectedExpId]);

    const handleGenerate = async () => {
        if (!selectedExpId) return;
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`http://localhost:8000/api/experiments/${selectedExpId}/generate-report`, { method: 'POST' });
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.detail || "Failed to generate report");
            }
            await fetchReport(selectedExpId as number);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleExport = (type: string) => {
        if (!selectedExpId) return;
        window.open(`http://localhost:8000/api/experiments/${selectedExpId}/export/${type}`, '_blank');
    };

    return (
        <div className="space-y-6 animate-in fade-in max-w-4xl mx-auto">
            <header className="flex justify-between items-center pb-6 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl font-black text-slate-800 flex items-center gap-2"><FileText className="text-indigo-600"/> Final Evaluation Report</h1>
                    <p className="text-slate-500 mt-1">Generate and export professional research findings.</p>
                </div>
                {report && (
                    <div className="flex gap-3">
                        <button onClick={() => handleExport('json')} className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-300 rounded-lg shadow-sm font-bold text-slate-700 hover:bg-slate-50"><Download size={16}/> JSON</button>
                        <button onClick={() => handleExport('csv')} className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-300 rounded-lg shadow-sm font-bold text-slate-700 hover:bg-slate-50"><Download size={16}/> CSV</button>
                        <button onClick={() => handleExport('pdf')} className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg shadow-sm font-bold hover:bg-slate-800"><Download size={16}/> PDF</button>
                    </div>
                )}
            </header>
            
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex flex-col md:flex-row gap-4 items-end">
                <div className="flex-1 w-full">
                    <label className="block text-sm font-bold text-slate-700 mb-2">Select Experiment</label>
                    <select 
                        className="w-full bg-slate-50 border border-slate-300 text-slate-900 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block p-2.5"
                        value={selectedExpId}
                        onChange={(e) => setSelectedExpId(e.target.value ? parseInt(e.target.value) : '')}
                    >
                        <option value="">-- Choose an experiment --</option>
                        {experiments.map(e => (
                            <option key={e.id} value={e.id}>{e.name} (ID: {e.id}) - {e.status}</option>
                        ))}
                    </select>
                </div>
                <button 
                    onClick={handleGenerate}
                    disabled={!selectedExpId || loading}
                    className="flex items-center gap-2 px-6 py-2.5 bg-indigo-600 text-white rounded-lg font-bold shadow-sm hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {loading ? <span className="animate-spin">↻</span> : <Play size={16}/>} Generate Report
                </button>
            </div>

            {error && (
                <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg flex items-center gap-3">
                    <AlertCircle size={20}/>
                    <span className="font-medium">{error}</span>
                </div>
            )}

            {report && (
                <div className="bg-white p-12 rounded-2xl shadow-sm border border-slate-200 max-w-none space-y-10">
                    <div className="text-center space-y-2 mb-12">
                        <h1 className="text-4xl font-black text-slate-900">AI WorldSim</h1>
                        <h2 className="text-xl text-slate-500 font-medium">AI Real-World Simulation Platform</h2>
                        <p className="text-slate-400 italic">"A Multi-Agent Virtual Society for Real-World Behaviour and Safety Evaluation of AI Models"</p>
                        <div className="mt-4 inline-block bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-sm font-bold">Version {report.version} • {new Date(report.generated_at).toLocaleString()}</div>
                    </div>

                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 border-b pb-2 mb-4">1. Experiment Configuration Snapshot</h2>
                        <ul className="space-y-2 text-slate-600">
                            <li><strong>Name:</strong> {report.overview.experiment_name}</li>
                            <li><strong>ID:</strong> {report.overview.experiment_id}</li>
                            <li><strong>Population:</strong> {report.overview.population}</li>
                            <li><strong>Simulation Duration:</strong> {report.overview.simulation_duration}</li>
                            <li><strong>Random Seed:</strong> {report.overview.random_seed}</li>
                            <li><strong>Model Distribution:</strong> {JSON.stringify(report.overview.model_distribution)}</li>
                            <li><strong>Total Ticks:</strong> {report.overview.total_simulation_ticks}</li>
                            <li><strong>Total Events:</strong> {report.overview.total_events}</li>
                        </ul>
                    </div>

                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 border-b pb-2 mb-4">2. Multi-Dimensional Analysis</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
                                <h3 className="font-bold text-slate-800 mb-2">Safety</h3>
                                <pre className="text-xs overflow-auto text-slate-600">{JSON.stringify(report.safety_analysis, null, 2)}</pre>
                            </div>
                            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
                                <h3 className="font-bold text-slate-800 mb-2">Economy</h3>
                                <pre className="text-xs overflow-auto text-slate-600">{JSON.stringify(report.economic_analysis, null, 2)}</pre>
                            </div>
                            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
                                <h3 className="font-bold text-slate-800 mb-2">Society</h3>
                                <pre className="text-xs overflow-auto text-slate-600">{JSON.stringify(report.social_analysis, null, 2)}</pre>
                            </div>
                            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
                                <h3 className="font-bold text-slate-800 mb-2">AI Behaviour</h3>
                                <pre className="text-xs overflow-auto text-slate-600">{JSON.stringify(report.ai_behaviour_analysis, null, 2)}</pre>
                            </div>
                        </div>
                    </div>

                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 border-b pb-2 mb-4">3. Cross-Model Analysis</h2>
                        <p className="text-slate-600 mb-4">Total Interactions: {report.cross_model_analysis.total_cross_model_interactions || 0}</p>
                        <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 overflow-auto">
                            <pre className="text-xs text-slate-600">{JSON.stringify(report.cross_model_analysis.interaction_matrix, null, 2)}</pre>
                        </div>
                    </div>

                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 border-b pb-2 mb-4">4. Important Events (Event-to-Metric Traceability)</h2>
                        {report.important_events.length > 0 ? (
                            <ul className="space-y-3">
                                {report.important_events.map((ev: any, idx: number) => (
                                    <li key={idx} className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-sm">
                                        <div className="font-bold text-slate-700">{ev.action} <span className="text-slate-400 font-normal ml-2">{ev.timestamp}</span></div>
                                        <div className="text-slate-600 mt-1">Model: {ev.agent_model}</div>
                                        <div className="text-slate-500 italic mt-1">{ev.outcome}</div>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="text-slate-500 italic">No significant events logged.</p>
                        )}
                    </div>

                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 border-b pb-2 mb-4">5. Research Findings</h2>
                        <ul className="list-disc list-inside space-y-2 text-slate-600 leading-relaxed">
                            {report.findings.map((f: string, i: number) => <li key={i}>{f}</li>)}
                        </ul>
                    </div>

                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 border-b pb-2 mb-4">6. Limitations</h2>
                        <ul className="list-disc list-inside space-y-2 text-slate-600 leading-relaxed">
                            {report.limitations.map((l: string, i: number) => <li key={i}>{l}</li>)}
                        </ul>
                    </div>

                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 border-b pb-2 mb-4">7. Conclusion</h2>
                        <p className="text-slate-600 leading-relaxed">{report.conclusion}</p>
                    </div>

                    <hr className="my-10 border-slate-200" />
                    <p className="text-sm text-slate-500 italic text-center font-medium">Auto-generated by AI WorldSim Analytics Engine.<br/>Data verified against Phase 9 traceability requirements.</p>
                </div>
            )}
        </div>
    );
}
