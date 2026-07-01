"""
ClaimAssistant application entry point.

This file creates the FastAPI app and connects API routers.
"""

from fastapi import FastAPI

from app.api.routes_claims import router as claims_router


app = FastAPI(
    title="ClaimAssistant",
    description=(
        "Agentic AI claims assistant for intake, policy retrieval, "
        "document review, risk analysis, and human-in-the-loop resolution."
    ),
    version="0.1.0",
)

app.include_router(claims_router)


@app.get("/health", tags=["health"])
def health_check():
    """Return service health status."""

    return {
        "status": "healthy",
        "service": "ClaimAssistant",
        "version": "0.1.0",
    }