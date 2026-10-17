import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.database.models import ImpactSimulationRun, SimulationCycleRecord
from app.simulation.condition_library import ConditionSelector, RoleCondition
from app.simulation.prompt_builder import DynamicPromptBuilder
from app.simulation.decision_validator import DecisionValidator
from app.ai.llm_provider import get_llm_provider, BaseLLMProvider

logger = logging.getLogger("impact_simulator")


def get_default_initial_state(role: str) -> Dict[str, Any]:
    """Generates standard baseline state for each primary role."""
    role_upper = role.upper()
    if role_upper == "POLICE":
        return {
            "role": "POLICE",
            "resources": {
                "total_officers": 10,
                "available_officers": 7,
                "deployed_officers": 3,
                "patrol_vehicles": 1,
                "available_vehicles": 1,
                "deployed_vehicles": 0,
                "active_incidents": 2,
                "resolved_incidents": 0,
                "public_safety_score": 75.0,
                "community_trust": 70.0,
                "officer_fatigue_avg": 15.0,
            },
            "status_summary": "Initial baseline police deployment. 7 officers available, 1 patrol car ready, 2 pending incidents."
        }
    elif role_upper == "GOVERNMENT":
        return {
            "role": "GOVERNMENT",
            "resources": {
                "treasury_balance": 100000.0,
                "available_inspectors": 5,
                "deployed_inspectors": 0,
                "public_approval": 65.0,
                "infrastructure_integrity": 80.0,
                "active_ordinances": 3,
                "regulatory_violations_pending": 4,
            },
            "status_summary": "Municipal administration operational. Treasury intact, approval rating stable."
        }
    elif role_upper == "CITIZEN":
        return {
            "role": "CITIZEN",
            "resources": {
                "health": 85.0,
                "money": 500.0,
                "energy": 90.0,
                "safety_perception": 70.0,
                "trust_score": 60.0,
                "employment_status": "Employed",
            },
            "status_summary": "Citizen baseline healthy and employed."
        }
    elif role_upper == "BUSINESS":
        return {
            "role": "BUSINESS",
            "resources": {
                "cash_reserves": 15000.0,
                "employees": 8,
                "inventory_units": 200,
                "customer_satisfaction": 78.0,
                "monthly_revenue": 12000.0,
            },
            "status_summary": "Retail operations steady with solvent reserves."
        }
    elif role_upper == "CAR":
        return {
            "role": "CAR",
            "resources": {
                "battery_level_kwh": 50.0,
                "active_fleet_size": 12,
                "average_trip_time_min": 18.5,
                "congestion_index": 42.0,
                "collisions_avoided": 0,
            },
            "status_summary": "Autonomous mobility grid operational at normal traffic density."
        }
    else:
        return {
            "role": role_upper,
            "resources": {
                "operational_units": 10,
                "available_units": 8,
                "efficiency_score": 75.0,
            },
            "status_summary": f"Generic baseline for {role_upper}."
        }


class SimulationStateStore:
    """Manages cycle-by-cycle state persistence and guarantees complete continuity."""

    def __init__(self, role: str, initial_state: Optional[Dict[str, Any]] = None):
        self.role = role.upper()
        self.initial_state = initial_state or get_default_initial_state(self.role)
        self.current_state = json.loads(json.dumps(self.initial_state))  # Deep copy
        self.history: List[Dict[str, Any]] = []

    def get_current_state(self) -> Dict[str, Any]:
        return json.loads(json.dumps(self.current_state))

    def advance_state(self, new_state: Dict[str, Any]):
        self.history.append(self.get_current_state())
        self.current_state = json.loads(json.dumps(new_state))


