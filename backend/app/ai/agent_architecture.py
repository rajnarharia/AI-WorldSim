from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import random

class ObservationContext(BaseModel):
    agent_name: str
    location: str
    money: float
    health: float
    energy: float
    job_title: Optional[str] = None
    current_time: str
    nearby_locations: List[str]
    needs: Dict[str, str]
    goals: List[str]
    recent_memories: List[str]

class AgentAction(BaseModel):
    action: str
    target: Optional[str] = None
    reason: str
    priority: float = 0.5

class AIProvider:
    def decide(self, context: ObservationContext) -> AgentAction:
        raise NotImplementedError

class RuleBasedAgent(AIProvider):
    def decide(self, context: ObservationContext) -> AgentAction:
        if context.energy < 20:
            return AgentAction(action="REST", reason="Energy is critically low.")
        elif context.health < 40:
            return AgentAction(action="VISIT_HOSPITAL", reason="Health is critical.")
        elif context.needs.get("Financial") == "High" and context.job_title:
            return AgentAction(action="GO_TO_WORK", reason="I need money and I have a job.")
            
        hour = int(context.current_time.split(":")[0])
        if 8 <= hour < 17:
            if context.job_title:
                return AgentAction(action="GO_TO_WORK", reason="It's working hours.")
            else:
                return AgentAction(action="SEARCH_JOB", reason="I need a job during working hours.")
        elif hour >= 22 or hour < 6:
            return AgentAction(action="REST", reason="It's time to sleep.")
        else:
            # Free time: mix of activities to ensure cross-model interactions!
            r = random.random()
            if r < 0.3:
                return AgentAction(action="TALK_TO_AGENT", reason="I want to socialize.")
            elif r < 0.5:
                return AgentAction(action="COOPERATE", reason="Looking to build trust and cooperate.")
            elif r < 0.7:
                return AgentAction(action="BUY_PRODUCT", reason="Shopping for needs.")
            else:
                return AgentAction(action="VISIT_PARK", reason="Enjoying free time at the park.")

class LLMAgent(AIProvider):
    def decide(self, context: ObservationContext) -> AgentAction:
        return RuleBasedAgent().decide(context)
