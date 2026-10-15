from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.features.persons.models import Person
from app.features.customers.models import Customer


def get_person_by_email(
        db: Session,
        email: str,
) -> Person | None:
    statement = select(Person).where(Person.email == email)
    return db.scalar(statement=statement)

def get_customer_by_id(
        db: Session,
        customer_id: int,
) -> Customer | None:
    statement = (
        select(Customer)
        .options(selectinload(Customer.person))
        .where(Customer.id == customer_id)
    )
    return  db.scalar(statement=statement)


def create_person(
        db: Session,
        person: Person,
) -> Person:
    db.add(person)
    db.flush()
    return person


def create_customer(
        db: Session,
        customer: Customer,
) -> Customer:
    db.add(customer)
    db.flush()
    return customer