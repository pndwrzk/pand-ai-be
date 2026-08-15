from fastapi import APIRouter
from fastapi import Depends

from app.core.dependency import get_user_service
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.schemas.requests.create_user_request import CreateUserRequest
from app.common.response import ApiResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    "",
    response_model=UserResponse,
)
async def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(get_user_service),
):

    user = service.create(request)

    return ApiResponse.success(
        message="User created successfully",
        data=UserResponse.model_validate(user).model_dump(),    
        status_code=201,
    )

