from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import models, database
from pydantic import BaseModel
from typing import List

router = APIRouter()

class LocationBase(BaseModel):
    name: str
    type: str
    x: int = 0
    y: int = 0
    capacity: int = 10

class LocationCreate(LocationBase):
    pass

class LocationResponse(LocationBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

@router.get("/", response_model=List[LocationResponse])
def get_locations(db: Session = Depends(database.get_db)):
    return db.query(models.Location).all()

@router.post("/", response_model=LocationResponse)
def create_location(location: LocationCreate, db: Session = Depends(database.get_db)):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location
