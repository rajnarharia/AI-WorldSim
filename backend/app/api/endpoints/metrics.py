from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models, database
from app.simulation.metrics_engine import METRIC_REGISTRY

router = APIRouter()

@router.get("/definitions")
def get_metric_definitions():
    return METRIC_REGISTRY

@router.get("/snapshots")
def get_metric_snapshots(db: Session = Depends(database.get_db), limit: int = 100):
    snapshots = db.query(models.MetricSnapshot).order_by(models.MetricSnapshot.tick.desc()).limit(limit).all()
    return [
        {
            "tick": s.tick,
            "safety_score": s.safety_score,
            "economy_score": s.economy_score,
            "stability_score": s.stability_score,
            "cooperation_score": s.cooperation_score,
            "employment_rate": s.employment_rate,
            "average_income": s.average_income,
        }
        for s in snapshots
    ]

@router.get("/results")
def get_metric_results(db: Session = Depends(database.get_db), run_id: int = None, limit: int = 200):
    q = db.query(models.MetricResult)
    if run_id:
        q = q.filter(models.MetricResult.run_id == run_id)
    results = q.order_by(models.MetricResult.tick.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "run_id": r.run_id,
            "tick": r.tick,
            "simulation_day": r.simulation_day,
            "category": r.category,
            "metric_name": r.metric_name,
            "metric_value": r.metric_value,
            "model_type": r.model_type,
        }
        for r in results
    ]

@router.get("/by-model")
def get_metrics_by_model(db: Session = Depends(database.get_db)):
    """Aggregate metrics grouped by model type — used by the Analytics dashboard."""
    results = db.query(
        models.MetricResult.metric_name,
        models.MetricResult.model_type,
        func.avg(models.MetricResult.metric_value).label("mean"),
        func.max(models.MetricResult.metric_value).label("max"),
        func.min(models.MetricResult.metric_value).label("min"),
    ).filter(
        models.MetricResult.model_type != None
    ).group_by(models.MetricResult.metric_name, models.MetricResult.model_type).all()

    out = {}
    for r in results:
        if r.metric_name not in out:
            out[r.metric_name] = {}
        out[r.metric_name][r.model_type] = {
            "mean": round(r.mean, 4),
            "max": round(r.max, 4),
            "min": round(r.min, 4),
        }
    return out
