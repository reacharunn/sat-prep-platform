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
