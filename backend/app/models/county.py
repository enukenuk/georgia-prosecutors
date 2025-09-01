from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class County(Base):
    __tablename__ = "counties"

    id = Column(Integer, primary_key=True, index=True)
    county_id = Column(String(5), nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    judicial_circuit = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    people = relationship("Person", secondary="person_counties", back_populates="counties")