from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models, database
from app.simulation.metrics_engine import METRIC_REGISTRY
from app.simulation.experiment_runner import ExperimentRunner

router = APIRouter()

@router.get("/definitions")
def get_metric_definitions():
    return METRIC_REGISTRY
