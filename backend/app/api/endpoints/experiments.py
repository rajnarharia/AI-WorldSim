from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models, database
from app.simulation.experiment_runner import ExperimentRunner

router = APIRouter()

@router.post("")
def create_experiment(name: str, population: int = 30, runs: int = 3, duration_days: int = 2, db: Session = Depends(database.get_db)):
    runner = ExperimentRunner(db)
    models_config = {"Model A": 34, "Model B": 33, "Model C": 33}
    exp = runner.create_experiment(name, population, runs, duration_days, models_config)
    return {"id": exp.id, "name": exp.name, "population": exp.population_size}

@router.get("")
def get_experiments(db: Session = Depends(database.get_db)):
    return db.query(models.Experiment).order_by(models.Experiment.id.desc()).all()

@router.get("/{exp_id}")
def get_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()

@router.post("/{exp_id}/run")
def run_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    runner = ExperimentRunner(db)
    runner.run_experiment(exp_id)
    return {"status": "success"}

@router.post("/{exp_id}/start")
def start_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    runner = ExperimentRunner(db)
    runner.run_experiment(exp_id)
    return {"status": "success"}

@router.post("/{exp_id}/pause")
def pause_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    return {"status": "paused"}

@router.post("/{exp_id}/resume")
def resume_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    return {"status": "resumed"}

@router.post("/{exp_id}/stop")
def stop_experiment(exp_id: int, db: Session = Depends(database.get_db)):
    return {"status": "stopped"}

@router.get("/{exp_id}/models")
def get_experiment_models(exp_id: int, db: Session = Depends(database.get_db)):
    assignments = db.query(models.ExperimentModelAssignment).filter(models.ExperimentModelAssignment.experiment_id == exp_id).all()
    return assignments

@router.get("/{exp_id}/metrics")
def get_experiment_metrics(exp_id: int, db: Session = Depends(database.get_db)):
    runs = db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == exp_id).all()
    run_ids = [r.id for r in runs]
    metrics = db.query(models.MetricResult).filter(models.MetricResult.run_id.in_(run_ids)).all()
    return metrics

@router.get("/{exp_id}/events")
def get_experiment_events(exp_id: int, db: Session = Depends(database.get_db)):
    runs = db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == exp_id).all()
    run_ids = [r.id for r in runs]
    events = db.query(models.EventLog).filter(models.EventLog.run_id.in_(run_ids)).all()
    return events

@router.get("/{exp_id}/cross-model-interactions")
def get_cmi(exp_id: int, db: Session = Depends(database.get_db)):
    cmis = db.query(models.CrossModelInteraction).filter(models.CrossModelInteraction.experiment_id == exp_id).all()
    matrix = {}
    for c in cmis:
        src = c.source_model_id or "Unknown"
        tgt = c.target_model_id or "Unknown"
        if src not in matrix: matrix[src] = {}
        if tgt not in matrix[src]: matrix[src][tgt] = 0
        matrix[src][tgt] += 1
    return matrix

@router.get("/{exp_id}/comparison")
def get_model_comparison(exp_id: int, db: Session = Depends(database.get_db)):
    runs = db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == exp_id).all()
    run_ids = [r.id for r in runs]
    
    results = db.query(
        models.MetricResult.metric_name, 
        models.MetricResult.model_type,
        func.avg(models.MetricResult.metric_value).label('mean'),
        func.max(models.MetricResult.metric_value).label('max'),
        func.min(models.MetricResult.metric_value).label('min')
    ).filter(
        models.MetricResult.run_id.in_(run_ids),
        models.MetricResult.model_type != None
    ).group_by(models.MetricResult.metric_name, models.MetricResult.model_type).all()
    
    comparison = {}
    for r in results:
        if r.metric_name not in comparison:
            comparison[r.metric_name] = {}
        comparison[r.metric_name][r.model_type] = {
            "mean": round(r.mean, 2),
            "max": round(r.max, 2),
            "min": round(r.min, 2)
        }
    return comparison
