import pytest
from app.simulation.engine import SimulationEngine
from app.simulation.world_state import WorldState
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_simulation_clock_and_tick():
    engine = SimulationEngine()
    
    assert engine.world_state.current_tick == 0
    assert engine.world_state.simulation_day == 1
    assert engine.world_state.simulation_time_str == "00:00"
    
    engine.world_state.update_time(5)
    assert engine.world_state.current_tick == 5
    assert engine.world_state.simulation_day == 1
    assert engine.world_state.simulation_time_str == "05:00"
    
    engine.world_state.update_time(25)
    assert engine.world_state.current_tick == 25
    assert engine.world_state.simulation_day == 2
    assert engine.world_state.simulation_time_str == "01:00"

@pytest.mark.asyncio
async def test_start_pause_reset():
    engine = SimulationEngine()
    engine.start()
    assert engine.is_running == True
    
    engine.pause()
    assert engine.is_running == False
    
    engine.reset()
    assert engine.world_state.current_tick == 0
    assert engine.is_running == False

def test_api_status():
    response = client.get("/api/simulation/status")
    assert response.status_code == 200
    data = response.json()
    assert "is_running" in data
    assert "current_tick" in data

def test_api_start():
    # Use TestClient synchronously but it should work if endpoint is async
    response = client.post("/api/simulation/start")
    assert response.status_code == 200
    assert response.json()["status"] == "started"
    
    res2 = client.get("/api/simulation/status")
    assert res2.json()["is_running"] == True
    
    client.post("/api/simulation/stop")
