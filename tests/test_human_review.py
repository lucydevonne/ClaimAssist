"""
Human review API tests for ClaimAssist.

These tests verify that human-in-the-loop review actions update stored
claims and create traceable review outcomes.
"""


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