"""
Human review API tests for ClaimAssist.

These tests verify that human-in-the-loop review actions return
structured responses.
"""


def test_submit_human_review_returns_review_status(client) -> None:
    """
    Verify that a human review action returns an updated review status.
    """

    payload = {
        "action": "escalate",
        "reviewer_notes": "High-risk claim needs supervisor review.",
    }

    response = client.post("/claims/CLM-TEST123/human-review", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["claim_id"] == "CLM-TEST123"
    assert data["action"] == "escalate"
    assert data["status"] == "escalated_to_supervisor"
    assert data["reviewer_notes"] == "High-risk claim needs supervisor review."