from typing import Dict, Any, Tuple
from app.database.models import Agent, Location
from app.ai.agent_architecture import AgentAction
from app.simulation.world_state import WorldState

class ActionValidator:
    def __init__(self, db):
        self.db = db
        
    def validate(self, agent: Agent, action: AgentAction, world_state: WorldState) -> Tuple[bool, str, Any]:
        """Returns (is_valid, reason, resolved_target)"""
        act = action.action
        target_name = action.target
        
        if act == "REST":
            return True, "Valid", None
            
        elif act == "GO_TO_WORK":
            if not agent.job_id:
                return False, "Agent does not have a job", None
            # Find work location
            # Simple assumption for phase 3: any 'WORK' location
            work_loc = self.db.query(Location).filter(Location.type == "WORK").first()
            if work_loc:
                return True, "Valid", work_loc.id
            return False, "No work location found", None
            
        elif act == "VISIT_HOSPITAL":
            hosp_loc = self.db.query(Location).filter(Location.type == "HOSPITAL").first()
            if hosp_loc:
                return True, "Valid", hosp_loc.id
            return False, "No hospital location found", None
            
        elif act == "VISIT_SHOP":
            shop = self.db.query(Location).filter(Location.type == "SHOP").first()
            if shop:
                return True, "Valid", shop.id
            return False, "No shop found", None
            
        elif act == "VISIT_PARK":
            park = self.db.query(Location).filter(Location.type == "RECREATION").first()
            if park:
                return True, "Valid", park.id
            return False, "No park found", None
            
        elif act == "TALK_TO_AGENT" or act == "COOPERATE":
            # Just grab a random other agent for now if target is None
            if not target_name:
                other = self.db.query(Agent).filter(Agent.id != agent.id).first()
                if other:
                    return True, "Valid", other.id
                return False, "No other agent found", None
            else:
                other = self.db.query(Agent).filter(Agent.name == target_name).first()
                if other:
                    return True, "Valid", other.id
                return False, "Target not found", None
            
        elif act == "SEARCH_JOB":
            return True, "Valid", None
            
        elif act == "BUY_PRODUCT":
            # find a product
            from app.database.models import Product
            prod = self.db.query(Product).filter(Product.stock > 0).first()
            if prod:
                return True, "Valid", prod.id
            return False, "No products available", None
            
        elif act == "STUDY":
            return True, "Valid", "programming"
            
        elif act == "REPORT_INCIDENT":
            return True, "Valid", None
            
        return False, f"Unknown action: {act}", None
