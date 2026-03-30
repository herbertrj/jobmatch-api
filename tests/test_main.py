from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_candidate() -> None:
    payload = {
        "full_name": "Herbert Silva",
        "email": "herbert@example.com",
        "years_of_experience": 1,
        "skills": ["python", "fastapi"],
    }
    response = client.post("/api/v1/candidates", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["full_name"] == payload["full_name"]
    assert body["id"] >= 1
