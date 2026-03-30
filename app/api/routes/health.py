from fastapi import APIRouter

router = APIRouter(tags=["Saude"])


@router.get(
    "/health",
    summary="Verificar status da API",
    description="Retorna o status atual da API para monitoramento basico.",
)
def health_check() -> dict[str, str]:
    # Endpoint simples para validar se a API esta no ar.
    return {"status": "ok"}


@router.get(
    "/version",
    summary="Consultar versao da API",
    description="Retorna o nome da aplicacao e a versao atual do projeto.",
)
def version() -> dict[str, str]:
    return {"app": "JobMatch API", "version": "0.1.0"}
