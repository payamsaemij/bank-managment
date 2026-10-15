
import pytest
from pydantic import ValidationError

from app.features.customers.schemas import CustomerCreate


def test_customer_create_with_valid_data():
    customer = CustomerCreate(
        first_name="Ali",
        last_name="Ahmadi",
        email="ali@example.com",
        password="StrongPass123",
    )

    assert customer.first_name == "Ali"
    assert customer.email == "ali@example.com"
    assert customer.birth_date is None


def test_customer_create_rejects_invalid_email():
    with pytest.raises(ValidationError):
        CustomerCreate(
            first_name="Ali",
            last_name="Ahmadi",
            email="invalid-email",
            password="StrongPass123",
        )


def test_customer_create_rejects_short_password():
    with pytest.raises(ValidationError):
        CustomerCreate(
            first_name="Ali",
            last_name="Ahmadi",
            email="ali@example.com",
            password="123",
        )
