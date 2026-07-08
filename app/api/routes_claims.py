"""
Claims API routes for ClaimAssist.

This module exposes HTTP endpoints for claim intake.
The API layer should stay thin: it receives requests, validates schemas,
and calls services or workflow orchestration.
"""

from app.schemas.claim import ClaimIntakeRequest, ClaimIntakeResponse, ClaimDecisionResponse, ClaimRecordResponse, ClaimAuditLogResponse, HumanReviewRequest, HumanReviewResponse, HumanReviewRecordResponse
from app.services.claim_service import create_claim_intake, create_claim_decision, get_claim_by_id, get_claim_audit_logs, record_human_review, get_claim_human_reviews

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db_session

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("", response_model=ClaimIntakeResponse)
def create_claim(request: ClaimIntakeRequest) -> ClaimIntakeResponse:
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
    try:
        return create_claim_intake(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

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
    try:
        return create_claim_decision(
            request=request,
            db=db,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    

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

@router.get("/{claim_id}/audit-logs", response_model=list[ClaimAuditLogResponse])
def read_claim_audit_logs(
    claim_id: str,
    db: Session = Depends(get_db_session),
) -> list[ClaimAuditLogResponse]:
    """
    Retrieve audit logs linked to a claim.

    Current behavior:
    - Reads claim_id from the URL path.
    - Opens a database session through dependency injection.
    - Calls the service layer to fetch audit logs from PostgreSQL.
    - Returns structured audit log records.

    Future production behavior:
    - Support pagination and filtering.
    - Enforce examiner authorization.
    - Return a full explainability timeline for the claim.
    """

    return get_claim_audit_logs(
        claim_id=claim_id,
        db=db,
    )
    
@router.post("/{claim_id}/human-review", response_model=HumanReviewResponse)
def submit_human_review(
    claim_id: str,
    request: HumanReviewRequest,
    db: Session = Depends(get_db_session),
) -> HumanReviewResponse:
    """
    Submit a human review decision for a claim.

    Current behavior:
    - Reads claim_id from the URL path.
    - Validates the reviewer action and notes.
    - Updates the stored claim status in PostgreSQL.
    - Persists a human-review audit event.
    - Returns a structured review response.

    Future production behavior:
    - Persist human review records in a dedicated table.
    - Enforce examiner authentication and permissions.
    - Return the full human review timeline.
    """

    review_response = record_human_review(
        claim_id=claim_id,
        request=request,
        db=db,
    )

    if review_response is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found.",
        )

    return review_response

@router.get("/{claim_id}/human-reviews", response_model=list[HumanReviewRecordResponse])
def read_claim_human_reviews(
    claim_id: str,
    db: Session = Depends(get_db_session),
) -> list[HumanReviewRecordResponse]:
    """
    Retrieve human review history linked to a claim.
    """

    return get_claim_human_reviews(
        claim_id=claim_id,
        db=db,
    )