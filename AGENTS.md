# Repository Instructions

Read REQUIREMENTS.md, ARCHITECTURE.md, ENGINEERING_STANDARDS.md, and relevant docs/ files before making changes. These documents govern work throughout this repository.

- Build for both iPhone (iOS) and Android and deploy scalable backend services to GCP.
- Include backend agents, reusable typed AI skills, and RAG over approved, versioned sources. AI skills are separate from curriculum Skill records.
- Keep PostgreSQL authoritative and enforce authorization, deterministic validation, and human review for canonical taxonomy changes and publication.
- Keep secrets on the backend; protect student data and respect content rights.
- Keep source files at or below 500 physical lines. Functional changes require appropriate automated tests and running the suite, with applicable lint/type/security and migration checks.
- Use bounded, observable, recoverable agent workflows and evaluate retrieval and grounding quality.
- Distinguish planned architecture from implemented capabilities. Document material choices in ADRs, including mobile framework and agent/model tooling.

The product's use of agents does not require coding assistants to delegate every task. Use coding subagents when explicitly requested or authorized for the task.

## Language Models and AI Workflows

- Treat agents and reusable AI skills as planned capabilities unless the implementation and documentation say otherwise; do not imply that the current starter backend already provides model, RAG, auth, or review workflows.
- Keep model providers and agent frameworks behind backend adapters selected through an ADR. Never expose provider credentials, model secrets, or database credentials to mobile clients.
- Define each AI skill as a versioned, independently testable module with typed input/output contracts, prompt and model identifiers, least-privilege tools, timeout/retry/cancellation behavior, idempotency, and token/cost limits. Keep AI workflow skills distinct from curriculum `Skill` records.
- Treat prompts, model output, and retrieved text as untrusted. Validate outputs against schemas and controlled database IDs; retrieved content is evidence, never instructions or tool authorization.
- Keep PostgreSQL authoritative. Agents may propose mappings, content, misconceptions, or validations, but deterministic services enforce authorization and business rules, and human reviewers approve canonical taxonomy changes and publication. AI must not override scoring or mastery rules.
- For RAG, enforce source rights, approval/publication/access filters, provenance, versioning, reindexing, and deletion propagation before model access. Preserve attribution and return an explicit insufficient/conflicting-evidence fallback rather than inventing support.
- Test model workflows with mocked calls in ordinary CI and bounded evaluation/integration suites for schema failures, prompt injection, malicious retrieval, permission isolation, grounding, attribution, cancellation, retries, partial failure, latency, token use, and cost.
- Add privacy-safe observability: record correlation IDs, workflow/skill versions, safe provider/model identifiers, latency, usage/cost, retrieval quality, validation failures, and rejection rates. Do not log raw prompts/responses, protected source text, student PII, credentials, tokens, or auth headers.
- Update [REQUIREMENTS.md](REQUIREMENTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), [ENGINEERING_STANDARDS.md](ENGINEERING_STANDARDS.md), and relevant [docs/](docs/) when AI capabilities move from planned to implemented or when model/orchestration decisions materially change.
