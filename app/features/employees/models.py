from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        primary_key=True,
    )

    employee_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    person: Mapped["Person"] = relationship(
        back_populates="employee",
    )