# SAT / ACT Prep App — Observability

## Goals
Determine whether services are healthy, where failures occur, how requests flow, whether performance is degrading, and whether important learning workflows function.

## Standard
Prefer OpenTelemetry. Initial GCP destinations may include Cloud Logging, Cloud Monitoring, Cloud Trace, and Error Reporting.

## Structured Logging
Use structured logs rather than print statements. Useful fields include event, timestamp, environment, service/version, trace ID, endpoint, latency, status/error class, and appropriate non-sensitive domain IDs.

Never log passwords, tokens, secrets, raw authentication headers, or unnecessary student PII.

## Metrics
Track request count, error rate, latency, dependency/database latency, DB connection utilization, and question-delivery failures. Later add questions attempted, completion rate, response duration, content-validation failures, and adaptive-selection failures.

## Tracing
Trace significant flows from API entry through services, database, and external dependencies. Preserve trace/correlation IDs.

## AI Observability
When AI is introduced, observe latency, provider/model, token usage/cost where available, generation errors, schema-validation failures, and content rejection rates. Do not log sensitive prompts/responses by default.

## Health
Provide liveness/health and readiness endpoints.

## Initial SLO Candidates
Validate against real workloads before finalizing:
- API availability ≥ 99.9%
- p95 normal non-AI API latency < 500 ms
- server 5xx rate < 1%

## Alerts
Alerts should be actionable. Candidates include sustained 5xx elevation, sustained latency/SLO violations, DB connection exhaustion, deployment health failure, and unusual authentication/security failures.
