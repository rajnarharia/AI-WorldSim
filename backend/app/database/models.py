from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model_type = Column(String)  # Model A, Model B, Model C
    personality = Column(String) # JSON or simple string
    age = Column(Integer, default=25)
    money = Column(Float, default=1000.0)
    health = Column(Float, default=100.0)
    energy = Column(Float, default=100.0)
    # Education & Skills
    education_level = Column(Integer, default=1)
    education_progress = Column(Float, default=0.0)
    skills = Column(String, nullable=True) # JSON dict {"programming": 50}
    
    # Needs (0 to 100)
    need_social = Column(Float, default=50.0)
    need_financial = Column(Float, default=50.0)
    
    # Goals (JSON strings)
    short_term_goals = Column(String, nullable=True)
    long_term_goals = Column(String, nullable=True)
    
    current_location_id = Column(Integer, ForeignKey("locations.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    
    # Relationships
    location = relationship("Location")
    job = relationship("Job", foreign_keys=[job_id])
    memories = relationship("AgentMemory", back_populates="agent")
    decisions = relationship("DecisionHistory", back_populates="agent")

class AgentMemory(Base):
    __tablename__ = "agent_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    tick = Column(Integer)
    memory_type = Column(String) # SHORT_TERM, LONG_TERM, RELATIONSHIP, EVENT, PREFERENCE
    memory_text = Column(String)
    importance = Column(Float, default=1.0)
    
    agent = relationship("Agent", back_populates="memories")

class DecisionHistory(Base):
    __tablename__ = "decision_history"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    tick = Column(Integer)
    simulation_time_str = Column(String)
    observation_summary = Column(String)
    selected_action = Column(String)
    target = Column(String, nullable=True)
    reason = Column(String)
    model_type = Column(String)
    result = Column(String)
    
    agent = relationship("Agent", back_populates="decisions")

class Relationship(Base):
    __tablename__ = "relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id_1 = Column(Integer, ForeignKey("agents.id"))
    agent_id_2 = Column(Integer, ForeignKey("agents.id"))
    trust = Column(Float, default=0.5)
    interaction_count = Column(Integer, default=0)
    cooperation_score = Column(Float, default=0.5)
    relationship_type = Column(String, default="NEUTRAL") # FRIEND, FAMILY, COLLEAGUE, NEUTRAL, CONFLICT

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String) # RESIDENTIAL, WORK, HOSPITAL, SHOP, POLICE, COURT, etc.
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)
    capacity = Column(Integer, default=10)

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location_id = Column(Integer, ForeignKey("locations.id"))
    owner_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    balance = Column(Float, default=5000.0)
    revenue = Column(Float, default=0.0)
    expenses = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    
    jobs = relationship("Job", back_populates="business")
    products = relationship("Product", back_populates="business")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    salary = Column(Float)
    required_education = Column(Integer, default=1)
    required_skills = Column(String, nullable=True) # JSON dict of skill: level
    employee_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    
    business = relationship("Business", back_populates="jobs")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer, default=100)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    
    business = relationship("Business", back_populates="products")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    tick = Column(Integer)
    sender_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    amount = Column(Float)
    transaction_type = Column(String)
    description = Column(String, nullable=True)

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer)
    tick = Column(Integer)
    incident_type = Column(String) # RULE_VIOLATION, CONFLICT, ACCIDENT, PROPERTY_DISPUTE
    severity = Column(String) # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String) # REPORTED, RESPONDING, INVESTIGATING, IN_COURT, RESOLVED
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    description = Column(String)
    reporter_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    involved_agent_ids = Column(String) # JSON list of agent IDs
    
class PoliceResponse(Base):
    __tablename__ = "police_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    tick_started = Column(Integer)
    tick_completed = Column(Integer, nullable=True)
    status = Column(String) # RESPONDING, COMPLETED
    
class Investigation(Base):
    __tablename__ = "investigations"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    tick_started = Column(Integer)
    tick_completed = Column(Integer, nullable=True)
    status = Column(String) # PENDING, INVESTIGATING, REVIEWED, COMPLETED
    evidence_summary = Column(String, nullable=True)

class CourtCase(Base):
    __tablename__ = "court_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    tick_created = Column(Integer)
    status = Column(String) # CREATED, UNDER_REVIEW, DECIDED, RESOLVED
    decision = Column(String, nullable=True) # NO_VIOLATION, WARNING, FINE, MEDIATION
    resolution = Column(String, nullable=True)

class GovernmentPolicy(Base):
    __tablename__ = "government_policies"
    
    id = Column(Integer, primary_key=True, index=True)
    tax_rate = Column(Float, default=10.0)
    healthcare_budget = Column(Float, default=100000.0)
    education_budget = Column(Float, default=100000.0)
    police_effectiveness = Column(Float, default=0.8)
    public_service_level = Column(Float, default=0.75)
    government_funds = Column(Float, default=500000.0)

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    population_size = Column(Integer)
    duration_days = Column(Integer)
    runs_count = Column(Integer)
    status = Column(String, default="CREATED") # CREATED, RUNNING, COMPLETED

class ExperimentRun(Base):
    __tablename__ = "experiment_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    run_index = Column(Integer)
    seed = Column(Integer)
    status = Column(String, default="RUNNING") # RUNNING, COMPLETED

