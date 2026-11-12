from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_practice_page():
    response = client.get("/practice")
    assert response.status_code == 200
    assert "Divya SAT Prep" in response.text
    assert 'name="viewport"' in response.text

def test_static_assets():
    for name in ("app.js", "style.css"):
        response = client.get(f"/practice/static/{name}")
        assert response.status_code == 200
    assert "Reading Comprehension" in client.get("/practice/static/app.js").text

def test_source_file_line_limit():
    root = Path(__file__).resolve().parents[1]
    for path in (root / "app" / "practice").rglob("*"):
        if path.is_file() and path.suffix in {".js", ".css", ".html", ".py"}:
            assert len(path.read_text(encoding="utf-8").splitlines()) <= 500, str(path)
