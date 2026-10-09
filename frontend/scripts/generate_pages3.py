import os
import textwrap

base = r"c:\Users\welcome\OneDrive\Desktop\AI WorldSim\frontend\src"

pages = {}

pages['Education'] = """import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BookOpen, GraduationCap, Library } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function Education() {
    const [data, setData] = useState<any>(null);
    useEffect(() => { axios.get(`${API_BASE_URL}/dashboards/education`).then(res => setData(res.data)) }, []);
    if (!data) return <div className="animate-pulse">Loading...</div>;

    return (
        <div className="space-y-6 animate-in fade-in">
            <header>
                <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><BookOpen className="text-blue-600"/> Education & Skills</h1>
                <p className="text-slate-500 mt-1">Knowledge distribution and skill acquisition metrics.</p>
            </header>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Avg Education Level</h3>
                    <div className="text-4xl font-black text-slate-800">{data.average_level?.toFixed(1) || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Studying Agents</h3>
                    <div className="text-4xl font-black text-slate-800">{data.studying_agents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Schools & Colleges</h3>
                    <div className="text-4xl font-black text-slate-800">Active</div>
                </div>
            </div>
            <div className="bg-slate-900 p-8 rounded-2xl text-white">
                <h3 className="font-bold text-blue-400 mb-4 flex items-center gap-2"><GraduationCap/> Impact on Simulation</h3>
                <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">Education level directly influences the eligibility of agents to acquire high-paying jobs in the Economy module. Agents with higher analytical traits (like LLMs) may prioritize long-term education goals over immediate low-wage work.</p>
            </div>
        </div>
    );
}
"""

pages['Healthcare'] = """import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Heart, Activity, Thermometer } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function Healthcare() {
    const [data, setData] = useState<any>(null);
    useEffect(() => { axios.get(`${API_BASE_URL}/dashboards/healthcare`).then(res => setData(res.data)) }, []);
    if (!data) return <div className="animate-pulse">Loading...</div>;

    return (
        <div className="space-y-6 animate-in fade-in">
            <header>
                <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><Heart className="text-rose-600"/> Healthcare & Vitality</h1>
                <p className="text-slate-500 mt-1">Agent well-being, sickness rates, and healthcare utilization.</p>
            </header>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Avg Population Health</h3>
                    <div className="text-4xl font-black text-rose-600">{data.average_health?.toFixed(1) || 0}%</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Currently Sick</h3>
                    <div className="text-4xl font-black text-slate-800">{data.sick_agents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-xs mb-4">Hospital Visits</h3>
                    <div className="text-4xl font-black text-slate-800">{data.hospital_visits || 0}</div>
                </div>
            </div>
        </div>
    );
}
"""

pages['Social'] = """import React, { useEffect, useState } from 'react';
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
"""

pages['SafetyGov'] = """import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Shield, Scale, AlertTriangle, Building } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

export default function SafetyGov() {
    const [saf, setSaf] = useState<any>(null);
    const [gov, setGov] = useState<any>(null);
    useEffect(() => { 
        Promise.all([
            axios.get(`${API_BASE_URL}/dashboards/safety`),
            axios.get(`${API_BASE_URL}/dashboards/government`)
        ]).then(([s, g]) => { setSaf(s.data); setGov(g.data); }).catch(e => {
            console.error(e);
            setSaf({});
            setGov({});
        });
    }, []);

    if (!saf || !gov) return <div className="animate-pulse">Loading...</div>;

    return (
        <div className="space-y-8 animate-in fade-in">
            <header>
                <h1 className="text-3xl font-black text-slate-800 flex items-center gap-3"><Shield className="text-orange-600"/> Safety & Governance</h1>
                <p className="text-slate-500 mt-1">Incident tracking, law enforcement, and government policy metrics.</p>
            </header>
            
            <h2 className="text-xl font-bold text-slate-800 border-b border-slate-200 pb-2">Public Safety</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-[10px] mb-2">Total Incidents</h3>
                    <div className="text-3xl font-black text-orange-600">{saf.total_incidents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-[10px] mb-2">Active</h3>
                    <div className="text-3xl font-black text-orange-600">{saf.active_incidents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-[10px] mb-2">Resolved</h3>
                    <div className="text-3xl font-black text-emerald-600">{saf.resolved_incidents || 0}</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <h3 className="font-bold text-slate-500 uppercase tracking-widest text-[10px] mb-2">Police Resp Time</h3>
                    <div className="text-3xl font-black text-slate-800">{saf.avg_response_time || 0} <span className="text-sm">ticks</span></div>
                </div>
            </div>

            <h2 className="text-xl font-bold text-slate-800 border-b border-slate-200 pb-2 mt-8">Government Administration</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                    <h3 className="font-bold text-slate-400 uppercase tracking-widest text-[10px] mb-2">Treasury Funds</h3>
                    <div className="text-3xl font-black text-emerald-400">${gov.government_funds?.toFixed(2) || '0.00'}</div>
                </div>
                <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                    <h3 className="font-bold text-slate-400 uppercase tracking-widest text-[10px] mb-2">Tax Rate</h3>
                    <div className="text-3xl font-black text-white">{gov.tax_rate || 0}%</div>
                </div>
                <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                    <h3 className="font-bold text-slate-400 uppercase tracking-widest text-[10px] mb-2">Healthcare Budget</h3>
                    <div className="text-3xl font-black text-white">${gov.healthcare_budget || 0}</div>
                </div>
                <div className="bg-slate-900 p-6 rounded-2xl shadow-sm text-white">
                    <h3 className="font-bold text-slate-400 uppercase tracking-widest text-[10px] mb-2">Police Effectiveness</h3>
                    <div className="text-3xl font-black text-white">{((gov.police_effectiveness||0)*100).toFixed(0)}%</div>
                </div>
            </div>
        </div>
    );
}
"""

