from fastapi import APIRouter, HTTPException, status

from app.api.routes.candidates import candidates_db
from app.api.routes.jobs import jobs_db
from app.schemas.candidate import CandidateResponse
from app.schemas.job import JobResponse
from app.schemas.match import CandidateMatchResult

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


@router.get(
    "/jobs/{job_id}/candidates",
    response_model=list[CandidateMatchResult],
    summary="Rankear candidatos por vaga",
    description="Retorna candidatos ordenados por score de compatibilidade para uma vaga.",
)
def match_candidates_for_job(job_id: int) -> list[CandidateMatchResult]:
    selected_job = next((job for job in jobs_db if job.id == job_id), None)
    if selected_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vaga nao encontrada.",
        )

    results = [calculate_score(candidate, selected_job) for candidate in candidates_db]
    return sorted(results, key=lambda item: item.score, reverse=True)
