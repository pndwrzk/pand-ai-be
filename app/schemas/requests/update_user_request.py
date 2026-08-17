from pydantic import BaseModel
from pydantic import EmailStr

from app.constants.user_role import UserRole
from app.constants.user_status import UserStatus


class UpdateUserRequest(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = None
    role: UserRole | None = None
    status: UserStatus | None = None
