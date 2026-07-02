"""
Database-backed API tests for ClaimAssist claim decisions.

These tests verify that the decision endpoint can run the workflow,
persist claim decisions, and return structured outputs.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_claim_decision_returns_workflow_output(client) -> None:
    """
    Verify that the decision endpoint returns workflow results.
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