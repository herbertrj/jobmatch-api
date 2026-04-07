from fastapi import APIRouter, HTTPException, status

from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.job import Job
from app.schemas.candidate import CandidateResponse
from app.schemas.job import JobResponse
from app.schemas.match import CandidateMatchResult, JobMatchResult

router = APIRouter(prefix="/match", tags=["Compatibilidade"])


def calculate_score(candidate: CandidateResponse, job: JobResponse) -> CandidateMatchResult:
    # Regra simples para o Dia 2: skills valem mais, experiencia complementa.
    candidate_skills = {skill.lower() for skill in candidate.skills}
    required_skills = {skill.lower() for skill in job.required_skills}

    matched_skills = sorted(required_skills.intersection(candidate_skills))
    missing_skills = sorted(required_skills.difference(candidate_skills))

    score = len(matched_skills) * 20
    experience_ok = candidate.years_of_experience >= job.minimum_experience
    if experience_ok:
        score += 20

    return CandidateMatchResult(
        candidate_id=candidate.id,
        candidate_name=candidate.full_name,
        score=min(score, 100),
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        experience_ok=experience_ok,
    )


def parse_candidate(candidate: Candidate) -> CandidateResponse:
    return CandidateResponse(
        id=candidate.id,
        full_name=candidate.full_name,
        email=candidate.email,
        years_of_experience=candidate.years_of_experience,
        skills=[skill for skill in candidate.skills_text.split(",") if skill],
    )


def parse_job(job: Job) -> JobResponse:
    return JobResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        minimum_experience=job.minimum_experience,
        required_skills=[skill for skill in job.required_skills_text.split(",") if skill],
    )


@router.get(
    "/jobs/{job_id}/candidates",
    response_model=list[CandidateMatchResult],
    summary="Rankear candidatos por vaga",
    description="Retorna candidatos ordenados por score de compatibilidade para uma vaga.",
)
def match_candidates_for_job(job_id: int) -> list[CandidateMatchResult]:
    with SessionLocal() as db:
        selected_job = db.query(Job).filter(Job.id == job_id).first()
        if selected_job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vaga nao encontrada.",
            )

        job_data = parse_job(selected_job)

        candidates = db.query(Candidate).all()
        candidate_data = [parse_candidate(candidate) for candidate in candidates]

        results = [calculate_score(candidate, job_data) for candidate in candidate_data]
        return sorted(results, key=lambda item: item.score, reverse=True)


@router.get(
    "/candidates/{candidate_id}/jobs",
    response_model=list[JobMatchResult],
    summary="Rankear vagas por candidato",
    description="Retorna vagas ordenadas por score de compatibilidade para um candidato.",
)
def match_jobs_for_candidate(candidate_id: int) -> list[JobMatchResult]:
    with SessionLocal() as db:
        selected_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if selected_candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidato nao encontrado.",
            )

        candidate_data = parse_candidate(selected_candidate)
        jobs = db.query(Job).all()
        results: list[JobMatchResult] = []

        for job in jobs:
            job_data = parse_job(job)
            candidate_result = calculate_score(candidate_data, job_data)
            results.append(
                JobMatchResult(
                    job_id=job_data.id,
                    job_title=job_data.title,
                    company=job_data.company,
                    score=candidate_result.score,
                    matched_skills=candidate_result.matched_skills,
                    missing_skills=candidate_result.missing_skills,
                    experience_ok=candidate_result.experience_ok,
                )
            )

        return sorted(results, key=lambda item: item.score, reverse=True)
