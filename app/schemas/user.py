from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr

from app.constants.user_role import UserRole
from app.constants.user_status import UserStatus


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str
    status: UserStatus = UserStatus.ACTIVE
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
