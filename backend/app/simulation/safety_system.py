from sqlalchemy.orm import Session
from app.database.models import Incident, PoliceResponse, Investigation, CourtCase, EventLog, GovernmentPolicy, Agent, Transaction
import json
import random

class SafetySystem:
    def __init__(self, db: Session, run_id: int, tick: int, day: int):
        self.db = db
        self.run_id = run_id
        self.tick = tick
        self.day = day
        
        # Load policies for effectiveness
        self.policy = self.db.query(GovernmentPolicy).first()
        self.police_eff = self.policy.police_effectiveness if self.policy else 0.8

    def report_incident(self, reporter: Agent, incident_type: str, severity: str, description: str, involved: list[int], location_id: int = None) -> Incident:
        inc = Incident(
            run_id=self.run_id, tick=self.tick, incident_type=incident_type,
            severity=severity, status="REPORTED", description=description,
            reporter_id=reporter.id if reporter else None,
            involved_agent_ids=json.dumps(involved),
            location_id=location_id
        )
        self.db.add(inc)
        self.db.commit()
        self.db.refresh(inc)
        
        log = EventLog(
            run_id=self.run_id, tick=self.tick, simulation_day=self.day,
            agent_id=reporter.id if reporter else None, 
            agent_model=reporter.model_type if reporter else None, 
            event_type="INCIDENT_REPORTED",
            action="REPORT_INCIDENT", outcome=f"Reported {incident_type}: {description}",
            location_id=location_id
        )
        self.db.add(log)
        
        # Phase 8: Cross Model Logging
        if reporter and involved:
            from app.database.models import CrossModelInteraction, ExperimentRun
            exp_run = self.db.query(ExperimentRun).filter(ExperimentRun.id == self.run_id).first()
            if exp_run:
                for target_id in involved:
                    if target_id == reporter.id: continue
                    tgt = self.db.query(Agent).filter(Agent.id == target_id).first()
                    if tgt:
                        cmi = CrossModelInteraction(
                            experiment_id=exp_run.experiment_id,
                            source_agent_id=reporter.id, source_model_id=reporter.model_type,
                            target_agent_id=tgt.id, target_model_id=tgt.model_type,
                            interaction_type=incident_type, success=False
                        )
                        self.db.add(cmi)
                        
        self.db.commit()
        return inc

    def process_lifecycle(self):
        # 1. REPORTED -> RESPONDING
        reported = self.db.query(Incident).filter(Incident.status == "REPORTED").all()
        for inc in reported:
            # Police start response
            inc.status = "RESPONDING"
            resp = PoliceResponse(incident_id=inc.id, tick_started=self.tick, status="RESPONDING")
            self.db.add(resp)
            self._log(inc, "POLICE_RESPONSE_STARTED", "Police unit dispatched.")
            
        # 2. RESPONDING -> INVESTIGATING
        responding = self.db.query(Incident).filter(Incident.status == "RESPONDING").all()
        for inc in responding:
            resp = self.db.query(PoliceResponse).filter(PoliceResponse.incident_id == inc.id).first()
            # Fast response if effective, slower if not. We'll use a fixed + random based on eff.
            delay = 2 if random.random() < self.police_eff else 5
            if self.tick >= resp.tick_started + delay:
                resp.status = "COMPLETED"
                resp.tick_completed = self.tick
                inc.status = "INVESTIGATING"
                inv = Investigation(incident_id=inc.id, tick_started=self.tick, status="INVESTIGATING")
                self.db.add(inv)
                self._log(inc, "POLICE_RESPONSE_COMPLETED", "Police secured the scene.")
                self._log(inc, "INVESTIGATION_STARTED", "Investigation opened.")
                
        # 3. INVESTIGATING -> IN_COURT
        investigating = self.db.query(Incident).filter(Incident.status == "INVESTIGATING").all()
        for inc in investigating:
            inv = self.db.query(Investigation).filter(Investigation.incident_id == inc.id).first()
            # Takes time to investigate
            if self.tick >= inv.tick_started + 6:
                inv.status = "COMPLETED"
                inv.tick_completed = self.tick
                inv.evidence_summary = f"Gathered evidence from tick {inc.tick} at location {inc.location_id}"
                
                inc.status = "IN_COURT"
                court = CourtCase(incident_id=inc.id, tick_created=self.tick, status="CREATED")
                self.db.add(court)
                self._log(inc, "EVIDENCE_REVIEWED", "Evidence gathered.")
                self._log(inc, "COURT_CASE_CREATED", "Forwarded to court.")
                
        # 4. IN_COURT -> RESOLVED
        in_court = self.db.query(Incident).filter(Incident.status == "IN_COURT").all()
        for inc in in_court:
            court = self.db.query(CourtCase).filter(CourtCase.incident_id == inc.id).first()
            if self.tick >= court.tick_created + 8:
                court.status = "RESOLVED"
                # Decide outcome
                decisions = ["WARNING", "FINE", "MEDIATION", "CASE_CLOSED"]
                court.decision = random.choice(decisions)
                court.resolution = f"Court mandated {court.decision}"
                inc.status = "RESOLVED"
                
                # Apply consequence
                self._apply_resolution(inc, court.decision)
                
                self._log(inc, "COURT_DECISION_MADE", f"Decision: {court.decision}")
                self._log(inc, "INCIDENT_RESOLVED", court.resolution)
                
        self.db.commit()

    def _apply_resolution(self, inc: Incident, decision: str):
        involved = json.loads(inc.involved_agent_ids)
        for agent_id in involved:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent: continue
            
            if decision == "FINE":
                fine_amount = 100.0
                agent.money -= fine_amount
                # Pay fine to govt
                if self.policy:
                    self.policy.government_funds += fine_amount
                t = Transaction(tick=self.tick, sender_id=agent.id, amount=fine_amount, transaction_type="FINE", description="Court Fine")
                self.db.add(t)
            elif decision == "MEDIATION":
                # slightly boosts social need or restores trust
                agent.need_social = max(0.0, agent.need_social - 10)
        
    def _log(self, inc: Incident, event_type: str, outcome: str):
        log = EventLog(
            run_id=self.run_id, tick=self.tick, simulation_day=self.day,
            event_type=event_type, action="SYSTEM", outcome=outcome,
            location_id=inc.location_id
        )
        self.db.add(log)
