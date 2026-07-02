"""
Input validation guardrails for ClaimAssist.

This module contains lightweight safety checks for user-submitted claim text.

Current behavior:
- Detects obvious prompt-injection style phrases in claim descriptions.
- Blocks claims that appear to instruct the AI system to ignore rules,
  bypass policies, or reveal internal prompts.

Future production behavior:
- Add stronger prompt-injection detection.
- Add PII and sensitive-data redaction.
- Add policy-aware validation for required claim fields.
- Store rejected input attempts in PostgreSQL audit logs.
- Combine rule-based checks with LLM safety classifiers.
"""

from app.schemas.claim import ClaimIntakeRequest


BLOCKED_PHRASES = [
    "ignore previous instructions",
    "ignore all instructions",
    "bypass policy",
    "override the system",
    "reveal your system prompt",
    "show me your hidden prompt",
    "delete audit logs",
    "skip human review",
]


def validate_claim_input(request: ClaimIntakeRequest) -> None:
    """
    Validate claim intake text before workflow execution.

    Args:
        request: Validated claim intake request from the API layer.

    Raises:
        ValueError: If the claim description contains blocked unsafe phrases.

    Current behavior:
    - Checks incident_description against a list of blocked phrases.

    Future production behavior:
    - Return structured validation errors.
    - Save blocked attempts to PostgreSQL.
    - Add claim-specific validation rules for documents and policy context.
    """

    description = request.incident_description.lower()

    for phrase in BLOCKED_PHRASES:
        if phrase in description:
            raise ValueError(
                "Claim description contains unsafe workflow instructions."
            )