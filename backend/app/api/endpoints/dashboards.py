from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import database, models

router = APIRouter()

@router.get("/economy")
def get_economy_stats(db: Session = Depends(database.get_db)):
    agents = db.query(models.Agent).all()
    jobs = db.query(models.Job).all()
    businesses = db.query(models.Business).all()
    
    total_agents = len(agents)
    employed = sum(1 for a in agents if a.job_id is not None)
    employment_rate = (employed / total_agents * 100) if total_agents > 0 else 0
    
    avg_income = db.query(func.avg(models.Job.salary)).filter(models.Job.employee_id != None).scalar() or 0
    total_transactions = db.query(models.Transaction).count()
    
    return {
        "employment_rate": round(employment_rate, 2),
        "employed_count": employed,
        "avg_income": round(avg_income, 2),
        "business_count": len(businesses),
        "total_transactions": total_transactions
    }

@router.get("/education")
def get_education_stats(db: Session = Depends(database.get_db)):
    agents = db.query(models.Agent).all()
    levels = {}
    for a in agents:
        levels[a.education_level] = levels.get(a.education_level, 0) + 1
        
    return {
        "average_level": sum(a.education_level for a in agents) / len(agents) if agents else 1,
        "level_distribution": levels
    }

@router.get("/healthcare")
def get_healthcare_stats(db: Session = Depends(database.get_db)):
    agents = db.query(models.Agent).all()
    avg_health = sum(a.health for a in agents) / len(agents) if agents else 100
    sick_agents = sum(1 for a in agents if a.health < 50)
    
    hospital_visits = db.query(models.EventLog).filter(models.EventLog.action == "VISIT_HOSPITAL").count()
    
    return {
        "average_health": round(avg_health, 2),
        "sick_agents": sick_agents,
        "hospital_visits": hospital_visits
    }

@router.get("/social")
def get_social_stats(db: Session = Depends(database.get_db)):
    rels = db.query(models.Relationship).all()
    avg_trust = sum(r.trust for r in rels) / len(rels) if rels else 0
    coop_score = sum(r.cooperation_score for r in rels) / len(rels) if rels else 0
    
    return {
        "total_relationships": len(rels),
        "average_trust": round(avg_trust, 2),
        "average_cooperation": round(coop_score, 2)
    }

@router.get("/safety")
def get_safety_stats(db: Session = Depends(database.get_db)):
    incidents = db.query(models.Incident).all()
    active = sum(1 for i in incidents if i.status != "RESOLVED")
    resolved = sum(1 for i in incidents if i.status == "RESOLVED")
    
    # Calculate response times
    responses = db.query(models.PoliceResponse).filter(models.PoliceResponse.tick_completed != None).all()
    avg_resp = sum((r.tick_completed - r.tick_started) for r in responses) / len(responses) if responses else 0
    
    return {
        "total_incidents": len(incidents),
        "active_incidents": active,
        "resolved_incidents": resolved,
        "avg_response_time": round(avg_resp, 2)
    }

@router.get("/government")
def get_government_stats(db: Session = Depends(database.get_db)):
    policy = db.query(models.GovernmentPolicy).first()
    if not policy:
        return {}
    return {
        "tax_rate": policy.tax_rate,
        "healthcare_budget": policy.healthcare_budget,
        "education_budget": policy.education_budget,
        "police_effectiveness": policy.police_effectiveness,
        "public_service_level": policy.public_service_level,
        "government_funds": policy.government_funds
    }
