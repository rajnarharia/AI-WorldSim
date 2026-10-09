import pytest
from app.database import models
from app.database.database import SessionLocal, Base, engine as db_engine
from app.simulation.safety_system import SafetySystem
from app.simulation.engine import SimulationEngine
import json

Base.metadata.create_all(bind=db_engine)

@pytest.fixture
def db():
    db = SessionLocal()
    db.query(models.CourtCase).delete()
    db.query(models.Investigation).delete()
    db.query(models.PoliceResponse).delete()
    db.query(models.Incident).delete()
    db.query(models.EventLog).delete()
    db.query(models.GovernmentPolicy).delete()
    db.query(models.Transaction).delete()
    db.query(models.Agent).delete()
    
    a1 = models.Agent(name="Suspect", money=100)
    a2 = models.Agent(name="Victim", money=100)
    gov = models.GovernmentPolicy(police_effectiveness=1.0)
    
    db.add_all([a1, a2, gov])
    db.commit()
    
    try:
        yield db
    finally:
        db.close()

def test_incident_lifecycle(db):
    suspect = db.query(models.Agent).filter_by(name="Suspect").first()
    victim = db.query(models.Agent).filter_by(name="Victim").first()
    
    sys = SafetySystem(db, run_id=1, tick=1, day=1)
    
    # 1. Report
    inc = sys.report_incident(suspect, "CONFLICT", "HIGH", "Simulated fight", [suspect.id, victim.id])
    assert inc.status == "REPORTED"
    
    # Tick to RESPONDING
    sys.process_lifecycle()
    db.refresh(inc)
    assert inc.status == "RESPONDING"
    
    # Tick forward +2 (police response time)
    sys.tick = 3
    sys.process_lifecycle()
    db.refresh(inc)
    assert inc.status == "INVESTIGATING"
    
    # Tick forward +6 (investigation time)
    sys.tick = 9
    sys.process_lifecycle()
    db.refresh(inc)
    assert inc.status == "IN_COURT"
    
    # Tick forward +8 (court decision time)
    sys.tick = 17
    sys.process_lifecycle()
    db.refresh(inc)
    assert inc.status == "RESOLVED"
    
    # Check consequences
    court = db.query(models.CourtCase).filter_by(incident_id=inc.id).first()
    assert court.status == "RESOLVED"
    
    # If the decision was a FINE, check if money was deducted.
    db.refresh(suspect)
    db.refresh(victim)
    if court.decision == "FINE":
        # A fine docks money from BOTH involved currently (as per simple implementation)
        assert suspect.money == 0.0
        assert victim.money == 0.0
