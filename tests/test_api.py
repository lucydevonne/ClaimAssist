"""
API tests for ClaimAssist.

These tests verify that the public FastAPI endpoints return the expected
status codes and response shapes.

Current behavior:
- Tests the health endpoint.
- Tests the claim intake endpoint.

Future production behavior:
- Add database-backed decision endpoint tests.
- Add audit log retrieval tests.
- Add test database fixtures so PostgreSQL tests do not touch local dev data.
"""




def test_health_check_returns_healthy_status(client) -> None:
    """
    Verify that the health endpoint confirms the API is running.

    This test protects the basic startup path of the FastAPI application.
    """

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "ClaimAssist",
        "version": "0.1.0",
    }


def test_create_claim_returns_intake_response(client) -> None:
    """
    Verify that claim intake returns a structured response.

    This test confirms that:
    - the API accepts a valid claim intake request
    - Pydantic validates the request body
    - the service layer returns a claim ID, status, message, and next steps
    """

    payload = {
        "claimant_name": "Jane Doe",
        "claim_type": "workers_compensation",
        "date_of_loss": "2026-07-02",
        "incident_description": (
            "Employee reported lower back pain after lifting inventory boxes "
            "during a warehouse shift."
        ),
    }

    response = client.post("/claims", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["claim_id"].startswith("CLM-")
    assert data["status"] == "resolution_recommendation_completed"
    assert data["message"] == "Claim intake received successfully."
    assert isinstance(data["next_steps"], list)
    assert len(data["next_steps"]) == 3