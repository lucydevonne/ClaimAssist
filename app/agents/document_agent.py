"""
Document review agent for ClaimAssistant.

This agent is responsible for reviewing claim-related documents and
adding a document summary to the shared workflow state.

Current version:
- creates a placeholder document summary
- updates workflow state for the next stage

Future version:
- will extract facts from claim notes, medical documents, employer reports,
  and supporting evidence using document intelligence.
"""

from app.graph.state import ClaimWorkflowState


def review_claim_documents(
    state: ClaimWorkflowState,
) -> ClaimWorkflowState:
    """
    Review claim documents and update the workflow state.

    Args:
        state: Current claim workflow state.

    Returns:
        Updated claim workflow state with document summary.
    """

    state.document_summary = (
        "Document review pending. No uploaded claim documents have been "
        "processed yet."
    )
    state.status = "document_review_completed"

    return state