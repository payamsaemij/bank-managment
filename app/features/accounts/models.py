
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
from app.db.base import Base


class AccountType(str, enum.Enum):
    CHECKING = "checking"
    SAVINGS = "savings"


class AccountStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    BLOCKED = "blocked"
    CLOSED = "closed"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    account_type: Mapped[AccountType] = mapped_column(
        Enum(
            AccountType,
            name="account_type_enum",
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
        ),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="IRR",
        server_default="IRR",

    )

    status: Mapped[AccountStatus] = mapped_column(
        Enum(
            AccountStatus,
            name="account_status_enum",
            values_callable=lambda enum_cls: [
                item.value for item in enum_cls
            ],
        ),
        nullable=False,
        default=AccountStatus.PENDING,
        server_default="pending",
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    customer_accounts = relationship(
        "CustomerAccount",
        back_populates="account",
    )
