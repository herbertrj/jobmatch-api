from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar usuario",
    description="Cria um usuario para acessar rotas protegidas da API.",
)
def register(payload: RegisterRequest) -> UserResponse:
    with SessionLocal() as db:
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email ja cadastrado.",
            )

        user = User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserResponse(id=user.id, full_name=user.full_name, email=user.email)


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Realizar login",
    description="Autentica um usuario e retorna um token JWT.",
)
def login(payload: LoginRequest) -> AuthResponse:
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == payload.email).first()
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais invalidas.",
            )

        token = create_access_token(user_id=user.id, email=user.email)
        return AuthResponse(access_token=token)
