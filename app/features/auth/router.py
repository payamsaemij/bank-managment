
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_person
from app.db.session import get_db
from app.features.auth import service
from app.features.auth.schemas import LoginRequest, TokenResponse
from app.features.persons.models import Person


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    try:
        access_token = service.login(db=db, data=data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return TokenResponse(access_token=access_token)


@router.get("/me")
def get_me(
    current_person: Person = Depends(get_current_person),
) -> dict:
    return {
        "id": current_person.id,
        "email": current_person.email,
    }
