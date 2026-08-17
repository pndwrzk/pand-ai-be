from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class MeResponse(BaseModel):
    name: str
    email: EmailStr
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )
