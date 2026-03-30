from fastapi import APIRouter, status

from app.schemas.candidate import CandidateCreate, CandidateResponse

router = APIRouter(prefix="/candidates", tags=["Candidatos"])

candidates_db: list[CandidateResponse] = []


@router.post(
    "",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar candidato",
    description="Cria um novo candidato com dados basicos e lista de habilidades.",
)
def create_candidate(payload: CandidateCreate) -> CandidateResponse:
    # Armazenamento em memoria para o primeiro dia de projeto.
    candidate = CandidateResponse(id=len(candidates_db) + 1, **payload.model_dump())
    candidates_db.append(candidate)
    return candidate


@router.get(
    "",
    response_model=list[CandidateResponse],
    summary="Listar candidatos",
    description="Retorna todos os candidatos cadastrados ate o momento.",
)
def list_candidates() -> list[CandidateResponse]:
    return candidates_db
