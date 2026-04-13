from fastapi import Header, HTTPException, status
from jwt import InvalidTokenError

from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User


def require_auth(authorization: str | None = Header(default=None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente ou invalido.",
        )

    token = authorization.replace("Bearer ", "", 1)
    try:
        payload = decode_access_token(token)
        return int(payload["sub"])
    except (InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido.",
        ) from None


def get_current_user(authorization: str | None = Header(default=None)) -> User:
    user_id = require_auth(authorization)
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario nao encontrado.",
            )
        return user
