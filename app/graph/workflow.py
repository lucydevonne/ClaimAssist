"""
Claim workflow orchestration for ClaimAssistant.

This module defines the stateful workflow that will coordinate agents
across claim intake, document review, policy retrieval, risk analysis,
and human-in-the-loop decision support.
"""

from app.agents.document_agent import review_claim_documents
from app.agents.policy_agent import review_policy_guidance
from app.graph.state import ClaimWorkflowState


def run_claim_workflow(initial_state: ClaimWorkflowState) -> ClaimWorkflowState:
    """
    Run the claim workflow from the initial claim state.

    Current workflow:
    1. Receive initial claim state.
    2. Run document review agent.
    3. Run policy review agent.
    4. Return updated workflow state.
    """

    workflow_state = review_claim_documents(initial_state)
    workflow_state = review_policy_guidance(workflow_state)
    
    return workflow_state