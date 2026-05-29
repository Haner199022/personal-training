"""鉴权依赖：从 Bearer token 解出当前 coach_id。"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.core.security import decode_token

_bearer = HTTPBearer(auto_error=False)


async def get_current_coach_id(
    cred: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> int:
    if cred is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    try:
        payload = decode_token(cred.credentials)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    sub = payload.get("sub", "")
    if payload.get("role") != "coach" or not sub.startswith("coach:"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not a coach token")
    return int(sub.split(":", 1)[1])
