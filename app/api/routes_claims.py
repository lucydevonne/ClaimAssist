"""
Claims API routes for ClaimAssistant.

This module exposes HTTP endpoints for claim intake.
The API layer should stay thin: it receives requests, validates schemas,
and calls services or workflow orchestration.
"""

from uuid import uuid4
from fastapi import APIRouter

from app.schemas.claim import ClaimIntakeRequest, ClaimIntakeResponse


router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("", response_model=ClaimIntakeResponse)
def create_claim(request: ClaimIntakeRequest) -> ClaimIntakeResponse:
    """
    Create a new claim intake case.

    For the MVP, this endpoint only validates the request and returns a
    generated claim ID. Later, this will trigger the LangGraph workflow.
    """

    claim_id = f"CLM-{uuid4().hex[:8].upper()}"

    return ClaimIntakeResponse(
        claim_id=claim_id,
        status="intake_received",
        message=f"Claim intake received for {request.claim_type}.",
        next_steps=[
        "Start document review workflow.",
        "Retrieve relevant policy and SOP guidance.",
        "Route claim to risk and severity analysis.",
    ],
)