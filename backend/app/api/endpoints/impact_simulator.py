from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

from app.database.database import get_db
from app.database.models import ModelConfiguration, ImpactSimulationRun, SimulationCycleRecord
from app.simulation.condition_library import ConditionSelector, PRIMARY_ROLES
from app.simulation.impact_simulator import AIImpactSimulatorEngine, get_default_initial_state
from app.ai.llm_provider import get_llm_provider, mask_api_key

router = APIRouter()


class TestConnectionRequest(BaseModel):
    provider: str
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_slot: Optional[str] = "Model A"


class SaveModelConfigRequest(BaseModel):
    model_slot: str
    provider: str
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None


class RunSimulationRequest(BaseModel):
    role: str = "POLICE"
    total_loops: int = Field(default=10, ge=1, le=1000)
    seed: int = 42
    model_slot: str = "Model A"
    model_name: Optional[str] = "rule-based-v1"
    provider_name: Optional[str] = "Local Rule-Based"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    custom_initial_state: Optional[Dict[str, Any]] = None
    simulation_name: Optional[str] = None


@router.post("/models/test-connection")
async def test_model_connection(req: TestConnectionRequest, db: Session = Depends(get_db)):
    """
    Tests connectivity to an AI model provider using a lightweight handshake.
    Never exposes raw API keys. Updates connection status in database.
    """
    provider = get_llm_provider(
        provider_type=req.provider,
        model_name=req.model_name,
        api_key=req.api_key,
        base_url=req.base_url,
    )

    result = await provider.test_connection()
    masked = mask_api_key(req.api_key)

    # Persist or update connection status in ModelConfiguration
    if req.model_slot:
        config = db.query(ModelConfiguration).filter(ModelConfiguration.model_slot == req.model_slot).first()
        if not config:
            config = ModelConfiguration(
                model_slot=req.model_slot,
                provider=req.provider,
                model_name=req.model_name or "default",
                api_key_masked=masked,
                base_url=req.base_url,
                connection_status=result.get("status", "Not Tested"),
                latency_ms=result.get("latency_ms"),
                error_message=result.get("error"),
                last_tested_at=datetime.utcnow(),
            )
            db.add(config)
        else:
            config.provider = req.provider
            if req.model_name:
                config.model_name = req.model_name
            if req.api_key:
                config.api_key_masked = masked
            config.base_url = req.base_url
            config.connection_status = result.get("status", "Not Tested")
            config.latency_ms = result.get("latency_ms")
            config.error_message = result.get("error")
            config.last_tested_at = datetime.utcnow()
        db.commit()

    return {
        "status": result.get("status", "Connection Failed"),
        "latency_ms": result.get("latency_ms", 0.0),
        "masked_key": masked,
        "model_slot": req.model_slot,
        "model_name": req.model_name,
        "provider": req.provider,
        "message": result.get("message"),
        "error": result.get("error"),
    }


@router.get("/models/configs")
def list_model_configs(db: Session = Depends(get_db)):
    """Returns all stored model configurations with masked secrets."""
    configs = db.query(ModelConfiguration).all()
    # Default initial slots if empty
    if not configs:
        slots = [
            ("Model A", "Local Rule-Based", "rule-based-v1", "Connected"),
            ("Model B", "Google Gemini", "gemini-1.5-flash", "Not Tested"),
            ("Model C", "OpenAI-compatible", "gpt-4o-mini", "Not Tested"),
        ]
        created = []
        for slot, prov, name, status in slots:
            c = ModelConfiguration(
                model_slot=slot,
                provider=prov,
                model_name=name,
                api_key_masked="None",
                connection_status=status,
                last_tested_at=datetime.utcnow() if status == "Connected" else None,
            )
            db.add(c)
            created.append(c)
        db.commit()
        configs = created

    return [
        {
            "id": c.id,
            "model_slot": c.model_slot,
            "provider": c.provider,
            "model_name": c.model_name,
            "api_key_masked": c.api_key_masked,
            "base_url": c.base_url,
            "connection_status": c.connection_status,
            "latency_ms": c.latency_ms,
            "last_tested_at": c.last_tested_at.isoformat() if c.last_tested_at else None,
            "error_message": c.error_message,
        }
        for c in configs
    ]


@router.post("/models/configs")
def save_model_config(req: SaveModelConfigRequest, db: Session = Depends(get_db)):
    """Saves or updates a model slot configuration."""
    config = db.query(ModelConfiguration).filter(ModelConfiguration.model_slot == req.model_slot).first()
    masked = mask_api_key(req.api_key) if req.api_key else (config.api_key_masked if config else "None")

    if not config:
        config = ModelConfiguration(
            model_slot=req.model_slot,
            provider=req.provider,
            model_name=req.model_name,
            api_key_masked=masked,
            base_url=req.base_url,
            connection_status="Not Tested",
        )
        db.add(config)
    else:
        config.provider = req.provider
        config.model_name = req.model_name
        if req.api_key:
            config.api_key_masked = masked
        config.base_url = req.base_url
        config.connection_status = "Not Tested"

    db.commit()
    db.refresh(config)
    return {
        "id": config.id,
        "model_slot": config.model_slot,
        "provider": config.provider,
        "model_name": config.model_name,
        "api_key_masked": config.api_key_masked,
        "connection_status": config.connection_status,
    }


