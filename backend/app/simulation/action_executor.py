from sqlalchemy.orm import Session
from app.database.models import Agent, EventLog, Location, DecisionHistory, AgentMemory
from app.simulation.world_state import WorldState
from app.ai.agent_architecture import AgentAction

class ActionExecutor:
    def __init__(self, db: Session):
        self.db = db

    def execute_action(self, agent: Agent, action: AgentAction, resolved_target: any, world_state: WorldState, run_id: int) -> bool:
        act = action.action
        outcome_msg = f"Executed {act}"
        
        # Default energy drain
        agent.energy = max(0.0, agent.energy - 5.0)
        
        if act == "REST":
            agent.energy = min(100.0, agent.energy + 30.0)
            outcome_msg = "Rested and recovered energy."
            
        elif act in ["GO_TO_WORK", "VISIT_SHOP", "VISIT_PARK"]:
            if resolved_target:
                agent.current_location_id = resolved_target
                loc_name = self.db.query(Location).filter(Location.id == resolved_target).first().name
                outcome_msg = f"Moved to {loc_name}"
                if act == "GO_TO_WORK":
                    # Salary is handled periodically by economy system now, but we can drain energy here
                    agent.energy = max(0.0, agent.energy - 10.0)
                    outcome_msg += " and worked."
                    
        elif act == "TALK_TO_AGENT" or act == "COOPERATE":
            from app.simulation.social_system import SocialSystem
            social = SocialSystem(self.db, run_id, world_state.current_tick, world_state.simulation_day)
            target_agent = self.db.query(Agent).filter(Agent.id == resolved_target).first()
            if target_agent:
                if act == "TALK_TO_AGENT":
                    social.talk(agent, target_agent)
                    outcome_msg = f"Talked to {target_agent.name}"
                else:
                    social.cooperate(agent, target_agent)
                    outcome_msg = f"Cooperated with {target_agent.name}"
            
        elif act == "SEARCH_JOB":
            from app.simulation.economy_system import EconomySystem
            from app.database.models import Job
            econ = EconomySystem(self.db, run_id, world_state.current_tick, world_state.simulation_day)
            avail_job = self.db.query(Job).filter(Job.employee_id == None).first()
            if avail_job:
                success = econ.assign_job(agent, avail_job.id)
                if success:
                    outcome_msg = f"Searched and got hired for {avail_job.title}"
                else:
                    outcome_msg = "Searched but didn't meet requirements."
            else:
                outcome_msg = "Searched but no jobs available."
                
        elif act == "BUY_PRODUCT":
            from app.simulation.economy_system import EconomySystem
            econ = EconomySystem(self.db, run_id, world_state.current_tick, world_state.simulation_day)
            success = econ.buy_product(agent, resolved_target)
            if success:
                outcome_msg = "Bought a product successfully."
            else:
                outcome_msg = "Failed to buy product."
                
        elif act == "STUDY":
            from app.simulation.education_system import EducationSystem
            edu = EducationSystem(self.db, run_id, world_state.current_tick, world_state.simulation_day)
            edu.study(agent, resolved_target)
            outcome_msg = "Studied and improved skills."
            
        elif act == "VISIT_HOSPITAL":
            from app.simulation.healthcare_system import HealthcareSystem
            health = HealthcareSystem(self.db, run_id, world_state.current_tick, world_state.simulation_day)
            success = health.treat_agent(agent, resolved_target)
            if success:
                outcome_msg = "Received hospital treatment."
            else:
                outcome_msg = "Visited hospital but couldn't afford treatment."
                
        elif act == "REPORT_INCIDENT":
            from app.simulation.safety_system import SafetySystem
            safety = SafetySystem(self.db, run_id, world_state.current_tick, world_state.simulation_day)
            # Find a random other agent to blame for a simulated conflict
            other = self.db.query(Agent).filter(Agent.id != agent.id).first()
            inv = [agent.id, other.id] if other else [agent.id]
            safety.report_incident(agent, "CONFLICT", "MEDIUM", "A simulated disagreement occurred.", inv, agent.current_location_id)
            outcome_msg = "Reported an incident to the authorities."
            
        # Log event
        log = EventLog(
            run_id=run_id,
            tick=world_state.current_tick,
            simulation_day=world_state.simulation_day,
            agent_id=agent.id,
            agent_model=agent.model_type,
            event_type="AGENT_ACTION",
            action=act,
            location_id=agent.current_location_id,
            reason=action.reason,
            outcome=outcome_msg
        )
        self.db.add(log)
        
        # Add Memory
        mem = AgentMemory(
            agent_id=agent.id,
            tick=world_state.current_tick,
            memory_type="EVENT",
            memory_text=f"I performed {act}. {outcome_msg}"
        )
        self.db.add(mem)
        
        # Update DecisionHistory result
        if hasattr(action, 'priority'): # hacky way we passed the history id
            history = self.db.query(DecisionHistory).filter(DecisionHistory.id == int(action.priority)).first()
            if history:
                history.result = "SUCCESS"
        
        self.db.commit()
        return True