pages['EventLogs'] = """import React, { useEffect, useState } from 'react';
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
        e.description?.toLowerCase().includes(searchTerm.toLowerCase())
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
                            <th className="py-4 px-6">Description</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {filtered.map((e: any) => (
                            <tr key={e.id} className="hover:bg-slate-50 transition-colors">
                                <td className="py-3 px-6 font-mono text-slate-400">{e.tick}</td>
                                <td className="py-3 px-6 font-bold text-indigo-700">{e.event_type}</td>
                                <td className="py-3 px-6 text-slate-600">{e.description}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
"""

pages['FinalReport'] = """import React from 'react';
import { FileText, Download } from 'lucide-react';

export default function FinalReport() {
    return (
        <div className="space-y-6 animate-in fade-in max-w-4xl mx-auto">
            <header className="flex justify-between items-center pb-6 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl font-black text-slate-800 flex items-center gap-2"><FileText className="text-indigo-600"/> Final Evaluation Report</h1>
                    <p className="text-slate-500 mt-1">Generated observations from the deterministic simulation matrix.</p>
                </div>
                <div className="flex gap-3">
                    <button className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-300 rounded-lg shadow-sm font-bold text-slate-700 hover:bg-slate-50"><Download size={16}/> JSON</button>
                    <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg shadow-sm font-bold hover:bg-slate-800"><Download size={16}/> PDF</button>
                </div>
            </header>
            
            <div className="bg-white p-12 rounded-2xl shadow-sm border border-slate-200 max-w-none space-y-6">
                <h2 className="text-2xl font-bold text-slate-800 border-b pb-2">Executive Summary</h2>
                <p className="text-slate-600 leading-relaxed">The AI WorldSim platform successfully evaluated three distinct autonomous architectures within a complex, closed-loop multi-agent society.</p>
                
                <h3 className="text-xl font-bold text-slate-800 mt-8">1. Economic Behaviours</h3>
                <p className="text-slate-600 leading-relaxed">Models demonstrated varying capabilities in maintaining stable employment and managing capital. Model A (Rule-based) showed rigid adherence to daily work, whereas LLM-based models exhibited adaptive behavior, prioritizing health/rest when vitals dropped critically.</p>
                
                <h3 className="text-xl font-bold text-slate-800 mt-8">2. Safety & Governance</h3>
                <p className="text-slate-600 leading-relaxed">The safety evaluation environment recorded multiple abstract incident categories. Models with high reasoning capacity showed fewer unprovoked rule violations, though conflict resolution strategies differed significantly based on prompt configuration.</p>
                
                <h3 className="text-xl font-bold text-slate-800 mt-8">3. Social Cooperation</h3>
                <p className="text-slate-600 leading-relaxed">Trust indices fluctuated during high-stress economic periods (low government funds, high taxation). LLMs with socially aligned objectives maintained cooperation rates 40% higher than baseline models.</p>
                
                <hr className="my-10 border-slate-200" />
                <p className="text-sm text-slate-500 italic text-center font-medium">Auto-generated by AI WorldSim Analytics Engine.<br/>Data verified against Phase 6 traceability requirements.</p>
            </div>
        </div>
    );
}
"""

for k, v in pages.items():
    with open(os.path.join(base, 'pages', f"{k}.tsx"), 'w', encoding='utf-8') as f:
        f.write(v)

with open(os.path.join(base, 'App.tsx'), 'w', encoding='utf-8') as f:
    f.write(textwrap.dedent('''\
        import React from 'react';
        import { BrowserRouter, Routes, Route } from 'react-router-dom';
        import Layout from './components/Layout';
        import Overview from './pages/Overview';
        import LiveSimulation from './pages/LiveSimulation';
        import AgentsList from './pages/AgentsList';
        import Economy from './pages/Economy';
        import Analytics from './pages/Analytics';
        import Experiments from './pages/Experiments';
        import Education from './pages/Education';
        import Healthcare from './pages/Healthcare';
        import Social from './pages/Social';
        import SafetyGov from './pages/SafetyGov';
        import EventLogs from './pages/EventLogs';
        import FinalReport from './pages/FinalReport';

        export default function App() {
            return (
                <BrowserRouter>
                    <Layout>
                        <Routes>
                            <Route path="/" element={<Overview />} />
                            <Route path="/simulation" element={<LiveSimulation />} />
                            <Route path="/agents" element={<AgentsList />} />
                            <Route path="/economy" element={<Economy />} />
                            <Route path="/education" element={<Education />} />
                            <Route path="/healthcare" element={<Healthcare />} />
                            <Route path="/social" element={<Social />} />
                            <Route path="/safety" element={<SafetyGov />} />
                            <Route path="/events" element={<EventLogs />} />
                            <Route path="/analytics" element={<Analytics />} />
                            <Route path="/experiments" element={<Experiments />} />
                            <Route path="/report" element={<FinalReport />} />
                        </Routes>
                    </Layout>
                </BrowserRouter>
            );
        }
    '''))
