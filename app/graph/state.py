"""
Workflow state models for ClaimAssistant.

The workflow state represents the shared data object that moves through
the agentic claims workflow. Each agent will read from this state, add
new information, and pass the updated state to the next workflow step.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.claim import ClaimType


class ClaimWorkflowState(BaseModel):
    """
    Shared state for the ClaimAssistant agent workflow.

    This state starts with claim intake data and grows as agents add
    document findings, policy guidance, risk signals, and recommendations.
    """

    claim_id: str = Field(
        ...,
        description="Unique claim identifier created during intake.",
    )

    claimant_name: str = Field(
        ...,
        description="Name of the person filing or associated with the claim.",
    )

    claim_type: ClaimType = Field(
        ...,
        description="Type of insurance claim being processed.",
    )

    date_of_loss: date = Field(
        ...,
        description="Date when the claim incident occurred.",
    )

    incident_description: str = Field(
        ...,
        description="Original claim incident description from intake.",
    )

    status: str = Field(
        default="intake_received",
        description="Current workflow status.",
    )

    document_summary: Optional[str] = Field(
        default=None,
        description="Summary produced by the future document review agent.",
    )

    policy_guidance: Optional[str] = Field(
        default=None,
        description="Relevant policy guidance retrieved by the future RAG agent.",
    )

    risk_level: Optional[str] = Field(
        default=None,
        description="Risk or severity level assigned by the future risk agent.",
    )

    recommended_action: Optional[str] = Field(
        default=None,
        description="Next-best-action recommendation from the future resolution agent.",
    )

    requires_human_review: bool = Field(
        default=False,
        description="Whether the claim must be reviewed by a human examiner.",
    )