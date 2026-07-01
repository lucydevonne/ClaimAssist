"""
Health API routes for ClaimAssistant.

This module exposes service health endpoints used to confirm
that the API is running.
"""

from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """Return service health status."""

    return {
        "status": "healthy",
        "service": "ClaimAssistant",
        "version": "0.1.0",
    }