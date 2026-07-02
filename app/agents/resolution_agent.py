"""
Resolution recommendation agent for ClaimAssistant.

This agent recommends the next best action based on the current
claim workflow state, risk level, policy guidance, and document summary.

Current version:
- uses rule-based logic
- creates a recommended action
- updates workflow status

Future version:
- will use LLM reasoning, policy citations, confidence scoring,
  and human-in-the-loop review controls.
"""

from app.graph.state import ClaimWorkflowState


def recommend_claim_resolution(
    state: ClaimWorkflowState,
) -> ClaimWorkflowState:
    """
    Recommend the next best action for the claim.

    Args:
        state: Current claim workflow state.

    Returns:
        Updated claim workflow state with recommended action.
    """

    if state.risk_level == "high":
        state.recommended_action = (
            "Escalate to a senior claims examiner for manual review."
        )
        state.requires_human_review = True

    elif state.risk_level == "medium":
        state.recommended_action = (
            "Request supporting documents and route to examiner review."
        )
        state.requires_human_review = True

    else:
        state.recommended_action = (
            "Continue standard claim processing workflow."
        )

    state.status = "resolution_recommendation_completed"

    return state