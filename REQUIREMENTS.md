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

Required deployment platform: GCP. Baseline stack:
- Installable mobile apps for iPhone (iOS) and Android, with shared product behavior
- Python/FastAPI backend
- PostgreSQL system of record
- GCP
- Cloud Run
- Cloud SQL for PostgreSQL
- Firebase Authentication
- Cloud Storage as needed

## AI and RAG
Agents, reusable AI skills, and retrieval-augmented generation (RAG) are required product capabilities. Agents orchestrate bounded workflows; skills encapsulate reusable, independently testable capabilities such as retrieval, concept mapping, explanation drafting, and content validation. AI skills are distinct from SAT taxonomy Skill records.

The relational database remains authoritative for taxonomy, content, mappings, attempts, and mastery. RAG grounds explanations and content workflows in approved, versioned material with source attribution. Start with PostgreSQL + pgvector; document any alternative in an architecture decision. Retrieval must respect content rights and access permissions, and insufficient evidence must produce an explicit fallback rather than invented support.

Agents run on the backend and use explicit tool permissions, validated inputs/outputs, bounded execution, and cost limits. Canonical taxonomy changes and publication require the existing human review workflow. AI must not autonomously override deterministic scoring or mastery rules.

## Nonfunctional Requirements
Secure by design, observable, testable, maintainable, CI/CD deployed, scalable, and privacy-conscious.

## Definition of Done
A functional change is complete only when required tests exist/update and pass, source files comply with the 500-line maximum, applicable lint/type/security gates pass, relevant observability is included, and material documentation is updated.

## Mobile Delivery and Scalability
Deliver and test both iPhone and Android apps. Select the mobile framework through an ADR before implementation, favoring shared code where practical. Support accessible interfaces, secure session storage, interrupted networks, and safe retry behavior. Define supported OS versions and release acceptance criteria before the first mobile release.

Deploy backend APIs and workers to GCP with separate staging and production environments. Keep request services stateless, persist durable state, and queue long-running AI and ingestion work. Define load, latency, availability, and AI cost budgets before production; demonstrate expected peak load and recovery behavior in staging. Mobile store releases and backend deployments have separate pipelines and compatible API contracts.
