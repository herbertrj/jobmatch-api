from fastapi import APIRouter, status

from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse

router = APIRouter(prefix="/candidates", tags=["Candidatos"])


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar candidato",
    description="Cria um novo candidato com dados basicos e lista de habilidades.",
)
def create_candidate(payload: CandidateCreate) -> CandidateResponse:
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

        return CandidateResponse(
            id=candidate.id,
            full_name=candidate.full_name,
            email=candidate.email,
            years_of_experience=candidate.years_of_experience,
            skills=[skill for skill in candidate.skills_text.split(",") if skill],
        )


@router.get(
    "",
    response_model=list[CandidateResponse],
    summary="Listar candidatos",
    description="Retorna todos os candidatos cadastrados ate o momento.",
)
def list_candidates() -> list[CandidateResponse]:
    with SessionLocal() as db:
        candidates = db.query(Candidate).all()
        return [
            CandidateResponse(
                id=candidate.id,
                full_name=candidate.full_name,
                email=candidate.email,
                years_of_experience=candidate.years_of_experience,
                skills=[skill for skill in candidate.skills_text.split(",") if skill],
            )
            for candidate in candidates
        ]
