# SAT / ACT Prep App — Engineering Standards

These standards apply to human- and AI-authored code.

## Source File Size
No source-code file may exceed 500 physical lines. CI must enforce this. Prefer splitting modules well before the limit. Generated/vendor/build/virtual-environment artifacts may be excluded when justified.

## Automated Testing
Every functional change requires appropriate automated tests and the test suite must be run after changes. Backend framework: pytest. Use unit, FastAPI/API, database/integration, content-validation, and E2E tests as applicable.

## Coverage
Use pytest-cov. Initial target: at least 80% coverage on new/changed production code where meaningful. Meaningful assertions matter more than the percentage alone.

## E2E
Use Playwright for browser/admin-web workflows when a web UI exists. Use a native-mobile-appropriate framework for the eventual mobile client.

## Code Quality
Use Ruff for Python linting/formatting. Use explicit type hints and add Pyright or mypy as a CI gate.

## CI Gates
Run dependency installation, 500-line validation, Ruff checks, type checking, pytest, coverage, applicable migration/database tests, and security scans automatically. Add UI E2E when relevant.

## Security
Use Bandit or equivalent SAST, pip-audit or equivalent dependency scanning, and Gitleaks or equivalent secret detection. Never commit passwords, keys, service-account credentials, production secrets, or API tokens. Use Secret Manager for deployed secrets.

## Sonar
Add SonarCloud/SonarQube after foundational CI is stable for maintainability, duplication, code smells, security analysis, and quality gates. It supplements rather than replaces the other tools.

## Database Changes
Use Alembic for production PostgreSQL schema changes. Migrations must be reviewed and tested.

## Observability
Significant production functionality must include appropriate structured logs, metrics, distributed traces, error reporting, and health/readiness behavior. Prefer OpenTelemetry. Never log secrets, tokens, or unnecessary student PII.

## Pull Requests
Keep changes reviewable. PRs should identify what changed, why, tests performed, migration impact, observability impact, and security/privacy considerations where applicable.

## Definition of Done
Code within size limits; appropriate tests exist and pass; lint/type/security checks pass; migrations are included/tested if needed; observability is included where appropriate; material documentation is current.
