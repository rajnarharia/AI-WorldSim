import pytest
from app.database import models
from app.database.database import SessionLocal, Base, engine as db_engine
from app.simulation.metrics_engine import MetricsEngine
from app.simulation.experiment_runner import ExperimentRunner
import json

Base.metadata.create_all(bind=db_engine)

@pytest.fixture
def db():
    db = SessionLocal()
    runner = ExperimentRunner(db)
    runner._reset_simulation_data()
    db.query(models.ExperimentRun).delete()
    db.query(models.Experiment).delete()
    db.query(models.MetricResult).delete()
    db.commit()
    
    # Add dummy data
    a1 = models.Agent(name="A1", model_type="Model A", job_id=1)
    a2 = models.Agent(name="A2", model_type="Model B", job_id=None)
    inc = models.Incident(status="REPORTED", incident_type="RULE_VIOLATION", reporter_id=1)
    db.add_all([a1, a2, inc])
    db.commit()
    
    try:
        yield db
    finally:
        db.close()

def test_metrics_calculation(db):
    engine = MetricsEngine(db, run_id=1)
    engine.calculate_and_store_metrics(tick=12, day=1)
    
    results = db.query(models.MetricResult).all()
    assert len(results) >= 4
    
    # Verify specific metrics
    emp_rate = next(r.metric_value for r in results if r.metric_name == "employment_rate")
    assert emp_rate == 50.0  # 1 out of 2 employed
    
    inc_rate = next(r.metric_value for r in results if r.metric_name == "incident_rate")
    assert inc_rate == 1.0
    
    compliance = next(r.metric_value for r in results if r.metric_name == "law_compliance")
    assert compliance == 50.0  # 1 violator out of 2 agents

def test_experiment_runner(db):
    runner = ExperimentRunner(db)
    exp = runner.create_experiment("Test Exp", population=6, runs=2, duration=1)
    
    assert exp.population_size == 6
    assert exp.runs_count == 2
    
    # Run the experiment
    runner.run_experiment(exp.id)
    
    # Check that runs were created
    runs = db.query(models.ExperimentRun).filter_by(experiment_id=exp.id).all()
    assert len(runs) == 2
    for r in runs:
        assert r.status == "COMPLETED"
    
    # Check that metrics were generated for the runs
    metrics = db.query(models.MetricResult).filter(models.MetricResult.run_id.in_([r.id for r in runs])).all()
    assert len(metrics) > 0
