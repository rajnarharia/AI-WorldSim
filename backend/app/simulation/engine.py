import asyncio
import random
import logging
from datetime import datetime
from app.database.database import SessionLocal
from app.database.models import EventLog, MetricSnapshot, Agent, Location, SimulationRun
from app.simulation.world_state import WorldState
from app.simulation.action_executor import ActionExecutor

logger = logging.getLogger("simulation")
logging.basicConfig(level=logging.INFO)

class SimulationEngine:
    def __init__(self):
        self.is_running = False
        self.speed = 1.0
        self.day_length = 24 # 24 ticks = 1 day
        self._task = None
        self.world_state = WorldState()
        self.run_id = None
        
        # Load initial state from db
        db = SessionLocal()
        try:
            self._load_world_state(db)
        except Exception:
            pass
        finally:
            db.close()

    def start(self):
        if not self.is_running:
            db = SessionLocal()
            try:
                if not self.run_id:
                    # Create a new run
                    new_run = SimulationRun(
                        status="RUNNING",
                        number_of_agents=db.query(Agent).count(),
                        random_seed=42 # default for now
                    )
                    db.add(new_run)
                    db.commit()
                    db.refresh(new_run)
                    self.run_id = new_run.id
                    self.world_state.simulation_run_id = self.run_id
                else:
                    run = db.query(SimulationRun).filter(SimulationRun.id == self.run_id).first()
                    if run:
                        run.status = "RUNNING"
                        db.commit()

                # Load initial state
                self._load_world_state(db)
                
            except Exception as e:
                logger.error(f"Failed to start simulation: {e}")
            finally:
                db.close()
                
            self.is_running = True
            logger.info("Simulation started.")
            self._task = asyncio.create_task(self._run_loop())

    def pause(self):
        if self.is_running:
            self.is_running = False
            if self._task:
                self._task.cancel()
            db = SessionLocal()
            try:
                run = db.query(SimulationRun).filter(SimulationRun.id == self.run_id).first()
                if run:
                    run.status = "PAUSED"
                    db.commit()
            except Exception as e:
                logger.error(f"Failed to pause simulation: {e}")
            finally:
                db.close()
            logger.info("Simulation paused.")

    def stop(self):
        self.pause()
        db = SessionLocal()
        try:
            if self.run_id:
                run = db.query(SimulationRun).filter(SimulationRun.id == self.run_id).first()
                if run:
                    run.status = "STOPPED"
                    run.end_time = datetime.utcnow()
                    run.simulation_duration_ticks = self.world_state.current_tick
                    db.commit()
        finally:
            db.close()
        self.run_id = None
        logger.info("Simulation stopped.")

    def reset(self):
        self.stop()
        self.world_state = WorldState()
        logger.info("Simulation reset.")

    def _load_world_state(self, db):
        agents = db.query(Agent).all()
        locations = db.query(Location).all()
        
        self.world_state.agents = {
            a.id: {
                "id": a.id,
                "name": a.name,
                "model_type": a.model_type or "Model A",
                "personality": a.personality or "Balanced",
                "location_id": a.current_location_id,
                "current_location_id": a.current_location_id,
                "money": round(float(a.money or 0.0), 2),
                "health": round(float(a.health or 100.0), 1),
                "energy": round(float(a.energy or 100.0), 1),
                "age": int(a.age or 25),
                "job_id": a.job_id,
                "education_level": int(a.education_level or 1),
                "need_rest": max(0.0, 100.0 - float(a.energy or 100.0)),
                "need_money": float(getattr(a, 'need_financial', 50.0) or 50.0),
                "need_health": max(0.0, 100.0 - float(a.health or 100.0)),
                "need_social": float(getattr(a, 'need_social', 50.0) or 50.0),
            }
            for a in agents
        }
        self.world_state.locations = {
            l.id: {
                "id": l.id,
                "name": l.name,
                "type": l.type,
                "capacity": l.capacity,
                "x": l.x,
                "y": l.y,
                "pos_x": l.x if l.x > 50 else (l.x * 9 + 40),
                "pos_y": l.y if l.y > 50 else (l.y * 7 + 40),
            }
            for l in locations
        }

    def _get_time_components(self):
        return self.world_state.simulation_day, self.world_state.simulation_time_str

    async def step(self):
        self.world_state.update_time(self.world_state.current_tick + 1)
        day, time_str = self._get_time_components()
        
        random.seed(42 + self.world_state.current_tick) 
        
        db = SessionLocal()
        try:
            agents = db.query(Agent).all()
            from app.ai.decision_engine import AgentDecisionEngine
            from app.simulation.action_validator import ActionValidator
            from app.simulation.action_executor import ActionExecutor
            from app.ai.agent_architecture import AgentAction
            
            decision_engine = AgentDecisionEngine(db, self.world_state)
            validator = ActionValidator(db)
            executor = ActionExecutor(db)
            
            # Domain Systems
            from app.simulation.healthcare_system import HealthcareSystem
            from app.simulation.economy_system import EconomySystem
            from app.simulation.safety_system import SafetySystem
            from app.database.models import GovernmentPolicy
            
            # Ensure policy exists
            if not db.query(GovernmentPolicy).first():
                db.add(GovernmentPolicy())
                db.commit()
            
            health_sys = HealthcareSystem(db, self.run_id, self.world_state.current_tick, day)
            econ_sys = EconomySystem(db, self.run_id, self.world_state.current_tick, day)
            safety_sys = SafetySystem(db, self.run_id, self.world_state.current_tick, day)
            
            # 1. Background domain logic
            health_sys.process_health_degradation()
            safety_sys.process_lifecycle()
            
            if self.world_state.current_tick > 0 and self.world_state.current_tick % 24 == 0:
                econ_sys.process_salaries()
                
            # Time-series metrics recording (every 12 ticks)
            if self.world_state.current_tick > 0 and self.world_state.current_tick % 12 == 0:
                from app.simulation.metrics_engine import MetricsEngine
                metrics_engine = MetricsEngine(db, self.run_id)
                metrics_engine.calculate_and_store_metrics(self.world_state.current_tick, day)
            
            for agent in agents:
                # 2. & 3. & 4. OBSERVE, REASON, CHOOSE ACTION
                action = decision_engine.evaluate_action(agent, self.run_id)
                
                # 4. VALIDATE
                is_valid, reason, resolved_target = validator.validate(agent, action, self.world_state)
                
                if not is_valid:
                    # Fallback action if invalid
                    action = AgentAction(action="REST", reason=f"Fallback due to invalid action: {reason}", priority=action.priority)
                    resolved_target = None
                
                # 5. EXECUTE & RECORD
                executor.execute_action(agent, action, resolved_target, self.world_state, self.run_id)
            
            # Log tick
            log = EventLog(
                run_id=self.run_id,
                tick=self.world_state.current_tick,
                simulation_day=day,
                event_type="SYSTEM",
                action="TICK_PROCESSED",
                outcome=f"Advanced to {day} {time_str}"
            )
            db.add(log)
            db.commit()
            
            self._load_world_state(db) # Refresh state from DB
        except Exception as e:
            logger.error(f"Error during step: {e}")
            db.rollback()
        finally:
            db.close()

    async def _run_loop(self):
        while self.is_running:
            await self.step()
            delay = 1.0 / self.speed
            await asyncio.sleep(delay)

sim_engine = SimulationEngine()
