"""
Claim service layer for ClaimAssist.

The service layer contains business logic for claim operations.
API routes should call this layer instead of handling business logic directly.
"""

from uuid import uuid4

from sqlalchemy.orm import Session

from app.agents.intake_agent import create_initial_claim_state
from app.graph.workflow import run_claim_workflow
from app.schemas.claim import ClaimIntakeRequest, ClaimIntakeResponse, ClaimDecisionResponse, ClaimRecordResponse, ClaimAuditLogResponse

from app.repositories.audit_repository import create_audit_log_record, get_audit_logs_by_claim_id
from app.repositories.claim_repository import create_claim_record, get_claim_record_by_id

from app.services.audit_service import create_audit_event

from app.observability.logging_config import get_logger

from app.guardrails.input_validation import validate_claim_input

logger = get_logger(__name__)

def create_claim_intake(request: ClaimIntakeRequest) -> ClaimIntakeResponse:
    """
    Create a new claim intake response.

    Current behavior:
    - Generates a claim ID.
    - Creates the initial workflow state.
    - Returns a structured intake response.

    Future production behavior:
    - Save the raw claim intake record to PostgreSQL.
    - Trigger the LangGraph workflow asynchronously.
    - Persist an intake audit event.
    """

    validate_claim_input(request)
    
    claim_id = f"CLM-{uuid4().hex[:8].upper()}"

    initial_state = create_initial_claim_state(
        claim_id=claim_id,
        request=request,
    )
        
    workflow_state = run_claim_workflow(initial_state)

    return ClaimIntakeResponse(
        claim_id=claim_id,
        status=workflow_state.status,
        message="Claim intake received successfully.",
        next_steps=[
            "Start document review workflow.",
            "Retrieve relevant policy and SOP guidance.",
            "Route claim to risk and severity analysis.",
        ],
    )
    
def create_claim_decision(request: ClaimIntakeRequest, db: Session,) -> ClaimDecisionResponse:
    """
    Run the claim workflow and return a decision-style response.

    Current behavior:
    - Generates a claim ID.
    - Creates the initial workflow state.
    - Runs the current agent workflow.
    - Saves the completed claim state to PostgreSQL.
    - Creates and saves an audit event to PostgreSQL.
    - Returns the decision response.

    Future production behavior:
    - Persist every intermediate workflow state transition.
    - Store every agent and tool execution as an audit log.
    - Trigger long-running workflows through LangGraph.
    - Add rollback handling so claim and audit writes stay consistent.
    """

    validate_claim_input(request)
    
    claim_id = f"CLM-{uuid4().hex[:8].upper()}"
    
    logger.info("claim_decision_workflow_started claim_id=%s", claim_id)

    initial_state = create_initial_claim_state(
        claim_id=claim_id,
        request=request,
    )

    workflow_state = run_claim_workflow(initial_state)
    
    logger.info(
    "claim_decision_workflow_completed claim_id=%s status=%s risk_level=%s requires_human_review=%s",
    workflow_state.claim_id,
    workflow_state.status,
    workflow_state.risk_level,
    workflow_state.requires_human_review,
    )

    create_claim_record(
        db=db,
        state=workflow_state,
    )

    audit_event = create_audit_event(
        claim_id=workflow_state.claim_id,
        event_type="claim_decision_generated",
        details={
            "status": workflow_state.status,
            "risk_level": workflow_state.risk_level,
            "requires_human_review": workflow_state.requires_human_review,
            "recommended_action": workflow_state.recommended_action,
        },
    )

    create_audit_log_record(
        db=db,
        audit_event=audit_event,
    )
    
    logger.info(
    "claim_decision_persisted claim_id=%s event_type=%s",
    workflow_state.claim_id,
    audit_event["event_type"],
    )

    return ClaimDecisionResponse(
        claim_id=workflow_state.claim_id,
        status=workflow_state.status,
        risk_level=workflow_state.risk_level,
        recommended_action=workflow_state.recommended_action,
        requires_human_review=workflow_state.requires_human_review,
        summary="Claim workflow completed and recommendation generated.",
        audit_event=audit_event,
    )
    
def get_claim_by_id(
    claim_id: str,
    db: Session,
) -> ClaimRecordResponse | None:
    """
    Retrieve a stored claim by claim ID.

    Current behavior:
    - Calls the claim repository to fetch a PostgreSQL claim record.
    - Converts the database model into a response schema.

    Future production behavior:
    - Enforce role-based access control.
    - Include linked audit logs, documents, and workflow trace data.
    - Support examiner-facing claim detail views.
    """

    claim = get_claim_record_by_id(
        db=db,
        claim_id=claim_id,
    )

    if claim is None:
        return None

    return ClaimRecordResponse(
        claim_id=claim.id,
        claimant_name=claim.claimant_name,
        claim_type=claim.claim_type,
        date_of_loss=claim.date_of_loss,
        incident_description=claim.incident_description,
        status=claim.status,
        risk_level=claim.risk_level,
        recommended_action=claim.recommended_action,
        requires_human_review=claim.requires_human_review,
    )
    
def get_claim_audit_logs(
    claim_id: str,
    db: Session,
) -> list[ClaimAuditLogResponse]:
    """
    Retrieve audit logs for a stored claim.

    Current behavior:
    - Calls the audit repository to fetch PostgreSQL audit records.
    - Converts database models into API response schemas.

    Future production behavior:
    - Return a complete workflow timeline for examiner review.
    - Include model prompts, tool calls, retrieved policy chunks,
      and human override decisions where appropriate.
    """

    audit_logs = get_audit_logs_by_claim_id(
        db=db,
        claim_id=claim_id,
    )

    return [
        ClaimAuditLogResponse(
            audit_id=audit_log.id,
            claim_id=audit_log.claim_id,
            event_type=audit_log.event_type,
            details=audit_log.details,
            created_at=audit_log.created_at,
        )
        for audit_log in audit_logs
    ]