"""
Human review API tests for ClaimAssist.

These tests verify that human-in-the-loop review actions update stored
claims and create traceable review outcomes.
"""
from app.database.models import Claim

from sqlalchemy import select

from app.database.models import AuditLog

def test_submit_human_review_returns_review_status(client) -> None:
    """
    Verify that a human review action updates an existing claim.

    Current behavior:
    - Creates a claim decision first.
    - Submits a human review action for that saved claim.
    - Confirms the review status is returned.

    Future production behavior:
    - Confirm human review audit logs are persisted.
    - Confirm reviewer identity and permissions are enforced.
    """

    claim_payload = {
        "claimant_name": "Jane Doe",
        "claim_type": "workers_compensation",
        "date_of_loss": "2026-07-02",
        "incident_description": (
            "Employee reported severe lower back pain and possible surgery "
            "after lifting inventory boxes."
        ),
    }

    claim_response = client.post("/claims/decision", json=claim_payload)
    claim_data = claim_response.json()
    claim_id = claim_data["claim_id"]

    review_payload = {
        "action": "escalate",
        "reviewer_notes": "High-risk claim needs supervisor review.",
    }

    response = client.post(
        f"/claims/{claim_id}/human-review",
        json=review_payload,
    )
    data = response.json()

    assert response.status_code == 200
    assert data["claim_id"] == claim_id
    assert data["action"] == "escalate"
    assert data["status"] == "escalated_to_supervisor"
    assert data["reviewer_notes"] == "High-risk claim needs supervisor review."
    
def test_human_review_updates_claim_status_in_database(client, db_session,) -> None:
    """
    Verify that a human review action updates the stored claim status.
    """

    claim_payload = {
        "claimant_name": "Jane Doe",
        "claim_type": "workers_compensation",
        "date_of_loss": "2026-07-02",
        "incident_description": (
            "Employee reported severe injury and possible surgery "
            "after a workplace incident."
        ),
    }

    claim_response = client.post("/claims/decision", json=claim_payload)
    claim_id = claim_response.json()["claim_id"]

    review_payload = {
        "action": "approve",
        "reviewer_notes": "Reviewed and approved by examiner.",
    }

    response = client.post(
        f"/claims/{claim_id}/human-review",
        json=review_payload,
    )

    saved_claim = db_session.get(Claim, claim_id)

    assert response.status_code == 200
    assert saved_claim is not None
    assert saved_claim.status == "human_review_approved"
    
def test_human_review_creates_audit_log(client,db_session,) -> None:
    """
    Verify that a human review action creates a PostgreSQL audit log.
    """

    claim_payload = {
        "claimant_name": "Jane Doe",
        "claim_type": "workers_compensation",
        "date_of_loss": "2026-07-02",
        "incident_description": (
            "Employee reported severe injury and possible surgery "
            "after a workplace incident."
        ),
    }

    claim_response = client.post("/claims/decision", json=claim_payload)
    claim_id = claim_response.json()["claim_id"]

    review_payload = {
        "action": "escalate",
        "reviewer_notes": "Escalated for supervisor review.",
    }

    response = client.post(
        f"/claims/{claim_id}/human-review",
        json=review_payload,
    )

    audit_log = db_session.execute(
        select(AuditLog).where(
            AuditLog.claim_id == claim_id,
            AuditLog.event_type == "human_review_recorded",
        )
    ).scalar_one_or_none()

    assert response.status_code == 200
    assert audit_log is not None
    assert audit_log.details["action"] == "escalate"
    assert audit_log.details["status"] == "escalated_to_supervisor"
    assert audit_log.details["reviewer_notes"] == "Escalated for supervisor review."