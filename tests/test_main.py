import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Garante que a raiz do projeto esteja no path durante os testes.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.job import Job
from app.main import app

client = TestClient(app)


def reset_database_data() -> None:
    with SessionLocal() as db:
        db.query(Candidate).delete()
        db.query(Job).delete()
        db.commit()


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_candidate() -> None:
    reset_database_data()

    payload = {
        "full_name": "Herbert Albuquerque",
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
    reset_database_data()

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


def test_search_candidates_with_filters() -> None:
    reset_database_data()

    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Carla Dev",
            "email": "carla@example.com",
            "years_of_experience": 3,
            "skills": ["python", "sql"],
        },
    )
    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Diego Jr",
            "email": "diego@example.com",
            "years_of_experience": 1,
            "skills": ["javascript"],
        },
    )

    response = client.get("/api/v1/candidates/search?skill=python&min_experience=2")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["full_name"] == "Carla Dev"


def test_match_jobs_for_candidate() -> None:
    reset_database_data()

    candidate_response = client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Pedro Backend",
            "email": "pedro@example.com",
            "years_of_experience": 2,
            "skills": ["python", "fastapi", "sql"],
        },
    )
    candidate_id = candidate_response.json()["id"]

    client.post(
        "/api/v1/jobs",
        json={
            "title": "Python Developer",
            "company": "Alpha",
            "minimum_experience": 1,
            "required_skills": ["python", "fastapi"],
        },
    )
    client.post(
        "/api/v1/jobs",
        json={
            "title": "Front-end Intern",
            "company": "Beta",
            "minimum_experience": 0,
            "required_skills": ["javascript", "react"],
        },
    )

    response = client.get(f"/api/v1/match/candidates/{candidate_id}/jobs")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 2
    assert body[0]["job_title"] == "Python Developer"
    assert body[0]["score"] >= body[1]["score"]
