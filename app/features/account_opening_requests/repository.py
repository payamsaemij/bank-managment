
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.account_opening_requests.models import AccountOpeningRequest
from app.features.branches.models import Branch

def get_branch_by_id(db: Session, branch_id: int) -> Branch | None:
    statement = select(Branch).where(Branch.id == branch_id)
    return db.scalar(statement)


def create_account_opening_request(
    db: Session,
    request: AccountOpeningRequest,
) -> AccountOpeningRequest:
    db.add(request)
    db.flush()
    return request
