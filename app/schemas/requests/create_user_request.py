from pydantic import BaseModel
from pydantic import EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str