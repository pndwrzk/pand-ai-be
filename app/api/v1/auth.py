from fastapi import APIRouter, Depends

from app.constants.entry_point import EntryPoint
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

    token = service.login(request, EntryPoint.APP)

    return ApiResponse.success(
        message="Login successful",
        data=token,
        status_code=200,
    )
    
@router.post(
    "/internal/login",
    response_model=LoginResponse,
)
async def login_dashboard(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):

    token = service.login(request, entry_point=EntryPoint.INTERNAL)

    return ApiResponse.success(
        message="Login successful",
        data=token,
        status_code=200,
    )