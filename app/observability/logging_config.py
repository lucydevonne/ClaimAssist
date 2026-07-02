"""
Logging configuration for ClaimAssist.

This module centralizes application logging setup.

Current behavior:
- Configures standard Python logging for the application.
- Creates a reusable logger for ClaimAssist modules.
- Sends structured workflow messages to the console during local development.

Future production behavior:
- Send logs to an observability backend.
- Add correlation IDs for claim_id, workflow_id, and request_id.
- Integrate with OpenTelemetry traces, metrics, and logs.
- Support claims workflow monitoring for failures, latency, and agent behavior.
"""

import logging


LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def configure_logging() -> None:
    """
    Configure application-wide logging.

    Current behavior:
    - Sets the default logging level to INFO.
    - Applies a consistent log format across the application.

    Future production behavior:
    - Add JSON-formatted logs.
    - Add request IDs and workflow correlation IDs.
    - Export logs to OpenTelemetry-compatible observability tools.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger for a module.

    Args:
        name: Name of the module requesting a logger.

    Returns:
        Configured Python logger instance.

    Current behavior:
    - Returns a standard Python logger.

    Future production behavior:
    - Return a structured logger with claim/workflow context attached.
    """

    return logging.getLogger(name)