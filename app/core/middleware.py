import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.constants.entry_point import EntryPoint
from app.core.security import decode_access_token
from app.db.base import set_current_user_id, clear_current_user_id

logger = logging.getLogger(__name__)


PUBLIC_PATHS = {
    "/api/v1/auth/login",
    "/api/v1/auth/internal/login",
    "/docs",
    "/docs/oauth2-redirect",
    "/openapi.json",
    "/redoc",
}


def _get_entry_point_from_path(path: str) -> int:
    if "/internal" in path:
        return EntryPoint.INTERNAL
    return EntryPoint.APP


class AuditContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path in PUBLIC_PATHS or path.startswith("/docs") or path.startswith("/openapi") or path.startswith("/redoc"):
            response = await call_next(request)
            return response
        
      
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            clear_current_user_id()
            return JSONResponse(
                status_code=401,
                content={"message": "Missing or invalid Authorization header","data": None}
            )
        
        try:
            token = auth_header[7:]  
            

            entry_point = _get_entry_point_from_path(request.url.path)
            
            payload = decode_access_token(token, entry_point=entry_point)
            user_id = payload.get("sub")
            if not user_id:
                clear_current_user_id()
                return JSONResponse(
                    status_code=401,
                    content={"message": "Invalid token: missing user ID","data": None}
                )
            set_current_user_id(user_id)
        except Exception as e:
            logger.debug(f"AuditContextMiddleware: Token validation failed: {e}")
            clear_current_user_id()
            return JSONResponse(
                status_code=401,
                content={"message": "Invalid or expired token","data": None}
            )
        
        try:
            response = await call_next(request)
        finally:
            clear_current_user_id()
        
        return response

