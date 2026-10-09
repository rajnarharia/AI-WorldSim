from sqlalchemy.orm import Session
from app.database.models import Agent, EventLog
import json

class EducationSystem:
    def __init__(self, db: Session, run_id: int, tick: int, day: int):
        self.db = db
        self.run_id = run_id
        self.tick = tick
        self.day = day

    def study(self, agent: Agent, subject: str = "programming") -> bool:
        agent.energy = max(0.0, agent.energy - 15.0)
        agent.education_progress += 10.0
        
        # Skill increase
        skills = json.loads(agent.skills) if agent.skills else {}
        skills[subject] = skills.get(subject, 0) + 5
        agent.skills = json.dumps(skills)
        
        outcome_msg = f"Studied {subject}. Skill is now {skills[subject]}."
        
        # Education level up
        if agent.education_progress >= 100.0:
            agent.education_level += 1
            agent.education_progress = 0.0
            outcome_msg += f" Reached education level {agent.education_level}."
            
            log_edu = EventLog(
                run_id=self.run_id, tick=self.tick, simulation_day=self.day,
                agent_id=agent.id, event_type="STUDY_COMPLETED", action="LEVEL_UP",
                outcome=f"Education level increased to {agent.education_level}"
            )
            self.db.add(log_edu)
            
        log = EventLog(
            run_id=self.run_id, tick=self.tick, simulation_day=self.day,
            agent_id=agent.id, event_type="SKILL_INCREASED", action="STUDY",
            outcome=outcome_msg
        )
        self.db.add(log)
        return True
