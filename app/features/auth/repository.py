
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.persons.models import Person


def get_person_by_email(db: Session, email: str) -> Person | None:
    statement = select(Person).where(Person.email == email)
    return db.scalar(statement)

def get_person_by_id(db: Session, person_id: int) -> Person | None:
    return db.get(Person, person_id)

