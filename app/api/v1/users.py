from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.core.auth import require_superadmin
from app.core.dependency import get_user_service
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.schemas.requests.create_user_request import CreateUserRequest
from app.schemas.requests.update_user_request import UpdateUserRequest
from app.common.response import ApiResponse

router = APIRouter(
    prefix="/internal/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
async def get_users(
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_superadmin),
):

    users = service.get_all()

    return ApiResponse.success(
        message="Users retrieved successfully",
        data=[UserResponse.model_validate(user).model_dump() for user in users],
    )


@router.get(
    "/{id}",
    response_model=UserResponse,
)
async def get_user(
    id: UUID,
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_superadmin),
):

    user = service.get_by_id(id)

    return ApiResponse.success(
        message="User retrieved successfully",
        data=UserResponse.model_validate(user).model_dump(),
    )


@router.post(
    "",
    response_model=UserResponse,
)
async def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_superadmin),
):

    user = service.create(request)

    return ApiResponse.success(
        message="User created successfully",
        data=UserResponse.model_validate(user).model_dump(),
        status_code=201,
    )


@router.put(
    "/{id}",
    response_model=UserResponse,
)
async def update_user(
    id: UUID,
    request: UpdateUserRequest,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_superadmin),
):

    user = service.update(id, request)

    return ApiResponse.success(
        message="User updated successfully",
        data=UserResponse.model_validate(user).model_dump(),
    )


@router.delete(
    "/{id}",
)
async def delete_user(
    id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_superadmin),
):

    service.delete(id, current_user_id=current_user.id)

    return ApiResponse.success(
        message="User deleted successfully",
    )
