from pydantic import BaseModel


class CreateModuleRequest(BaseModel):
    name: str
    description: str | None = None


