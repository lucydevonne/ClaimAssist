# ClaimAssist

![ClaimAssist Tests](https://github.com/lucydevonne/ClaimAssist/actions/workflows/tests.yml/badge.svg)

ClaimAssist is an agentic AI claims assistant MVP built to explore how multi-step claim workflows can support insurance adjusters. It provides a FastAPI backend with a sequential agent pipeline, PostgreSQL persistence, human-in-the-loop review, and basic safety guardrails.

The project is intentionally structured like a production system, with separate API, service, agent, repository, and guardrail layers, but most agent steps are currently rule-based placeholders rather than LLM-powered reasoning.

## Purpose

ClaimAssist demonstrates how a claims workflow can be broken into discrete agent steps: intake, document review, policy review, risk analysis, and resolution recommendation. It shows how to persist decisions, audit events, and examiner overrides so AI-assisted recommendations stay traceable and reviewable.

This system does not replace human claims examiners. It prepares structured claim outputs, flags risk, recommends next actions, and routes high-risk cases to human review.

## What Works Today

### API and workflow

- **FastAPI** backend with health check and claims routes
- **Pydantic** schemas for request/response validation across intake, decisions, audit logs, and human review
- **Sequential claim workflow** that passes shared state through five agent steps
- **Two intake modes:**
  - `POST /claims` — runs the workflow and returns an intake-style response (does not persist to the database)
  - `POST /claims/decision` — runs the workflow, saves the claim and an audit event to PostgreSQL, and returns a full decision response

### Agents (current behavior)

| Agent | What it does today |
| --- | --- |
| Intake | Builds initial workflow state from validated claim input |
| Document review | Adds a placeholder document summary |
| Policy review | Adds placeholder policy guidance |
| Risk analysis | Rule-based keyword matching (e.g. "surgery", "fraud") to assign low/medium/high risk |
| Resolution | Rule-based next-action recommendation based on risk level |

### Persistence and human review

- **PostgreSQL** with SQLAlchemy models for claims, audit logs, and human reviews
- **Alembic** migrations for schema management
- **Audit logging** for claim decisions and human review actions
- **Human-in-the-loop** endpoints to approve, reject, or escalate a stored claim, with review history

### Safety and quality

- **Input guardrails** — blocks obvious prompt-injection phrases in claim descriptions
- **Output guardrails** — validates risk level, recommended action, and human-review requirements before returning results
- **Structured logging** for workflow events during local development

### Testing and CI

- **pytest** suite covering health checks, claim intake, decision persistence, guardrails, and human review
- **GitHub Actions** CI with a PostgreSQL service container

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Service health check |
| `POST` | `/claims` | Run workflow and return intake response (no DB write) |
| `POST` | `/claims/decision` | Run workflow, persist claim + audit log, return decision |
| `GET` | `/claims/{claim_id}` | Retrieve a stored claim |
| `GET` | `/claims/{claim_id}/audit-logs` | List audit events for a claim |
| `POST` | `/claims/{claim_id}/human-review` | Record approve / reject / escalate decision |
| `GET` | `/claims/{claim_id}/human-reviews` | List human review history for a claim |

Interactive API docs: `http://127.0.0.1:8000/docs`

## Architecture

```text
Client
  └── FastAPI routes (claims, health)

Service layer
  └── Claim intake, decision, lookup, human review, audit

Guardrails
  └── Input validation, output validation

Workflow orchestration (sequential Python)
  ├── Intake agent
  ├── Document review agent      (placeholder)
  ├── Policy review agent        (placeholder)
  ├── Risk analysis agent        (rule-based)
  └── Resolution agent           (rule-based)

Persistence
  └── PostgreSQL (claims, audit_logs, human_reviews)
```

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic / pydantic-settings
- SQLAlchemy
- PostgreSQL
- Alembic
- pytest
- GitHub Actions

## Running Locally

### 1. Set up PostgreSQL

Create two databases — one for local development and one for tests:

```sql
CREATE DATABASE claimassist;
CREATE DATABASE claimassist_test;
```

### 2. Configure environment

Copy the example env file and adjust if needed:

```bash
cp .env.example .env
```

### 3. Install and migrate

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Health check: `http://127.0.0.1:8000/health`

### 5. Run tests

```bash
pytest
```

Tests expect PostgreSQL running at the URL in `TEST_DATABASE_URL` (default: `claimassist_test` on localhost).

## Example Requests

### Claim intake (no persistence)

```text
POST /claims
```

```json
{
  "claimant_name": "Jane Doe",
  "claim_type": "workers_compensation",
  "date_of_loss": "2026-06-12",
  "incident_description": "Employee reported lower back pain after lifting heavy inventory boxes during a warehouse shift."
}
```

The workflow runs through all agent steps synchronously. The response includes a generated claim ID and the final workflow status.

### Claim decision (with persistence)

```text
POST /claims/decision
```

Same request body as above. Returns risk level, recommended action, human-review flag, and an audit event. The claim and audit log are saved to PostgreSQL.

Example high-risk response shape:

```json
{
  "claim_id": "CLM-AB12CD34",
  "status": "resolution_recommendation_completed",
  "risk_level": "high",
  "recommended_action": "Escalate to a senior claims examiner for manual review.",
  "requires_human_review": true,
  "summary": "Claim workflow completed and recommendation generated.",
  "audit_event": {
    "event_type": "claim_decision_generated",
    "claim_id": "CLM-AB12CD34",
    "details": { "...": "..." }
  }
}
```

### Human review

```text
POST /claims/{claim_id}/human-review
```

```json
{
  "action": "escalate",
  "reviewer_notes": "High-risk claim needs supervisor review."
}
```

Supported actions: `approve`, `reject`, `escalate`.

## Project Structure

```text
ClaimAssist/
  alembic/                  # Database migrations
  app/
    agents/                 # Intake, document, policy, risk, resolution agents
    api/                    # FastAPI route handlers
    core/                   # Application settings
    database/               # SQLAlchemy models and session
    graph/                  # Workflow state and orchestration
    guardrails/             # Input and output validation
    observability/          # Logging configuration
    repositories/           # PostgreSQL data access
    schemas/                # Pydantic request/response models
    services/               # Business logic layer
    main.py
  tests/
  .github/workflows/        # CI pipeline
  requirements.txt
  alembic.ini
  .env.example
```

## What Could Be Improved

These are areas the codebase is structured for but has not implemented yet.

### AI and reasoning

- Replace placeholder agents with **LLM-powered reasoning** (OpenAI / Azure OpenAI)
- Add **LangGraph** (or similar) for stateful, resumable workflow orchestration instead of a single synchronous function chain
- Use **RAG** over policy and SOP documents (`pgvector` or another vector store) in the policy review step
- Extract facts from uploaded documents in the document review step

### Retrieval, tools, and data

- Add a **tools layer** for policy search, claim lookup, and external integrations
- Populate **policy document data** and wire up retrieval pipelines
- Persist **every agent and tool step** as separate audit events, not just final decisions

### Production readiness

- **Docker** and **Kubernetes** deployment configs (the `infra/` directory is reserved but empty)
- **Authentication and RBAC** for examiner-facing endpoints
- **OpenTelemetry** tracing, metrics, and structured JSON logs
- Transaction rollback in tests instead of create/drop tables per test
- Async or background job execution for long-running workflows

### Evaluation and safety

- **Evaluation framework** for retrieval quality, reasoning accuracy, and workflow reliability
- Stronger prompt-injection detection, PII handling, and policy-aware validation
- Citation checks and confidence thresholds before auto-resolution
- Store reviewer identity and supervisor approval chains

### API and product gaps

- `POST /claims` does not persist claims — only `/claims/decision` writes to the database
- Intake response `next_steps` are static and do not reflect actual workflow output
- All non-high-risk claims are currently flagged for human review as well
- No document upload or file processing endpoints yet

## Development Status

Active development. The core workflow, PostgreSQL persistence, human review loop, guardrails, and test suite are in place. LLM integration, RAG, and deployment tooling are the main areas still ahead.
