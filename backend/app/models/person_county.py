from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class PersonCounty(Base):
    __tablename__ = "person_counties"

    person_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), primary_key=True)
    county_id = Column(Integer, ForeignKey("counties.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())