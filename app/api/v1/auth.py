from fastapi import APIRouter, Depends

from app.core.dependency import get_auth_service
from app.schemas.requests.login_request import LoginRequest
from app.schemas.responses.login_response import LoginResponse
from app.services.auth_service import AuthService
from app.common.response import ApiResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):

    token = service.login(request)

    return ApiResponse.success(
        message="Login successful",
        data=token,
        status_code=200,
    )