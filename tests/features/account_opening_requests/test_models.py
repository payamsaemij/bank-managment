
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.accounts.models import AccountType
from app.features.account_opening_requests.models import (
    AccountOpeningRequest,
    AccountOpeningRequestStatus,
)
from app.features.branches.models import Branch
from app.features.customers.models import Customer
from app.features.persons.models import Person


def create_customer_and_branch(
    db_session: Session,
) -> tuple[Customer, Branch]:
    """Create the minimum data required for an account opening request."""

    person = Person(
        first_name="Test",
        last_name="Customer",
        email="test.customer@example.com",
        password_hash="test-hash",
    )
    db_session.add(person)
    db_session.flush()

    customer = Customer(id=person.id)

    branch = Branch(
        branch_code="TEST-001",
        name="Test Branch",
        address="Test Address",
    )

    db_session.add_all([customer, branch])
    db_session.flush()

    return customer, branch


def test_create_account_opening_request(db_session: Session) -> None:
    customer, branch = create_customer_and_branch(db_session)

    request = AccountOpeningRequest(
        customer_id=customer.id,
        branch_id=branch.id,
        account_type=AccountType.CHECKING,
    )

    db_session.add(request)
    db_session.flush()

    assert request.id is not None
    assert request.customer_id == customer.id
    assert request.branch_id == branch.id
    assert request.account_type == AccountType.CHECKING
    assert request.status == AccountOpeningRequestStatus.PENDING
    assert request.reviewed_by is None
    assert request.reviewed_at is None
    assert request.rejection_reason is None


def test_account_opening_request_relationships(
    db_session: Session,
) -> None:
    customer, branch = create_customer_and_branch(db_session)

    request = AccountOpeningRequest(
        customer_id=customer.id,
        branch_id=branch.id,
        account_type=AccountType.SAVINGS,
    )

    db_session.add(request)
    db_session.flush()

    saved_request = db_session.scalars(
        select(AccountOpeningRequest).where(
            AccountOpeningRequest.id == request.id
        )
    ).one()

    assert saved_request.customer.id == customer.id
    assert saved_request.branch.id == branch.id


def test_account_opening_request_rejects_invalid_customer(
    db_session: Session,
) -> None:
    _, branch = create_customer_and_branch(db_session)

    request = AccountOpeningRequest(
        customer_id=-999,
        branch_id=branch.id,
        account_type=AccountType.CHECKING,
    )

    db_session.add(request)

    with pytest.raises(IntegrityError):
        db_session.flush()

    db_session.rollback()
