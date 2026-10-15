from fastapi import APIRouter
from app.api.endpoints import agents, simulation, metrics, locations, dashboards, experiments

router = APIRouter()

router.include_router(agents.router, prefix="/agents", tags=["agents"])
router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
router.include_router(locations.router, prefix="/locations", tags=["locations"])
router.include_router(dashboards.router, prefix="/dashboards", tags=["dashboards"])
router.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
router.include_router(experiments.router, prefix="/metrics/experiments", tags=["metrics-experiments"])
