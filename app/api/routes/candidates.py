from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.core.auth import require_auth
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse

router = APIRouter(prefix="/candidates", tags=["Candidatos"])


def to_candidate_response(candidate: Candidate) -> CandidateResponse:
    return CandidateResponse(
        id=candidate.id,
        full_name=candidate.full_name,
        email=candidate.email,
        years_of_experience=candidate.years_of_experience,
        skills=[skill for skill in candidate.skills_text.split(",") if skill],
    )


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar candidato",
    description="Cria um novo candidato com dados basicos e lista de habilidades.",
)
def create_candidate(
    payload: CandidateCreate,
    _: int = Depends(require_auth),
) -> CandidateResponse:
    # Persistencia simples em SQLite para manter o projeto leve.
    skills_text = ",".join(payload.skills)
    with SessionLocal() as db:
        candidate = Candidate(
            full_name=payload.full_name,
            email=payload.email,
            years_of_experience=payload.years_of_experience,
            skills_text=skills_text,
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        return to_candidate_response(candidate)


@router.get(
    "",
    response_model=list[CandidateResponse],
    summary="Listar candidatos",
    description="Retorna todos os candidatos cadastrados ate o momento.",
)
def list_candidates(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[CandidateResponse]:
    with SessionLocal() as db:
        candidates = db.query(Candidate).order_by(Candidate.id).offset(skip).limit(limit).all()
        return [to_candidate_response(candidate) for candidate in candidates]


@router.get(
    "/search",
    response_model=list[CandidateResponse],
    summary="Buscar candidatos com filtros",
    description="Filtra candidatos por habilidade e experiencia minima.",
)
def search_candidates(
    skill: str | None = Query(default=None),
    min_experience: int | None = Query(default=None, ge=0),
) -> list[CandidateResponse]:
    with SessionLocal() as db:
        candidates = db.query(Candidate).all()
        results: list[CandidateResponse] = []

        for candidate in candidates:
            candidate_skills = [
                item.strip().lower()
                for item in candidate.skills_text.split(",")
                if item.strip()
            ]

            if skill and skill.lower() not in candidate_skills:
                continue

            if (
                min_experience is not None
                and candidate.years_of_experience < min_experience
            ):
                continue

            results.append(
                to_candidate_response(candidate)
            )

        return results


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
    summary="Buscar candidato por id",
    description="Retorna os dados completos de um candidato especifico.",
)
def get_candidate(candidate_id: int) -> CandidateResponse:
    with SessionLocal() as db:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidato nao encontrado.",
            )
        return to_candidate_response(candidate)


@router.put(
    "/{candidate_id}",
    response_model=CandidateResponse,
    summary="Atualizar candidato",
    description="Atualiza todos os dados de um candidato existente.",
)
def update_candidate(
    candidate_id: int,
    payload: CandidateCreate,
    _: int = Depends(require_auth),
) -> CandidateResponse:
    with SessionLocal() as db:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidato nao encontrado.",
            )

        candidate.full_name = payload.full_name
        candidate.email = payload.email
        candidate.years_of_experience = payload.years_of_experience
        candidate.skills_text = ",".join(payload.skills)

        db.commit()
        db.refresh(candidate)
        return to_candidate_response(candidate)


@router.delete(
    "/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover candidato",
    description="Remove um candidato pelo identificador informado.",
)
def delete_candidate(
    candidate_id: int,
    _: int = Depends(require_auth),
) -> Response:
    with SessionLocal() as db:
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidato nao encontrado.",
            )

        db.delete(candidate)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
