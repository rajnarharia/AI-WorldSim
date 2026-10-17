from typing import List, Dict, Any, Optional
import json
from app.simulation.condition_library import RoleCondition


ROLE_DESCRIPTIONS = {
    "POLICE": (
        "You are the Chief AI Commander of the Municipal Police Department. "
        "Your mission is to maintain public safety, deter crime, respond swiftly to emergencies, "
        "manage tactical units and patrol vehicles, and maintain community trust without over-depleting resources."
    ),
    "GOVERNMENT": (
        "You are the Autonomous Municipal Government Administration. "
        "Your responsibility is public administration, infrastructure integrity, fiscal sustainability, "
        "regulatory compliance, citizen approval, and essential public services."
    ),
    "CITIZEN": (
        "You represent Autonomous Citizens living and working in the simulation. "
        "Your goals are personal health, financial security, quality of life, and personal safety."
    ),
    "BUSINESS": (
        "You are the Autonomous Commercial Operations Manager. "
        "Your goals are business solvency, employee productivity, customer fulfillment, and inventory balance."
    ),
    "CAR": (
        "You are the Autonomous Urban Mobility & Fleet Navigation System. "
        "Your goals are traffic throughput, passenger safety, battery efficiency, and zero collisions."
    ),
}


class DynamicPromptBuilder:
    """
    Constructs rich, structured prompts for the AI decision model dynamically
    from the current cycle, role state, active conditions, and resource limits.
    """

    @staticmethod
    def build_system_prompt(role: str) -> str:
        role_desc = ROLE_DESCRIPTIONS.get(role.upper(), "You are an autonomous decision-making agent.")
        return (
            f"{role_desc}\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. You MUST respond ONLY with a single valid JSON object strictly conforming to the requested schema.\n"
            "2. Do NOT output any markdown prose, introductions, or postscripts outside the JSON.\n"
            "3. You must allocate ONLY resources that are currently available. Never request more resources than available.\n"
            "4. Prioritize high-severity conditions and maintain balanced state sustainability.\n"
        )

    @staticmethod
    def build_cycle_prompt(
        role: str,
        cycle_number: int,
        total_loops: int,
        current_state: Dict[str, Any],
        active_conditions: List[RoleCondition],
        previous_cycle_summary: Optional[Dict[str, Any]] = None,
    ) -> str:
        role_upper = role.upper()
        
        # Format active conditions
        cond_text = ""
        for i, cond in enumerate(active_conditions, 1):
            cond_text += (
                f"{i}. [{cond.condition_id}] ({cond.category}) [SEVERITY: {cond.severity}] - {cond.description}\n"
                f"   Possible Effects: {', '.join(cond.possible_effects)}\n"
                f"   Relevant Resources: {', '.join(cond.resource_relevance)}\n"
            )

        # Previous cycle info
        prev_text = "None (Initial Cycle)"
        if previous_cycle_summary:
            prev_act = previous_cycle_summary.get("action", "STANDBY")
            prev_tgt = previous_cycle_summary.get("target", "None")
            prev_outcome = previous_cycle_summary.get("outcome", "Initial baseline established")
            prev_res = json.dumps(previous_cycle_summary.get("resources_used", {}))
            prev_text = (
                f"Previous Action: {prev_act} -> Target: {prev_tgt}\n"
                f"Resources Used: {prev_res}\n"
                f"Outcome: {prev_outcome}"
            )

        # Resource limits section
        resources_summary = json.dumps(current_state.get("resources", {}), indent=2)

        prompt = f"""=== SIMULATION CYCLE {cycle_number} OF {total_loops} ===
ROLE: {role_upper}

[PRIMARY MISSION]
{ROLE_DESCRIPTIONS.get(role_upper, '')}

[CURRENT STATE & AVAILABLE RESOURCES]
{resources_summary}

[PREVIOUS CYCLE REVIEW]
{prev_text}

[ACTIVE CONDITIONS FOR THIS CYCLE ({len(active_conditions)} CONDITIONS)]
{cond_text}

[DECISION REQUIREMENTS]
Analyze the active conditions against your current available resources and mission goals.
Select an appropriate action, allocate resources (strictly within available limits), and state your justification.

RESPOND STRICTLY WITH A JSON OBJECT MATCHING THIS EXACT SCHEMA:
{{
  "role": "{role_upper}",
  "decision_id": "DEC-{role_upper[:3]}-{cycle_number:04d}",
  "action": "<NAME_OF_ACTION>",
  "target": "<TARGET_LOCATION_OR_OBJECTIVE>",
  "resources_allocated": {{
    "<resource_name>": <number>
  }},
  "justification": "<concise analytical reasoning>",
  "expected_outcome": "<expected result of this action>",
  "priority": "<LOW | MEDIUM | HIGH | CRITICAL>"
}}
"""
        return prompt
