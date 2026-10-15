
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import get_db
from app.features.customers import service


@pytest.fixture
def client():
    def override_get_db():
        yield object()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_register_customer_success(client, monkeypatch):
    customer = SimpleNamespace(
        id=1,
        registered_at=datetime.now(timezone.utc),
        person=SimpleNamespace(
            id=1,
            first_name="Ali",
            last_name="Ahmadi",
            birth_date=None,
            email="ali@example.com",
        ),
    )

    def mock_register_customer(db, data):
        return customer

    monkeypatch.setattr(
        service,
        "register_customer",
        mock_register_customer,
    )

    response = client.post(
        "/customer/",
        json={
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "birth_date": None,
            "email": "ali@example.com",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["id"] == 1
    assert body["person"]["email"] == "ali@example.com"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_customer_duplicate_email(client, monkeypatch):
    def mock_register_customer(db, data):
        raise ValueError("A person with this email already exists.")

    monkeypatch.setattr(
        service,
        "register_customer",
        mock_register_customer,
    )

    response = client.post(
        "/customer/",
        json={
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "birth_date": None,
            "email": "ali@example.com",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "A person with this email already exists."
    )


def test_register_customer_invalid_email(client):
    response = client.post(
        "/customer/",
        json={
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "birth_date": None,
            "email": "not-an-email",
            "password": "StrongPass123",
        },
    )

    assert response.status_code == 422
