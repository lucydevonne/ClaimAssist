"""
Risk analysis agent for ClaimAssistant.

This agent reviews the current claim workflow state and assigns an initial
risk or severity level. It also decides whether the claim should require
human review.

Current version:
- uses simple rule-based logic
- updates risk level
- updates human review flag

Future version:
- will use claim history, document signals, policy guidance, fraud indicators,
  and LLM-based reasoning with structured output validation.
"""

from app.graph.state import ClaimWorkflowState


def analyze_claim_risk(
    state: ClaimWorkflowState,
) -> ClaimWorkflowState:
    """
    Analyze claim risk and update the workflow state.

    Args:
        state: Current claim workflow state.

    Returns:
        Updated claim workflow state with risk level and review decision.
    """

    description = state.incident_description.lower()

    high_risk_terms = [
        "fraud",
        "lawsuit",
        "hospitalized",
        "surgery",
        "severe",
        "death",
        "permanent injury",
    ]

    if any(term in description for term in high_risk_terms):
        state.risk_level = "high"
        state.requires_human_review = True
    else:
        state.risk_level = "medium"
        state.requires_human_review = True

    state.status = "risk_analysis_completed"

    return state