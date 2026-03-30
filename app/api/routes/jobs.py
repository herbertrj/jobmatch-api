from fastapi import APIRouter, status

from app.schemas.job import JobCreate, JobResponse

router = APIRouter(prefix="/jobs", tags=["Vagas"])

jobs_db: list[JobResponse] = []


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar vaga",
    description="Cria uma nova vaga com requisitos minimos e habilidades exigidas.",
)
def create_job(payload: JobCreate) -> JobResponse:
    # Armazenamento em memoria para acelerar a entrega do MVP.
    job = JobResponse(id=len(jobs_db) + 1, **payload.model_dump())
    jobs_db.append(job)
    return job


@router.get(
    "",
    response_model=list[JobResponse],
    summary="Listar vagas",
    description="Retorna todas as vagas cadastradas no momento.",
)
def list_jobs() -> list[JobResponse]:
    return jobs_db
