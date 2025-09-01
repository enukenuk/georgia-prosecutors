from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.person import Person
from ..models.county import County

class PersonService:
    def __init__(self, db: Session):
        self.db = db

    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        return self.db.query(Person).options(
            joinedload(Person.addresses),
            joinedload(Person.counties)
        ).filter(Person.id == person_id).first()

    def get_people_by_county(self, county_id: str) -> List[Person]:
        return self.db.query(Person).join(
            Person.counties
        ).filter(County.county_id == county_id).all()

    def search_people_by_name(self, name: str) -> List[Person]:
        return self.db.query(Person).filter(
            Person.name.ilike(f"%{name}%")
        ).all()