import React, { useEffect, useState } from 'react';
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
