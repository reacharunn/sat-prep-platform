# SAT / ACT Taxonomy Design

## Purpose
Represent what a student must know to answer a question correctly and why plausible wrong answers occur.

## Controlled Hierarchy
Section → Domain → Skill → Concept → Subconcept → Misconception.

Canonical concepts and misconceptions receive stable identifiers.

## Question Mapping
A question may map to multiple concepts with roles:
- PRIMARY — principal concept assessed
- REQUIRED — knowledge required to solve
- SUPPORTING — relevant but not central

A production question should normally have exactly one PRIMARY concept.

## Prerequisites
Concepts may depend on other concepts. The prerequisite graph must reject self-references and circular dependencies.

## Misconceptions
Misconceptions are first-class controlled entities. Where pedagogically appropriate, incorrect choices map to the misconception/error pattern that plausibly generates them.

## Difficulty
Difficulty is not a permanent property of a concept. Drivers can include number of concepts, reasoning steps, arithmetic complexity, abstraction, context interpretation, representation changes, and distractor similarity.

## Research Workflow
Reference question → identify required knowledge → propose mappings → normalize against controlled taxonomy → human review → approve/update taxonomy → misconception mapping → original question creation.

## Initial Scope
SAT Math → Algebra → Linear equations in one variable. Analyze in small batches and track concept saturation.