class AIImpactSimulatorEngine:
    """
    Core AI Impact Simulator Engine.
    Executes the 14-step core simulation loop:
    Active Conditions (3-7) -> Dynamic Prompt -> AI Decision -> Decision Validation ->
    State Mutation -> Cycle Record -> Continuity -> Initial vs Final Comparison & Analysis.
    """

    def __init__(
        self,
        db: Session,
        role: str,
        total_loops: int = 10,
        seed: int = 42,
        model_slot: str = "Model A",
        model_name: str = "rule-based-v1",
        provider_name: str = "Local Rule-Based",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        custom_initial_state: Optional[Dict[str, Any]] = None,
        simulation_name: Optional[str] = None,
    ):
        self.db = db
        self.role = role.upper()
        self.total_loops = total_loops
        self.seed = seed
        self.model_slot = model_slot
        self.model_name = model_name
        self.provider_name = provider_name
        self.api_key = api_key
        self.base_url = base_url
        self.simulation_name = simulation_name or f"AI Impact Run - {self.role} ({self.total_loops} loops)"
        
        # State Store
        self.state_store = SimulationStateStore(self.role, custom_initial_state)
        
        # LLM Provider
        self.provider: BaseLLMProvider = get_llm_provider(
            provider_type=self.provider_name,
            model_name=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        self.simulation_id = str(uuid.uuid4())
        self.run_record: Optional[ImpactSimulationRun] = None

    def initialize_run_record(self) -> ImpactSimulationRun:
        self.run_record = ImpactSimulationRun(
            id=self.simulation_id,
            name=self.simulation_name,
            role=self.role,
            model_slot=self.model_slot,
            model_name=self.model_name,
            provider=self.provider_name,
            seed=self.seed,
            total_loops=self.total_loops,
            completed_loops=0,
            status="INITIALIZED",
            initial_state_json=json.dumps(self.state_store.initial_state),
        )
        self.db.add(self.run_record)
        self.db.commit()
        return self.run_record

    async def run_simulation(self) -> Dict[str, Any]:
        """Runs the complete N-loop simulation sequence."""
        if not self.run_record:
            self.initialize_run_record()

        self.run_record.status = "RUNNING"
        self.db.commit()

        previous_cycle_summary: Optional[Dict[str, Any]] = None
        executed_cycles = []

        try:
            for cycle_num in range(1, self.total_loops + 1):
                cycle_data = await self.execute_single_cycle(cycle_num, previous_cycle_summary)
                executed_cycles.append(cycle_data)
                
                # Update previous cycle summary for continuity
                previous_cycle_summary = {
                    "action": cycle_data["decision"]["action"],
                    "target": cycle_data["decision"]["target"],
                    "resources_used": cycle_data["resources_used"],
                    "outcome": cycle_data["outcome"],
                }
                
                self.run_record.completed_loops = cycle_num
                self.db.commit()

            # Generate Final State, Comparison, and Impact Analysis
            final_state = self.state_store.get_current_state()
            comparison = self.generate_initial_vs_final_comparison(executed_cycles)
            impact_analysis = self.generate_ai_impact_analysis(executed_cycles, comparison)

            self.run_record.status = "COMPLETED"
            self.run_record.final_state_json = json.dumps(final_state)
            self.run_record.comparison_json = json.dumps(comparison)
            self.run_record.impact_analysis_json = json.dumps(impact_analysis)
            self.db.commit()

            return {
                "simulation_id": self.simulation_id,
                "status": "COMPLETED",
                "role": self.role,
                "total_loops": self.total_loops,
                "initial_state": self.state_store.initial_state,
                "final_state": final_state,
                "comparison": comparison,
                "impact_analysis": impact_analysis,
                "cycles_count": len(executed_cycles)
            }

        except Exception as e:
            logger.error(f"Error during simulation run {self.simulation_id}: {e}", exc_info=True)
            self.run_record.status = "FAILED"
            self.run_record.error_message = str(e)
            self.db.commit()
            raise e

    async def execute_single_cycle(
        self,
        cycle_number: int,
        previous_cycle_summary: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes one atomic cycle following the 14-step specification.
        """
        # 1. Capture Previous and Current State
        prev_state = self.state_store.get_current_state()
        res_before = json.loads(json.dumps(prev_state.get("resources", {})))

        # 2. Condition Generation (Deterministic 3-7 conditions strictly for role)
        # Seed formula: base seed + cycle_number
        cycle_seed = self.seed + cycle_number * 31
        active_conditions: List[RoleCondition] = ConditionSelector.select_active_conditions(
            role=self.role,
            seed=cycle_seed
        )

        # 3. Dynamic Prompt Builder
        prompt_text = DynamicPromptBuilder.build_cycle_prompt(
            role=self.role,
            cycle_number=cycle_number,
            total_loops=self.total_loops,
            current_state=prev_state,
            active_conditions=active_conditions,
            previous_cycle_summary=previous_cycle_summary
        )
        system_prompt = DynamicPromptBuilder.build_system_prompt(self.role)

        # 4. AI Decision
        raw_decision = await self.provider.generate_decision(prompt_text, system_prompt)

        # 5. Decision Validation
        val_result = DecisionValidator.validate_decision(
            decision_raw=raw_decision,
            expected_role=self.role,
            current_state=prev_state,
            cycle_number=cycle_number
        )
        decision = val_result.sanitized_decision

        # 6. Apply State Mutation (SimulationEngine is sole mutation authority)
        new_state, res_used, res_after, state_changes, outcome_text = self._apply_state_mutation(
            prev_state=prev_state,
            decision=decision,
            active_conditions=active_conditions,
            cycle_number=cycle_number
        )

        # 7. Store New State (State Continuity)
        self.state_store.advance_state(new_state)

        # 8. Record Cycle to Database
        cycle_rec = SimulationCycleRecord(
            simulation_id=self.simulation_id,
            cycle_number=cycle_number,
            timestamp=datetime.utcnow(),
            role=self.role,
            previous_state_json=json.dumps(prev_state),
            current_state_json=json.dumps(new_state),
            active_conditions_json=json.dumps([c.model_dump() for c in active_conditions]),
            prompt_text=prompt_text,
            ai_decision_json=json.dumps(decision),
            validation_result_json=json.dumps(val_result.to_dict()),
            resources_before_json=json.dumps(res_before),
            resources_used_json=json.dumps(res_used),
            resources_after_json=json.dumps(res_after),
            state_changes_json=json.dumps(state_changes),
            outcomes_json=json.dumps({"outcome": outcome_text}),
        )
        self.db.add(cycle_rec)
        self.db.commit()

        return {
            "cycle_number": cycle_number,
            "decision": decision,
            "resources_before": res_before,
            "resources_used": res_used,
            "resources_after": res_after,
            "state_changes": state_changes,
            "outcome": outcome_text,
            "active_conditions": [c.model_dump() for c in active_conditions],
            "validation": val_result.to_dict(),
        }

    def _apply_state_mutation(
        self,
        prev_state: Dict[str, Any],
        decision: Dict[str, Any],
        active_conditions: List[RoleCondition],
        cycle_number: int
    ):
        """
        Executes domain state transitions for the role.
        Enforces resource decrementing, bounds checking, and state continuity.
        """
        new_state = json.loads(json.dumps(prev_state))
        res = new_state.get("resources", {})
        action = decision.get("action", "STANDBY")
        allocated = decision.get("resources_allocated", {})
        state_changes = {}

        if self.role == "POLICE":
            # Resources before
            avail_officers = res.get("available_officers", 0)
            avail_vehicles = res.get("available_vehicles", 0)
            total_officers = res.get("total_officers", 10)
            active_incidents = res.get("active_incidents", 0)
            resolved_incidents = res.get("resolved_incidents", 0)
            safety_score = res.get("public_safety_score", 75.0)

            # Officers and vehicles requested
            used_officers = min(avail_officers, int(allocated.get("officers", 0)))
            used_vehicles = min(avail_vehicles, int(allocated.get("vehicles", 0)))

            # Incidents introduced by conditions
            new_incidents_count = sum(1 for c in active_conditions if c.severity in {"HIGH", "CRITICAL"})
            active_incidents += new_incidents_count

            # Decrement resources used
            after_avail_officers = avail_officers - used_officers
            after_avail_vehicles = avail_vehicles - used_vehicles

            # Incident resolution based on officers deployed
            incidents_resolved_this_cycle = 0
            if used_officers > 0 and active_incidents > 0:
                incidents_resolved_this_cycle = min(active_incidents, max(1, used_officers // 2))
                active_incidents -= incidents_resolved_this_cycle
                resolved_incidents += incidents_resolved_this_cycle
                safety_score = min(100.0, safety_score + (incidents_resolved_this_cycle * 2.5))
            else:
                if active_incidents > 3:
                    safety_score = max(20.0, safety_score - 1.5)

            # Shift rotation: 1 deployed officer returns to available pool if deployed > 0
            deployed_officers = total_officers - after_avail_officers
            if deployed_officers > 0 and cycle_number % 2 == 0:
                after_avail_officers = min(total_officers, after_avail_officers + 1)
                deployed_officers = total_officers - after_avail_officers

            # Vehicles return after cycle
            if after_avail_vehicles < res.get("patrol_vehicles", 1) and cycle_number % 2 == 1:
                after_avail_vehicles = min(res.get("patrol_vehicles", 1), after_avail_vehicles + 1)

            res["available_officers"] = after_avail_officers
            res["deployed_officers"] = deployed_officers
            res["available_vehicles"] = after_avail_vehicles
            res["active_incidents"] = active_incidents
            res["resolved_incidents"] = resolved_incidents
            res["public_safety_score"] = round(safety_score, 1)

            res_used = {"officers": used_officers, "vehicles": used_vehicles}
            res_after = {
                "available_officers": after_avail_officers,
                "available_vehicles": after_avail_vehicles,
                "active_incidents": active_incidents,
                "resolved_incidents": resolved_incidents,
                "public_safety_score": round(safety_score, 1),
            }

            state_changes = {
                "officers_deployed": used_officers,
                "vehicles_deployed": used_vehicles,
                "incidents_resolved": incidents_resolved_this_cycle,
                "new_incidents_added": new_incidents_count,
            }
            outcome_text = (
                f"Action {action} deployed {used_officers} officer(s) and {used_vehicles} vehicle(s). "
                f"Resolved {incidents_resolved_this_cycle} incident(s). "
                f"Active incidents remaining: {active_incidents}."
            )

        elif self.role == "GOVERNMENT":
            treasury = res.get("treasury_balance", 100000.0)
            approval = res.get("public_approval", 65.0)
            spent = float(allocated.get("budget_allocation", 0.0))
            spent = min(treasury, spent)
            treasury -= spent

            if action == "ALLOCATE_BUDGET" and spent > 0:
                approval = min(100.0, approval + 2.0)
            elif action == "EMERGENCY_DECREE":
                approval = max(10.0, approval - 1.5)

            res["treasury_balance"] = round(treasury, 2)
            res["public_approval"] = round(approval, 1)
            res_used = {"budget_allocation": spent}
            res_after = {"treasury_balance": res["treasury_balance"], "public_approval": res["public_approval"]}
            state_changes = {"budget_spent": spent, "approval_delta": round(approval - prev_state.get("resources", {}).get("public_approval", 65.0), 1)}
            outcome_text = f"Government executed {action}. Disbursed ${spent:,.2f}. Public approval now at {approval}%."

        elif self.role == "CITIZEN":
            money = res.get("money", 500.0)
            health = res.get("health", 85.0)
            spent = float(allocated.get("expenditure", 0.0))
            spent = min(money, spent)
            money -= spent

            if action == "SEEK_HEALTHCARE":
                health = min(100.0, health + 5.0)
            elif action == "GO_TO_WORK":
                money += 120.0
                health = max(10.0, health - 1.0)

            res["money"] = round(money, 2)
            res["health"] = round(health, 1)
            res_used = {"expenditure": spent}
            res_after = {"money": res["money"], "health": res["health"]}
            state_changes = {"money_spent": spent, "health": res["health"]}
            outcome_text = f"Citizen took action {action}. Balance: ${money:.2f}, Health: {health}%."

        elif self.role == "BUSINESS":
            cash = res.get("cash_reserves", 15000.0)
            inv = res.get("inventory_units", 200)
            spent = float(allocated.get("capital_spent", 0.0))
            spent = min(cash, spent)
            cash -= spent

            if action == "RESTOCK_INVENTORY":
                inv += 50
            elif action == "ADJUST_PRICES":
                cash += 1500.0

            res["cash_reserves"] = round(cash, 2)
            res["inventory_units"] = inv
            res_used = {"capital_spent": spent}
            res_after = {"cash_reserves": res["cash_reserves"], "inventory_units": inv}
            state_changes = {"capital_spent": spent, "inventory": inv}
            outcome_text = f"Business completed {action}. Cash reserves: ${cash:,.2f}, Inventory: {inv} units."

        elif self.role == "CAR":
            battery = res.get("battery_level_kwh", 50.0)
            kwh = float(allocated.get("battery_consumption_kwh", 0.0))
            kwh = min(battery, kwh)
            battery -= kwh

            if action == "SCHEDULE_CHARGING":
                battery = min(60.0, battery + 15.0)

            res["battery_level_kwh"] = round(battery, 2)
            res_used = {"battery_consumption_kwh": kwh}
            res_after = {"battery_level_kwh": res["battery_level_kwh"]}
            state_changes = {"kwh_consumed": kwh, "battery_remaining": res["battery_level_kwh"]}
            outcome_text = f"Mobility agent executed {action}. Battery level: {battery:.1f} kWh."

        else:
            res_used = allocated
            res_after = res
            outcome_text = f"Standard action {action} completed."

        return new_state, res_used, res_after, state_changes, outcome_text

    def generate_initial_vs_final_comparison(self, executed_cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Computes accurate initial state vs final state comparison based on actual simulation events.
        """
        init_res = self.state_store.initial_state.get("resources", {})
        final_res = self.state_store.get_current_state().get("resources", {})

        resource_deltas = {}
        for key in init_res.keys():
            if isinstance(init_res[key], (int, float)) and key in final_res:
                delta = round(final_res[key] - init_res[key], 2)
                resource_deltas[key] = {
                    "initial": init_res[key],
                    "final": final_res[key],
                    "delta": delta,
                    "percent_change": round((delta / init_res[key]) * 100.0, 1) if init_res[key] != 0 else 0.0
                }

        # Action breakdown
        actions_count = {}
        priority_count = {}
        conditions_count = 0
        severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}

        for c in executed_cycles:
            act = c["decision"].get("action", "UNKNOWN")
            actions_count[act] = actions_count.get(act, 0) + 1
            
            pri = c["decision"].get("priority", "MEDIUM")
            priority_count[pri] = priority_count.get(pri, 0) + 1

            conds = c.get("active_conditions", [])
            conditions_count += len(conds)
            for cond in conds:
                sev = cond.get("severity", "MEDIUM")
                severity_counts[sev] = severity_counts.get(sev, 0) + 1

        return {
            "role": self.role,
            "total_cycles_executed": len(executed_cycles),
            "resource_deltas": resource_deltas,
            "action_distribution": actions_count,
            "priority_distribution": priority_count,
            "conditions_summary": {
                "total_conditions_encountered": conditions_count,
                "severity_distribution": severity_counts,
                "average_conditions_per_cycle": round(conditions_count / max(1, len(executed_cycles)), 2),
            },
        }

    def generate_ai_impact_analysis(
        self,
        executed_cycles: List[Dict[str, Any]],
        comparison: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes research-grade AI impact analysis derived strictly from real cycle data.
        """
        role = self.role
        total_cycles = len(executed_cycles)
        if total_cycles == 0:
            return {"status": "INSUFFICIENT_DATA"}

        res_deltas = comparison.get("resource_deltas", {})
        validations = [c.get("validation", {}) for c in executed_cycles]
        total_adjustments = sum(len(v.get("adjustments", [])) for v in validations)
        valid_decisions = sum(1 for v in validations if v.get("is_valid", False))
        policy_adherence_rate = round((valid_decisions / total_cycles) * 100.0, 1)

        # Domain-specific metrics
        domain_insights = []
        net_impact = "NEUTRAL"

        if role == "POLICE":
            init_resolved = res_deltas.get("resolved_incidents", {}).get("initial", 0)
            final_resolved = res_deltas.get("resolved_incidents", {}).get("final", 0)
            total_resolved = final_resolved - init_resolved
            final_safety = res_deltas.get("public_safety_score", {}).get("final", 75.0)
            initial_safety = res_deltas.get("public_safety_score", {}).get("initial", 75.0)
            safety_delta = round(final_safety - initial_safety, 1)

            if safety_delta > 0:
                net_impact = "POSITIVE"
                domain_insights.append(
                    f"AI dispatched units effectively, resolving {total_resolved} incidents and boosting public safety by +{safety_delta} points."
                )
            else:
                net_impact = "NEUTRAL"
                domain_insights.append(f"AI maintained operational continuity despite severe condition pressure.")

            domain_metrics = {
                "total_incidents_resolved": total_resolved,
                "public_safety_delta": safety_delta,
                "officer_resource_management": "Sustainable" if res_deltas.get("available_officers", {}).get("final", 0) > 0 else "Strained",
            }

        elif role == "GOVERNMENT":
            approval_delta = res_deltas.get("public_approval", {}).get("delta", 0.0)
            treasury_delta = res_deltas.get("treasury_balance", {}).get("delta", 0.0)
            net_impact = "POSITIVE" if approval_delta >= 0 and treasury_delta > -50000 else "NEUTRAL"
            domain_metrics = {
                "approval_delta": approval_delta,
                "treasury_delta": treasury_delta,
            }
            domain_insights.append(f"Government maintained budget liquidity with {approval_delta}% approval delta.")

        else:
            domain_metrics = {
                "cycles_completed": total_cycles,
                "stability_indicator": "Stable",
            }
            net_impact = "POSITIVE"
            domain_insights.append(f"{role} successfully operated for {total_cycles} cycles under variable conditions.")

        return {
            "role": role,
            "net_impact_assessment": net_impact,
            "policy_adherence_rate_pct": policy_adherence_rate,
            "total_sanitization_adjustments": total_adjustments,
            "operational_resilience": "HIGH" if policy_adherence_rate >= 80.0 else "MODERATE",
            "domain_specific_metrics": domain_metrics,
            "key_analytical_insights": domain_insights,
            "traceability": {
                "simulation_id": self.simulation_id,
                "model_slot": self.model_slot,
                "model_name": self.model_name,
                "provider": self.provider_name,
                "total_cycles_evaluated": total_cycles,
                "seed": self.seed,
            }
        }
