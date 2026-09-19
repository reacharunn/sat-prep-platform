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
iPhone and Android apps → Firebase Authentication → FastAPI on Cloud Run → Cloud SQL/PostgreSQL + pgvector, Cloud Storage, backend agent/skill orchestration, and observability. Queue long-running workflows for separately scalable GCP workers.

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
RAG is required for grounded AI learning/content workflows. Use Cloud Storage for approved source artifacts and Cloud SQL/PostgreSQL + pgvector for retrieval metadata and embeddings initially. Keep relational records authoritative.

Ingestion must validate rights and approval status, parse and chunk sources, preserve provenance, record document/chunk/embedding versions, and support reindexing and deletion. Retrieval must apply authorization and publication filters before returning context to the model. Generated responses must preserve source references and handle missing or conflicting evidence. Treat retrieved text as untrusted data, never as instructions or tool authorization.

## Environments and Deployment
LOCAL → CI → STAGING → PRODUCTION.

GitHub → GitHub Actions → quality/security gates → container → Artifact Registry → Cloud Run staging → smoke/E2E validation → approved production deployment.

## Architecture Decisions
Material architectural changes should eventually be captured in short ADRs under `docs/adr/`.

## Agents and Reusable AI Skills
Use explicit, bounded backend workflows with specialized agents where useful. Each skill declares its purpose, typed input/output contracts, allowed tools, version, timeout, and failure behavior. Keep domain logic in deterministic services and expose only scoped operations to agents. Agent frameworks and model providers must be selected through ADRs and isolated behind adapters.

Record durable workflow state and correlation IDs. Limit steps, time, tokens, cost, and retries; support cancellation and idempotent recovery. Agents may propose content and taxonomy changes, but validated services and human review govern approval and publication.

## Mobile Architecture
Support both iPhone and Android from the initial mobile release. Choose the framework in an ADR covering shared code, native integrations, accessibility, testing, and release maintenance. Keep AI keys and database credentials on the backend. Use versioned API contracts, secure platform credential storage, and backward-compatible server changes for installed clients.

## GCP Scaling and Operations
Use stateless Cloud Run services with bounded autoscaling and database connection pools sized against Cloud SQL capacity. Run asynchronous work through managed queues such as Cloud Tasks or Pub/Sub with retry limits, idempotency, and dead-letter handling where applicable. Select queue semantics in an ADR.

Manage infrastructure as code, service-specific IAM identities, Secret Manager, and separate environment configuration. Configure database backups and test recovery. Set scaling ceilings, request and AI quotas, budget alerts, and load-test acceptance thresholds. Apply migrations as a controlled deployment step; verify readiness, staged rollout, and rollback before production releases.
