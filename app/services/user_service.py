from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.requests.create_user_request import CreateUserRequest
from app.exceptions import ConflictException

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, dto: CreateUserRequest) -> User:
      
        if self.repository.find_by_email(dto.email):
            raise ConflictException(
                message="Email already exists"
            )

      
        if self.repository.find_by_username(dto.username):
            raise ConflictException(
                message="Username already exists"
            )

   
        user = User(
            email=dto.email,
            username=dto.username,
            full_name=dto.full_name,
            password=hash_password(dto.password),
        )

        return self.repository.create(user)

   