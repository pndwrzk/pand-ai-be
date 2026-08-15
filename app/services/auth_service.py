from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.requests.login_request import LoginRequest
from app.schemas.responses.login_response import LoginResponse
from app.exceptions import UnauthorizedException


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def login(self, dto: LoginRequest) -> LoginResponse:

        user = self.repository.find_by_email(dto.email)

        if user is None:
            raise UnauthorizedException(
                message="Invalid email or password"
            )

        if not verify_password(dto.password, user.password):
            raise UnauthorizedException(
                message="Invalid email or password"
            )

        token = create_access_token(
            {"sub": str(user.id)}
        )

        return LoginResponse(
            access_token=token,
            token_type="Bearer",
        )