from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Laptop(Base):
    __tablename__ = "laptops"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    brand = Column(String, index=True)
    price = Column(Float)
    ram_gb = Column(Integer)
    ssd_gb = Column(Integer)
    spec_score = Column(Integer)
    no_of_cores = Column(Integer)
    is_used = Column(Boolean, default=False)
    # used_price is synthetic or real depending on availability
    used_price = Column(Float, nullable=True) 
