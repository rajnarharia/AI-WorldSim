# AI WorldSim — AI Real-World Simulation Platform

**AI WorldSim** is an autonomous multi-agent simulation platform designed to evaluate and compare multiple Large Language Models (LLMs) and decision-making architectures within a single, unified virtual society.

In AI WorldSim, autonomous AI citizens powered by **Model A**, **Model B**, and **Model C** coexist inside **one shared city**—sharing locations, the economy, companies, banks, schools, hospitals, legal/police systems, and government.

---

## 🏛️ System Architecture

AI WorldSim adheres to a strict unidirectional simulation loop:

```
[ Frontend: React 18 + Tailwind + Lucide + Chart.js ]
                     │  HTTP / REST
                     ▼
[ FastAPI Backend / Async API Gateway ]
                     │
                     ▼
[ SimulationEngine (Tick Clock: 1 tick = 1 hr, 24 ticks = 1 day) ]
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
 [Observation]  [Decision]   [Validation]
  Engine         Engine       Engine
        │            │            │
        └────────────┼────────────┘
                     ▼
           [ActionExecutor]
                     │
   ┌─────────────────┼─────────────────┐
   ▼                 ▼                 ▼
[Economy]       [Society]          [Safety & Gov]
• Jobs & Salaries • Trust & Ties    • Incident Report
• Purchases       • Cooperation     • Investigation
• Businesses      • Conversations   • Court Resolution
   │                 │                 │
   └─────────────────┼─────────────────┘
                     ▼
       [Database / SQLite & EventLog]
                     │
                     ▼
[MetricsEngine, Multi-Run ExperimentRunner & FinalAnalysisEngine]
```

---

## 🌟 Key Features

1. **Shared Virtual City**:
   - 10 distinct physical zones: Residential, Corporate Park, Financial Center, City Hospital, University, Shopping Mall, Police HQ, District Court, City Hall, Central Park.
   - Coordinates-based movement and capacity management.

2. **Multi-Model Agent Population**:
   - AI citizens assigned across configurable distributions of **Model A**, **Model B**, and **Model C**.
   - Structured JSON observations: needs (energy, health, money, social), surroundings, local opportunities.
   - Fallback and strict rule-based safety nets to guarantee zero crashes during provider downtime.

3. **Domain Systems**:
   - **Economy System**: Dynamic balance, salaries, product catalogs, shopping, jobs with education/skill prerequisites.
   - **Healthcare System**: Health degradation, disease contagion risks, hospital check-ins, medical recovery.
   - **Education System**: Courses, skill progression, academic tiers qualifying citizens for high-paying roles.
   - **Social System**: Trust scoring (-1.0 to 1.0), cooperation index, cross-model dialogue, and reciprocity history.
   - **Safety & Governance System**: Crime/rule violation generation, police investigations, courtroom trials, bail, and deterrence laws.

4. **Experimentation & Research Analysis**:
   - Automated multi-run deterministic simulations with customizable random seeds.
   - Metrics Engine calculating 14+ standardized indicators per model category.
   - Cross-Model Interaction matrix mapping emergent behavior (cooperation vs. competition).
   - Automated report generation with findings, limitations, and multi-format exports:
     - **JSON** (Raw structured research data)
     - **CSV** (Metrics tables for R / Python data science analysis)
     - **PDF** (Formal research paper report format)

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, SQLite, Pydantic v2, FPDF2, Pytest.
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide React, React Router v6.
- **AI Engine**: Provider abstractions for OpenAI, Anthropic, Gemini, with local Rule-Based fallback engines.

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/rajnarharia/AI-WorldSim.git
cd AI-WorldSim
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

---

## 💻 Running the Platform Locally

### Start the Backend Server
```bash
# In backend directory with venv activated:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Documentation (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- Interactive OpenAPI Specs: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

### Start the Frontend Dashboard
```bash
# In frontend directory:
npm run dev
```
- Web Application: [http://localhost:5173](http://localhost:5173)

---

## 🧪 Testing & Verification

AI WorldSim includes a comprehensive 45-test suite covering core unit systems and end-to-end integration workflows.

### Running Pytest
```bash
cd backend
.\venv\Scripts\activate
python -m pytest tests/ -v
```

**Test Coverage Highlights:**
- `test_simulation.py`: Clock ticks, day/night cycles, state transitions (start/pause/resume/stop/reset).
- `test_ai_agents.py`: Observation generation, heuristic decision fallbacks, full step loop execution.
- `test_society_systems.py`: Salary payouts, retail transactions, education progression, medical care, social bonding.
- `test_safety_system.py`: Incident reporting, police dispatch, investigation, court verdicts.
- `test_metrics_engine.py`: Multi-model statistical aggregation, snapshot recording.
- `test_phase10_integration.py`: End-to-end API lifecycle, shared-world data consistency, multi-model experiments, report generation, and JSON/CSV/PDF exports.

### Frontend Production Build
```bash
cd frontend
npm run build
```

---

## 📊 Available Dashboards & Views

| Route | View Name | Description |
|---|---|---|
| `/` | **Overview** | High-level simulation health, population stats, live clock. |
| `/simulation` | **Live Simulation** | Real-time map with interactive controls and tick inspector. |
| `/agents` | **Citizens Directory** | Inspect individual agent profiles, model types, needs, and wallets. |
| `/economy` | **Economy Dashboard** | Business revenues, job listings, transactions ledger. |
| `/education` | **Education Dashboard** | University enrollments, skill milestones, degree holders. |
| `/healthcare` | **Healthcare Dashboard** | Hospital occupancy, wellness indices, treatment recovery stats. |
| `/social` | **Social & Relations** | Trust network, cooperation metrics, interpersonal links. |
| `/safety` | **Safety & Governance** | Active police cases, court hearings, law compliance ratings. |
| `/events` | **Event Logs** | Real-time filtered feed of all societal interactions. |
| `/analytics` | **Analytics Engine** | Comparative model metrics and aggregate snapshots. |
| `/experiments` | **Experiment Runner** | Configure population distribution, batch runs, seed controls. |
| `/matrix` | **Interaction Matrix** | Heatmap of Model A ↔ Model B ↔ Model C cross-model actions. |
| `/report` | **Final Research Report**| Automated formal report generator with PDF/CSV/JSON exports. |

---

## 📄 License
MIT License. Built for advanced multi-agent behavioral research.
