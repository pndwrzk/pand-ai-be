from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr

from app.constants.user_role import UserRole


class InternalMeResponse(BaseModel):
    role: UserRole
    name: str
    email: EmailStr
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )
