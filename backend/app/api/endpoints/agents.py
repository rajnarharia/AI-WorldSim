from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import models, database
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

router = APIRouter()

class AgentBase(BaseModel):
    name: str
    model_type: Optional[str] = "Model A"
    personality: Optional[str] = "BALANCED"
    age: int = 25
    money: float = 1000.0
    health: float = 100.0
    energy: float = 100.0
    education_level: int = 1
    need_social: float = 50.0
    need_financial: float = 50.0

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    current_location_id: Optional[int] = None
    job_id: Optional[int] = None

@router.get("/", response_model=List[AgentResponse])
def get_agents(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 100):
    return db.query(models.Agent).offset(skip).limit(limit).all()

@router.post("/", response_model=AgentResponse)
def create_agent(agent: AgentCreate, db: Session = Depends(database.get_db)):
    db_agent = models.Agent(**agent.model_dump())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(database.get_db)):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent
