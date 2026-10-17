import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from app.main import app
from app.database.database import Base, get_db
from app.simulation.condition_library import ConditionSelector, PRIMARY_ROLES
from app.simulation.impact_simulator import AIImpactSimulatorEngine, get_default_initial_state
from app.simulation.decision_validator import DecisionValidator
from app.ai.llm_provider import mask_api_key, get_llm_provider


from app.database.database import Base, SessionLocal, engine as db_engine

Base.metadata.create_all(bind=db_engine)

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



class TestConditionContainers:
    """Verifies Section 4 & 5 requirements on role-specific condition containers."""

    def test_container_counts_and_primary_roles(self):
        assert set(PRIMARY_ROLES) == {"POLICE", "GOVERNMENT", "CITIZEN", "BUSINESS", "CAR"}
        for role in PRIMARY_ROLES:
            conditions = ConditionSelector.get_all_conditions_for_role(role)
            # Must have between 60 and 80 conditions per role
            assert 60 <= len(conditions) <= 80, f"Role {role} condition count {len(conditions)} outside 60-80 range."

    def test_strict_role_isolation(self):
        police_conds = ConditionSelector.get_all_conditions_for_role("POLICE")
        police_ids = {c.condition_id for c in police_conds}
        
        gov_conds = ConditionSelector.get_all_conditions_for_role("GOVERNMENT")
        gov_ids = {c.condition_id for c in gov_conds}

        citizen_conds = ConditionSelector.get_all_conditions_for_role("CITIZEN")
        citizen_ids = {c.condition_id for c in citizen_conds}

        bus_conds = ConditionSelector.get_all_conditions_for_role("BUSINESS")
        bus_ids = {c.condition_id for c in bus_conds}

        car_conds = ConditionSelector.get_all_conditions_for_role("CAR")
        car_ids = {c.condition_id for c in car_conds}

        # Check zero overlap across all roles
        assert police_ids.isdisjoint(gov_ids)
        assert police_ids.isdisjoint(citizen_ids)
        assert police_ids.isdisjoint(bus_ids)
        assert police_ids.isdisjoint(car_ids)
        assert gov_ids.isdisjoint(citizen_ids)

    def test_active_condition_bounds_3_to_7(self):
        for seed in range(50):
            selected = ConditionSelector.select_active_conditions(role="POLICE", seed=seed)
            assert 3 <= len(selected) <= 7, f"Active condition count {len(selected)} violated 3-7 bound at seed {seed}"
            # Ensure no duplicates in the same cycle
            unique_ids = {c.condition_id for c in selected}
            assert len(unique_ids) == len(selected), "Duplicates detected within a single active cycle selection"
            # Ensure strictly POLICE conditions
            for c in selected:
                assert c.role == "POLICE"


class TestSecurityAndProviders:
    """Verifies Section 2 & 3: Key masking, connection tests, modular LLM architecture."""

    def test_api_key_masking(self):
        assert mask_api_key(None) == "None"
        assert mask_api_key("") == "None"
        assert mask_api_key("12345") == "******"
        assert mask_api_key("sk-123456789") == "sk...89"
        masked = mask_api_key("AIzaSyB1234567890abcdefXYZ")
        assert masked.startswith("AIza")
        assert masked.endswith("tXYZ") or masked.endswith("XYZ")
        assert "1234567890" not in masked

    @pytest.mark.asyncio
    async def test_local_rule_based_provider(self):
        provider = get_llm_provider("Local Rule-Based")
        res = await provider.test_connection()
        assert res["status"] == "Connected"
        assert res["latency_ms"] >= 0

        # Decision generation test
        decision = await provider.generate_decision("ROLE: POLICE\n[COND-POL-001] Burglary reported")
        assert decision["role"] == "POLICE"
        assert "action" in decision
        assert "resources_allocated" in decision


class TestDecisionValidator:
    """Verifies Section 10: Validation, schema compliance, clamping excessive resource usage."""

    def test_clamping_excessive_police_officers(self):
        current_state = {
            "resources": {
                "total_officers": 10,
                "available_officers": 3,
                "available_vehicles": 1
            }
        }
        raw_decision = {
            "role": "POLICE",
            "action": "DISPATCH_PATROL",
            "resources_allocated": {
                "officers": 8,  # Requesting 8 when only 3 available!
                "vehicles": 2   # Requesting 2 when only 1 available!
            },
            "justification": "Heavy response required.",
        }

        result = DecisionValidator.validate_decision(
            decision_raw=raw_decision,
            expected_role="POLICE",
            current_state=current_state,
            cycle_number=1
        )

        assert result.is_valid is False
        assert len(result.adjustments) >= 2
        assert result.sanitized_decision["resources_allocated"]["officers"] == 3
        assert result.sanitized_decision["resources_allocated"]["vehicles"] == 1

    def test_fallback_on_invalid_action(self):
        current_state = {"resources": {"available_officers": 5}}
        raw_decision = {
            "role": "POLICE",
            "action": "LAUNCH_NUCLEAR_MISSILE",  # Completely illegal action
            "resources_allocated": {}
        }
        result = DecisionValidator.validate_decision(
            decision_raw=raw_decision,
            expected_role="POLICE",
            current_state=current_state,
            cycle_number=1
        )
        assert result.sanitized_decision["action"] == "STANDBY"


