from sqlalchemy.orm import Session
from app.database import models

def seed_data(db: Session):
    if db.query(models.Location).count() == 0:
        locs = [
            models.Location(name="City Park", type="RECREATION", x=10, y=10),
            models.Location(name="Central Bank", type="BANK", x=20, y=20),
            models.Location(name="Main Hospital", type="HOSPITAL", x=30, y=30),
            models.Location(name="Tech Corp", type="WORK", x=40, y=40),
            models.Location(name="Residential Area A", type="RESIDENTIAL", x=50, y=50)
        ]
        db.add_all(locs)
        db.commit()

    if db.query(models.Agent).count() == 0:
        loc = db.query(models.Location).filter(models.Location.type == "RESIDENTIAL").first()
        agents = [
            models.Agent(name="Alice", model_type="Model A", personality="Cautious", current_location_id=loc.id),
            models.Agent(name="Bob", model_type="Model B", personality="Risk-taker", current_location_id=loc.id),
            models.Agent(name="Charlie", model_type="Model C", personality="Balanced", current_location_id=loc.id),
        ]
        db.add_all(agents)
        db.commit()

    if db.query(models.Business).count() == 0:
        tech = db.query(models.Location).filter(models.Location.type == "WORK").first()
        shop_loc = db.query(models.Location).filter(models.Location.type == "RECREATION").first() # treating as shop for now
        
        b1 = models.Business(name="Tech Innovations", location_id=tech.id, balance=10000)
        b2 = models.Business(name="City Mart", location_id=shop_loc.id, balance=5000)
        db.add_all([b1, b2])
        db.commit()
        
        # Add Jobs
        j1 = models.Job(title="Software Developer", business_id=b1.id, salary=300, required_education=2)
        j2 = models.Job(title="Shop Worker", business_id=b2.id, salary=100, required_education=1)
        db.add_all([j1, j2])
        
        # Add Products
        p1 = models.Product(name="Groceries", price=20, stock=50, business_id=b2.id)
        p2 = models.Product(name="Electronics", price=150, stock=10, business_id=b2.id)
        db.add_all([p1, p2])
        db.commit()
