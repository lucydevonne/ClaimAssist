"""
Shared pytest configuration for ClaimAssist.

This file defines reusable test fixtures.

Current behavior:
- Creates a test database engine.
- Creates database tables before tests run.
- Overrides the FastAPI database dependency so tests use claimassist_test.

Future production behavior:
- Use transaction rollback fixtures for faster isolated tests.
- Add seed data for claims, audit logs, policy documents, and agent workflows.
- Run test database setup automatically in CI/CD.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings
from app.database.models import Base
from app.database.session import get_db_session
from app.main import app


test_engine = create_engine(
    settings.test_database_url,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """
    Create a clean database session for one test.

    Current behavior:
    - Creates all database tables in the test database.
    - Opens a test database session.
    - Drops all database tables after the test finishes.

    Future production behavior:
    - Replace table drop/create with transaction rollback for speed.
    - Support parallel test execution.
    """

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a FastAPI test client using the test database session.

    Current behavior:
    - Overrides get_db_session so API tests use claimassist_test.
    - Clears dependency overrides after the test finishes.

    Future production behavior:
    - Add authentication overrides for examiner/admin test users.
    """

    def override_get_db_session() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()