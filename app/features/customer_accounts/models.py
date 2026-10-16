
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CustomerAccount(Base):
    __tablename__ = "customer_accounts"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="RESTRICT"),
        primary_key=True,
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        primary_key=True,
    )

    ownership_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    linked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    customer = relationship(
        "Customer",
        back_populates="customer_accounts",
    )

    account = relationship(
        "Account",
        back_populates="customer_accounts",
    )
