"""
Claims API routes for ClaimAssistant.

This module exposes HTTP endpoints for claim intake.
The API layer should stay thin: it receives requests, validates schemas,
and calls services or workflow orchestration.
"""

from uuid import uuid4
from fastapi import APIRouter

from app.schemas.claim import ClaimIntakeRequest, ClaimIntakeResponse, ClaimDecisionResponse
from app.services.claim_service import create_claim_intake, create_claim_decision


router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("", response_model=ClaimIntakeResponse)
def create_claim(request: ClaimIntakeRequest) -> ClaimIntakeResponse:
    """
    Receive a new claim intake request.

    The request data is validated by ClaimIntakeRequest.
    The business logic is handled by the claim service layer.
    """
    return create_claim_intake(request)

@router.post("/decision", response_model=ClaimDecisionResponse)
def create_claim_decision_response(
    request: ClaimIntakeRequest,
) -> ClaimDecisionResponse:
    """
    Receive a claim intake request and return the workflow decision output.

    This endpoint runs the current agent workflow and exposes the risk level,
    recommended action, and human review requirement.
    """

    return create_claim_decision(request)