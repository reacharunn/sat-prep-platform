from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Domain(Base):
    __tablename__ = "domains"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)

    skills: Mapped[list["Skill"]] = relationship(
        back_populates="domain",
        cascade="all, delete-orphan",
    )


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    domain_id: Mapped[int] = mapped_column(ForeignKey("domains.id"))

    domain: Mapped["Domain"] = relationship(back_populates="skills")
    concepts: Mapped[list["Concept"]] = relationship(
        back_populates="skill",
        cascade="all, delete-orphan",
    )


class Concept(Base):
    __tablename__ = "concepts"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(200))

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id")
    )

    parent_concept_id: Mapped[int | None] = mapped_column(
        ForeignKey("concepts.id"),
        nullable=True,
    )

    is_atomic: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    skill: Mapped["Skill"] = relationship(
        back_populates="concepts"
    )

    misconceptions: Mapped[list["Misconception"]] = relationship(
        back_populates="concept",
        cascade="all, delete-orphan",
    )


class ConceptPrerequisite(Base):
    __tablename__ = "concept_prerequisites"

    id: Mapped[int] = mapped_column(primary_key=True)

    concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id")
    )

    prerequisite_concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id")
    )

    __table_args__ = (
        UniqueConstraint(
            "concept_id",
            "prerequisite_concept_id",
            name="uq_concept_prerequisite",
        ),
    )


class Misconception(Base):
    __tablename__ = "misconceptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(200))

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id")
    )

    concept: Mapped["Concept"] = relationship(
        back_populates="misconceptions"
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    stem: Mapped[str] = mapped_column(Text)

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    difficulty: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        default="ORIGINAL",
    )

    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    choices: Mapped[list["AnswerChoice"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )

    concept_links: Mapped[list["QuestionConcept"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )


class QuestionConcept(Base):
    __tablename__ = "question_concepts"

    id: Mapped[int] = mapped_column(primary_key=True)

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id")
    )

    concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id")
    )

    role: Mapped[str] = mapped_column(String(30))
    # PRIMARY, REQUIRED, SUPPORTING

    question: Mapped["Question"] = relationship(
        back_populates="concept_links"
    )

    __table_args__ = (
        UniqueConstraint(
            "question_id",
            "concept_id",
            "role",
            name="uq_question_concept_role",
        ),
    )


class AnswerChoice(Base):
    __tablename__ = "answer_choices"

    id: Mapped[int] = mapped_column(primary_key=True)

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id")
    )

    label: Mapped[str] = mapped_column(String(5))

    text: Mapped[str] = mapped_column(Text)

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    misconception_id: Mapped[int | None] = mapped_column(
        ForeignKey("misconceptions.id"),
        nullable=True,
    )

    question: Mapped["Question"] = relationship(
        back_populates="choices"
    )

    __table_args__ = (
        UniqueConstraint(
            "question_id",
            "label",
            name="uq_question_choice",
        ),
    )