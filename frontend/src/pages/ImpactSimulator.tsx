import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
    Cpu, Shield, CheckCircle2, AlertTriangle, Play, RefreshCw, Zap, 
    ArrowRight, Activity, Database, Check, X, FileText, ChevronRight, Sliders, Layers
} from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

interface ModelSlotConfig {
    slot: string;
    provider: string;
    model_name: string;
    api_key: string;
    status: 'Connected' | 'Connection Failed' | 'Not Tested';
    latency_ms?: number;
    error_message?: string;
}

export default function ImpactSimulator() {
    const [activeTab, setActiveTab] = useState<'models' | 'role' | 'run' | 'trace' | 'analysis'>('models');
    
    // Model Selection & Providers
    const [modelMode, setModelMode] = useState<'single' | 'multi'>('single');
    const [configs, setConfigs] = useState<ModelSlotConfig[]>([
        { slot: 'Model A', provider: 'Local Rule-Based', model_name: 'rule-based-v1', api_key: '', status: 'Not Tested' },
        { slot: 'Model B', provider: 'Google Gemini', model_name: 'gemini-1.5-flash', api_key: '', status: 'Not Tested' },
        { slot: 'Model C', provider: 'OpenAI-compatible', model_name: 'gpt-4o-mini', api_key: '', status: 'Not Tested' },
    ]);
    const [testingSlot, setTestingSlot] = useState<string | null>(null);

    // Role & Conditions
    const [selectedRole, setSelectedRole] = useState<'POLICE' | 'GOVERNMENT' | 'CITIZEN' | 'BUSINESS' | 'CAR'>('POLICE');
    const [roleConditions, setRoleConditions] = useState<any[]>([]);
    const [loadingConditions, setLoadingConditions] = useState(false);

    // Simulation Setup
    const [loopCount, setLoopCount] = useState<number>(10);
    const [customLoop, setCustomLoop] = useState<string>('10');
    const [seed, setSeed] = useState<number>(42);
    const [isSimulating, setIsSimulating] = useState(false);
    
    // Results
    const [simulationResult, setSimulationResult] = useState<any>(null);
    const [cycleTraces, setCycleTraces] = useState<any[]>([]);
    const [selectedCycleIndex, setSelectedCycleIndex] = useState<number>(0);

    // Fetch initial role conditions on role change
    useEffect(() => {
        fetchRoleConditions(selectedRole);
    }, [selectedRole]);

    const fetchRoleConditions = async (role: string) => {
        try {
            setLoadingConditions(true);
            const res = await axios.get(`${API_BASE_URL}/impact/roles/${role}/conditions`);
            setRoleConditions(res.data.conditions || []);
        } catch (e) {
            console.error('Failed to load role conditions', e);
        } finally {
            setLoadingConditions(false);
        }
    };

    const handleTestConnection = async (slotName: string) => {
        const target = configs.find(c => c.slot === slotName);
        if (!target) return;

        setTestingSlot(slotName);
        try {
            const res = await axios.post(`${API_BASE_URL}/impact/models/test-connection`, {
                provider: target.provider,
                model_name: target.model_name,
                api_key: target.api_key,
                model_slot: slotName,
            });

            setConfigs(prev => prev.map(c => {
                if (c.slot === slotName) {
                    return {
                        ...c,
                        status: res.data.status,
                        latency_ms: res.data.latency_ms,
                        error_message: res.data.error,
                    };
                }
                return c;
            }));
        } catch (err: any) {
            setConfigs(prev => prev.map(c => {
                if (c.slot === slotName) {
                    return {
                        ...c,
                        status: 'Connection Failed',
                        error_message: err.message,
                    };
                }
                return c;
            }));
        } finally {
            setTestingSlot(null);
        }
    };

    const handleRunSimulation = async () => {
        const effectiveLoops = loopCount === -1 ? parseInt(customLoop) || 10 : loopCount;
        setIsSimulating(true);
        try {
            const activeConfig = configs[0];
            const payload = {
                role: selectedRole,
                total_loops: effectiveLoops,
                seed: seed,
                model_slot: activeConfig.slot,
                model_name: activeConfig.model_name,
                provider_name: activeConfig.provider,
                api_key: activeConfig.api_key || undefined,
            };

            const runRes = await axios.post(`${API_BASE_URL}/impact/simulations/run`, payload);
            setSimulationResult(runRes.data);

            // Fetch cycle traces
            const simId = runRes.data.simulation_id;
            const cycleRes = await axios.get(`${API_BASE_URL}/impact/simulations/${simId}/cycles`);
            setCycleTraces(cycleRes.data || []);
            setSelectedCycleIndex(0);

            // Jump to Trace or Analysis
            setActiveTab('trace');
        } catch (err: any) {
            console.error('Simulation run failed', err);
            alert(`Simulation Failed: ${err.response?.data?.detail || err.message}`);
        } finally {
            setIsSimulating(false);
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-500 pb-16">
            {/* Header */}
            <header className="flex flex-col md:flex-row justify-between items-start md:items-end border-b border-slate-200 pb-6 gap-4">
                <div>
                    <div className="flex items-center gap-2 mb-1">
                        <span className="bg-indigo-100 text-indigo-700 text-xs px-2.5 py-0.5 rounded-full font-bold uppercase tracking-wider">
                            Phase 10.5 Core Alignment
                        </span>
                        <span className="bg-emerald-100 text-emerald-700 text-xs px-2.5 py-0.5 rounded-full font-bold">
                            Deterministic State Store
                        </span>
                    </div>
                    <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3">
                        <Zap className="text-indigo-600 fill-indigo-600" /> AI Impact Simulator
                    </h1>
                    <p className="text-slate-500 mt-1">
                        Closed-loop condition-decision-state mutation cycle across autonomous municipal roles.
                    </p>
                </div>

                {/* Workflow Navigation Pills */}
                <div className="flex bg-slate-100 p-1.5 rounded-xl border border-slate-200 gap-1 text-xs font-bold">
                    <button 
                        onClick={() => setActiveTab('models')}
                        className={`px-3 py-2 rounded-lg transition-all ${activeTab === 'models' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        1. Models & Keys
                    </button>
                    <button 
                        onClick={() => setActiveTab('role')}
                        className={`px-3 py-2 rounded-lg transition-all ${activeTab === 'role' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        2. Role & Library
                    </button>
                    <button 
                        onClick={() => setActiveTab('run')}
                        className={`px-3 py-2 rounded-lg transition-all ${activeTab === 'run' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                    >
                        3. Execute Loops
                    </button>
                    {simulationResult && (
                        <>
                            <button 
                                onClick={() => setActiveTab('trace')}
                                className={`px-3 py-2 rounded-lg transition-all ${activeTab === 'trace' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                            >
                                4. Live Cycle Trace
                            </button>
                            <button 
                                onClick={() => setActiveTab('analysis')}
                                className={`px-3 py-2 rounded-lg transition-all ${activeTab === 'analysis' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
                            >
                                5. Impact Analysis
                            </button>
                        </>
                    )}
                </div>
            </header>

            {/* TAB 1: MODEL CONFIGURATION */}
            {activeTab === 'models' && (
                <div className="space-y-6">
                    <div className="flex justify-between items-center bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                        <div>
                            <h2 className="text-xl font-bold text-slate-800">Model Deployment Mode</h2>
                            <p className="text-sm text-slate-500">Configure single evaluation or cross-model benchmark slots.</p>
                        </div>
                        <div className="flex bg-slate-100 p-1 rounded-xl border border-slate-200">
                            <button 
                                onClick={() => setModelMode('single')}
                                className={`px-4 py-2 rounded-lg font-bold text-sm transition-all ${modelMode === 'single' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600'}`}
                            >
                                Single AI Model
                            </button>
                            <button 
                                onClick={() => setModelMode('multi')}
                                className={`px-4 py-2 rounded-lg font-bold text-sm transition-all ${modelMode === 'multi' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600'}`}
                            >
                                Multi-Model (A, B, C)
                            </button>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {(modelMode === 'single' ? [configs[0]] : configs).map((conf, idx) => (
                            <div key={conf.slot} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between space-y-6">
                                <div className="space-y-4">
                                    <div className="flex justify-between items-center">
                                        <span className="font-extrabold text-lg text-slate-800">{conf.slot}</span>
                                        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold ${
                                            conf.status === 'Connected' ? 'bg-emerald-100 text-emerald-700' :
                                            conf.status === 'Connection Failed' ? 'bg-rose-100 text-rose-700' :
                                            'bg-slate-100 text-slate-600'
                                        }`}>
                                            <span className={`w-2 h-2 rounded-full ${
                                                conf.status === 'Connected' ? 'bg-emerald-500' :
                                                conf.status === 'Connection Failed' ? 'bg-rose-500' : 'bg-slate-400'
                                            }`} />
                                            {conf.status}
                                        </span>
                                    </div>

                                    {/* Provider Selector */}
                                    <div>
                                        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">Provider</label>
                                        <select 
                                            value={conf.provider}
                                            onChange={(e) => {
                                                const val = e.target.value;
                                                setConfigs(prev => prev.map((c, i) => i === idx ? { ...c, provider: val, status: 'Not Tested' } : c));
                                            }}
                                            className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                        >
                                            <option value="Local Rule-Based">Local Rule-Based (Deterministic Offline)</option>
                                            <option value="Google Gemini">Google Gemini</option>
                                            <option value="OpenAI-compatible">OpenAI-compatible</option>
                                            <option value="Anthropic-compatible">Anthropic Claude</option>
                                        </select>
                                    </div>

                                    {/* Model Name */}
                                    <div>
                                        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">Model Name</label>
                                        <input 
                                            type="text" 
                                            value={conf.model_name}
                                            onChange={(e) => {
                                                const val = e.target.value;
                                                setConfigs(prev => prev.map((c, i) => i === idx ? { ...c, model_name: val, status: 'Not Tested' } : c));
                                            }}
                                            placeholder="e.g. gemini-1.5-flash or gpt-4o"
                                            className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-800 font-mono focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                        />
                                    </div>

                                    {/* API Key */}
                                    <div>
                                        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                                            API Key <span className="text-[10px] text-slate-400 font-normal">(Never exposed)</span>
                                        </label>
                                        <input 
                                            type="password" 
                                            value={conf.api_key}
                                            onChange={(e) => {
                                                const val = e.target.value;
                                                setConfigs(prev => prev.map((c, i) => i === idx ? { ...c, api_key: val, status: 'Not Tested' } : c));
                                            }}
                                            placeholder={conf.provider === 'Local Rule-Based' ? 'Not required for offline local' : 'Paste API Key'}
                                            disabled={conf.provider === 'Local Rule-Based'}
                                            className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
                                        />
                                    </div>

                                    {conf.latency_ms !== undefined && (
                                        <div className="text-xs text-slate-500 flex justify-between bg-slate-50 p-2 rounded-lg border border-slate-100">
                                            <span>Ping Latency:</span>
                                            <span className="font-bold text-slate-700">{conf.latency_ms} ms</span>
                                        </div>
                                    )}

                                    {conf.error_message && (
                                        <div className="text-xs text-rose-600 bg-rose-50 p-2.5 rounded-lg border border-rose-200 leading-tight">
                                            {conf.error_message}
                                        </div>
                                    )}
                                </div>

                                <button 
                                    onClick={() => handleTestConnection(conf.slot)}
                                    disabled={testingSlot === conf.slot}
                                    className="w-full flex items-center justify-center gap-2 bg-slate-900 hover:bg-slate-800 text-white font-bold py-2.5 rounded-xl text-sm transition-all disabled:opacity-50"
                                >
                                    {testingSlot === conf.slot ? <RefreshCw size={16} className="animate-spin" /> : <Activity size={16} />}
                                    Test Connection
                                </button>
                            </div>
                        ))}
                    </div>

                    <div className="flex justify-end pt-4">
                        <button 
                            onClick={() => setActiveTab('role')}
                            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-3 rounded-xl shadow-lg shadow-indigo-600/30 transition-all"
                        >
                            Continue to Role Configuration <ArrowRight size={18} />
                        </button>
                    </div>
                </div>
            )}

            {/* TAB 2: ROLE CONFIGURATION & DEDICATED CONTAINER */}
            {activeTab === 'role' && (
                <div className="space-y-6">
                    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                        <h2 className="text-xl font-bold text-slate-800 mb-2">Primary Agent Role & Isolated Condition Container</h2>
                        <p className="text-sm text-slate-500 mb-6">
                            Each role possesses an independent container of 70 specialized conditions. Conditions never cross roles.
                        </p>

                        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                            {(['POLICE', 'GOVERNMENT', 'CITIZEN', 'BUSINESS', 'CAR'] as const).map(role => (
                                <button
                                    key={role}
                                    onClick={() => setSelectedRole(role)}
                                    className={`p-4 rounded-xl border text-left transition-all ${
                                        selectedRole === role 
                                        ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-500 shadow-sm' 
                                        : 'border-slate-200 bg-white hover:border-slate-300'
                                    }`}
                                >
                                    <div className="font-extrabold text-sm text-slate-800">{role}</div>
                                    <div className="text-xs text-slate-500 mt-1">70 Conditions</div>
                                    <div className="mt-2 text-[10px] uppercase font-bold text-indigo-600">
                                        {selectedRole === role ? 'Active Role' : 'Select'}
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Condition Container Inspector */}
                    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
                        <div className="flex justify-between items-center border-b border-slate-100 pb-4">
                            <div>
                                <h3 className="text-lg font-bold text-slate-800">
                                    Condition Library for {selectedRole} ({roleConditions.length} Total)
                                </h3>
                                <p className="text-xs text-slate-500">
                                    During each simulation cycle, the engine deterministically samples 3 to 7 active conditions.
                                </p>
                            </div>
                            <span className="text-xs font-mono font-bold bg-slate-100 px-3 py-1.5 rounded-lg text-slate-700">
                                Container: ROLE_{selectedRole}
                            </span>
                        </div>

                        {loadingConditions ? (
                            <div className="py-12 flex justify-center text-slate-400">
                                <RefreshCw className="animate-spin mr-2" size={20} /> Loading condition library...
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar">
                                {roleConditions.map(c => (
                                    <div key={c.condition_id} className="p-3.5 rounded-xl border border-slate-100 bg-slate-50 hover:bg-white hover:border-slate-200 transition-all text-xs space-y-2">
                                        <div className="flex justify-between items-start gap-2">
                                            <span className="font-mono font-bold text-slate-700">{c.condition_id}</span>
                                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                                c.severity === 'CRITICAL' ? 'bg-rose-100 text-rose-700' :
                                                c.severity === 'HIGH' ? 'bg-amber-100 text-amber-700' :
                                                c.severity === 'MEDIUM' ? 'bg-blue-100 text-blue-700' :
                                                'bg-slate-200 text-slate-700'
                                            }`}>
                                                {c.severity}
                                            </span>
                                        </div>
                                        <p className="font-medium text-slate-800 leading-snug">{c.description}</p>
                                        <div className="flex flex-wrap gap-1 text-[10px] text-slate-500">
                                            <span className="bg-white border border-slate-200 px-1.5 py-0.5 rounded">{c.category}</span>
                                            {c.resource_relevance?.slice(0, 2).map((r: string) => (
                                                <span key={r} className="bg-indigo-50 text-indigo-700 px-1.5 py-0.5 rounded">{r}</span>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    <div className="flex justify-between pt-4">
                        <button 
                            onClick={() => setActiveTab('models')}
                            className="text-slate-600 font-bold px-4 py-2 hover:text-slate-900"
                        >
                            Back to Models
                        </button>
                        <button 
                            onClick={() => setActiveTab('run')}
                            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-3 rounded-xl shadow-lg shadow-indigo-600/30 transition-all"
                        >
                            Configure & Run Simulation <ArrowRight size={18} />
                        </button>
                    </div>
                </div>
            )}

            {/* TAB 3: SIMULATION EXECUTION */}
            {activeTab === 'run' && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2 space-y-6">
                        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
                            <div>
                                <h2 className="text-xl font-bold text-slate-800">Simulation Parameters</h2>
                                <p className="text-sm text-slate-500">Set cycle loop count and deterministic seed.</p>
                            </div>

                            {/* Loop Count Selection */}
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Cycle Loop Count</label>
                                <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
                                    {[10, 50, 100, 500, 1000].map(cnt => (
                                        <button
                                            key={cnt}
                                            onClick={() => setLoopCount(cnt)}
                                            className={`py-2.5 rounded-xl font-bold text-sm border transition-all ${
                                                loopCount === cnt 
                                                ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' 
                                                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-white'
                                            }`}
                                        >
                                            {cnt} Loops
                                        </button>
                                    ))}
                                    <button
                                        onClick={() => setLoopCount(-1)}
                                        className={`py-2.5 rounded-xl font-bold text-sm border transition-all ${
                                            loopCount === -1 
                                            ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' 
                                            : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-white'
                                        }`}
                                    >
                                        Custom
                                    </button>
                                </div>
                                {loopCount === -1 && (
                                    <div className="mt-2">
                                        <input 
                                            type="number"
                                            value={customLoop}
                                            onChange={(e) => setCustomLoop(e.target.value)}
                                            placeholder="Enter number of loops (1-1000)"
                                            className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm font-bold text-slate-800"
                                        />
                                    </div>
                                )}
                            </div>

                            {/* Deterministic Seed */}
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Deterministic Random Seed</label>
                                <input 
                                    type="number"
                                    value={seed}
                                    onChange={(e) => setSeed(parseInt(e.target.value) || 0)}
                                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm font-mono text-slate-800 font-bold"
                                />
                                <span className="text-xs text-slate-400">Section 21 benchmark seed: 42.</span>
                            </div>

                            <button 
                                onClick={handleRunSimulation}
                                disabled={isSimulating}
                                className={`w-full py-4 rounded-xl font-black text-white text-base shadow-xl flex items-center justify-center gap-3 transition-all ${
                                    isSimulating 
                                    ? 'bg-slate-400 cursor-not-allowed' 
                                    : 'bg-indigo-600 hover:bg-indigo-700 hover:scale-[1.01] active:scale-[0.99] shadow-indigo-600/30'
                                }`}
                            >
                                {isSimulating ? <RefreshCw className="animate-spin" size={20} /> : <Play size={20} />}
                                {isSimulating ? 'EXECUTING SIMULATION PIPELINE...' : 'EXECUTE AI IMPACT SIMULATION'}
                            </button>
                        </div>
                    </div>

                    {/* Initial State Preview */}
                    <div className="bg-slate-900 text-white p-6 rounded-2xl shadow-sm space-y-4">
                        <div className="flex items-center gap-2 text-indigo-400 font-bold text-sm">
                            <Database size={18} /> Baseline Initial State ({selectedRole})
                        </div>
                        <p className="text-xs text-slate-400 leading-relaxed">
                            Initial resources deployed to the State Store before Cycle 1.
                        </p>

                        <div className="space-y-2.5 text-xs font-mono">
                            {selectedRole === 'POLICE' && (
                                <>
                                    <div className="flex justify-between border-b border-slate-800 pb-1.5">
                                        <span className="text-slate-400">Total Officers:</span>
                                        <span className="font-bold text-white">10</span>
                                    </div>
                                    <div className="flex justify-between border-b border-slate-800 pb-1.5">
                                        <span className="text-slate-400">Available Officers:</span>
                                        <span className="font-bold text-emerald-400">7</span>
                                    </div>
                                    <div className="flex justify-between border-b border-slate-800 pb-1.5">
                                        <span className="text-slate-400">Patrol Vehicles:</span>
                                        <span className="font-bold text-white">1</span>
                                    </div>
                                    <div className="flex justify-between border-b border-slate-800 pb-1.5">
                                        <span className="text-slate-400">Active Incidents:</span>
                                        <span className="font-bold text-rose-400">2</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-400">Public Safety Score:</span>
                                        <span className="font-bold text-indigo-400">75.0 / 100</span>
                                    </div>
                                </>
                            )}
                            {selectedRole === 'GOVERNMENT' && (
                                <>
                                    <div className="flex justify-between border-b border-slate-800 pb-1.5">
                                        <span className="text-slate-400">Treasury Balance:</span>
                                        <span className="font-bold text-emerald-400">$100,000.00</span>
                                    </div>
                                    <div className="flex justify-between border-b border-slate-800 pb-1.5">
                                        <span className="text-slate-400">Available Inspectors:</span>
                                        <span className="font-bold text-white">5</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-400">Public Approval:</span>
                                        <span className="font-bold text-indigo-400">65.0%</span>
                                    </div>
                                </>
                            )}
                            {selectedRole !== 'POLICE' && selectedRole !== 'GOVERNMENT' && (
                                <div className="text-slate-400 text-xs py-2">Standard operational profile ready.</div>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* TAB 4: LIVE CYCLE TRACE */}
            {activeTab === 'trace' && simulationResult && (
                <div className="space-y-6">
                    {/* Cycle Selector Bar */}
                    <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between gap-4 overflow-x-auto">
                        <div className="flex items-center gap-2 shrink-0">
                            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Cycle Timeline:</span>
                        </div>
                        <div className="flex gap-2">
                            {cycleTraces.map((c, i) => (
                                <button
                                    key={c.cycle_number}
                                    onClick={() => setSelectedCycleIndex(i)}
                                    className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                                        selectedCycleIndex === i 
                                        ? 'bg-indigo-600 text-white shadow-sm' 
                                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    }`}
                                >
                                    Cycle {c.cycle_number}
                                </button>
                            ))}
                        </div>
                        <button 
                            onClick={() => setActiveTab('analysis')}
                            className="shrink-0 flex items-center gap-1.5 bg-slate-900 text-white text-xs font-bold px-4 py-2 rounded-xl"
                        >
                            View Final Impact <ChevronRight size={14} />
                        </button>
                    </div>

                    {/* Active Cycle Details */}
                    {cycleTraces[selectedCycleIndex] && (
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                            {/* Column 1: Active Conditions (3-7) */}
                            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
                                <div className="flex justify-between items-center border-b border-slate-100 pb-3">
                                    <h3 className="font-bold text-slate-800 text-sm">Active Conditions</h3>
                                    <span className="text-xs font-bold bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded">
                                        {cycleTraces[selectedCycleIndex].active_conditions.length} Conditions
                                    </span>
                                </div>
                                <div className="space-y-3">
                                    {cycleTraces[selectedCycleIndex].active_conditions.map((cond: any) => (
                                        <div key={cond.condition_id} className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1.5">
                                            <div className="flex justify-between">
                                                <span className="font-mono font-bold text-slate-700">{cond.condition_id}</span>
                                                <span className="font-bold text-rose-600">{cond.severity}</span>
                                            </div>
                                            <p className="font-medium text-slate-800">{cond.description}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Column 2: AI Decision & Validation */}
                            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
                                <div className="flex justify-between items-center border-b border-slate-100 pb-3">
                                    <h3 className="font-bold text-slate-800 text-sm">AI Decision (Validated)</h3>
                                    <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                                        cycleTraces[selectedCycleIndex].validation?.is_valid 
                                        ? 'bg-emerald-50 text-emerald-700' 
                                        : 'bg-amber-50 text-amber-700'
                                    }`}>
                                        {cycleTraces[selectedCycleIndex].validation?.is_valid ? 'Schema Compliant' : 'Sanitized'}
                                    </span>
                                </div>

                                <div className="space-y-3 text-xs">
                                    <div>
                                        <span className="text-slate-400 block mb-0.5 font-bold uppercase">Action</span>
                                        <span className="font-mono font-bold text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-lg text-sm block">
                                            {cycleTraces[selectedCycleIndex].decision.action}
                                        </span>
                                    </div>
                                    <div>
                                        <span className="text-slate-400 block mb-0.5 font-bold uppercase">Target Location</span>
                                        <span className="font-semibold text-slate-700">
                                            {cycleTraces[selectedCycleIndex].decision.target}
                                        </span>
                                    </div>
                                    <div>
                                        <span className="text-slate-400 block mb-0.5 font-bold uppercase">Resources Allocated</span>
                                        <pre className="bg-slate-900 text-emerald-400 p-2.5 rounded-lg text-[11px] font-mono">
                                            {JSON.stringify(cycleTraces[selectedCycleIndex].decision.resources_allocated, null, 2)}
                                        </pre>
                                    </div>
                                    <div>
                                        <span className="text-slate-400 block mb-0.5 font-bold uppercase">Justification</span>
                                        <p className="text-slate-600 italic bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                                            "{cycleTraces[selectedCycleIndex].decision.justification}"
                                        </p>
                                    </div>
                                </div>
                            </div>

                            {/* Column 3: State Continuity & Resources */}
                            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
                                <div className="flex justify-between items-center border-b border-slate-100 pb-3">
                                    <h3 className="font-bold text-slate-800 text-sm">State Continuity Delta</h3>
                                    <span className="text-xs font-bold text-slate-500">SimulationEngine Applied</span>
                                </div>

                                <div className="space-y-3 text-xs font-mono">
                                    <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 space-y-1">
                                        <div className="text-slate-400 uppercase text-[10px] font-bold">Resources Before Cycle</div>
                                        {Object.entries(cycleTraces[selectedCycleIndex].resources_before).slice(0, 4).map(([k, v]: any) => (
                                            <div key={k} className="flex justify-between text-slate-600">
                                                <span>{k}:</span>
                                                <span className="font-bold text-slate-800">{v}</span>
                                            </div>
                                        ))}
                                    </div>

                                    <div className="bg-indigo-50/50 p-3 rounded-xl border border-indigo-100 space-y-1">
                                        <div className="text-indigo-600 uppercase text-[10px] font-bold">Resources Allocated / Used</div>
                                        {Object.entries(cycleTraces[selectedCycleIndex].resources_used).map(([k, v]: any) => (
                                            <div key={k} className="flex justify-between text-indigo-900">
                                                <span>{k}:</span>
                                                <span className="font-bold text-rose-600">-{v}</span>
                                            </div>
                                        ))}
                                    </div>

                                    <div className="bg-emerald-50/40 p-3 rounded-xl border border-emerald-100 space-y-1">
                                        <div className="text-emerald-700 uppercase text-[10px] font-bold">Resulting Resources After</div>
                                        {Object.entries(cycleTraces[selectedCycleIndex].resources_after).slice(0, 4).map(([k, v]: any) => (
                                            <div key={k} className="flex justify-between text-emerald-950">
                                                <span>{k}:</span>
                                                <span className="font-bold text-emerald-700">{v}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* TAB 5: INITIAL VS FINAL & AI IMPACT ANALYSIS */}
            {activeTab === 'analysis' && simulationResult && (
                <div className="space-y-8 animate-in fade-in duration-500">
                    {/* Top KPI Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Net Impact</span>
                            <span className={`text-2xl font-black mt-1 block ${
                                simulationResult.impact_analysis.net_impact_assessment === 'POSITIVE' ? 'text-emerald-600' : 'text-slate-800'
                            }`}>
                                {simulationResult.impact_analysis.net_impact_assessment}
                            </span>
                            <span className="text-xs text-slate-500 mt-1 block">Validated by state deltas</span>
                        </div>
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Policy Adherence</span>
                            <span className="text-2xl font-black text-indigo-600 mt-1 block">
                                {simulationResult.impact_analysis.policy_adherence_rate_pct}%
                            </span>
                            <span className="text-xs text-slate-500 mt-1 block">Zero unauthorized state mutations</span>
                        </div>
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Total Cycles Evaluated</span>
                            <span className="text-2xl font-black text-slate-800 mt-1 block">
                                {simulationResult.cycles_count} Loops
                            </span>
                            <span className="text-xs text-slate-500 mt-1 block">Deterministic seed {simulationResult.impact_analysis.traceability?.seed}</span>
                        </div>
                        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Operational Resilience</span>
                            <span className="text-2xl font-black text-teal-600 mt-1 block">
                                {simulationResult.impact_analysis.operational_resilience}
                            </span>
                            <span className="text-xs text-slate-500 mt-1 block">Condition adaptation profile</span>
                        </div>
                    </div>

                    {/* Initial vs Final Comparison Table */}
                    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                        <div className="p-6 border-b border-slate-200">
                            <h2 className="text-xl font-bold text-slate-800">Initial State vs. Final State Comparison</h2>
                            <p className="text-xs text-slate-500 mt-0.5">
                                Exact resource deltas tracked from Cycle 0 through Cycle {simulationResult.cycles_count}.
                            </p>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse text-sm">
                                <thead>
                                    <tr className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                                        <th className="p-4 pl-6">Resource / Metric</th>
                                        <th className="p-4">Initial Value (Cycle 0)</th>
                                        <th className="p-4">Final Value (Cycle {simulationResult.cycles_count})</th>
                                        <th className="p-4">Absolute Delta</th>
                                        <th className="p-4 pr-6">% Shift</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100 font-mono text-xs">
                                    {Object.entries(simulationResult.comparison?.resource_deltas || {}).map(([key, data]: any) => (
                                        <tr key={key} className="hover:bg-slate-50/50">
                                            <td className="p-4 pl-6 font-bold text-slate-800">{key}</td>
                                            <td className="p-4 text-slate-600">{data.initial}</td>
                                            <td className="p-4 font-bold text-slate-800">{data.final}</td>
                                            <td className={`p-4 font-bold ${
                                                data.delta > 0 ? 'text-emerald-600' : data.delta < 0 ? 'text-rose-600' : 'text-slate-500'
                                            }`}>
                                                {data.delta > 0 ? `+${data.delta}` : data.delta}
                                            </td>
                                            <td className="p-4 pr-6 text-slate-500">
                                                {data.percent_change > 0 ? `+${data.percent_change}%` : `${data.percent_change}%`}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* Key Analytical Insights */}
                    <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-sm space-y-4">
                        <div className="flex items-center gap-2 text-indigo-400 font-bold text-sm">
                            <CheckCircle2 size={18} /> Research Findings & AI Impact Synthesis
                        </div>
                        <div className="space-y-2 text-sm text-slate-300">
                            {simulationResult.impact_analysis.key_analytical_insights?.map((insight: string, idx: number) => (
                                <p key={idx} className="flex items-start gap-2 leading-relaxed">
                                    <span className="text-indigo-400 font-bold">•</span> {insight}
                                </p>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
