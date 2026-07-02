"""
Claim service layer for ClaimAssistant.

The service layer contains business logic for claim operations.
API routes should call this layer instead of handling business logic directly.
"""

from uuid import uuid4

from app.services.audit_service import create_audit_event
from app.agents.intake_agent import create_initial_claim_state
from app.graph.workflow import run_claim_workflow
from app.schemas.claim import ClaimIntakeRequest, ClaimIntakeResponse, ClaimDecisionResponse


def create_claim_intake(request: ClaimIntakeRequest) -> ClaimIntakeResponse:
    """
    Create a new claim intake response.

    For the current version, this function generates a claim ID and returns
    the first workflow steps. Later, this function will save the claim to
    the database and trigger the LangGraph workflow.
    """

    claim_id = f"CLM-{uuid4().hex[:8].upper()}"
    
    initial_state = create_initial_claim_state(
        claim_id=claim_id,
        request=request,
    )
        
    workflow_state = run_claim_workflow(initial_state)
    
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
    
def create_claim_decision(request: ClaimIntakeRequest) -> ClaimDecisionResponse:
    """
    Run the claim workflow and return a decision-style response.

    This function is used when the caller wants the workflow output,
    not just the initial intake confirmation.
    """

    claim_id = f"CLM-{uuid4().hex[:8].upper()}"

    initial_state = create_initial_claim_state(
        claim_id=claim_id,
        request=request,
    )

    workflow_state = run_claim_workflow(initial_state)

    return ClaimDecisionResponse(
        claim_id=workflow_state.claim_id,
        status=workflow_state.status,
        risk_level=workflow_state.risk_level,
        recommended_action=workflow_state.recommended_action,
        requires_human_review=workflow_state.requires_human_review,
        summary="Claim workflow completed and recommendation generated.",
    )