# SAT / ACT Prep App — Data Model

## Taxonomy
Domain, Skill, Concept, ConceptPrerequisite, and Misconception.

Concept supports parent/child structure for subconcepts. ConceptPrerequisite is a directed many-to-many relationship.

## Content
Question stores original/licensed production content and metadata. QuestionConcept maps questions to concepts using PRIMARY, REQUIRED, and SUPPORTING roles. AnswerChoice stores answer options; an incorrect option may reference a Misconception.

## Student Learning — Planned
StudentAttempt records question response, selected choice, correctness, duration, timestamp, and delivery/session context.

ConceptMastery stores or materializes student mastery by concept. The mastery methodology will be specified before implementation.

## Integrity
Canonical codes are unique. Published questions normally have exactly one PRIMARY concept and exactly one correct answer. References must exist. Self/circular prerequisites are rejected. Published content must satisfy validation requirements.

## Provenance
Research/source provenance remains separate from production content. Public accessibility does not by itself grant rights to reproduce copyrighted questions.

## Planned Agent and Retrieval Records
Add versioned source documents and chunks with provenance, rights/approval state, access scope, content hashes, and embedding model/version metadata. Track indexing and deletion status. Embeddings are derived data and must be rebuildable from approved sources.

Persist agent workflow runs, skill versions, execution status, idempotency keys, and safe audit metadata. Link generated proposals to source references and reviewer decisions. Keep AI workflow skills separate from the existing curriculum Skill entity. These are design requirements; add schema changes through reviewed migrations when implemented.
