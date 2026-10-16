from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.features.accounts.models import AccountType
from app.features.account_opening_requests.models import (
    AccountOpeningRequestStatus,
)


class AccountOpeningRequestCreate(BaseModel):
    branch_id: int = Field(gt=0)
    account_type: AccountType
    initial_deposit_amount: int = Field(ge=0)


class AccountOpeningRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    branch_id: int
    account_type: AccountType
    initial_deposit_amount: int
    status: AccountOpeningRequestStatus
    created_at: datetime
