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
import InteractionMatrix from './pages/InteractionMatrix';
import ImpactSimulator from './pages/ImpactSimulator';

export default function App() {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                    <Route path="/" element={<Overview />} />
                    <Route path="/impact" element={<ImpactSimulator />} />
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
                    <Route path="/matrix" element={<InteractionMatrix />} />
                    <Route path="/report" element={<FinalReport />} />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
}
