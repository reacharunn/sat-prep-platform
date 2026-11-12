"""Bounded AI question proposals; generated content is not automatically published."""
import json
import os
from typing import Literal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field, model_validator

router = APIRouter(prefix="/api/ai", tags=["AI practice"])
TOPICS = {
    "math": {"Algebra", "Advanced Math", "Geometry & Trigonometry"},
    "english": {"Grammar", "Transitions", "Reading Comprehension"},
}


class GenerateRequest(BaseModel):
    subject: Literal["math", "english"]
    topic: str = Field(min_length=1, max_length=80)
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    count: int = Field(default=5, ge=1, le=10)


class GeneratedQuestion(BaseModel):
    subject: Literal["math", "english"]
    topic: str = Field(min_length=1, max_length=80)
    concept: str = Field(min_length=3, max_length=120)
    stem: str = Field(min_length=20, max_length=1500)
    choices: list[str] = Field(min_length=4, max_length=4)
    answer: int = Field(ge=0, le=3)
    explanation: str = Field(min_length=30, max_length=2000)
    distractor_misconceptions: list[str] = Field(min_length=4, max_length=4)

    @model_validator(mode="after")
    def validate_choices(self):
        normalized = [choice.strip().casefold() for choice in self.choices]
        if any(not c or len(c) > 350 for c in normalized):
            raise ValueError("Choices must be nonempty and at most 350 characters")
        if len(set(normalized)) != 4:
            raise ValueError("Choices must be distinct")
        if not self.distractor_misconceptions[self.answer].strip().lower() == "correct":
            raise ValueError("Correct choice misconception must be 'Correct'")
        if any(not s.strip() for s in self.distractor_misconceptions):
            raise ValueError("Misconception labels must be nonempty")
        return self


class GeneratedSet(BaseModel):
    questions: list[GeneratedQuestion]


def validate_set(raw: dict, request: GenerateRequest) -> GeneratedSet:
    result = GeneratedSet.model_validate(raw)
    if len(result.questions) != request.count:
        raise ValueError("Incorrect number of questions")
    if any(q.subject != request.subject or q.topic != request.topic for q in result.questions):
        raise ValueError("Subject/topic mismatch")
    if len({q.stem.strip().casefold() for q in result.questions}) != request.count:
        raise ValueError("Duplicate questions")
    return result


def generate(request: GenerateRequest) -> GeneratedSet:
    if request.topic not in TOPICS[request.subject]:
        raise ValueError("Unsupported SAT topic")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("AI provider not configured")
    model = os.getenv("SAT_AI_MODEL", "gpt-4o-mini")
    instructions = (
        "You are a careful SAT practice item writer. Produce entirely original, "
        "self-contained multiple-choice questions. Never copy official SAT items. "
        "Return a JSON object with a questions array. Each item must have subject, "
        "topic, concept, stem, choices (exactly four strings), answer (zero-based "
        "index), explanation, and distractor_misconceptions (four strings, with "
        "'Correct' at the right answer index). Make wrong choices reflect plausible "
        "student errors. Provide rigorous step-by-step explanations. For Math, "
        "independently check arithmetic, uniqueness and solvability; for English, "
        "ensure exactly one defensible choice. Avoid ambiguous wording, outside "
        "sources, images, copyrighted passages and personal information. "
        "Do not include markdown fences or extra text."
    )
    prompt = (
        f"Create {request.count} distinct SAT-style questions. "
        f"Subject: {request.subject}. Topic: {request.topic}. "
        f"Difficulty: {request.difficulty}. Return valid JSON only."
    )
    payload = {
        "model": model,
        "temperature": 0.6,
        "max_tokens": 6500,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt},
        ],
    }
    http_request = Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(http_request, timeout=45) as response:
        data = json.load(response)
    raw = json.loads(data["choices"][0]["message"]["content"])
    return validate_set(raw, request)


@router.post("/generate", response_model=GeneratedSet)
def generate_questions(payload: GenerateRequest, x_practice_token: str | None = Header(None)):
    configured_token = os.getenv("SAT_PRACTICE_TOKEN", "")
    if not configured_token:
        raise HTTPException(status_code=503, detail="Practice access is not configured")
    import hmac
    if not x_practice_token or not hmac.compare_digest(x_practice_token, configured_token):
        raise HTTPException(status_code=401, detail="Invalid practice access token")
    if payload.topic not in TOPICS[payload.subject]:
        raise HTTPException(status_code=422, detail="Unsupported SAT topic")
    try:
        return generate(payload)
    except RuntimeError:
        raise HTTPException(status_code=503, detail="AI provider not configured") from None
    except (ValueError, KeyError, TypeError):
        raise HTTPException(status_code=502, detail="Generated questions failed validation") from None
    except (HTTPError, URLError, TimeoutError, OSError):
        raise HTTPException(status_code=502, detail="AI provider unavailable") from None
