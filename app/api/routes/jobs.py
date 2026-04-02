from fastapi import APIRouter, status

from app.db.session import SessionLocal
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse

router = APIRouter(prefix="/jobs", tags=["Vagas"])


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar vaga",
    description="Cria uma nova vaga com requisitos minimos e habilidades exigidas.",
)
def create_job(payload: JobCreate) -> JobResponse:
    # Persistencia simples em SQLite para manter o projeto leve.
    required_skills_text = ",".join(payload.required_skills)
    with SessionLocal() as db:
        job = Job(
            title=payload.title,
            company=payload.company,
            minimum_experience=payload.minimum_experience,
            required_skills_text=required_skills_text,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        return JobResponse(
            id=job.id,
            title=job.title,
            company=job.company,
            minimum_experience=job.minimum_experience,
            required_skills=[skill for skill in job.required_skills_text.split(",") if skill],
        )


@router.get(
    "",
    response_model=list[JobResponse],
    summary="Listar vagas",
    description="Retorna todas as vagas cadastradas no momento.",
)
def list_jobs() -> list[JobResponse]:
    with SessionLocal() as db:
        jobs = db.query(Job).all()
        return [
            JobResponse(
                id=job.id,
                title=job.title,
                company=job.company,
                minimum_experience=job.minimum_experience,
                required_skills=[
                    skill for skill in job.required_skills_text.split(",") if skill
                ],
            )
            for job in jobs
        ]
