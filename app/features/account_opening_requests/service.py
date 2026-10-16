from sqlalchemy.orm import Session

from app.features.account_opening_requests import repository
from app.features.account_opening_requests.models import (
    AccountOpeningRequest,
    AccountOpeningRequestStatus,
)
from app.features.account_opening_requests.schemas import (
    AccountOpeningRequestCreate)


def create_account_opening_request(
    db: Session,
    customer_id: int,
    data: AccountOpeningRequestCreate,
) -> AccountOpeningRequest:
    branch = repository.get_branch_by_id(
        db=db,
        branch_id=data.branch_id,
    )

    if branch is None:
        raise ValueError("Branch not found.")

    request = AccountOpeningRequest(
        customer_id=customer_id,
        branch_id=data.branch_id,
        account_type=data.account_type,
        initial_deposit_amount=data.initial_deposit_amount,
        status=AccountOpeningRequestStatus.PENDING,
    )

    try:
        request = repository.create_account_opening_request(
            db=db,
            request=request,
        )
        db.commit()
        db.refresh(request)
        return request
    except Exception:
        db.rollback()
        raise
