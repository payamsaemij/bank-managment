from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.features.customers.schemas import CustomerCreate, CustomerResponse
from app.features.customers import service


router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
)

@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def register_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.register_customer(db=db, data=data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc