import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Garante que a raiz do projeto esteja no path durante os testes.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.user import User
from app.main import app

client = TestClient(app)


def reset_database_data() -> None:
    with SessionLocal() as db:
        db.query(Candidate).delete()
        db.query(Job).delete()
        db.query(User).delete()
        db.commit()


def create_auth_header() -> dict[str, str]:
    register_payload = {
        "full_name": "Test User",
        "email": "testuser@example.com",
        "password": "123456",
    }
    client.post("/api/v1/auth/register", json=register_payload)
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_candidate() -> None:
    reset_database_data()
    headers = create_auth_header()

    payload = {
        "full_name": "Herbert Albuquerque",
        "email": "herbert@example.com",
        "years_of_experience": 1,
        "skills": ["python", "fastapi"],
    }
    response = client.post("/api/v1/candidates", json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 201
    assert body["full_name"] == payload["full_name"]
    assert body["id"] >= 1


def test_match_candidates_for_job() -> None:
    reset_database_data()
    headers = create_auth_header()

    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Ana Souza",
            "email": "ana@example.com",
            "years_of_experience": 2,
            "skills": ["python", "fastapi", "sql"],
        },
        headers=headers,
    )
    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Bruno Lima",
            "email": "bruno@example.com",
            "years_of_experience": 0,
            "skills": ["python"],
        },
        headers=headers,
    )
    job_response = client.post(
        "/api/v1/jobs",
        json={
            "title": "Backend Intern",
            "company": "TechCo",
            "minimum_experience": 1,
            "required_skills": ["python", "fastapi"],
        },
        headers=headers,
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
    headers = create_auth_header()

    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Carla Dev",
            "email": "carla@example.com",
            "years_of_experience": 3,
            "skills": ["python", "sql"],
        },
        headers=headers,
    )
    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Diego Jr",
            "email": "diego@example.com",
            "years_of_experience": 1,
            "skills": ["javascript"],
        },
        headers=headers,
    )

    response = client.get("/api/v1/candidates/search?skill=python&min_experience=2")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["full_name"] == "Carla Dev"


def test_match_jobs_for_candidate() -> None:
    reset_database_data()
    headers = create_auth_header()

    candidate_response = client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Pedro Backend",
            "email": "pedro@example.com",
            "years_of_experience": 2,
            "skills": ["python", "fastapi", "sql"],
        },
        headers=headers,
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
        headers=headers,
    )
    client.post(
        "/api/v1/jobs",
        json={
            "title": "Front-end Intern",
            "company": "Beta",
            "minimum_experience": 0,
            "required_skills": ["javascript", "react"],
        },
        headers=headers,
    )

    response = client.get(f"/api/v1/match/candidates/{candidate_id}/jobs")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 2
    assert body[0]["job_title"] == "Python Developer"
    assert body[0]["score"] >= body[1]["score"]


def test_create_candidate_requires_auth() -> None:
    reset_database_data()
    response = client.post(
        "/api/v1/candidates",
        json={
            "full_name": "No Auth",
            "email": "noauth@example.com",
            "years_of_experience": 1,
            "skills": ["python"],
        },
    )
    assert response.status_code == 401


def test_auth_me_returns_logged_user() -> None:
    reset_database_data()
    headers = create_auth_header()

    response = client.get("/api/v1/auth/me", headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body["full_name"] == "Test User"
    assert body["email"] == "testuser@example.com"


def test_auth_me_requires_token() -> None:
    reset_database_data()
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_list_candidates_with_pagination() -> None:
    reset_database_data()
    headers = create_auth_header()

    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Candidate One",
            "email": "one@example.com",
            "years_of_experience": 1,
            "skills": ["python"],
        },
        headers=headers,
    )
    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Candidate Two",
            "email": "two@example.com",
            "years_of_experience": 2,
            "skills": ["fastapi"],
        },
        headers=headers,
    )
    client.post(
        "/api/v1/candidates",
        json={
            "full_name": "Candidate Three",
            "email": "three@example.com",
            "years_of_experience": 3,
            "skills": ["sql"],
        },
        headers=headers,
    )

    response = client.get("/api/v1/candidates?skip=1&limit=1")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["full_name"] == "Candidate Two"


def test_list_jobs_with_pagination() -> None:
    reset_database_data()
    headers = create_auth_header()

    client.post(
        "/api/v1/jobs",
        json={
            "title": "Job One",
            "company": "AA",
            "minimum_experience": 0,
            "required_skills": ["python"],
        },
        headers=headers,
    )
    client.post(
        "/api/v1/jobs",
        json={
            "title": "Job Two",
            "company": "BB",
            "minimum_experience": 1,
            "required_skills": ["sql"],
        },
        headers=headers,
    )
    client.post(
        "/api/v1/jobs",
        json={
            "title": "Job Three",
            "company": "CC",
            "minimum_experience": 2,
            "required_skills": ["fastapi"],
        },
        headers=headers,
    )

    response = client.get("/api/v1/jobs?skip=2&limit=1")
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["title"] == "Job Three"
