from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.features.persons.models import Person


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        primary_key=True,
    )

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    person: Mapped["Person"] = relationship(
        back_populates="customer",
    )

    customer_accounts = relationship(
        "CustomerAccount",
        back_populates="customer",
    )
