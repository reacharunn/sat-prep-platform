from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SAT Prep Taxonomy API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/domains", response_model=schemas.DomainOut)
def create_domain(payload: schemas.DomainCreate, db: Session = Depends(get_db)):
    obj = models.Domain(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/domains", response_model=list[schemas.DomainOut])
def list_domains(db: Session = Depends(get_db)):
    return db.query(models.Domain).all()

@app.post("/skills", response_model=schemas.SkillOut)
def create_skill(payload: schemas.SkillCreate, db: Session = Depends(get_db)):
    if not db.get(models.Domain, payload.domain_id):
        raise HTTPException(404, "Domain not found")
    obj = models.Skill(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/skills", response_model=list[schemas.SkillOut])
def list_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()

@app.post("/concepts", response_model=schemas.ConceptOut)
def create_concept(payload: schemas.ConceptCreate, db: Session = Depends(get_db)):
    if not db.get(models.Skill, payload.skill_id):
        raise HTTPException(404, "Skill not found")
    obj = models.Concept(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/concepts", response_model=list[schemas.ConceptOut])
def list_concepts(db: Session = Depends(get_db)):
    return db.query(models.Concept).all()

@app.post("/misconceptions", response_model=schemas.MisconceptionOut)
def create_misconception(payload: schemas.MisconceptionCreate, db: Session = Depends(get_db)):
    if not db.get(models.Concept, payload.concept_id):
        raise HTTPException(404, "Concept not found")
    obj = models.Misconception(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/misconceptions", response_model=list[schemas.MisconceptionOut])
def list_misconceptions(db: Session = Depends(get_db)):
    return db.query(models.Misconception).all()
