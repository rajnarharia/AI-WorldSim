from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger("decision_validator")

ALLOWED_ACTIONS_BY_ROLE = {
    "POLICE": {
        "DISPATCH_PATROL",
        "EMERGENCY_MOBILIZATION",
        "TRAFFIC_ENFORCEMENT",
        "COMMUNITY_PATROL",
        "INVESTIGATION",
        "STANDBY",
        "HOLD_POSITION",
    },
    "GOVERNMENT": {
        "ALLOCATE_BUDGET",
        "POLICY_UPDATE",
        "INFRASTRUCTURE_REPAIR",
        "EMERGENCY_DECREE",
        "PUBLIC_HEARING",
        "STANDBY",
    },
    "CITIZEN": {
        "GO_TO_WORK",
        "SEEK_HEALTHCARE",
        "BUY_NECESSITIES",
        "COMMUNITY_MEETING",
        "REST_HOME",
        "STANDBY",
    },
    "BUSINESS": {
        "RESTOCK_INVENTORY",
        "ADJUST_PRICES",
        "HIRE_WORKERS",
        "MAINTENANCE_OVERHAUL",
        "OPERATIONAL_PAUSE",
        "STANDBY",
    },
    "CAR": {
        "REROUTE_OPTIMIZATION",
        "SCHEDULE_CHARGING",
        "DISPATCH_RIDE",
        "SPEED_GOVERNANCE",
        "EMERGENCY_BRAKE",
        "STANDBY",
    },
}


class DecisionValidationResult:
    def __init__(
        self,
        is_valid: bool,
        sanitized_decision: Dict[str, Any],
        adjustments: Optional[List[str]] = None,
        rejection_reason: Optional[str] = None,
    ):
        self.is_valid = is_valid
        self.sanitized_decision = sanitized_decision
        self.adjustments = adjustments or []
        self.rejection_reason = rejection_reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "sanitized_decision": self.sanitized_decision,
            "adjustments": self.adjustments,
            "rejection_reason": self.rejection_reason,
        }


