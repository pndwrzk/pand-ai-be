from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str


class UserUpdate(BaseModel):
    full_name: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: str

    model_config = ConfigDict(
        from_attributes=True
    )