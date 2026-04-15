from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.core.auth import require_auth
from app.db.session import SessionLocal
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse

router = APIRouter(prefix="/jobs", tags=["Vagas"])


def to_job_response(job: Job) -> JobResponse:
    return JobResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        minimum_experience=job.minimum_experience,
        required_skills=[skill for skill in job.required_skills_text.split(",") if skill],
    )


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar vaga",
    description="Cria uma nova vaga com requisitos minimos e habilidades exigidas.",
)
def create_job(
    payload: JobCreate,
    _: int = Depends(require_auth),
) -> JobResponse:
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
        return to_job_response(job)


@router.get(
    "",
    response_model=list[JobResponse],
    summary="Listar vagas",
    description="Retorna todas as vagas cadastradas no momento.",
)
def list_jobs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[JobResponse]:
    with SessionLocal() as db:
        jobs = db.query(Job).order_by(Job.id).offset(skip).limit(limit).all()
        return [to_job_response(job) for job in jobs]


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Buscar vaga por id",
    description="Retorna os dados completos de uma vaga especifica.",
)
def get_job(job_id: int) -> JobResponse:
    with SessionLocal() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vaga nao encontrada.",
            )
        return to_job_response(job)


@router.put(
    "/{job_id}",
    response_model=JobResponse,
    summary="Atualizar vaga",
    description="Atualiza todos os dados de uma vaga existente.",
)
def update_job(
    job_id: int,
    payload: JobCreate,
    _: int = Depends(require_auth),
) -> JobResponse:
    with SessionLocal() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vaga nao encontrada.",
            )

        job.title = payload.title
        job.company = payload.company
        job.minimum_experience = payload.minimum_experience
        job.required_skills_text = ",".join(payload.required_skills)

        db.commit()
        db.refresh(job)
        return to_job_response(job)


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover vaga",
    description="Remove uma vaga pelo identificador informado.",
)
def delete_job(
    job_id: int,
    _: int = Depends(require_auth),
) -> Response:
    with SessionLocal() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vaga nao encontrada.",
            )

        db.delete(job)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
