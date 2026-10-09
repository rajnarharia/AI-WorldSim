import pytest
from app.database import models
from app.database.database import SessionLocal, Base, engine as db_engine
from app.simulation.economy_system import EconomySystem
from app.simulation.education_system import EducationSystem
from app.simulation.healthcare_system import HealthcareSystem
from app.simulation.social_system import SocialSystem

Base.metadata.create_all(bind=db_engine)

@pytest.fixture
def db():
    db = SessionLocal()
    # Ensure fresh data for tests
    db.query(models.Transaction).delete()
    db.query(models.EventLog).delete()
    db.query(models.Relationship).delete()
    db.query(models.Agent).delete()
    db.query(models.Job).delete()
    db.query(models.Product).delete()
    db.query(models.Business).delete()
    
    b1 = models.Business(name="Test Biz", balance=1000)
    db.add(b1)
    db.commit()
    
    j1 = models.Job(title="Dev", business_id=b1.id, salary=100, required_education=1)
    p1 = models.Product(name="Item", price=50, stock=10, business_id=b1.id)
    a1 = models.Agent(name="A1", money=100, health=50, energy=100)
    a2 = models.Agent(name="A2", money=100, health=100, energy=100)
    
    db.add_all([j1, p1, a1, a2])
    db.commit()
    
    try:
        yield db
    finally:
        db.close()

def test_economy_job_and_salary(db):
    agent = db.query(models.Agent).filter_by(name="A1").first()
    job = db.query(models.Job).first()
    
    econ = EconomySystem(db, run_id=1, tick=1, day=1)
    
    # Hire
    assert econ.assign_job(agent, job.id) == True
    db.commit()
    assert job.employee_id == agent.id
    
    # Salary
    old_money = agent.money
    econ.process_salaries()
    db.commit()
    db.refresh(agent)
    
    assert agent.money == old_money + job.salary

def test_economy_shopping(db):
    agent = db.query(models.Agent).filter_by(name="A1").first()
    product = db.query(models.Product).first()
    
    econ = EconomySystem(db, run_id=1, tick=1, day=1)
    
    success = econ.buy_product(agent, product.id)
    assert success == True
    db.commit()
    db.refresh(agent)
    assert agent.money == 50 # 100 - 50

def test_education_study(db):
    agent = db.query(models.Agent).filter_by(name="A1").first()
    edu = EducationSystem(db, run_id=1, tick=1, day=1)
    
    edu.study(agent, "programming")
    db.commit()
    db.refresh(agent)
    
    assert agent.education_progress == 10.0
    assert "programming" in agent.skills

def test_healthcare_treatment(db):
    agent = db.query(models.Agent).filter_by(name="A1").first()
    health = HealthcareSystem(db, run_id=1, tick=1, day=1)
    
    # Money = 100, Cost = 50, Health = 50
    success = health.treat_agent(agent, 1)
    
    assert success == True
    db.commit()
    db.refresh(agent)
    assert agent.health == 100.0
    assert agent.money == 50.0

def test_social_interaction(db):
    a1 = db.query(models.Agent).filter_by(name="A1").first()
    a2 = db.query(models.Agent).filter_by(name="A2").first()
    
    social = SocialSystem(db, run_id=1, tick=1, day=1)
    
    social.talk(a1, a2)
    db.commit()
    
    rel = db.query(models.Relationship).first()
    # default trust 0.5 + 0.05
    assert rel.trust > 0.5
    assert rel.interaction_count == 1
    
    # test cooperation
    success = social.cooperate(a1, a2)
    db.commit()
    assert success == True # Trust is now 0.55 > 0.4
    
    db.refresh(rel)
    assert rel.cooperation_score > 0.5
