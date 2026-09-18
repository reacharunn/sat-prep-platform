from pydantic import BaseModel, ConfigDict

class DomainCreate(BaseModel):
    code: str
    name: str

class DomainOut(DomainCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SkillCreate(BaseModel):
    code: str
    name: str
    domain_id: int

class SkillOut(SkillCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ConceptCreate(BaseModel):
    code: str
    name: str
    description: str | None = None
    skill_id: int
    is_atomic: bool = True

class ConceptOut(ConceptCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MisconceptionCreate(BaseModel):
    code: str
    name: str
    description: str | None = None
    concept_id: int

class MisconceptionOut(MisconceptionCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
