import json
import logging
from typing import Dict, Any, List
from app.database.models import Agent, Location, EventLog, DecisionHistory, AgentMemory
from sqlalchemy.orm import Session
from app.ai.agent_architecture import ObservationContext, RuleBasedAgent, LLMAgent, AgentAction
from app.simulation.world_state import WorldState

logger = logging.getLogger("decision_engine")

class AgentDecisionEngine:
    def __init__(self, db: Session, world_state: WorldState):
        self.db = db
        self.world_state = world_state
        self.providers = {
            "Model A": RuleBasedAgent(),
            "Model B": LLMAgent(),
            "Model C": RuleBasedAgent() # Fallback for now
        }

    def generate_observation(self, agent: Agent) -> ObservationContext:
        loc = self.world_state.locations.get(agent.current_location_id)
        location_name = loc["name"] if loc else "Unknown"
        
        # Calculate derived needs
        needs = {
            "Financial": "High" if agent.money < 500 else "Low",
            "Social": "High" if getattr(agent, 'need_social', 50) > 80 else "Low"
        }
        
        # Get memories
        recent_memories = [m.memory_text for m in agent.memories[-3:]]
        goals = []
        if agent.short_term_goals:
            try:
                goals.extend(json.loads(agent.short_term_goals))
            except:
                goals.append(agent.short_term_goals)
                
        # nearby locations
        nearby = [l["name"] for l in self.world_state.locations.values()]
        
        return ObservationContext(
            agent_name=agent.name,
            location=location_name,
            money=agent.money,
            health=agent.health,
            energy=getattr(agent, 'energy', 100.0),
            job_title="Employee" if agent.job_id else None,
            current_time=self.world_state.simulation_time_str,
            nearby_locations=nearby,
            needs=needs,
            goals=goals,
            recent_memories=recent_memories
        )

    def evaluate_action(self, agent: Agent, run_id: int) -> AgentAction:
        context = self.generate_observation(agent)
        provider = self.providers.get(agent.model_type, self.providers["Model A"])
        
        try:
            action = provider.decide(context)
            
            # Record decision history
            history = DecisionHistory(
                agent_id=agent.id,
                tick=self.world_state.current_tick,
                simulation_time_str=self.world_state.simulation_time_str,
                observation_summary=f"Needs: {context.needs}, Energy: {context.energy}",
                selected_action=action.action,
                target=action.target,
                reason=action.reason,
                model_type=agent.model_type,
                result="PENDING"
            )
            self.db.add(history)
            self.db.commit()
            
            # attach history ID so validator/executor can update it
            action.priority = history.id 
            return action
        except Exception as e:
            logger.error(f"Error evaluating action for {agent.name}: {e}")
            return AgentAction(action="REST", reason="Error fallback")
