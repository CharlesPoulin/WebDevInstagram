"""Pytest configuration and fixtures.

This module provides shared test fixtures including the FastAPI test client
with proper database isolation for integration tests.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.adapters.outbound.persistence.database import get_db
from src.adapters.outbound.persistence.models import Base
from src.application.config import settings
from src.main import app

# Use the same PostgreSQL database from settings for testing
TEST_DATABASE_URL = settings.DATABASE_URL

test_engine = create_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db() -> Generator[Session]:
    """Override database dependency for testing."""
    db = TestSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_database() -> Generator[None]:
    """Create fresh database tables before each test and drop after."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop all tables after test to ensure clean state
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client() -> Generator[TestClient]:
    """Provide a test client with database dependency overridden."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
