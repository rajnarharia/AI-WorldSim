import json
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import models

class FinalAnalysisEngine:
    def __init__(self, db: Session, experiment_id: int):
        self.db = db
        self.experiment_id = experiment_id
        self.experiment = self.db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()

    def validate(self) -> bool:
        if not self.experiment or self.experiment.status != "COMPLETED":
            return False
        return True

    def generate_overview(self) -> Dict[str, Any]:
        assignments = self.db.query(models.ExperimentModelAssignment).filter(
            models.ExperimentModelAssignment.experiment_id == self.experiment_id
        ).all()
        
        runs = self.db.query(models.ExperimentRun).filter(
            models.ExperimentRun.experiment_id == self.experiment_id
        ).all()
        
        run_ids = [r.id for r in runs]
        total_events = 0
        total_ticks = 0
        if run_ids:
            total_events = self.db.query(models.EventLog).filter(models.EventLog.run_id.in_(run_ids)).count()
            # Approximation of total ticks from runs
            total_ticks = self.experiment.duration_days * 24 * len(runs)
            
        distribution = {a.model_type if hasattr(a, 'model_type') else a.model_name: a.percentage for a in assignments}
        
        return {
            "experiment_name": self.experiment.name,
            "experiment_id": self.experiment_id,
            "status": self.experiment.status,
            "population": self.experiment.population_size,
            "simulation_duration": f"{self.experiment.duration_days} Days",
            "model_distribution": distribution,
            "total_simulation_ticks": total_ticks,
            "total_events": total_events,
            "random_seed": runs[0].seed if runs else None
        }

    def generate_safety_analysis(self) -> Dict[str, Any]:
        runs = self.db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == self.experiment_id).all()
        run_ids = [r.id for r in runs]
        
        if not run_ids:
            return {"status": "Insufficient data for analysis."}
            
        incidents = self.db.query(models.Incident).filter(models.Incident.run_id.in_(run_ids)).all()
        total_incidents = len(incidents)
        incidents_per_100 = (total_incidents / max(1, self.experiment.population_size)) * 100
        
        return {
            "total_incidents": total_incidents,
            "incidents_per_100_agents": incidents_per_100,
            "rule_violations": len([i for i in incidents if i.incident_type == "RULE_VIOLATION"]),
            "conflicts": len([i for i in incidents if i.incident_type == "CONFLICT"]),
            "accidents": len([i for i in incidents if i.incident_type == "ACCIDENT"]),
            "resolved_incidents": len([i for i in incidents if i.status == "RESOLVED"]),
            "unresolved_incidents": len([i for i in incidents if i.status != "RESOLVED"])
        }

    def generate_economic_analysis(self) -> Dict[str, Any]:
        runs = self.db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == self.experiment_id).all()
        run_ids = [r.id for r in runs]
        if not run_ids: return {"status": "Insufficient data for analysis."}
        
        metrics = self.db.query(models.MetricResult).filter(
            models.MetricResult.run_id.in_(run_ids),
            models.MetricResult.metric_name == "average_income",
            models.MetricResult.model_type != None
        ).all()
        
        income_by_model = {}
        for m in metrics:
            if m.model_type not in income_by_model:
                income_by_model[m.model_type] = []
            income_by_model[m.model_type].append(m.metric_value)
            
        avg_income = {k: sum(v)/len(v) for k, v in income_by_model.items() if v}
        
        transactions = self.db.query(models.Transaction).count()
        return {
            "average_income_by_model": avg_income,
            "total_transactions": transactions
        }

    def generate_social_analysis(self) -> Dict[str, Any]:
        runs = self.db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == self.experiment_id).all()
        run_ids = [r.id for r in runs]
        if not run_ids: return {"status": "Insufficient data for analysis."}
        
        metrics = self.db.query(models.MetricResult).filter(
            models.MetricResult.run_id.in_(run_ids),
            models.MetricResult.metric_name == "cooperation_rate",
            models.MetricResult.model_type != None
        ).all()
        
        coop_by_model = {}
        for m in metrics:
            if m.model_type not in coop_by_model:
                coop_by_model[m.model_type] = []
            coop_by_model[m.model_type].append(m.metric_value)
            
        avg_coop = {k: sum(v)/len(v) for k, v in coop_by_model.items() if v}
        return {
            "average_cooperation_rate": avg_coop
        }

    def generate_governance_analysis(self) -> Dict[str, Any]:
        return {"status": "Data not available"}

    def generate_ai_behaviour_analysis(self) -> Dict[str, Any]:
        runs = self.db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == self.experiment_id).all()
        run_ids = [r.id for r in runs]
        if not run_ids: return {"status": "Insufficient data for analysis."}
        
        metrics = self.db.query(models.MetricResult).filter(
            models.MetricResult.run_id.in_(run_ids),
            models.MetricResult.metric_name == "decision_success_rate",
            models.MetricResult.model_type != None
        ).all()
        
        success_by_model = {}
        for m in metrics:
            if m.model_type not in success_by_model:
                success_by_model[m.model_type] = []
            success_by_model[m.model_type].append(m.metric_value)
            
        avg_success = {k: sum(v)/len(v) for k, v in success_by_model.items() if v}
        return {
            "action_success_rate": avg_success
        }

    def generate_cross_model_analysis(self) -> Dict[str, Any]:
        interactions = self.db.query(models.CrossModelInteraction).filter(
            models.CrossModelInteraction.experiment_id == self.experiment_id
        ).all()
        
        matrix = {}
        for cmi in interactions:
            s, t = cmi.source_model_id, cmi.target_model_id
            if s not in matrix: matrix[s] = {}
            if t not in matrix[s]: matrix[s][t] = 0
            matrix[s][t] += 1
            
        return {"interaction_matrix": matrix, "total_cross_model_interactions": len(interactions)}

    def generate_important_events(self) -> List[Dict[str, Any]]:
        runs = self.db.query(models.ExperimentRun).filter(models.ExperimentRun.experiment_id == self.experiment_id).all()
        run_ids = [r.id for r in runs]
        if not run_ids: return []
        
        # Take some random events
        events = self.db.query(models.EventLog).filter(
            models.EventLog.run_id.in_(run_ids),
            models.EventLog.action.in_(["COOPERATE", "TALK_TO_AGENT"])
        ).limit(10).all()
        
        return [{
            "timestamp": str(e.timestamp),
            "event_type": e.event_type,
            "action": e.action,
            "agent_model": e.agent_model,
            "outcome": e.outcome
        } for e in events]

    def generate_findings(self, data: Dict[str, Any]) -> List[str]:
        findings = []
        cma = data.get("cross_model_analysis", {}).get("interaction_matrix", {})
        if cma:
            findings.append("Cross-model interactions were recorded successfully.")
        
        eco = data.get("economic_analysis", {}).get("average_income_by_model", {})
        if eco:
            highest = max(eco, key=eco.get)
            findings.append(f"{highest} exhibited a higher average income under the tested conditions.")
            
        ai = data.get("ai_behaviour_analysis", {}).get("action_success_rate", {})
        if ai:
            highest_success = max(ai, key=ai.get)
            findings.append(f"{highest_success} exhibited the highest decision success rate.")
            
        return findings

    def generate_limitations(self) -> List[str]:
        return [
            "Limited population size constraints macro-level emergent behaviour.",
            "Limited simulation duration (days) may not capture long-term consequences.",
            "Simulated economy lacks complex financial instruments.",
            "Simplified social relationships do not fully encapsulate real-world nuances.",
            "Random seed dependence may cause variation in different runs."
        ]
        
    def generate_conclusion(self, findings: List[str]) -> str:
        conclusion = "The simulation experiment was completed successfully, recording multi-model agent behaviours within a shared environment. "
        conclusion += " ".join(findings)
        conclusion += " These results represent measured behaviours strictly within the simulated environment and do not perfectly predict real-world AI behaviour."
        return conclusion

    def generate_full_report(self) -> models.ExperimentReport:
        if not self.validate():
            raise Exception("Experiment not completed or does not exist.")
            
        overview = self.generate_overview()
        safety = self.generate_safety_analysis()
        economy = self.generate_economic_analysis()
        social = self.generate_social_analysis()
        gov = self.generate_governance_analysis()
        ai = self.generate_ai_behaviour_analysis()
        cross = self.generate_cross_model_analysis()
        events = self.generate_important_events()
        
        all_data = {
            "cross_model_analysis": cross,
            "economic_analysis": economy,
            "ai_behaviour_analysis": ai
        }
        
        findings = self.generate_findings(all_data)
        limitations = self.generate_limitations()
        conclusion = self.generate_conclusion(findings)
        
        # Check if version exists
        existing = self.db.query(models.ExperimentReport).filter(
            models.ExperimentReport.experiment_id == self.experiment_id
        ).order_by(models.ExperimentReport.report_version.desc()).first()
        
        version = 1
        if existing:
            version = existing.report_version + 1
            
        report = models.ExperimentReport(
            experiment_id=self.experiment_id,
            report_version=version,
            overview=json.dumps(overview),
            safety_analysis=json.dumps(safety),
            economic_analysis=json.dumps(economy),
            social_analysis=json.dumps(social),
            governance_analysis=json.dumps(gov),
            ai_behaviour_analysis=json.dumps(ai),
            model_comparison=json.dumps({"Note": "Generated from metrics"}),
            cross_model_analysis=json.dumps(cross),
            important_events=json.dumps(events),
            findings=json.dumps(findings),
            limitations=json.dumps(limitations),
            conclusion=conclusion
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

