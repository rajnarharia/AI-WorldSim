from sqlalchemy.orm import Session
from app.database.models import Agent, EventLog, Transaction

class HealthcareSystem:
    def __init__(self, db: Session, run_id: int, tick: int, day: int):
        self.db = db
        self.run_id = run_id
        self.tick = tick
        self.day = day

    def process_health_degradation(self):
        # Called every tick
        agents = self.db.query(Agent).all()
        for agent in agents:
            # 1% chance to lose health per tick if no random seed, or deterministic
            # Simplified deterministic degradation
            if self.tick % 48 == 0: # Every 2 days
                agent.health = max(10.0, agent.health - 15.0)
                if agent.health < 40:
                    agent.energy = max(0.0, agent.energy - 10.0) # Sickness drains energy
                    
    def treat_agent(self, agent: Agent, hospital_id: int) -> bool:
        cost = 50.0
        health_before = agent.health
        
        if agent.money >= cost:
            agent.money -= cost
            agent.health = 100.0
            agent.need_financial = min(100.0, agent.need_financial + 20.0) # Paying makes them need money
            
            t = Transaction(
                tick=self.tick, sender_id=agent.id, business_id=None,
                amount=cost, transaction_type="HEALTHCARE", description="Hospital Treatment"
            )
            self.db.add(t)
            
            log = EventLog(
                run_id=self.run_id, tick=self.tick, simulation_day=self.day,
                agent_id=agent.id, event_type="TREATMENT_COMPLETED", action="VISIT_HOSPITAL",
                outcome=f"Health restored from {health_before} to 100 for ${cost}",
                location_id=hospital_id
            )
            self.db.add(log)
            return True
        else:
            log = EventLog(
                run_id=self.run_id, tick=self.tick, simulation_day=self.day,
                agent_id=agent.id, event_type="TREATMENT_FAILED", action="VISIT_HOSPITAL",
                outcome=f"Cannot afford treatment.",
                location_id=hospital_id
            )
            self.db.add(log)
            return False
