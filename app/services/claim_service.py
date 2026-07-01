"""
Claim service layer for ClaimAssistant.

The service layer contains business logic for claim operations.
API routes should call this layer instead of handling business logic directly.
"""

from uuid import uuid4

from app.schemas.claim import ClaimIntakeRequest, ClaimIntakeResponse


def create_claim_intake(request: ClaimIntakeRequest) -> ClaimIntakeResponse:
    """
    Create a new claim intake response.

    For the current version, this function generates a claim ID and returns
    the first workflow steps. Later, this function will save the claim to
    the database and trigger the LangGraph workflow.
    """

    claim_id = f"CLM-{uuid4().hex[:8].upper()}"

    return ClaimIntakeResponse(
        claim_id=claim_id,
        status="intake_received",
        message="Claim intake received successfully.",
        next_steps=[
            "Start document review workflow.",
            "Retrieve relevant policy and SOP guidance.",
            "Route claim to risk and severity analysis.",
        ],
    )