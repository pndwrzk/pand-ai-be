from pydantic import BaseModel





class UpdateModuleRequest(BaseModel):
    name: str
    description: str | None = None
