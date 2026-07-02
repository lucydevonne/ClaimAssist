"""
Database-backed API tests for ClaimAssist claim decisions.

These tests verify that the decision endpoint can run the workflow,
persist claim decisions, persist audit events, and return structured outputs.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import AuditLog, Claim


def test_create_claim_decision_returns_workflow_output(client) -> None:
    """
    Verify that the decision endpoint returns workflow results.

    Current behavior:
    - Sends a valid claim intake request.
    - Runs the current agent workflow.
    - Returns risk level, recommended action, and audit event data.

    Future production behavior:
    - Add assertions for policy citations, model confidence, and workflow trace IDs.
    """

    payload = {
        "claimant_name": "Jane Doe",
        "claim_type": "workers_compensation",
        "date_of_loss": "2026-07-02",
        "incident_description": (
            "Employee reported severe lower back pain after lifting inventory "
            "boxes and may need surgery."
        ),
    }

    response = client.post("/claims/decision", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["claim_id"].startswith("CLM-")
    assert data["status"] == "resolution_recommendation_completed"
    assert data["risk_level"] == "high"
    assert data["recommended_action"] == (
        "Escalate to a senior claims examiner for manual review."
    )
    assert data["requires_human_review"] is True
    assert data["audit_event"]["event_type"] == "claim_decision_generated"
    assert data["audit_event"]["claim_id"] == data["claim_id"]


def test_create_claim_decision_persists_claim_and_audit_log(
    client,
    db_session: Session,
) -> None:
    """
    Verify that the decision endpoint saves claim and audit records.

    Current behavior:
    - Calls POST /claims/decision.
    - Queries the test PostgreSQL database for the saved claim.
    - Queries the test PostgreSQL database for the saved audit log.

    Future production behavior:
    - Validate multiple audit events across every workflow node.
    - Confirm audit records include agent name, model version, and tool calls.
    """

    payload = {
        "claimant_name": "John Smith",
        "claim_type": "workers_compensation",
        "date_of_loss": "2026-07-02",
        "incident_description": (
            "Employee reported severe shoulder pain and possible surgery "
            "after a workplace lifting incident."
        ),
    }

    response = client.post("/claims/decision", json=payload)
    data = response.json()
    claim_id = data["claim_id"]

    saved_claim = db_session.get(Claim, claim_id)

    audit_statement = select(AuditLog).where(AuditLog.claim_id == claim_id)
    saved_audit_log = db_session.scalars(audit_statement).first()

    assert response.status_code == 200
    assert saved_claim is not None
    assert saved_claim.id == claim_id
    assert saved_claim.risk_level == "high"
    assert saved_claim.requires_human_review is True

    assert saved_audit_log is not None
    assert saved_audit_log.claim_id == claim_id
    assert saved_audit_log.event_type == "claim_decision_generated"