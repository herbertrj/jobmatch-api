from fastapi.testclient import TestClient

from app.api.routes.candidates import candidates_db
from app.api.routes.jobs import jobs_db
from app.main import app

client = TestClient(app)


def reset_in_memory_data() -> None:
    candidates_db.clear()
    jobs_db.clear()


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_candidate() -> None:
    reset_in_memory_data()

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


def test_match_candidates_for_job() -> None:
    reset_in_memory_data()

    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Ana Souza",
            "email": "ana@example.com",
            "years_of_experience": 2,
            "skills": ["python", "fastapi", "sql"],
        },
    )
    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Bruno Lima",
            "email": "bruno@example.com",
            "years_of_experience": 0,
            "skills": ["python"],
        },
    )
    job_response = client.post(
        "/api/v1/jobs",
        json={
            "title": "Backend Intern",
            "company": "TechCo",
            "minimum_experience": 1,
            "required_skills": ["python", "fastapi"],
        },
    )
    job_id = job_response.json()["id"]

    response = client.get(f"/api/v1/match/jobs/{job_id}/candidates")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 2
    assert body[0]["candidate_name"] == "Ana Souza"
    assert body[0]["score"] >= body[1]["score"]
