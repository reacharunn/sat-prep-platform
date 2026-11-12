import pytest
from fastapi.testclient import TestClient

from app.ai_questions import GenerateRequest, GeneratedQuestion, validate_set
from app.main import app

client = TestClient(app)


def example():
    return {
        "subject": "math", "topic": "Algebra", "concept": "Linear equations",
        "stem": "If twice a number plus four is ten, what is the number?",
        "choices": ["2", "3", "4", "5"], "answer": 1,
        "explanation": "Subtract four from both sides, then divide by two to obtain three.",
        "distractor_misconceptions": ["Subtracts incorrectly", "Correct", "Divides incorrectly", "Guesses"],
    }


def test_valid_set():
    request = GenerateRequest(subject="math", topic="Algebra", count=1)
    assert validate_set({"questions": [example()]}, request).questions[0].answer == 1


@pytest.mark.parametrize("change", [
    {"choices": ["3", "3", "4", "5"]},
    {"answer": 4},
    {"distractor_misconceptions": ["a", "b", "c", "d"]},
])
def test_rejects_bad_questions(change):
    with pytest.raises(ValueError):
        GeneratedQuestion.model_validate({**example(), **change})


def test_rejects_duplicates():
    request = GenerateRequest(subject="math", topic="Algebra", count=2)
    with pytest.raises(ValueError):
        validate_set({"questions": [example(), example()]}, request)


def test_authentication_required(monkeypatch):
    monkeypatch.setenv("SAT_PRACTICE_TOKEN", "secret-for-tests")
    response = client.post("/api/ai/generate", json={
        "subject": "math", "topic": "Algebra", "count": 1
    })
    assert response.status_code == 401


def test_provider_mock(monkeypatch):
    monkeypatch.setenv("SAT_PRACTICE_TOKEN", "secret-for-tests")
    monkeypatch.setattr("app.ai_questions.generate", lambda request: validate_set(
        {"questions": [example()]}, request
    ))
    response = client.post(
        "/api/ai/generate",
        headers={"x-practice-token": "secret-for-tests"},
        json={"subject": "math", "topic": "Algebra", "count": 1},
    )
    assert response.status_code == 200
    assert response.json()["questions"][0]["answer"] == 1


def test_bad_topic(monkeypatch):
    monkeypatch.setenv("SAT_PRACTICE_TOKEN", "secret-for-tests")
    response = client.post(
        "/api/ai/generate",
        headers={"x-practice-token": "secret-for-tests"},
        json={"subject": "math", "topic": "Not a topic", "count": 1},
    )
    assert response.status_code == 422
