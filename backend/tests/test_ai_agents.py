import pytest
from app.simulation.engine import SimulationEngine
from app.simulation.world_state import WorldState
from app.ai.decision_engine import AgentDecisionEngine
from app.database import models
from app.database.database import SessionLocal, Base, engine as db_engine

# Setup DB for tests
Base.metadata.create_all(bind=db_engine)

@pytest.fixture
def db():
    db = SessionLocal()
    # Ensure some data exists
    if db.query(models.Location).count() == 0:
        db.add(models.Location(name="Home", type="RESIDENTIAL"))
        db.add(models.Location(name="Hospital", type="HOSPITAL"))
        db.add(models.Location(name="Work", type="WORK"))
        db.commit()
        
    if db.query(models.Agent).count() == 0:
        db.add(models.Agent(name="TestAgent", model_type="Model A", current_location_id=1, money=100, health=20, energy=10))
        db.commit()
        
    try:
        yield db
    finally:
        db.close()

def test_observation_generation(db):
    agent = db.query(models.Agent).first()
    world = WorldState()
    # load dummy locations
    world.locations = {1: {"id":1, "name":"Home", "type":"RESIDENTIAL"}}
    
    de = AgentDecisionEngine(db, world)
    obs = de.generate_observation(agent)
    
    assert obs.agent_name == agent.name
    assert obs.health == agent.health
    assert obs.energy == agent.energy

def test_rule_based_decision_low_energy(db):
    agent = db.query(models.Agent).first()
    agent.energy = 10 # low energy
    db.commit()
    
    world = WorldState()
    de = AgentDecisionEngine(db, world)
    action = de.evaluate_action(agent, run_id=1)
    
    assert action.action == "REST"
    assert "Energy is critically low" in action.reason

def test_rule_based_decision_low_health(db):
    agent = db.query(models.Agent).first()
    agent.energy = 100
    agent.health = 20 # low health
    db.commit()
    
    world = WorldState()
    de = AgentDecisionEngine(db, world)
    action = de.evaluate_action(agent, run_id=1)
    
    assert action.action == "VISIT_HOSPITAL"

@pytest.mark.asyncio
async def test_full_simulation_tick(db):
    # This tests the entire loop: observe -> reason -> validate -> execute -> memory
    sim = SimulationEngine()
    sim.run_id = 999
    
    # Pre-condition: low energy, should REST
    agent = db.query(models.Agent).first()
    agent.energy = 5
    db.commit()
    
    await sim.step()
    
    # Check if agent rested
    db.refresh(agent)
    assert agent.energy > 5
    
    # Check if event was created
    event = db.query(models.EventLog).filter(models.EventLog.run_id == 999).first()
    assert event is not None
    assert event.event_type == "AGENT_ACTION" or event.event_type == "SYSTEM"
    
    # Check if decision history recorded
    decision = db.query(models.DecisionHistory).filter(models.DecisionHistory.agent_id == agent.id).order_by(models.DecisionHistory.id.desc()).first()
    assert decision is not None
    assert decision.selected_action == "REST"
    assert decision.result == "SUCCESS"
