from sqlalchemy.orm import Session
from app.features.customers import repository
from app.features.customers.models import Customer
from app.features.customers.schemas import CustomerCreate
from app.features.persons.models import Person
from app.core.security import hash_password



def  register_customer(
        db: Session,
        data: CustomerCreate
) -> Customer:
    existing_person = repository.get_person_by_email(
        db=db,
        email=str(data.email),
    )
    if existing_person:
        raise ValueError("A person with this email already exists.")
    try:
        person = Person(
            first_name = data.first_name,
            last_name = data.last_name,
            birth_date = data.birth_date,
            email=str(data.email),
            password_hash = hash_password(data.password),
        )
        person = repository.create_person(
            db=db,
            person = person
        )
        customer = Customer(id=person.id)
        customer = repository.create_customer(
            db=db,
            customer=customer
        )
        db.commit()
        db.refresh(customer)
        return customer
    
    except Exception:
        db.rollback()
        raise
