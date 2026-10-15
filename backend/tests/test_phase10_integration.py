"""
Phase 10 — Comprehensive Integration & Regression Test Suite
Tests all critical workflows: API, simulation lifecycle, economy, society,
safety, education, healthcare, experiments, cross-model, report export.
"""
import pytest
import json
from fastapi.testclient import TestClient
from app.main import app
from app.database import models
from app.database.database import SessionLocal, Base, engine as db_engine
from app.database.seeder import seed_data

Base.metadata.create_all(bind=db_engine)

client = TestClient(app)

@pytest.fixture
def db():
    session = SessionLocal()
    seed_data(session)
    session.commit()
    try:
        yield session
    finally:
        session.close()

# ---------------------------------------------------------------------------
# 1. Simulation Lifecycle
# ---------------------------------------------------------------------------
class TestSimulationLifecycle:
    def test_status_endpoint_returns_correct_schema(self):
        r = client.get("/api/simulation/status")
        assert r.status_code == 200
        data = r.json()
        for key in ("is_running", "current_tick", "simulation_day", "simulation_time_str", "speed"):
            assert key in data

    def test_start_pause_resume_stop(self):
        r = client.post("/api/simulation/start")
        assert r.status_code == 200
        assert r.json()["status"] == "started"

        r = client.post("/api/simulation/pause")
        assert r.status_code == 200
        assert r.json()["status"] == "paused"

        r = client.post("/api/simulation/resume")
        assert r.status_code == 200
        assert r.json()["status"] == "resumed"

        r = client.post("/api/simulation/stop")
        assert r.status_code == 200
        assert r.json()["status"] == "stopped"

    def test_speed_update(self):
        r = client.post("/api/simulation/speed?speed=2.0")
        assert r.status_code == 200
        assert r.json()["speed"] == 2.0
        client.post("/api/simulation/speed?speed=1.0")

    def test_world_state_endpoint(self):
        r = client.get("/api/simulation/world")
        assert r.status_code == 200

    def test_events_endpoint(self):
        r = client.get("/api/simulation/events")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_runs_endpoint(self):
        r = client.get("/api/simulation/runs")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_decisions_endpoint(self):
        r = client.get("/api/simulation/decisions")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

# ---------------------------------------------------------------------------
# 2. Agent Endpoints
# ---------------------------------------------------------------------------
class TestAgentEndpoints:
    def test_get_agents_returns_list(self, db):
        r = client.get("/api/agents/")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_agents_have_required_fields(self, db):
        agents = client.get("/api/agents/").json()
        if agents:
            agent = agents[0]
            for field in ("id", "name", "model_type"):
                assert field in agent

    def test_get_single_agent(self, db):
        agents = client.get("/api/agents/").json()
        if agents:
            aid = agents[0]["id"]
            r = client.get(f"/api/agents/{aid}")
            assert r.status_code == 200
            assert r.json()["id"] == aid

# ---------------------------------------------------------------------------
# 3. Location Endpoints
# ---------------------------------------------------------------------------
class TestLocationEndpoints:
    def test_get_locations(self, db):
        r = client.get("/api/locations/")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_location_has_coordinates(self, db):
        locs = client.get("/api/locations/").json()
        if locs:
            loc = locs[0]
            assert "x" in loc and "y" in loc

# ---------------------------------------------------------------------------
# 4. Dashboard Endpoints
# ---------------------------------------------------------------------------
class TestDashboardEndpoints:
    DASHBOARDS = ["economy", "education", "healthcare", "social", "safety", "government"]

    @pytest.mark.parametrize("dashboard", DASHBOARDS)
    def test_dashboard_returns_200(self, dashboard, db):
        r = client.get(f"/api/dashboards/{dashboard}")
        assert r.status_code == 200

# ---------------------------------------------------------------------------
# 5. Economy System
# ---------------------------------------------------------------------------
class TestEconomySystem:
    def test_job_assignment_requires_education(self, db):
        from app.simulation.economy_system import EconomySystem
        agent = db.query(models.Agent).first()
        biz = db.query(models.Business).first()
        job = models.Job(title="Senior Scientist", business_id=biz.id, salary=500, required_education=99)
        db.add(job)
        db.commit()
        econ = EconomySystem(db, run_id=1, tick=1, day=1)
        result = econ.assign_job(agent, job.id)
        assert result is False

    def test_buy_product_deducts_money(self, db):
        from app.simulation.economy_system import EconomySystem
        agent = db.query(models.Agent).filter(models.Agent.money >= 50).first()
        product = db.query(models.Product).filter(models.Product.stock > 0).first()
        if agent and product:
            initial_money = agent.money
            econ = EconomySystem(db, run_id=1, tick=1, day=1)
            success = econ.buy_product(agent, product.id)
            db.commit()
            db.refresh(agent)
            assert success is True
            assert agent.money < initial_money

# ---------------------------------------------------------------------------
# 6. Education System
# ---------------------------------------------------------------------------
class TestEducationSystem:
    def test_study_increases_progress(self, db):
        from app.simulation.education_system import EducationSystem
        agent = db.query(models.Agent).first()
        initial_progress = agent.education_progress
        edu = EducationSystem(db, run_id=1, tick=1, day=1)
        edu.study(agent, None)
        db.refresh(agent)
        assert agent.education_progress >= initial_progress

# ---------------------------------------------------------------------------
# 7. Healthcare System
# ---------------------------------------------------------------------------
class TestHealthcareSystem:
    def test_health_degradation_and_treatment(self, db):
        from app.simulation.healthcare_system import HealthcareSystem
        agent = db.query(models.Agent).first()
        agent.health = 40.0
        agent.money = 200.0
        db.commit()
        hs = HealthcareSystem(db, run_id=1, tick=1, day=1)
        treated = hs.treat_agent(agent, None)
        db.commit()
        db.refresh(agent)
        assert treated is True
        assert agent.health > 40.0

# ---------------------------------------------------------------------------
# 8. Social System
# ---------------------------------------------------------------------------
class TestSocialSystem:
    def test_talk_and_cooperate(self, db):
        from app.simulation.social_system import SocialSystem
        agents = db.query(models.Agent).limit(2).all()
        if len(agents) == 2:
            ss = SocialSystem(db, run_id=1, tick=1, day=1)
            ss.talk(agents[0], agents[1])
            db.commit()
            rel = ss.get_or_create_relationship(agents[0].id, agents[1].id)
            assert rel is not None
            assert rel.trust >= 0.5

# ---------------------------------------------------------------------------
# 9. Safety System
# ---------------------------------------------------------------------------
class TestSafetySystem:
    def test_incident_reporting(self, db):
        from app.simulation.safety_system import SafetySystem
        agent = db.query(models.Agent).first()
        before = db.query(models.Incident).count()
        ss = SafetySystem(db, run_id=1, tick=1, day=1)
        ss.report_incident(agent, "CONFLICT", "LOW", "Test dispute", [agent.id], agent.current_location_id)
        db.commit()
        after = db.query(models.Incident).count()
        assert after > before

# ---------------------------------------------------------------------------
# 10. Metrics Engine
# ---------------------------------------------------------------------------
class TestMetricsEngine:
    def test_definitions_endpoint(self):
        r = client.get("/api/metrics/definitions")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, dict)
        assert "employment_rate" in data

    def test_snapshots_endpoint(self):
        r = client.get("/api/metrics/snapshots")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

# ---------------------------------------------------------------------------
# 11. Experiment & Report Lifecycle
# ---------------------------------------------------------------------------
class TestExperimentAndReport:
    def test_experiment_creation_run_and_report(self, db):
        # 1. Create experiment
        r = client.post("/api/experiments?name=FullExp&population=6&runs=1&duration_days=1")
        assert r.status_code == 200
        exp_id = r.json()["id"]

        # 2. Run experiment
        r2 = client.post(f"/api/experiments/{exp_id}/run")
        assert r2.status_code == 200
        assert r2.json()["status"] == "success"

        # 3. Generate Report
        r3 = client.post(f"/api/experiments/{exp_id}/generate-report")
        assert r3.status_code == 200
        assert r3.json()["status"] == "success"

        # 4. Fetch Report
        r4 = client.get(f"/api/experiments/{exp_id}/report")
        assert r4.status_code == 200
        report = r4.json()
        assert "overview" in report
        assert "findings" in report
        assert "limitations" in report
        assert "conclusion" in report

        # 5. Export JSON
        r_json = client.get(f"/api/experiments/{exp_id}/export/json")
        assert r_json.status_code == 200
        assert len(r_json.content) > 50

        # 6. Export CSV
        r_csv = client.get(f"/api/experiments/{exp_id}/export/csv")
        assert r_csv.status_code == 200
        assert len(r_csv.content) > 0

        # 7. Export PDF
        r_pdf = client.get(f"/api/experiments/{exp_id}/export/pdf")
        assert r_pdf.status_code == 200
        assert len(r_pdf.content) > 100

# ---------------------------------------------------------------------------
# 12. Shared World & Action Validation
# ---------------------------------------------------------------------------
class TestSharedWorldAndValidation:
    def test_all_models_share_locations(self, db):
        agents = db.query(models.Agent).all()
        loc_ids = {l.id for l in db.query(models.Location).all()}
        for a in agents:
            if a.current_location_id:
                assert a.current_location_id in loc_ids

    def test_action_validator_rest_and_invalid(self, db):
        from app.simulation.action_validator import ActionValidator
        from app.simulation.world_state import WorldState
        from app.ai.agent_architecture import AgentAction
        agent = db.query(models.Agent).first()
        validator = ActionValidator(db)
        ws = WorldState()
        ws.update_time(1)

        valid, _, _ = validator.validate(agent, AgentAction(action="REST", reason="resting"), ws)
        assert valid is True

        invalid, _, _ = validator.validate(agent, AgentAction(action="NON_EXISTENT_ACTION", reason="testing"), ws)
        assert invalid is False
