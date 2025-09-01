from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"))
    street_address = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    person = relationship("Person", back_populates="addresses")