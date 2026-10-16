
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import pytest
from app.features.persons.models import Person
from app.features.customers.models import Customer
from app.features.branches.models import Branch
from app.features.accounts.models import Account, AccountType
from app.features.customer_accounts.models import CustomerAccount


def create_customer(db_session: Session) -> Customer:
    person = Person(
        first_name="Ali",
        last_name="Ahmadi",
        email="ali@example.com",
        password_hash="test_hash",
    )
    db_session.add(person)
    db_session.flush()

    customer = Customer(id=person.id)
    db_session.add(customer)
    db_session.flush()

    return customer


def create_account(db_session: Session) -> Account:
    branch = Branch(
        branch_code="BR_TEST",
        name="Test Branch",
        address="Tehran",
    )
    db_session.add(branch)
    db_session.flush()

    account = Account(
        account_number="ACC_TEST_001",
        branch_id=branch.id,
        account_type=AccountType.CHECKING,
    )
    db_session.add(account)
    db_session.flush()

    return account


def test_create_customer_account(db_session: Session) -> None:
    customer = create_customer(db_session)
    account = create_account(db_session)

    link = CustomerAccount(
        customer_id=customer.id,
        account_id=account.id,
        ownership_type="primary",
    )
    db_session.add(link)
    db_session.commit()
    db_session.refresh(link)

    assert link.customer_id == customer.id
    assert link.account_id == account.id
    assert link.ownership_type == "primary"
    assert link.linked_at is not None


def test_customer_account_relationships(
    db_session: Session,
) -> None:
    customer = create_customer(db_session)
    account = create_account(db_session)

    link = CustomerAccount(
        customer=customer,
        account=account,
        ownership_type="primary",
    )
    db_session.add(link)
    db_session.commit()

    assert link.customer.id == customer.id
    assert link.account.id == account.id
    assert link in customer.customer_accounts
    assert link in account.customer_accounts


def test_customer_account_pair_must_be_unique(
    db_session: Session,
) -> None:
    customer = create_customer(db_session)
    account = create_account(db_session)

    first_link = CustomerAccount(
        customer_id=customer.id,
        account_id=account.id,
        ownership_type="primary",
    )
    db_session.add(first_link)
    db_session.commit()

    duplicate_link = CustomerAccount(
        customer_id=customer.id,
        account_id=account.id,
        ownership_type="joint",
    )
    db_session.add(duplicate_link)

    try:
        with pytest.raises(IntegrityError):
            db_session.commit()
    finally:
        db_session.rollback()

    links = db_session.scalars(
        select(CustomerAccount).where(
            CustomerAccount.customer_id == customer.id,
            CustomerAccount.account_id == account.id,
        )
    ).all()

    assert len(links) == 1
