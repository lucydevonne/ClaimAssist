"""
Claim repository for ClaimAssistant.

This module contains database access functions for claim records.

Current behavior:
- Defines reusable functions for creating claim model objects.
- Prepares the project for PostgreSQL persistence.

Future production behavior:
- Save submitted claims to the PostgreSQL claims table.
- Fetch claims by ID for examiner review.
- Update claim status, risk level, recommendation, and human-review flags.
- Keep database logic outside the API and service layers.
"""

from sqlalchemy.orm import Session

from app.database.models import Claim
from app.graph.state import ClaimWorkflowState


def create_claim_record(
    db: Session,
    state: ClaimWorkflowState,
) -> Claim:
    """
    Persist a claim workflow state as a database claim record.

    Args:
        db: Active SQLAlchemy database session.
        state: Current claim workflow state created by the intake agent
            and updated by workflow agents.

    Returns:
        The saved Claim database model.

    Current behavior:
    - Converts ClaimWorkflowState into a Claim SQLAlchemy model.
    - Adds the claim to the active database session.
    - Commits the transaction.
    - Refreshes the model so database-generated values are available.

    Future production behavior:
    - This function will be called after claim intake.
    - It will persist claim records to PostgreSQL.
    - It may later support retries, rollback handling, and audit correlation.
    """

    claim = Claim(
        id=state.claim_id,
        claimant_name=state.claimant_name,
        claim_type=state.claim_type.value,
        date_of_loss=state.date_of_loss,
        incident_description=state.incident_description,
        status=state.status,
        risk_level=state.risk_level,
        recommended_action=state.recommended_action,
        requires_human_review=state.requires_human_review,
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)

    return claim

def get_claim_record_by_id(
    db: Session,
    claim_id: str,
) -> Claim | None:
    """
    Retrieve one claim record by claim ID.

    Args:
        db: Active SQLAlchemy database session.
        claim_id: Primary key of the claim record.

    Returns:
        The matching Claim database model if found, otherwise None.

    Current behavior:
    - Uses SQLAlchemy Session.get() to fetch a claim by primary key.

    Future production behavior:
    - Add tenant/client-level access control.
    - Add examiner authorization checks.
    - Add related workflow state and audit log joins when needed.
    """

    return db.get(Claim, claim_id)