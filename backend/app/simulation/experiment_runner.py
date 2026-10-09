from sqlalchemy.orm import Session
from app.database import models
from app.database.seeder import seed_data
from app.simulation.engine import SimulationEngine
from app.simulation.metrics_engine import MetricsEngine
import random
import json

class ExperimentRunner:
    def __init__(self, db: Session):
        self.db = db
        
    def create_experiment(self, name: str, population: int, runs: int, duration: int, models_config: dict = None) -> models.Experiment:
        if not models_config:
            models_config = {"Model A": 34, "Model B": 33, "Model C": 33} # percentages basically
            
        exp = models.Experiment(name=name, population_size=population, runs_count=runs, duration_days=duration)
        self.db.add(exp)
        self.db.commit()
        self.db.refresh(exp)
        
        # Add model assignments
        for m_name, pct in models_config.items():
            cnt = int(population * (pct / 100.0))
            ema = models.ExperimentModelAssignment(
                experiment_id=exp.id, model_id=m_name, model_name=m_name,
                agent_count=cnt, percentage=pct
            )
            self.db.add(ema)
        self.db.commit()
        
        return exp
        
    def run_experiment(self, exp_id: int):
        exp = self.db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()
        if not exp: return
        
        assignments = self.db.query(models.ExperimentModelAssignment).filter(models.ExperimentModelAssignment.experiment_id == exp_id).all()
        model_distribution = {a.model_name: a.percentage for a in assignments}
        if not model_distribution:
            model_distribution = {"Model A": 34, "Model B": 33, "Model C": 33}
        
        base_seed = 42
        
        for r_idx in range(exp.runs_count):
            run_seed = base_seed + r_idx
            
            run = models.ExperimentRun(experiment_id=exp.id, run_index=r_idx, seed=run_seed)
            self.db.add(run)
            self.db.commit()
            self.db.refresh(run)
            
            self._execute_single_run(run.id, exp.duration_days, run_seed, exp.population_size, model_distribution)
            
            run.status = "COMPLETED"
            self.db.commit()
            
        exp.status = "COMPLETED"
        self.db.commit()
        
    def _execute_single_run(self, run_id: int, duration_days: int, seed: int, population: int, model_distribution: dict):
        self._reset_simulation_data()
        random.seed(seed)
        self._seed_deterministic_population(population, model_distribution)
        
        engine = SimulationEngine()
        engine.run_id = run_id
        
        ticks = duration_days * 24
        import asyncio
        for tick in range(1, ticks + 1):
            engine.world_state.current_tick = tick
            engine.world_state.simulation_day = (tick // 24) + 1
            asyncio.run(engine.step())
            
    def _reset_simulation_data(self):
        self.db.query(models.CrossModelInteraction).delete()
        self.db.query(models.CourtCase).delete()
        self.db.query(models.Investigation).delete()
        self.db.query(models.PoliceResponse).delete()
        self.db.query(models.Incident).delete()
        self.db.query(models.Transaction).delete()
        self.db.query(models.EventLog).delete()
        self.db.query(models.AgentMemory).delete()
        self.db.query(models.DecisionHistory).delete()
        self.db.query(models.Relationship).delete()
        self.db.query(models.Agent).delete()
        self.db.query(models.Job).delete()
        self.db.query(models.Product).delete()
        self.db.query(models.Business).delete()
        self.db.query(models.Location).delete()
        self.db.commit()
        
    def _seed_deterministic_population(self, population: int, model_distribution: dict):
        seed_data(self.db) 
        loc = self.db.query(models.Location).filter(models.Location.type == "RESIDENTIAL").first()
        
        # Build the exact counts
        counts = {}
        for m, pct in model_distribution.items():
            counts[m] = int(population * (pct / 100.0))
        
        # Fill remainder
        diff = population - sum(counts.values())
        if diff > 0 and counts:
            counts[list(counts.keys())[0]] += diff
            
        model_list = []
        for m, c in counts.items():
            model_list.extend([m]*c)
            
        # Shuffle for deterministic distribution across the population
        random.shuffle(model_list)
        
        agents = []
        for i in range(population):
            model_t = model_list[i] if i < len(model_list) else "Model A"
            agents.append(
                models.Agent(
                    name=f"Agent_{i}", model_type=model_t, personality="Neutral",
                    money=1000.0, health=100.0, energy=100.0, current_location_id=loc.id
                )
            )
        self.db.add_all(agents)
        self.db.commit()
