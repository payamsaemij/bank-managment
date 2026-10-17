from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from app.features.customers.models import Customer
from app.core.security import decode_access_token
from app.db.session import get_db
from app.features.auth import repository
from app.features.persons.models import Person


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_person(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Person:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized_exception

    try:
        payload = decode_access_token(credentials.credentials)
        subject = payload.get("sub")

        if not isinstance(subject, str) or not subject.isdecimal():
            raise unauthorized_exception

        person_id = int(subject)

        if person_id <= 0:
            raise unauthorized_exception

    except (InvalidTokenError, ValueError, TypeError) as exc:
        raise unauthorized_exception from exc

    person = repository.get_person_by_id(
        db=db,
        person_id=person_id,
    )

    if person is None:
        raise unauthorized_exception

    return person


def get_current_customer(
    current_person: Person = Depends(get_current_person),
    db: Session = Depends(get_db),
) -> Customer:
    customer = db.get(Customer, current_person.id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access required.",
        )

    return customer