@router.get("/roles")
def get_primary_roles():
    """Lists the 5 primary roles and their condition metrics."""
    res = []
    for role in PRIMARY_ROLES:
        conditions = ConditionSelector.get_all_conditions_for_role(role)
        default_state = get_default_initial_state(role)
        res.append({
            "role": role,
            "total_conditions": len(conditions),
            "description": f"Autonomous {role.capitalize()} Agent System",
            "default_state": default_state,
        })
    return res


@router.get("/roles/{role}/conditions")
def get_role_conditions(role: str):
    """Returns the dedicated condition container for the specified role."""
    role_upper = role.upper()
    if role_upper not in PRIMARY_ROLES:
        raise HTTPException(status_code=404, detail=f"Role '{role}' not in primary roles {PRIMARY_ROLES}")

    conditions = ConditionSelector.get_all_conditions_for_role(role_upper)
    return {
        "role": role_upper,
        "total_conditions": len(conditions),
        "conditions": [c.model_dump() for c in conditions],
    }


@router.post("/simulations/run")
async def run_impact_simulation(req: RunSimulationRequest, db: Session = Depends(get_db)):
    """
    Executes the full AI Impact Simulator sequence for N loops.
    Strictly adheres to the 14-step cycle pipeline.
    """
    role_upper = req.role.upper()
    if role_upper not in PRIMARY_ROLES:
        raise HTTPException(status_code=400, detail=f"Invalid role '{req.role}'. Must be one of {PRIMARY_ROLES}")

    engine = AIImpactSimulatorEngine(
        db=db,
        role=role_upper,
        total_loops=req.total_loops,
        seed=req.seed,
        model_slot=req.model_slot,
        model_name=req.model_name or "rule-based-v1",
        provider_name=req.provider_name or "Local Rule-Based",
        api_key=req.api_key,
        base_url=req.base_url,
        custom_initial_state=req.custom_initial_state,
        simulation_name=req.simulation_name,
    )

    result = await engine.run_simulation()
    return result


@router.get("/simulations")
def list_simulations(limit: int = 20, db: Session = Depends(get_db)):
    """Lists completed and active impact simulations."""
    runs = db.query(ImpactSimulationRun).order_by(ImpactSimulationRun.created_at.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "role": r.role,
            "model_slot": r.model_slot,
            "model_name": r.model_name,
            "provider": r.provider,
            "seed": r.seed,
            "total_loops": r.total_loops,
            "completed_loops": r.completed_loops,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in runs
    ]


@router.get("/simulations/{simulation_id}")
def get_simulation_details(simulation_id: str, db: Session = Depends(get_db)):
    """Fetches details, initial state, final state, comparison, and impact analysis."""
    run = db.query(ImpactSimulationRun).filter(ImpactSimulationRun.id == simulation_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Simulation not found.")

    return {
        "id": run.id,
        "name": run.name,
        "role": run.role,
        "model_slot": run.model_slot,
        "model_name": run.model_name,
        "provider": run.provider,
        "seed": run.seed,
        "total_loops": run.total_loops,
        "completed_loops": run.completed_loops,
        "status": run.status,
        "initial_state": json.loads(run.initial_state_json) if run.initial_state_json else {},
        "final_state": json.loads(run.final_state_json) if run.final_state_json else {},
        "comparison": json.loads(run.comparison_json) if run.comparison_json else {},
        "impact_analysis": json.loads(run.impact_analysis_json) if run.impact_analysis_json else {},
        "created_at": run.created_at.isoformat() if run.created_at else None,
    }


@router.get("/simulations/{simulation_id}/cycles")
def get_simulation_cycles(simulation_id: str, db: Session = Depends(get_db)):
    """Returns the cycle-by-cycle live trace records for verification and UI display."""
    cycles = (
        db.query(SimulationCycleRecord)
        .filter(SimulationCycleRecord.simulation_id == simulation_id)
        .order_by(SimulationCycleRecord.cycle_number.asc())
        .all()
    )

    return [
        {
            "cycle_number": c.cycle_number,
            "timestamp": c.timestamp.isoformat() if c.timestamp else None,
            "role": c.role,
            "active_conditions": json.loads(c.active_conditions_json) if c.active_conditions_json else [],
            "decision": json.loads(c.ai_decision_json) if c.ai_decision_json else {},
            "validation": json.loads(c.validation_result_json) if c.validation_result_json else {},
            "resources_before": json.loads(c.resources_before_json) if c.resources_before_json else {},
            "resources_used": json.loads(c.resources_used_json) if c.resources_used_json else {},
            "resources_after": json.loads(c.resources_after_json) if c.resources_after_json else {},
            "state_changes": json.loads(c.state_changes_json) if c.state_changes_json else {},
            "outcomes": json.loads(c.outcomes_json) if c.outcomes_json else {},
        }
        for c in cycles
    ]
