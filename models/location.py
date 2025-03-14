from sqlalchemy import Column, Integer, String, Float
from database.database import Base

class Location(Base):
    """SQLAlchemy model for location data"""
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
