from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.db.base import clear_current_user_id
from app.exceptions.exceptions import UnauthorizedException

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Generator[dict, None, None]:
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except Exception:
        clear_current_user_id()
        raise UnauthorizedException("Invalid token")

    try:
        yield payload
    finally:
        clear_current_user_id()