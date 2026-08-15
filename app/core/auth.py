from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import decode_access_token
from app.exceptions.exceptions import UnauthorizedException


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):

    token = credentials.credentials

    

    try:
        payload = decode_access_token(token)


        return payload

    except Exception as e:
        raise UnauthorizedException("Invalid token") 