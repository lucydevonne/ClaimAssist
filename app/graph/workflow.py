"""
Claim workflow orchestration for ClaimAssistant.

This module defines the stateful workflow that will coordinate agents
across claim intake, document review, policy retrieval, risk analysis,
and human-in-the-loop decision support.
"""

from app.graph.state import ClaimWorkflowState


def run_claim_workflow(
    initial_state: ClaimWorkflowState,
) -> ClaimWorkflowState:
    """
    Run the claim workflow from the initial claim state.

    Current version:
    - receives the initial state from the intake agent
    - marks the workflow as ready for document review

    Future version:
    - will use LangGraph to route the claim through multiple agents
    """

    initial_state.status = "ready_for_document_review"
    return initial_state