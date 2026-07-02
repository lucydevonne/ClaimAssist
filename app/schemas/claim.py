"""
Claim schemas for ClaimAssistant.

This file defines the structured data contracts for claim intake.
Schemas are used by FastAPI for request validation and by agents for
consistent state across the workflow.

Evidence:
- Pydantic validates Python data using type annotations.
- FastAPI uses Pydantic models for request and response bodies.
"""

from datetime import date
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class ClaimType(str, Enum):
    """Supported claim categories for the first MVP."""

    workers_compensation = "workers_compensation"
    property_damage = "property_damage"
    auto_liability = "auto_liability"
    general_liability = "general_liability"


class ClaimIntakeRequest(BaseModel):
    """Request body for creating a new claim intake case."""

    claimant_name: str = Field(
        ...,
        min_length=2,
        description="Name of the person filing or associated with the claim.",
    )
    claim_type: ClaimType = Field(
        ...,
        description="Type of insurance claim being submitted.",
    )
    date_of_loss: date = Field(
        ...,
        description="Date when the claim incident occurred.",
    )
    incident_description: str = Field(
        ...,
        min_length=20,
        description="Plain-language description of what happened.",
    )


class ClaimIntakeResponse(BaseModel):
    """Response returned after a claim intake request is accepted."""

    claim_id: str = Field(..., description="System-generated claim identifier.")
    status: str = Field(..., description="Current claim workflow status.")
    message: str = Field(..., description="Human-readable status message.")
   
    
class ClaimDecisionResponse(BaseModel):
    """Response returned after the claim workflow produces a recommendation."""

    claim_id: str = Field(
        ...,
        description="System-generated claim identifier.",
    )

    status: str = Field(
        ...,
        description="Current claim workflow status.",
    )

    risk_level: str | None = Field(
        default=None,
        description="Risk or severity level assigned during claim review.",
    )

    recommended_action: str | None = Field(
        default=None,
        description="Recommended next best action for the claim.",
    )

    requires_human_review: bool = Field(
        ...,
        description="Whether the claim requires review by a human examiner.",
    )

    summary: str = Field(
        ...,
        description="Short summary of the workflow outcome.",
    )
    
    audit_event: dict[str, Any] = Field(
        ...,
        description=(
            "Structured audit event for the generated decision. "
            "In production, this will be persisted to PostgreSQL."
        ),
    )
    
class ClaimRecordResponse(BaseModel):
    """Response returned when reading a stored claim record from PostgreSQL."""

    claim_id: str = Field(
        ...,
        description="System-generated claim identifier.",
    )

    claimant_name: str = Field(
        ...,
        description="Name of the person filing or associated with the claim.",
    )

    claim_type: str = Field(
        ...,
        description="Type of insurance claim.",
    )

    date_of_loss: date = Field(
        ...,
        description="Date when the claim incident occurred.",
    )

    incident_description: str = Field(
        ...,
        description="Original claim incident description.",
    )

    status: str = Field(
        ...,
        description="Current claim workflow status.",
    )

    risk_level: str | None = Field(
        default=None,
        description="Risk or severity level assigned during claim review.",
    )

    recommended_action: str | None = Field(
        default=None,
        description="Recommended next best action for the claim.",
    )

    requires_human_review: bool = Field(
        ...,
        description="Whether the claim requires human examiner review.",
    )