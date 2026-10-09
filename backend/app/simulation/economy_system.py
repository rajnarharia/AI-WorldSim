from sqlalchemy.orm import Session
from app.database.models import Agent, Business, Job, Product, Transaction, EventLog
import json

class EconomySystem:
    def __init__(self, db: Session, run_id: int, tick: int, day: int):
        self.db = db
        self.run_id = run_id
        self.tick = tick
        self.day = day

    def process_salaries(self):
        # Called every X days
        jobs = self.db.query(Job).filter(Job.employee_id != None).all()
        for job in jobs:
            employee = self.db.query(Agent).filter(Agent.id == job.employee_id).first()
            business = self.db.query(Business).filter(Business.id == job.business_id).first()
            
            if employee and business and business.balance >= job.salary:
                # Pay salary
                business.balance -= job.salary
                employee.money += job.salary
                business.expenses += job.salary
                
                # Create transaction
                t = Transaction(
                    tick=self.tick,
                    sender_id=None,
                    receiver_id=employee.id,
                    business_id=business.id,
                    amount=job.salary,
                    transaction_type="SALARY",
                    description=f"Salary from {business.name}"
                )
                self.db.add(t)
                
                # Event
                log = EventLog(
                    run_id=self.run_id, tick=self.tick, simulation_day=self.day,
                    agent_id=employee.id, agent_model=employee.model_type, event_type="SALARY_PAID", action="SALARY",
                    outcome=f"Received salary {job.salary} from {business.name}"
                )
                self.db.add(log)
                
                # Phase 8: Cross Model Interaction Logging
                if business.owner_id:
                    owner = self.db.query(Agent).filter(Agent.id == business.owner_id).first()
                    if owner:
                        from app.database.models import CrossModelInteraction, ExperimentRun
                        exp_run = self.db.query(ExperimentRun).filter(ExperimentRun.id == self.run_id).first()
                        if exp_run:
                            cmi = CrossModelInteraction(
                                experiment_id=exp_run.experiment_id,
                                source_agent_id=owner.id, source_model_id=owner.model_type,
                                target_agent_id=employee.id, target_model_id=employee.model_type,
                                interaction_type="PAY_SALARY", success=True
                            )
                            self.db.add(cmi)
                
                # Financial need decreases
                employee.need_financial = max(0.0, employee.need_financial - 40.0)
                
    def buy_product(self, agent: Agent, product_id: int) -> bool:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product or product.stock <= 0 or agent.money < product.price:
            return False
            
        business = self.db.query(Business).filter(Business.id == product.business_id).first()
        
        agent.money -= product.price
        business.balance += product.price
        business.revenue += product.price
        product.stock -= 1
        
        t = Transaction(
            tick=self.tick, sender_id=agent.id, business_id=business.id,
            amount=product.price, transaction_type="PURCHASE", description=f"Bought {product.name}"
        )
        self.db.add(t)
        
        log = EventLog(
            run_id=self.run_id, tick=self.tick, simulation_day=self.day,
            agent_id=agent.id, agent_model=agent.model_type, event_type="PRODUCT_PURCHASED", action="BUY_PRODUCT",
            outcome=f"Purchased {product.name} for {product.price}"
        )
        self.db.add(log)
        
        # Phase 8: Cross Model Interaction Logging
        if business.owner_id:
            owner = self.db.query(Agent).filter(Agent.id == business.owner_id).first()
            if owner:
                from app.database.models import CrossModelInteraction, ExperimentRun
                exp_run = self.db.query(ExperimentRun).filter(ExperimentRun.id == self.run_id).first()
                if exp_run:
                    cmi = CrossModelInteraction(
                        experiment_id=exp_run.experiment_id,
                        source_agent_id=agent.id, source_model_id=agent.model_type,
                        target_agent_id=owner.id, target_model_id=owner.model_type,
                        interaction_type="BUY_PRODUCT", success=True
                    )
                    self.db.add(cmi)
        
        # Check if business should hire
        if business.revenue > 1000 and self.db.query(Job).filter(Job.business_id == business.id, Job.employee_id == None).count() == 0:
            new_job = Job(title="Worker", business_id=business.id, salary=100.0, required_education=1)
            self.db.add(new_job)
            b_log = EventLog(run_id=self.run_id, tick=self.tick, simulation_day=self.day, event_type="BUSINESS_HIRED", action="CREATE_JOB", outcome=f"Business {business.name} created new job opening")
            self.db.add(b_log)
            
        return True

    def assign_job(self, agent: Agent, job_id: int) -> bool:
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job or job.employee_id is not None:
            return False
            
        # Check eligibility
        if agent.education_level < job.required_education:
            return False
            
        if job.required_skills:
            try:
                req_skills = json.loads(job.required_skills)
                agent_skills = json.loads(agent.skills) if agent.skills else {}
                for sk, lvl in req_skills.items():
                    if agent_skills.get(sk, 0) < lvl:
                        return False
            except:
                pass
                
        # Assign
        job.employee_id = agent.id
        agent.job_id = job.id
        
        log = EventLog(
            run_id=self.run_id, tick=self.tick, simulation_day=self.day,
            agent_id=agent.id, agent_model=agent.model_type, event_type="JOB_ASSIGNED", action="HIRED",
            outcome=f"Hired for {job.title}"
        )
        self.db.add(log)
        return True
