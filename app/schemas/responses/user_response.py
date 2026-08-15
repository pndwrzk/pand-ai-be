from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str

    model_config = ConfigDict(
        from_attributes=True
    )