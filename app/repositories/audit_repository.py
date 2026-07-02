"""
Audit repository for ClaimAssistant.

This module contains database access functions for audit log records.

Current behavior:
- Converts structured audit event dictionaries into AuditLog model objects.
- Provides a reusable function for saving audit events through SQLAlchemy.

Future production behavior:
- Persist every workflow, agent, tool, and human-review event to PostgreSQL.
- Support compliance review, debugging, traceability, and model governance.
- Link audit events to claim records and workflow execution IDs.
"""

from typing import Any

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.database.models import AuditLog


def create_audit_log_record(
    db: Session,
    audit_event: dict[str, Any],
) -> AuditLog:
    """
    Persist a structured audit event as an AuditLog database record.

    Args:
        db: Active SQLAlchemy database session.
        audit_event: Structured audit event created by audit_service.py.

    Returns:
        The saved AuditLog database model.

    Current behavior:
    - Reads claim_id, event_type, and details from the audit event.
    - Creates an AuditLog SQLAlchemy model.
    - Adds the audit log to the active database session.
    - Commits the database transaction.
    - Refreshes the model after commit.

    Future production behavior:
    - This function will be called after each agent or tool execution.
    - Audit records will be persisted to the PostgreSQL audit_logs table.
    - The audit trail will help explain what the AI system did and why.
    """

    audit_log = AuditLog(
        claim_id=audit_event["claim_id"],
        event_type=audit_event["event_type"],
        details=audit_event["details"],
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log

def get_audit_logs_by_claim_id(
    db: Session,
    claim_id: str,
) -> list[AuditLog]:
    """
    Retrieve audit logs for one claim.

    Args:
        db: Active SQLAlchemy database session.
        claim_id: Claim identifier used to filter audit logs.

    Returns:
        A list of AuditLog records linked to the claim.

    Current behavior:
    - Queries PostgreSQL for audit logs matching the claim ID.
    - Orders results from oldest to newest.

    Future production behavior:
    - Support pagination for large audit histories.
    - Filter by agent, tool, event type, or workflow run ID.
    - Return a full examiner-facing workflow timeline.
    """

    statement = (
        select(AuditLog)
        .where(AuditLog.claim_id == claim_id)
        .order_by(AuditLog.created_at.asc())
    )

    return list(db.scalars(statement).all())