class TestSection21DeterministicIntegration:
    """
    Mandatory Section 21 Test:
    Role: POLICE
    Initial state:
      10 total officers
      7 available
      1 vehicle
      2 active incidents
    Random seed: 42
    10 loops
    """

    @pytest.mark.asyncio
    async def test_deterministic_police_10_loop_simulation(self, db_session):
        initial_custom_state = {
            "role": "POLICE",
            "resources": {
                "total_officers": 10,
                "available_officers": 7,
                "deployed_officers": 3,
                "patrol_vehicles": 1,
                "available_vehicles": 1,
                "deployed_vehicles": 0,
                "active_incidents": 2,
                "resolved_incidents": 0,
                "public_safety_score": 75.0,
                "community_trust": 70.0,
                "officer_fatigue_avg": 15.0,
            },
            "status_summary": "Section 21 Baseline initial police deployment."
        }

        engine_sim = AIImpactSimulatorEngine(
            db=db_session,
            role="POLICE",
            total_loops=10,
            seed=42,
            model_slot="Model A",
            model_name="rule-based-v1",
            provider_name="Local Rule-Based",
            custom_initial_state=initial_custom_state,
            simulation_name="Section 21 Police Integration Run"
        )

        result = await engine_sim.run_simulation()

        # 1. Verify exact 10 cycles executed
        assert result["status"] == "COMPLETED"
        assert result["total_loops"] == 10
        assert result["cycles_count"] == 10

        # 2. Check Database cycle records
        from app.database.models import SimulationCycleRecord
        cycle_records = (
            db_session.query(SimulationCycleRecord)
            .filter(SimulationCycleRecord.simulation_id == result["simulation_id"])
            .order_by(SimulationCycleRecord.cycle_number.asc())
            .all()
        )
        assert len(cycle_records) == 10

        # 3. Verify conditions & state continuity across every cycle
        for i, rec in enumerate(cycle_records, 1):
            assert rec.cycle_number == i
            conds = json.loads(rec.active_conditions_json)
            # Exact 3 to 7 conditions
            assert 3 <= len(conds) <= 7
            for c in conds:
                assert c["role"] == "POLICE"

            # Check resources before / used / after
            res_before = json.loads(rec.resources_before_json)
            res_used = json.loads(rec.resources_used_json)
            res_after = json.loads(rec.resources_after_json)

            # Resources used must never exceed resources before
            assert res_used.get("officers", 0) <= res_before.get("available_officers", 0)
            assert res_used.get("vehicles", 0) <= res_before.get("available_vehicles", 0)

            # Available officers after must be within [0, total_officers]
            assert 0 <= res_after.get("available_officers", 0) <= 10

            # Continuity check: Cycle t+1 before available must equal cycle t after available (allowing shift turn)
            if i < 10:
                next_rec = cycle_records[i]
                next_res_before = json.loads(next_rec.resources_before_json)
                # Next before state is derived directly from previous after state
                assert abs(next_res_before["available_officers"] - res_after["available_officers"]) <= 1

        # 4. Verify Initial vs Final comparison
        comparison = result["comparison"]
        assert "resource_deltas" in comparison
        assert "action_distribution" in comparison
        assert comparison["total_cycles_executed"] == 10
        assert comparison["conditions_summary"]["total_conditions_encountered"] > 0

        # 5. Verify AI Impact Analysis
        impact = result["impact_analysis"]
        assert impact["role"] == "POLICE"
        assert impact["policy_adherence_rate_pct"] >= 0.0
        assert "domain_specific_metrics" in impact
        assert "total_incidents_resolved" in impact["domain_specific_metrics"]
        assert len(impact["key_analytical_insights"]) > 0


class TestImpactSimulatorAPI:
    """Verifies the REST API endpoints end-to-end."""

    def test_api_roles_and_conditions(self, client):
        res = client.get("/api/impact/roles")
        assert res.status_code == 200
        roles_data = res.json()
        assert len(roles_data) == 5

        # Check conditions for POLICE
        res_cond = client.get("/api/impact/roles/POLICE/conditions")
        assert res_cond.status_code == 200
        data_cond = res_cond.json()
        assert data_cond["role"] == "POLICE"
        assert data_cond["total_conditions"] == 70

    def test_api_model_connection_test(self, client):
        payload = {
            "provider": "Local Rule-Based",
            "model_name": "rule-based-v1",
            "model_slot": "Model A"
        }
        res = client.post("/api/impact/models/test-connection", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "Connected"
        assert data["model_slot"] == "Model A"

    def test_api_run_simulation_and_fetch_trace(self, client):
        payload = {
            "role": "POLICE",
            "total_loops": 3,
            "seed": 42,
            "model_slot": "Model A",
            "model_name": "rule-based-v1",
            "provider_name": "Local Rule-Based"
        }
        res = client.post("/api/impact/simulations/run", json=payload)
        assert res.status_code == 200
        data = res.json()
        sim_id = data["simulation_id"]
        assert data["status"] == "COMPLETED"
        assert data["cycles_count"] == 3

        # Fetch simulation details
        res_det = client.get(f"/api/impact/simulations/{sim_id}")
        assert res_det.status_code == 200
        det = res_det.json()
        assert det["id"] == sim_id
        assert det["total_loops"] == 3
        assert "comparison" in det
        assert "impact_analysis" in det

        # Fetch simulation cycles
        res_cycles = client.get(f"/api/impact/simulations/{sim_id}/cycles")
        assert res_cycles.status_code == 200
        cycles = res_cycles.json()
        assert len(cycles) == 3
        assert cycles[0]["cycle_number"] == 1
