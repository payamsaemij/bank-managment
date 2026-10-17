
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_customer
from app.db.session import get_db
from app.features.customers.models import Customer
from app.features.account_opening_requests import service
from app.features.account_opening_requests.schemas import (
    AccountOpeningRequestCreate,
    AccountOpeningRequestResponse,
)


router = APIRouter(
    prefix="/customer/account-opening-requests",
    tags=["Account Opening Requests"],
)


@router.post(
    "/",
    response_model=AccountOpeningRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_account_opening_request(
    data: AccountOpeningRequestCreate,
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer),
) -> AccountOpeningRequestResponse:
    try:
        request = service.create_account_opening_request(
            db=db,
            customer_id=current_customer.id,
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return request
