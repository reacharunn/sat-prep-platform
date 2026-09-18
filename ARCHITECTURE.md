# SAT / ACT Prep App — Architecture

## Principles
- Cloud-first but operationally simple.
- PostgreSQL is the system of record.
- Backend owns business logic.
- Clients never receive DB credentials or AI secrets.
- Structured taxonomy is authoritative.
- Prefer managed GCP services.
- Use open instrumentation standards.

## Target Architecture
Mobile App → Authentication → FastAPI on Cloud Run → Cloud SQL/PostgreSQL, Cloud Storage, backend-only AI services, Observability.

## Backend Domains
Separate modules as the system grows: taxonomy, questions/content, attempts, mastery/adaptive learning, administration/content validation, and AI-assisted content tooling. No source-code file may exceed 500 lines.

## Core Relationships
Domain → Skill → Concept → Subconcept.
Also: concept prerequisites, concept misconceptions, question↔concept roles (PRIMARY/REQUIRED/SUPPORTING), question→choices, incorrect choice→misconception, student→attempts, student↔concept mastery.

## Database
Production uses PostgreSQL on Cloud SQL. SQLite may be used locally initially where compatible. Use Alembic migrations before production; do not use create_all() as the production migration mechanism.

## API
Version APIs as the product grows. Expected areas: `/health`, `/ready`, `/api/v1/taxonomy`, `/questions`, `/practice`, `/attempts`, `/mastery`.

## Authentication
Firebase Authentication is preferred initially. Authorization is enforced server-side with roles such as student, content reviewer, and administrator.

## AI
AI may assist concept extraction, mapping proposals, misconception analysis, original question generation, and validation. Treat AI output as untrusted input and validate it against schemas and controlled IDs.

## RAG
Not required initially. Prefer PostgreSQL + pgvector if semantic retrieval becomes useful.

## Environments and Deployment
LOCAL → CI → STAGING → PRODUCTION.

GitHub → GitHub Actions → quality/security gates → container → Artifact Registry → Cloud Run staging → smoke/E2E validation → approved production deployment.

## Architecture Decisions
Material architectural changes should eventually be captured in short ADRs under `docs/adr/`.
