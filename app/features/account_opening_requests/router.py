from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
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
):
    try:
        # Authentication dependency will supply customer_id next.
        raise NotImplementedError("Customer authentication is'nt implemented.")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
