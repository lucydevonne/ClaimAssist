"""
Claims API routes for ClaimAssistant.

This module exposes HTTP endpoints for claim intake.
The API layer should stay thin: it receives requests, validates schemas,
and calls services or workflow orchestration.
"""

from uuid import uuid4
from fastapi import APIRouter

from app.schemas.claim import ClaimIntakeRequest, ClaimIntakeResponse, ClaimDecisionResponse, ClaimRecordResponse
from app.services.claim_service import create_claim_intake, create_claim_decision, get_claim_by_id 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db_session

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("", response_model=ClaimIntakeResponse)
def create_claim(request: ClaimIntakeRequest, db: Session = Depends(get_db_session),) -> ClaimIntakeResponse:
    """
    Receive a claim intake request and return the workflow decision output.

    Current behavior:
    - Validates the request body using ClaimIntakeRequest.
    - Opens a database session through FastAPI dependency injection.
    - Passes the database session to the service layer.
    - Returns the decision response.

    Future production behavior:
    - This endpoint will support authenticated examiner workflows.
    - It will persist claim decisions, audit logs, and workflow traces.
    """
    return create_claim_intake(request)

@router.post("/decision", response_model=ClaimDecisionResponse)
def create_claim_decision_response(
    request: ClaimIntakeRequest,
    db: Session = Depends(get_db_session),
) -> ClaimDecisionResponse:
    """
    Receive a claim intake request and return the workflow decision output.

    This endpoint runs the current agent workflow and exposes the risk level,
    recommended action, and human review requirement.
    """

    return create_claim_decision(request, db)

@router.get("/{claim_id}", response_model=ClaimRecordResponse)
def read_claim(
    claim_id: str,
    db: Session = Depends(get_db_session),
) -> ClaimRecordResponse:
    """
    Retrieve a stored claim record by claim ID.

    Current behavior:
    - Reads claim_id from the URL path.
    - Opens a database session through FastAPI dependency injection.
    - Calls the service layer to fetch the claim from PostgreSQL.
    - Returns a structured claim record response.

    Future production behavior:
    - Enforce authenticated examiner access.
    - Return linked documents, audit logs, and workflow timeline.
    """

    claim = get_claim_by_id(
        claim_id=claim_id,
        db=db,
    )

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found.",
        )

    return claim