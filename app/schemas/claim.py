"""
Claim schemas for ClaimAssistant.

This file defines the structured data contracts for claim intake.
Schemas are used by FastAPI for request validation and by agents for
consistent state across the workflow.

Evidence:
- Pydantic validates Python data using type annotations.
- FastAPI uses Pydantic models for request and response bodies.
"""

from enum import Enum
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
    date_of_loss: str = Field(
        ...,
        description="Date when the incident occurred. MVP uses string format first.",
        examples=["2026-06-12"],
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