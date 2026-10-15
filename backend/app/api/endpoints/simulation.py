from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.simulation.engine import sim_engine
from app.database import database, models
from sqlalchemy.orm import Session

router = APIRouter()

class SimulationStatus(BaseModel):
    is_running: bool
    state: str = "STOPPED"
    current_tick: int
    simulation_day: int
    simulation_time: str = "00:00"
    simulation_time_str: str = "00:00"
    speed: float
    run_id: Optional[int] = None

class SimulationControlRequest(BaseModel):
    action: str

@router.get("/status", response_model=SimulationStatus)
def get_status():
    state = "RUNNING" if sim_engine.is_running else ("PAUSED" if sim_engine.run_id else "STOPPED")
    time_str = sim_engine.world_state.simulation_time_str or "00:00"
    return {
        "is_running": sim_engine.is_running,
        "state": state,
        "current_tick": sim_engine.world_state.current_tick,
        "simulation_day": sim_engine.world_state.simulation_day,
        "simulation_time": time_str,
        "simulation_time_str": time_str,
        "speed": sim_engine.speed,
        "run_id": sim_engine.run_id
    }

@router.post("/control")
async def control_simulation(req: SimulationControlRequest, db: Session = Depends(database.get_db)):
    act = req.action.lower()
    if act in ("start", "resume"):
        sim_engine.start()
        return {"status": "started", "state": "RUNNING"}
    elif act == "pause":
        sim_engine.pause()
        return {"status": "paused", "state": "PAUSED"}
    elif act == "stop":
        sim_engine.stop()
        return {"status": "stopped", "state": "STOPPED"}
    elif act in ("next_tick", "step"):
        await sim_engine.step()
        state = "RUNNING" if sim_engine.is_running else ("PAUSED" if sim_engine.run_id else "STOPPED")
        return {"status": "stepped", "state": state}
    elif act == "reset":
        sim_engine.reset()
        sim_engine._load_world_state(db)
        return {"status": "reset", "state": "STOPPED"}
    return {"status": "unknown_action"}

@router.post("/start")
async def start_simulation():
    sim_engine.start()
    return {"status": "started"}

@router.post("/pause")
async def pause_simulation():
    sim_engine.pause()
    return {"status": "paused"}

@router.post("/resume")
async def resume_simulation():
    sim_engine.start() # Start acts as resume if paused
    return {"status": "resumed"}

@router.post("/stop")
async def stop_simulation():
    sim_engine.stop()
    return {"status": "stopped"}

@router.post("/step")
async def step_simulation():
    await sim_engine.step()
    return {"status": "stepped"}

@router.post("/reset")
def reset_simulation(db: Session = Depends(database.get_db)):
    sim_engine.reset()
    sim_engine._load_world_state(db)
    return {"status": "reset"}

@router.post("/speed")
def set_speed(speed: float):
    sim_engine.speed = speed
    return {"status": "speed_updated", "speed": speed}

@router.get("/world")
def get_world_state(db: Session = Depends(database.get_db)):
    if not sim_engine.world_state.agents:
        sim_engine._load_world_state(db)
    return sim_engine.world_state.model_dump()

@router.get("/agents")
def get_active_agents():
    return sim_engine.world_state.agents

@router.get("/locations")
def get_active_locations():
    return sim_engine.world_state.locations

@router.get("/events")
def get_events(db: Session = Depends(database.get_db), limit: int = 100):
    events = db.query(models.EventLog).order_by(models.EventLog.tick.desc()).limit(limit).all()
    return events

@router.get("/runs")
def get_runs(db: Session = Depends(database.get_db)):
    runs = db.query(models.SimulationRun).order_by(models.SimulationRun.id.desc()).all()
    return runs

@router.get("/decisions")
def get_decisions(db: Session = Depends(database.get_db), limit: int = 100):
    decisions = db.query(models.DecisionHistory).order_by(models.DecisionHistory.id.desc()).limit(limit).all()
    return decisions
