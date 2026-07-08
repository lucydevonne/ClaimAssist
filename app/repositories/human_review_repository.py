"""
Human review repository for ClaimAssist.

This module contains database access functions for human review records.

Current behavior:
- Persists examiner review decisions to the human_reviews table.

Future production behavior:
- Fetch review history by claim ID.
- Store reviewer identity and role-based approval metadata.
- Support multiple review rounds per claim.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import HumanReview


def create_human_review_record(
    db: Session,
    claim_id: str,
    action: str,
    status: str,
    reviewer_notes: str,
) -> HumanReview:
    """
    Persist a human review decision as a HumanReview database record.

    Args:
        db: Active SQLAlchemy database session.
        claim_id: Claim identifier linked to the review.
        action: Reviewer action (approve, reject, escalate).
        status: Updated claim status after the review.
        reviewer_notes: Examiner notes explaining the decision.

    Returns:
        The saved HumanReview database model.
    """

    human_review = HumanReview(
        claim_id=claim_id,
        action=action,
        status=status,
        reviewer_notes=reviewer_notes,
    )

    db.add(human_review)
    db.commit()
    db.refresh(human_review)

    return human_review


def get_human_reviews_by_claim_id(
    db: Session,
    claim_id: str,
) -> list[HumanReview]:
    """
    Retrieve human review records for one claim.

    Args:
        db: Active SQLAlchemy database session.
        claim_id: Claim identifier used to filter reviews.

    Returns:
        A list of HumanReview records linked to the claim.
    """

    statement = (
        select(HumanReview)
        .where(HumanReview.claim_id == claim_id)
        .order_by(HumanReview.created_at.asc())
    )

    return list(db.scalars(statement).all())