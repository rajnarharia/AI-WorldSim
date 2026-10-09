from sqlalchemy.orm import Session
from app.database.models import Agent, EventLog, Relationship

class SocialSystem:
    def __init__(self, db: Session, run_id: int, tick: int, day: int):
        self.db = db
        self.run_id = run_id
        self.tick = tick
        self.day = day

    def get_or_create_relationship(self, agent_id_1: int, agent_id_2: int) -> Relationship:
        a1, a2 = min(agent_id_1, agent_id_2), max(agent_id_1, agent_id_2)
        rel = self.db.query(Relationship).filter(Relationship.agent_id_1 == a1, Relationship.agent_id_2 == a2).first()
        if not rel:
            rel = Relationship(agent_id_1=a1, agent_id_2=a2)
            self.db.add(rel)
        return rel

    def talk(self, agent: Agent, target: Agent) -> bool:
        agent.need_social = max(0.0, (agent.need_social or 0) - 30.0)
        target.need_social = max(0.0, (target.need_social or 0) - 30.0)
        
        rel = self.get_or_create_relationship(agent.id, target.id)
        rel.interaction_count = (rel.interaction_count or 0) + 1
        rel.trust = min(1.0, (rel.trust or 0.5) + 0.05)
        
        log = EventLog(
            run_id=self.run_id, tick=self.tick, simulation_day=self.day,
            agent_id=agent.id, agent_model=agent.model_type, event_type="SOCIAL_INTERACTION", action="TALK_TO_AGENT",
            outcome=f"Talked to {target.name}. Trust increased to {rel.trust:.2f}"
        )
        self.db.add(log)
        
        # Phase 8: Cross Model Interaction Logging
        from app.database.models import CrossModelInteraction, ExperimentRun
        # run_id is ExperimentRun.id
        exp_run = self.db.query(ExperimentRun).filter(ExperimentRun.id == self.run_id).first()
        if exp_run:
            cmi = CrossModelInteraction(
                experiment_id=exp_run.experiment_id,
                source_agent_id=agent.id, source_model_id=agent.model_type,
                target_agent_id=target.id, target_model_id=target.model_type,
                interaction_type="TALK", success=True
            )
            self.db.add(cmi)
            
        return True

    def cooperate(self, agent: Agent, target: Agent) -> bool:
        rel = self.get_or_create_relationship(agent.id, target.id)
        
        # Phase 8 Helpers
        from app.database.models import CrossModelInteraction, ExperimentRun
        exp_run = self.db.query(ExperimentRun).filter(ExperimentRun.id == self.run_id).first()
        exp_id = exp_run.experiment_id if exp_run else None
        
        # High trust = success
        if (rel.trust or 0.5) > 0.4:
            rel.cooperation_score = min(1.0, (rel.cooperation_score or 0.5) + 0.1)
            rel.trust = min(1.0, (rel.trust or 0.5) + 0.1)
            
            # small financial benefit for both
            agent.money += 10.0
            target.money += 10.0
            
            log = EventLog(
                run_id=self.run_id, tick=self.tick, simulation_day=self.day,
                agent_id=agent.id, agent_model=agent.model_type, event_type="COOPERATION_COMPLETED", action="COOPERATE",
                outcome=f"Cooperated successfully with {target.name}."
            )
            self.db.add(log)
            if exp_id:
                self.db.add(CrossModelInteraction(experiment_id=exp_id, source_agent_id=agent.id, source_model_id=agent.model_type, target_agent_id=target.id, target_model_id=target.model_type, interaction_type="COOPERATE", success=True))
            return True
        else:
            rel.trust = max(0.0, (rel.trust or 0.5) - 0.1)
            log = EventLog(
                run_id=self.run_id, tick=self.tick, simulation_day=self.day,
                agent_id=agent.id, agent_model=agent.model_type, event_type="COOPERATION_FAILED", action="COOPERATE",
                outcome=f"Failed to cooperate with {target.name}. Trust dropped."
            )
            self.db.add(log)
            if exp_id:
                self.db.add(CrossModelInteraction(experiment_id=exp_id, source_agent_id=agent.id, source_model_id=agent.model_type, target_agent_id=target.id, target_model_id=target.model_type, interaction_type="COOPERATE", success=False))
            return False
