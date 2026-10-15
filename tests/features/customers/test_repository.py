
from unittest.mock import Mock, patch

from app.features.customers import repository
from app.features.customers.models import Customer
from app.features.persons.models import Person


def test_get_person_by_email_found():
    db = Mock()
    expected_person = Mock(spec=Person)

    with patch.object(
        repository,
        "select",
    ) as mock_select:
        statement = mock_select.return_value.where.return_value
        db.scalar.return_value = expected_person

        result = repository.get_person_by_email(
            db=db,
            email="ali@example.com",
        )

    assert result is expected_person
    db.scalar.assert_called_once_with(statement=statement)


def test_get_person_by_email_not_found():
    db = Mock()
    db.scalar.return_value = None

    result = repository.get_person_by_email(
        db=db,
        email="missing@example.com",
    )

    assert result is None


def test_get_customer_by_id_found():
    db = Mock()
    expected_customer = Mock(spec=Customer)

    with (
        patch.object(repository, "select") as mock_select,
        patch.object(repository, "selectinload") as mock_selectinload,
    ):
        statement = mock_select.return_value
        statement.options.return_value.where.return_value = statement
        db.scalar.return_value = expected_customer

        result = repository.get_customer_by_id(
            db=db,
            customer_id=10,
        )

    assert result is expected_customer
    mock_selectinload.assert_called_once_with(Customer.person)
    db.scalar.assert_called_once_with(statement=statement)


def test_get_customer_by_id_not_found():
    db = Mock()
    db.scalar.return_value = None

    result = repository.get_customer_by_id(
        db=db,
        customer_id=999,
    )

    assert result is None


def test_create_person():
    db = Mock()
    person = Mock(spec=Person)

    result = repository.create_person(
        db=db,
        person=person,
    )

    db.add.assert_called_once_with(person)
    db.flush.assert_called_once_with()
    assert result is person


def test_create_customer():
    db = Mock()
    customer = Mock(spec=Customer)

    result = repository.create_customer(
        db=db,
        customer=customer,
    )

    db.add.assert_called_once_with(customer)
    db.flush.assert_called_once_with()
    assert result is customer