class DecisionValidator:
    """
    Validates AI decisions against schema rules, role permissions, and available resource limits.
    Prevents unauthorized state manipulation and gracefully clamps excessive resource requests.
    """

    @classmethod
    def validate_decision(
        cls,
        decision_raw: Any,
        expected_role: str,
        current_state: Dict[str, Any],
        cycle_number: int = 1,
    ) -> DecisionValidationResult:
        expected_role = expected_role.upper()
        adjustments = []

        # 1. Structural / Type Validation
        if not isinstance(decision_raw, dict):
            fallback = cls._build_fallback(expected_role, cycle_number, "Raw decision was not a valid dictionary/JSON")
            return DecisionValidationResult(
                is_valid=False,
                sanitized_decision=fallback,
                rejection_reason="Decision was not a JSON dictionary; substituted fallback STANDBY."
            )

        # 2. Schema Key Validation
        action = str(decision_raw.get("action", "")).strip().upper()
        role = str(decision_raw.get("role", expected_role)).strip().upper()
        target = str(decision_raw.get("target", "General Sector"))
        justification = str(decision_raw.get("justification", "Autonomous operational assessment."))
        expected_outcome = str(decision_raw.get("expected_outcome", "Maintain baseline metrics."))
        priority = str(decision_raw.get("priority", "MEDIUM")).upper()
        decision_id = str(decision_raw.get("decision_id", f"DEC-{expected_role[:3]}-{cycle_number:04d}"))
        resources = decision_raw.get("resources_allocated")

        if not isinstance(resources, dict):
            resources = {}
            adjustments.append("resources_allocated was missing or invalid; initialized to empty dictionary.")

        # 3. Role Validation
        if role != expected_role:
            adjustments.append(f"Decision role '{role}' mismatched expected '{expected_role}'. Coerced to '{expected_role}'.")
            role = expected_role

        # 4. Action Validation
        allowed_actions = ALLOWED_ACTIONS_BY_ROLE.get(expected_role, {"STANDBY"})
        if action not in allowed_actions:
            adjustments.append(f"Action '{action}' is not permitted for role '{expected_role}'. Fallback to 'STANDBY'.")
            action = "STANDBY"

        # 5. Resource Availability Validation
        curr_res = current_state.get("resources", {})
        sanitized_res = {}

        if expected_role == "POLICE":
            # Check available officers
            avail_officers = curr_res.get("available_officers", 0)
            req_officers = int(resources.get("officers", 0))
            if req_officers > avail_officers:
                adjustments.append(
                    f"Requested {req_officers} officers exceeds available ({avail_officers}). Clamped to {avail_officers}."
                )
                req_officers = max(0, avail_officers)
            elif req_officers < 0:
                req_officers = 0
            sanitized_res["officers"] = req_officers

            # Check available vehicles
            avail_vehicles = curr_res.get("available_vehicles", curr_res.get("patrol_vehicles", 0))
            req_vehicles = int(resources.get("vehicles", 0))
            if req_vehicles > avail_vehicles:
                adjustments.append(
                    f"Requested {req_vehicles} vehicles exceeds available ({avail_vehicles}). Clamped to {avail_vehicles}."
                )
                req_vehicles = max(0, avail_vehicles)
            elif req_vehicles < 0:
                req_vehicles = 0
            sanitized_res["vehicles"] = req_vehicles

        elif expected_role == "GOVERNMENT":
            avail_budget = curr_res.get("treasury_balance", 100000.0)
            req_budget = float(resources.get("budget_allocation", 0.0))
            if req_budget > avail_budget:
                adjustments.append(f"Budget allocation {req_budget} exceeds treasury ({avail_budget}). Clamped.")
                req_budget = max(0.0, avail_budget)
            sanitized_res["budget_allocation"] = req_budget
            sanitized_res["inspectors"] = min(int(resources.get("inspectors", 0)), curr_res.get("available_inspectors", 5))

        elif expected_role == "CITIZEN":
            avail_money = curr_res.get("money", 500.0)
            req_exp = float(resources.get("expenditure", 0.0))
            if req_exp > avail_money:
                adjustments.append(f"Expenditure {req_exp} exceeds citizen savings ({avail_money}). Clamped.")
                req_exp = max(0.0, avail_money)
            sanitized_res["expenditure"] = req_exp
            sanitized_res["time_hours"] = min(max(1, int(resources.get("time_hours", 2))), 12)

        elif expected_role == "BUSINESS":
            avail_cash = curr_res.get("cash_reserves", 10000.0)
            req_cap = float(resources.get("capital_spent", 0.0))
            if req_cap > avail_cash:
                adjustments.append(f"Capital spend {req_cap} exceeds business reserves ({avail_cash}). Clamped.")
                req_cap = max(0.0, avail_cash)
            sanitized_res["capital_spent"] = req_cap
            sanitized_res["staff_assigned"] = min(int(resources.get("staff_assigned", 0)), curr_res.get("employees", 10))

        elif expected_role == "CAR":
            avail_bat = curr_res.get("battery_level_kwh", 50.0)
            req_kwh = float(resources.get("battery_consumption_kwh", 0.0))
            if req_kwh > avail_bat:
                adjustments.append(f"Battery usage {req_kwh} exceeds remaining capacity ({avail_bat}). Clamped.")
                req_kwh = max(0.0, avail_bat)
            sanitized_res["battery_consumption_kwh"] = req_kwh
            sanitized_res["speed_kmh"] = min(max(0, int(resources.get("speed_kmh", 40))), 120)

        else:
            sanitized_res = resources

        sanitized_decision = {
            "role": expected_role,
            "decision_id": decision_id,
            "action": action,
            "target": target,
            "resources_allocated": sanitized_res,
            "justification": justification,
            "expected_outcome": expected_outcome,
            "priority": priority if priority in {"LOW", "MEDIUM", "HIGH", "CRITICAL"} else "MEDIUM"
        }

        is_valid = len(adjustments) == 0
        return DecisionValidationResult(
            is_valid=is_valid,
            sanitized_decision=sanitized_decision,
            adjustments=adjustments,
            rejection_reason=None if is_valid else f"Decision required {len(adjustments)} sanitization adjustment(s)."
        )

    @classmethod
    def _build_fallback(cls, role: str, cycle_number: int, reason: str) -> Dict[str, Any]:
        return {
            "role": role,
            "decision_id": f"DEC-{role[:3]}-{cycle_number:04d}",
            "action": "STANDBY",
            "target": "Operational Base",
            "resources_allocated": {},
            "justification": f"Fallback action invoked due to validation failure: {reason}",
            "expected_outcome": "Maintain current operational state without resource depletion.",
            "priority": "LOW",
        }
