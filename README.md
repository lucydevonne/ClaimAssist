# ClaimAssist

![ClaimAssist Tests](https://github.com/lucydevonne/ClaimAssist/actions/workflows/tests.yml/badge.svg)

ClaimAssist is a production-style agentic AI claims assistant designed to support insurance claim workflows.

The system is built to handle claim intake, policy interpretation, document review, risk analysis, next-best-action recommendations, human-in-the-loop review, and audit logging.

## Purpose

This project demonstrates how LLM-powered and agentic AI systems can support claims professionals by reducing manual review time, improving consistency, and helping adjusters make evidence-based decisions.

ClaimAssist does not replace human claims examiners. It assists them by preparing structured claim summaries, retrieving relevant policy guidance, identifying risk indicators, and recommending the next best action with human oversight.

## Current Features

- FastAPI backend with dedicated API routing for claim intake, decisions, retrieval, and health checks
- Pydantic schemas for structured request and response validation
- Claim intake and decision workflow with generated claim IDs, status tracking, next-step responses, and decision outputs
- Service layer separating API routing from claim business logic
- Initial intake, document review, policy review, risk analysis, and resolution recommendation agents integrated into the claim workflow
- Audit service and PostgreSQL-backed audit log persistence for workflow traceability
- Database layer for PostgreSQL persistence, including models, sessions, settings, repositories, and migrations
- Automated testing setup with pytest, test database fixtures, and GitHub Actions CI
- Observability layer prepared for structured workflow logging and future OpenTelemetry integration
- Modular production-style architecture for agents, RAG, tools, guardrails, observability, and tests

## Planned Features

- LangGraph workflow orchestration
- Multi-agent claims review system
- RAG over policy and SOP documents
- Document intelligence for claim notes and medical documents
- Risk and severity analysis agent
- Human-in-the-loop review checkpoint
- Guardrails and structured output validation
- Audit logs for agent decisions and tool calls
- Evaluation framework for retrieval and reasoning quality
- Docker and Kubernetes deployment support

## Architecture

```text
Input Layer
  FastAPI claim intake endpoints

Schema Layer
  Pydantic validation models

Service Layer
  Claim intake business logic
  Claim ID generation
  Initial workflow step preparation

Planning and Reasoning Layer
  LangGraph workflow orchestration

Agent Layer
  Intake agent
  Policy review agent
  Document review agent
  Risk analysis agent
  Resolution recommendation agent

Tools and Retrieval Layer
  Policy search
  Claim lookup
  Risk scoring
  Audit logging

Evaluation Layer
  Output validation
  Citation checks
  Workflow reliability checks

Output Layer
  Structured claim summary
  Next-best-action recommendation
  Human review decision
```

## Tech Stack

- Python
- FastAPI
- Pydantic
- LangGraph
- PostgreSQL
- pgvector
- OpenAI / Azure OpenAI
- Docker
- Kubernetes
- Pytest
- OpenTelemetry

## Running Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Example Claim Intake Request

Endpoint:

```text
POST /claims
```

Request body:

```json
{
  "claimant_name": "Jane Doe",
  "claim_type": "workers_compensation",
  "date_of_loss": "2026-06-12",
  "incident_description": "Employee reported lower back pain after lifting heavy inventory boxes during a warehouse shift."
}
```

Example response:

```json
{
  "claim_id": "CLM-AB12CD34",
  "status": "intake_received",
  "message": "Claim intake received for workers_compensation.",
  "next_steps": [
    "Start document review workflow.",
    "Retrieve relevant policy and SOP guidance.",
    "Route claim to risk and severity analysis."
  ]
}
```

## Project Structure

```text
ClaimAssist/
  app/
    api/
    agents/
    graph/
    guardrails/
    observability/
    rag/
    schemas/
    services/
    tools/
    main.py
  data/
    policies/
  docs/
  infra/
  tests/
  README.md
  pyproject.toml
  .gitignore
```

## Development Status

This project is currently in active development.

Completed claim intake API with structured schema validation, API routers and service-layer.

## Next Milestones

- Add LangGraph workflow state
- Add intake agent
- Add policy RAG retrieval
- Add document review agent
- Add risk and severity analysis
- Add human review checkpoint
- Add audit logging
- Add evaluation tests
- Add Docker deployment