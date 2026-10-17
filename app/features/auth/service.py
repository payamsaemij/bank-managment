
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.features.auth import repository
from app.features.auth.schemas import LoginRequest


def login(db: Session, data: LoginRequest) -> str:
    person = repository.get_person_by_email(
        db=db,
        email=str(data.email),
    )

    if person is None:
        raise ValueError("Invalid email or password.")

    if not verify_password(data.password, person.password_hash):
        raise ValueError("Invalid email or password.")

    return create_access_token(subject=str(person.id))
