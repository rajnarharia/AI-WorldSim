from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base, SessionLocal
from app.api import api_router
from app.database.seeder import seed_data

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed database
db = SessionLocal()
try:
    seed_data(db)
    from app.simulation.engine import sim_engine
    sim_engine._load_world_state(db)
finally:
    db.close()

app = FastAPI(
    title="AI Real-World Simulation Platform",
    description="Multi-Agent Virtual Society for Real-World Behaviour and Safety Evaluation",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Real-World Simulation Platform API"}
