
import enum
from datetime import datetime
from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger
from app.db.base import Base
from app.features.accounts.models import AccountType


class AccountOpeningRequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AccountOpeningRequest(Base):
    __tablename__ = "account_opening_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    account_type: Mapped[AccountType] = mapped_column(
        Enum(
            AccountType,
            name="account_type_enum",
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
            create_type=False,
        ),
        nullable=False,
    )

    initial_deposit_amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
)

    status: Mapped[AccountOpeningRequestStatus] = mapped_column(
        Enum(
            AccountOpeningRequestStatus,
            name="account_opening_request_status_enum",
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
        ),
        nullable=False,
        default=AccountOpeningRequestStatus.PENDING,
        server_default="pending",
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    reviewed_by: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    customer = relationship("Customer")
    branch = relationship("Branch")
    reviewer = relationship("Employee")
