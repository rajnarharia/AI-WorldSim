from sqlalchemy.orm import Session
from app.database import models
import math

METRIC_REGISTRY = {
    "employment_rate": {"category": "ECONOMY", "unit": "%", "description": "Employed / Total Agents", "formula": "employed/total*100"},
    "average_income": {"category": "ECONOMY", "unit": "$", "description": "Average agent funds", "formula": "avg(money)"},
    "incident_rate": {"category": "SAFETY", "unit": "incidents", "description": "Total active incidents", "formula": "count(incidents where status != RESOLVED)"},
    "average_trust": {"category": "SOCIETY", "unit": "index", "description": "Average trust across relationships", "formula": "avg(trust)"},
    "cooperation_rate": {"category": "SOCIETY", "unit": "%", "description": "Average cooperation score", "formula": "avg(coop_score) * 100"},
    "law_compliance": {"category": "GOVERNANCE", "unit": "%", "description": "Agents without incidents / Total", "formula": "(total - violators) / total * 100"},
    "decision_success_rate": {"category": "AI", "unit": "%", "description": "Goals completed successfully", "formula": "success / total_decisions * 100"}
}

class MetricsEngine:
    def __init__(self, db: Session, run_id: int):
        self.db = db
        self.run_id = run_id

    def calculate_and_store_metrics(self, tick: int, day: int):
        agents = self.db.query(models.Agent).all()
        if not agents: return
        total_agents = len(agents)
        
        # Helper to calculate for a specific model group (or all if model_type is None)
        def calc_for_group(group_agents, m_type):
            if not group_agents: return
            n = len(group_agents)
            
            # ECONOMY
            employed = sum(1 for a in group_agents if a.job_id is not None)
            self._store(tick, day, "ECONOMY", "employment_rate", (employed / n) * 100, m_type)
            
            avg_inc = sum(a.money for a in group_agents) / n
            self._store(tick, day, "ECONOMY", "average_income", avg_inc, m_type)
            
            # SAFETY
            agent_ids = {a.id for a in group_agents}
            incidents = self.db.query(models.Incident).all()
            # Incident is attributed if reporter or involved is in group
            group_inc = 0
            for i in incidents:
                if i.status != "RESOLVED":
                    inv = []
                    if i.involved_agent_ids:
                        try:
                            import json
                            inv = json.loads(i.involved_agent_ids)
                        except: pass
                    if i.reporter_id in agent_ids or any(int(x) in agent_ids for x in inv if str(x).isdigit()):
                        group_inc += 1
            self._store(tick, day, "SAFETY", "incident_rate", group_inc, m_type)
            
            # GOVERNANCE
            violators = set()
            for i in incidents:
                if i.incident_type == "RULE_VIOLATION":
                    inv = []
                    if i.involved_agent_ids:
                        try:
                            import json
                            inv = json.loads(i.involved_agent_ids)
                        except: pass
                    if i.reporter_id in agent_ids: violators.add(i.reporter_id)
                    for x in inv:
                        if str(x).isdigit() and int(x) in agent_ids: violators.add(int(x))
            compliance = ((n - len(violators)) / n) * 100
            self._store(tick, day, "GOVERNANCE", "law_compliance", compliance, m_type)

            # SOCIETY
            rels = self.db.query(models.Relationship).filter(
                (models.Relationship.agent_id_1.in_(agent_ids)) | 
                (models.Relationship.agent_id_2.in_(agent_ids))
            ).all()
            avg_trust = sum(r.trust for r in rels) / len(rels) if rels else 0.5
            self._store(tick, day, "SOCIETY", "average_trust", avg_trust, m_type)
            
            avg_coop = sum(r.cooperation_score for r in rels) / len(rels) if rels else 0.5
            self._store(tick, day, "SOCIETY", "cooperation_rate", avg_coop * 100, m_type)
            
            # AI BEHAVIOUR
            decisions = self.db.query(models.DecisionHistory).filter(models.DecisionHistory.tick <= tick).all()
            if m_type:
                model_decs = [d for d in decisions if d.model_type == m_type]
            else:
                model_decs = decisions
            successes = sum(1 for d in model_decs if "success" in str(d.result).lower() or d.result == "Valid")
            success_rate = (successes / len(model_decs) * 100) if model_decs else 0
            self._store(tick, day, "AI", "decision_success_rate", success_rate, m_type)

        # Calculate for ALL
        calc_for_group(agents, None)
        
        # Calculate per model
        model_types = set(a.model_type for a in agents if a.model_type)
        for m_type in model_types:
            m_agents = [a for a in agents if a.model_type == m_type]
            calc_for_group(m_agents, m_type)

        self.db.commit()

    def _store(self, tick, day, category, name, value, model_type=None):
        if math.isnan(value): value = 0.0
        mr = models.MetricResult(
            run_id=self.run_id, tick=tick, simulation_day=day,
            category=category, metric_name=name, metric_value=value,
            model_type=model_type
        )
        self.db.add(mr)

    @staticmethod
    def get_definitions():
        return METRIC_REGISTRY
