"""
Database session configuration for ClaimAssistant.

This module defines the SQLAlchemy database engine and session factory.

Current behavior:
- Reads the database URL from the centralized settings object.
- Creates a SQLAlchemy engine.
- Creates a reusable session factory.
- Provides a database session generator for future API/service use.

Future production behavior:
- Connect to PostgreSQL using environment-specific DATABASE_URL values.
- Persist claims, audit logs, workflow state, and agent outputs.
- Use this session layer inside services and repositories.
- Support migrations through Alembic.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db_session() -> Generator[Session, None, None]:
    """
    Provide a database session for one unit of work.

    Yields:
        A SQLAlchemy Session connected to the configured database.

    Current behavior:
    - Opens a database session.
    - Yields it to the caller.
    - Closes it after the caller finishes.

    Future production behavior:
    - This will be used as a FastAPI dependency.
    - API routes or services will receive a database session through dependency injection.
    - Claim and audit data will be persisted to PostgreSQL through this session.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()