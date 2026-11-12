# Divya SAT practice (prototype)
Visit `/practice` when the FastAPI app is running. This is a responsive browser prototype served from the existing FastAPI service.

- Original SAT-style Math and Reading & Writing questions, topic selection, immediate explanations and browser-local progress.
- No login, cross-device syncing, parent dashboard, adaptive mastery engine, model-powered question generation, or production deployment yet.
- The question bank is deliberately small; sets larger than the available pool repeat questions. It is a UI integration milestone, **not** a validated full SAT question generator.
- Future work: reviewed concept-linked question bank in PostgreSQL, authenticated attempt API, deterministic scoring and mastery, then validated AI-assisted content workflows.
- Do not deploy student data features publicly without authentication, authorization, privacy controls, and content review.

Run `python -m pytest` and `python -m uvicorn app.main:app --reload`.

## AI generator (development integration)
The practice UI now supports **New AI questions**. The backend exposes `POST /api/ai/generate` with subject, topic, difficulty and count (1–10).

Configure server environment variables (never commit secrets):
- `OPENAI_API_KEY`: provider API key
- `SAT_PRACTICE_TOKEN`: administrator-created shared access token
- `SAT_AI_MODEL`: optional model identifier (default `gpt-4o-mini`)

The endpoint validates JSON shape, topic, distinct choices, answer index, misconception labels and unique stems. It does **not** independently prove correctness, enforce full curriculum alignment, or publish canonical content. Questions are unreviewed AI proposals.

**Not production ready:** Shared token is temporary and does not replace Firebase Authentication, per-user quotas, rate limits or cost controls. Do not deploy the generator publicly without those safeguards. The token is not stored in browser storage. AI API usage may incur charges.

Run `python -m pytest` and browser tests before merging. Live provider integration is unverified.
