import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Activity, Map, Users, DollarSign, BookOpen, Heart, MessageSquare, Shield, FileText, BarChart2, FlaskConical, LayoutDashboard, Settings, Target } from 'lucide-react';
import SimulationControls from './SimulationControls';

const navItems = [
    { name: 'Overview', path: '/', icon: LayoutDashboard },
    { name: 'Live Simulation', path: '/simulation', icon: Map },
    { name: 'AI Agents', path: '/agents', icon: Users },
    { name: 'Economy', path: '/economy', icon: DollarSign },
    { name: 'Education', path: '/education', icon: BookOpen },
    { name: 'Healthcare', path: '/healthcare', icon: Heart },
    { name: 'Social', path: '/social', icon: MessageSquare },
    { name: 'Safety & Gov', path: '/safety', icon: Shield },
    { name: 'Event Logs', path: '/events', icon: FileText },
    { name: 'Analytics', path: '/analytics', icon: BarChart2 },
    { name: 'Experiments', path: '/experiments', icon: FlaskConical },
    { name: 'Interaction Matrix', path: '/matrix', icon: Target },
    { name: 'Final Report', path: '/report', icon: FileText }
];

export default function Layout({ children }: { children: React.ReactNode }) {
    const location = useLocation();

    return (
        <div className="flex h-screen bg-slate-50 text-slate-800 font-sans">
            <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col shadow-xl z-20">
                <div className="p-6 pb-2">
                    <h1 className="text-2xl font-black text-white flex items-center gap-2">
                        <Activity className="text-indigo-500" /> WorldSim
                    </h1>
                    <p className="text-[10px] text-slate-500 mt-2 uppercase tracking-widest font-bold">Research Platform</p>
                </div>
                <nav className="flex-1 overflow-y-auto py-4 space-y-1 px-3 custom-scrollbar mt-4">
                    {navItems.map(item => {
                        const Icon = item.icon;
                        const active = location.pathname === item.path;
                        return (
                            <Link key={item.name} to={item.path} 
                                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${active ? 'bg-indigo-600 text-white font-medium shadow-md shadow-indigo-900/50' : 'hover:bg-slate-800 hover:text-white'}`}>
                                <Icon size={18} className={active ? 'text-indigo-200' : 'text-slate-500'} />
                                {item.name}
                            </Link>
                        )
                    })}
                </nav>
            </aside>
            <div className="flex-1 flex flex-col min-w-0 bg-slate-50 relative">
                <header className="bg-white border-b border-slate-200 h-16 flex items-center px-6 shrink-0 z-10 shadow-sm justify-end">
                    <SimulationControls />
                </header>
                <main className="flex-1 overflow-auto p-8 relative">
                    <div className="max-w-7xl mx-auto h-full">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
