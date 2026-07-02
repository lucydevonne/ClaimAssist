"""
ClaimAssistant application entry point.

This file creates the FastAPI app and connects API routers.
"""

from fastapi import FastAPI

from app.api.routes_claims import router as claims_router
from app.api.routes_health import router as health_router

from app.observability.logging_config import configure_logging

configure_logging()


app = FastAPI(
    title="ClaimAssistant",
    description=(
        "Agentic AI claims assistant for intake, policy retrieval, "
        "document review, risk analysis, and human-in-the-loop resolution."
    ),
    version="0.1.0",
)

app.include_router(claims_router)
app.include_router(health_router)