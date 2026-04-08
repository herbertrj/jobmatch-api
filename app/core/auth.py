from fastapi import Header, HTTPException, status
from jwt import InvalidTokenError

from app.core.security import decode_access_token


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