class MetricResult(Base):
    __tablename__ = "metric_results"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer) # Can be sim run or exp run
    tick = Column(Integer)
    simulation_day = Column(Integer)
    category = Column(String)
    metric_name = Column(String)
    metric_value = Column(Float)
    model_type = Column(String, nullable=True) # Used for model-specific metrics

class SimulationRun(Base):
    __tablename__ = "simulation_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    simulation_duration_ticks = Column(Integer, default=0)
    number_of_agents = Column(Integer, default=0)
    random_seed = Column(Integer, default=42)
    status = Column(String, default="CREATED") # CREATED, RUNNING, PAUSED, COMPLETED, STOPPED, FAILED

class EventLog(Base):
    __tablename__ = "event_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("simulation_runs.id"), nullable=True)
    tick = Column(Integer, index=True)
    simulation_day = Column(Integer, default=1)
    timestamp = Column(DateTime, default=datetime.utcnow)
    agent_id = Column(Integer, nullable=True)
    agent_model = Column(String, nullable=True)
    event_type = Column(String)
    action = Column(String)
    location_id = Column(Integer, nullable=True)
    reason = Column(String, nullable=True)
    outcome = Column(String, nullable=True)
    affected_agents = Column(String, nullable=True) # JSON list or comma separated
    metadata_json = Column(String, nullable=True) # JSON string
    
    run = relationship("SimulationRun")

class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    tick = Column(Integer, index=True)
    safety_score = Column(Float)
    economy_score = Column(Float)
    stability_score = Column(Float)
    cooperation_score = Column(Float)
    employment_rate = Column(Float)
    average_income = Column(Float)

class ExperimentModelAssignment(Base):
    __tablename__ = "experiment_model_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    model_id = Column(String)
    model_name = Column(String)
    agent_count = Column(Integer)
    percentage = Column(Float)

class CrossModelInteraction(Base):
    __tablename__ = "cross_model_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    source_agent_id = Column(Integer)
    source_model_id = Column(String)
    target_agent_id = Column(Integer)
    target_model_id = Column(String)
    interaction_type = Column(String)
    success = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ExperimentReport(Base):
    __tablename__ = 'experiment_reports'
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    generated_at = Column(DateTime, default=datetime.utcnow)
    report_version = Column(Integer, default=1)
    
    overview = Column(String) 
    safety_analysis = Column(String) 
    economic_analysis = Column(String) 
    social_analysis = Column(String) 
    governance_analysis = Column(String) 
    ai_behaviour_analysis = Column(String) 
    model_comparison = Column(String) 
    cross_model_analysis = Column(String) 
    important_events = Column(String) 
    findings = Column(String) 
    limitations = Column(String) 
    conclusion = Column(String)


class ModelConfiguration(Base):
    __tablename__ = "model_configurations"

    id = Column(Integer, primary_key=True, index=True)
    model_slot = Column(String, index=True)  # "Model A", "Model B", "Model C", "Single"
    provider = Column(String)                # "Google Gemini", "OpenAI-compatible", etc.
    model_name = Column(String)              # "gemini-1.5-pro", "gpt-4o", etc.
    api_key_masked = Column(String)          # Masked preview e.g. "AIZa...9xQ2", NEVER plain secret
    api_key_hash = Column(String, nullable=True) # Optional hash or identifier
    base_url = Column(String, nullable=True) # Custom endpoint URL if applicable
    connection_status = Column(String, default="Not Tested") # "Connected", "Connection Failed", "Not Tested"
    latency_ms = Column(Float, nullable=True)
    error_message = Column(String, nullable=True)
    last_tested_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ImpactSimulationRun(Base):
    __tablename__ = "impact_simulations"

    id = Column(String, primary_key=True, index=True) # UUUDString
    name = Column(String, index=True)
    role = Column(String, index=True) # POLICE, GOVERNMENT, CITIZEN, BUSINESS, CAR
    model_slot = Column(String)       # "Model A", "Single", etc.
    model_name = Column(String)
    provider = Column(String)
    seed = Column(Integer, default=42)
    total_loops = Column(Integer, default=10)
    completed_loops = Column(Integer, default=0)
    status = Column(String, default="INITIALIZED") # INITIALIZED, RUNNING, COMPLETED, PAUSED, FAILED

    initial_state_json = Column(String)  # JSON text
    final_state_json = Column(String, nullable=True) # JSON text
    comparison_json = Column(String, nullable=True) # JSON text
    impact_analysis_json = Column(String, nullable=True) # JSON text
    error_message = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cycles = relationship("SimulationCycleRecord", back_populates="simulation", cascade="all, delete-orphan")


class SimulationCycleRecord(Base):
    __tablename__ = "simulation_cycle_records"

    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(String, ForeignKey("impact_simulations.id"), index=True)
    cycle_number = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    role = Column(String)

    # State tracking
    previous_state_json = Column(String)
    current_state_json = Column(String)
    active_conditions_json = Column(String)
    prompt_text = Column(String)
    ai_decision_json = Column(String)
    validation_result_json = Column(String)
    resources_before_json = Column(String)
    resources_used_json = Column(String)
    resources_after_json = Column(String)
    state_changes_json = Column(String)
    outcomes_json = Column(String)

    simulation = relationship("ImpactSimulationRun", back_populates="cycles")
