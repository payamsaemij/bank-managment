
from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.accounts.models import (
    Account,
    AccountStatus,
    AccountType,
)
from app.features.branches.models import Branch


def create_branch(db_session: Session) -> Branch:
    branch = Branch(
        branch_code="BR001",
        name="Main Branch",
        address="Tehran",
    )
    db_session.add(branch)
    db_session.flush()
    return branch


def test_create_account(db_session: Session) -> None:
    branch = create_branch(db_session)

    account = Account(
        account_number="ACC10001",
        branch_id=branch.id,
        account_type=AccountType.CHECKING,
    )

    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)

    assert account.id is not None
    assert account.account_number == "ACC10001"
    assert account.branch_id == branch.id
    assert account.account_type == AccountType.CHECKING


def test_account_defaults(db_session: Session) -> None:
    branch = create_branch(db_session)

    account = Account(
        account_number="ACC10002",
        branch_id=branch.id,
        account_type=AccountType.SAVINGS,
    )

    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)

    assert account.currency == "IRR"
    assert account.status == AccountStatus.PENDING
    assert isinstance(account.opened_at, datetime)


def test_account_number_must_be_unique(
    db_session: Session,
) -> None:
    branch = create_branch(db_session)

    first_account = Account(
        account_number="ACC10003",
        branch_id=branch.id,
        account_type=AccountType.CHECKING,
    )
    db_session.add(first_account)
    db_session.commit()

    second_account = Account(
        account_number="ACC10003",
        branch_id=branch.id,
        account_type=AccountType.SAVINGS,
    )
    db_session.add(second_account)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    accounts = db_session.scalars(
        select(Account).where(
            Account.account_number == "ACC10003"
        )
    ).all()

    assert len(accounts) == 1


def test_account_type_values() -> None:
    assert AccountType.CHECKING.value == "checking"
    assert AccountType.SAVINGS.value == "savings"


def test_account_status_values() -> None:
    assert AccountStatus.PENDING.value == "pending"
    assert AccountStatus.ACTIVE.value == "active"
    assert AccountStatus.BLOCKED.value == "blocked"
    assert AccountStatus.CLOSED.value == "closed"
