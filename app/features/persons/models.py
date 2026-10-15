from datetime import date, datetime
from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    String,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Person(Base):
    __tablename__ = "persons"

    __table_args__ = (
        UniqueConstraint("email", name="uq_persons_email"),
        CheckConstraint(
            "length(email) > 0",
            name="ck_person_email_not_empty",
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    birth_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(225),
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(225),
        nullable=False
    )

    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    customer: Mapped["Customer | None"] = relationship(
        back_populates= "person",
        uselist=False,
    )

    employee: Mapped["Employee | None"] = relationship(
        back_populates="person",
        uselist=False,
    )
