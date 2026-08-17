from fastapi import APIRouter, Depends

from app.constants.entry_point import EntryPoint
from app.constants.user_role import UserRole
from app.core.auth import get_current_active_app_user, get_current_active_user
from app.core.dependency import get_auth_service
from app.models.user import User
from app.schemas.requests.login_request import LoginRequest
from app.schemas.responses.internal_me_response import InternalMeResponse
from app.schemas.responses.login_response import LoginResponse
from app.schemas.responses.me_response import MeResponse
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


@router.get(
    "/me",
    response_model=MeResponse,
)
async def get_me(
    current_user: User = Depends(get_current_active_app_user),
):

    data = MeResponse(
        name=current_user.full_name,
        email=current_user.email,
        username=current_user.username,
    )

    return ApiResponse.success(
        message="User retrieved successfully",
        data=data.model_dump(),
    )


@router.get(
    "/internal/me",
    response_model=InternalMeResponse,
)
async def get_internal_me(
    current_user: User = Depends(get_current_active_user),
):

    data = InternalMeResponse(
        role=UserRole(current_user.role),
        name=current_user.full_name,
        email=current_user.email,
        username=current_user.username,
    )

    return ApiResponse.success(
        message="User retrieved successfully",
        data=data.model_dump(),
    )