from pydantic import BaseModel
from pydantic import EmailStr

from app.constants.user_role import UserRole
from app.constants.user_status import UserStatus


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE
