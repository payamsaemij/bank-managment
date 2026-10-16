
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import settings
import app.db.models  # noqa: F401

@pytest.fixture
def db_session() -> Session:  # type: ignore
    engine = create_engine(
        settings.test_database_url,
        pool_pre_ping=True,
    )

    connection = engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
        autoflush=False,
        expire_on_commit=False,
    )

    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()
        engine.dispose()
