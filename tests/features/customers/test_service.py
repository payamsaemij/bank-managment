
from unittest.mock import Mock, patch
from app.features.customers import service
from app.features.customers.models import Customer
from app.features.customers.schemas import CustomerCreate
from app.features.persons.models import Person


def test_register_customer_success():
    db = Mock()

    data = CustomerCreate(
        first_name="Ali",
        last_name="Ahmadi",
        birth_date=None,
        email="ali@example.com",
        password="StrongPass123",
    )

    with (
        patch.object(
            service.repository,
            "get_person_by_email",
            return_value=None,
        ),
        patch.object(
            service,
            "hash_password",
            return_value="hashed_password",
        ),
        patch.object(
            service.repository,
            "create_person",
            side_effect=lambda db, person: person,
        ) as mock_create_person,
        patch.object(
            service.repository,
            "create_customer",
            side_effect=lambda db, customer: customer,
        ) as mock_create_customer,
    ):
        result = service.register_customer(db=db, data=data)

    assert isinstance(result, Customer)
    assert result.id == mock_create_person.call_args.kwargs["person"].id

    created_person = mock_create_person.call_args.kwargs["person"]
    assert isinstance(created_person, Person)
    assert created_person.email == "ali@example.com"
    assert created_person.password_hash == "hashed_password"

    mock_create_customer.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)
    db.rollback.assert_not_called()
