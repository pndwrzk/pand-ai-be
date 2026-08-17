from uuid import UUID

from app.constants.user_role import UserRole
from app.constants.user_status import UserStatus
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.requests.create_user_request import CreateUserRequest
from app.schemas.requests.update_user_request import UpdateUserRequest
from app.schemas.user import UserCreate
from app.exceptions import ConflictException, NotFoundException, ForbiddenException


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all(self):

        return self.repository.find_all()

    def get_by_id(self, user_id: UUID) -> User:

        user = self.repository.find_by_id(user_id)

        if not user:
            raise NotFoundException(
                message="User not found"
            )

        return user

    def create(self, dto: CreateUserRequest) -> User:

        if self.repository.find_by_email(dto.email):
            raise ConflictException(
                message="Email already exists"
            )

        if self.repository.find_by_username(dto.username):
            raise ConflictException(
                message="Username already exists"
            )

        user = UserCreate(
            email=dto.email,
            username=dto.username,
            full_name=dto.full_name,
            password=hash_password(dto.password),
            status=dto.status,
            role=dto.role,
        )

        return self.repository.create(user)

    def update(self, user_id: UUID, dto: UpdateUserRequest) -> User:

        user = self.get_by_id(user_id)

        if dto.email is not None and dto.email != user.email:
            if self.repository.find_by_email(dto.email):
                raise ConflictException(
                    message="Email already exists"
                )
            user.email = dto.email

        if dto.username is not None and dto.username != user.username:
            if self.repository.find_by_username(dto.username):
                raise ConflictException(
                    message="Username already exists"
                )
            user.username = dto.username

        if dto.full_name is not None:
            user.full_name = dto.full_name

        if dto.password is not None:
            user.password = hash_password(dto.password)

        if dto.role is not None:
            user.role = int(dto.role)

        if dto.status is not None:
            user.status = int(dto.status)

        return self.repository.update(user)

    def delete(self, user_id: UUID, current_user_id: UUID | None = None) -> None:

        user = self.get_by_id(user_id)

        if current_user_id is not None and user.id == current_user_id:
            raise ForbiddenException(
                message="You cannot delete your own account"
            )

        self.repository.delete(user)
