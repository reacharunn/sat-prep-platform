# SAT / ACT Prep App — Product Requirements

## Product Vision
Build a mobile-first SAT/ACT preparation platform that diagnoses what a student understands and misunderstands at the concept level, then delivers targeted practice and remediation. Initial focus: SAT Math.

## Concept-First Model
Controlled taxonomy: Section → Domain → Skill → Concept → Subconcept → Misconception.

Each question supports one primary concept, required/prerequisite concepts, supporting concepts, solution steps, difficulty drivers, answer choices, a correct answer, and diagnostic misconception mappings where applicable.

## Content and IP
Publicly accessible and appropriately usable SAT material may be analyzed as research evidence. Production content must be original or appropriately licensed. Do not ship copyrighted source question text, explanations, screenshots, diagrams, or lightly rewritten copies unless rights permit it. Keep research provenance separate from production content.

## Workflow
Reference question → concept extraction → controlled taxonomy mapping → human review → misconception mapping → original question creation → validation → publication.

AI may propose mappings and new concepts, but production taxonomy IDs are controlled and new canonical concepts require review.

## Diagnostic Learning
Wrong answers should be diagnostically meaningful where possible and may represent conceptual misunderstandings, prerequisite gaps, procedural errors, arithmetic/sign errors, or context misinterpretation.

## Platform and Scale
Design initially for hundreds of users while allowing growth without redesigning the core data model.

Preferred stack:
- Mobile-first client
- Python/FastAPI backend
- PostgreSQL system of record
- GCP
- Cloud Run
- Cloud SQL for PostgreSQL
- Firebase Authentication
- Cloud Storage as needed

## AI and RAG
The relational database is authoritative for taxonomy, content, mappings, attempts, and mastery. RAG is optional. Prefer PostgreSQL + pgvector before a separate vector database.

## Nonfunctional Requirements
Secure by design, observable, testable, maintainable, CI/CD deployed, scalable, and privacy-conscious.

## Definition of Done
A functional change is complete only when required tests exist/update and pass, source files comply with the 500-line maximum, applicable lint/type/security gates pass, relevant observability is included, and material documentation is updated.
