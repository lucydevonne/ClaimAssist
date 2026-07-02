"""
Database models for ClaimAssistant.

This module defines the SQLAlchemy ORM models that will map Python classes
to PostgreSQL tables.

Current behavior:
- Defines claim and audit log table structures only.

Future production behavior:
- These models will be used with PostgreSQL migrations.
- Claim records will be persisted when a claim is submitted.
- Audit events will be persisted every time an agent, workflow, or tool runs.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Every database model in ClaimAssistant will inherit from this class
    so SQLAlchemy can discover and map it to a database table.
    """


class Claim(Base):
    """
    Claim database model.

    Represents a submitted insurance claim.

    Future production use:
    - Store claim intake data from POST /claims.
    - Link claim records to workflow state, documents, audit logs,
      and final examiner decisions.
    """

    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"CLM-{uuid4().hex[:8].upper()}",
    )
    claimant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    claim_type: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_loss: Mapped[Date] = mapped_column(Date, nullable=False)
    incident_description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="intake_received",
    )
    risk_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    recommended_action: Mapped[str | None] = mapped_column(Text, nullable=True)
    requires_human_review: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class AuditLog(Base):
    """
    Audit log database model.

    Represents a traceable workflow, agent, or tool event.

    Future production use:
    - Store every important workflow event.
    - Record model decisions, tool calls, human review checkpoints,
      and final recommendations.
    - Support compliance, debugging, and explainability.
    """

    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"AUD-{uuid4().hex[:10].upper()}",
    )
    claim_id: Mapped[str] = mapped_column(String, nullable=False)
    event_type: Mapped[str] = mapped_column(String(150), nullable=False)
    details: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )