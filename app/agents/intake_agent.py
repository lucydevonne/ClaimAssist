"""
Intake agent for ClaimAssistant.

The intake agent converts validated claim intake data into the first
workflow state used by the agentic claims review process.
"""

from app.graph.state import ClaimWorkflowState
from app.schemas.claim import ClaimIntakeRequest


def create_initial_claim_state(
    claim_id: str,
    request: ClaimIntakeRequest,
) -> ClaimWorkflowState:
    """
    Create the initial workflow state from a validated claim intake request.

    This is the first agent step in the claims workflow. Later, this agent
    can be expanded to classify claim complexity, detect missing fields,
    and prepare the case for document review.
    """

    return ClaimWorkflowState(
        claim_id=claim_id,
        claimant_name=request.claimant_name,
        claim_type=request.claim_type,
        date_of_loss=request.date_of_loss,
        incident_description=request.incident_description,
        status="intake_received",
    )