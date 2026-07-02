"""
Output validation guardrails for ClaimAssist.

This module validates workflow outputs before they are returned by the API
or persisted for downstream use.

Current behavior:
- Checks that risk level is within an allowed set.
- Checks that high-risk claims require human review.
- Checks that a recommendation exists before returning a decision.

Future production behavior:
- Validate LLM-generated structured outputs before persistence.
- Enforce policy-specific decision rules.
- Block unsafe or incomplete recommendations.
- Store failed output validation attempts in PostgreSQL audit logs.
- Add schema-level and business-rule validation for agent outputs.
"""

from app.graph.state import ClaimWorkflowState


ALLOWED_RISK_LEVELS = {"low", "medium", "high"}


def validate_workflow_output(state: ClaimWorkflowState) -> None:
    """
    Validate the final workflow state before returning a decision.

    Args:
        state: Completed claim workflow state.

    Raises:
        ValueError: If the workflow output is incomplete or unsafe.

    Current behavior:
    - Ensures risk_level is present and valid.
    - Ensures recommended_action is present.
    - Ensures high-risk claims require human review.

    Future production behavior:
    - Validate LLM responses against strict schemas.
    - Check policy citation requirements.
    - Check confidence thresholds before allowing auto-resolution.
    - Route failed outputs to human review instead of returning them directly.
    """

    if state.risk_level not in ALLOWED_RISK_LEVELS:
        raise ValueError("Workflow output contains an invalid risk level.")

    if not state.recommended_action:
        raise ValueError("Workflow output is missing a recommended action.")

    if state.risk_level == "high" and not state.requires_human_review:
        raise ValueError(
            "High-risk claims must be routed to human review."
        )