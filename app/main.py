from fastapi import FastAPI

from app.api.routes.candidates import router as candidates_router
from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.match import router as match_router

app = FastAPI(
    title="JobMatch API",
    description="API para gerenciar candidatos, vagas e futura logica de compatibilidade.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(candidates_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(match_router, prefix="/api/v1")
