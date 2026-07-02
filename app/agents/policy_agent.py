"""
Policy review agent for ClaimAssistant.

This agent is responsible for adding policy guidance to the claim workflow state.

Current version:
- adds placeholder policy guidance
- updates workflow state for the next stage

Future version:
- will use RAG to retrieve relevant policy, SOP, and coverage guidance.
"""

from app.graph.state import ClaimWorkflowState


def review_policy_guidance(
    state: ClaimWorkflowState,
) -> ClaimWorkflowState:
    """
    Review policy guidance and update the workflow state.

    Args:
        state: Current claim workflow state.

    Returns:
        Updated claim workflow state with policy guidance.
    """

    state.policy_guidance = (
        "Policy review pending. No policy or SOP documents have been retrieved yet."
    )
    state.status = "policy_review_completed"

    return state