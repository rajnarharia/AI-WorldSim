from pydantic import BaseModel
from typing import Dict, List, Any

class WorldState(BaseModel):
    simulation_run_id: int = 0
    simulation_day: int = 1
    simulation_time_str: str = "00:00"
    current_tick: int = 0
    
    # State snapshots (can be maintained in-memory for fast access during ticks)
    agents: Dict[int, Any] = {}
    locations: Dict[int, Any] = {}
    jobs: Dict[int, Any] = {}
    businesses: Dict[int, Any] = {}
    
    # Metrics
    metrics: Dict[str, float] = {
        "safety": 100.0,
        "economy": 100.0,
        "stability": 100.0
    }

    def update_time(self, tick: int):
        self.current_tick = tick
        self.simulation_day = (tick // 24) + 1
        hour = tick % 24
        self.simulation_time_str = f"{hour:02d}:00"
