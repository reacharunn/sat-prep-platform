# SAT Prep Taxonomy Backend

A starter backend for a concept-first SAT prep application.

## What is included

- FastAPI API
- SQLAlchemy data model
- Domain → Skill → Concept → Misconception hierarchy
- SQLite for local development
- PostgreSQL-ready DATABASE_URL
- Dockerfile suitable for Cloud Run

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy environment file:

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

Start API:

```bash
uvicorn app.main:app --reload
```

Then open:

http://127.0.0.1:8000/docs

## First records to create

Domain:

```json
{
  "code": "MATH-ALG",
  "name": "Algebra"
}
```

Skill:

```json
{
  "code": "ALG-LEV",
  "name": "Linear equations in one variable",
  "domain_id": 1
}
```

Concept:

```json
{
  "code": "ALG-LEV-001",
  "name": "Preserve equality using equivalent operations",
  "description": "Apply equivalent operations to both sides of an equation.",
  "skill_id": 1,
  "is_atomic": true
}
```

Misconception:

```json
{
  "code": "ALG-MIS-001",
  "name": "One-sided operation",
  "description": "Student changes one side of an equation without applying an equivalent operation to the other side.",
  "concept_id": 1
}
```

## Cloud SQL later

Replace the local DATABASE_URL with a PostgreSQL connection string and deploy the same container to Cloud Run.
