"""
Audit service for ClaimAssistant.

This module records important workflow events.
In production, audit logs would be stored in a database or log system.
"""

from datetime import datetime, timezone
from typing import Any


def create_audit_event(
    claim_id: str,
    event_type: str,
    details: dict[str, Any],
) -> dict[str, Any]:
    """
    Create an audit event for a claim workflow action.

    Args:
        claim_id: Unique claim identifier.
        event_type: Name of the workflow event.
        details: Extra event details.

    Returns:
        Structured audit event dictionary.
    """

    return {
        "claim_id": claim_id,
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": details,
    }