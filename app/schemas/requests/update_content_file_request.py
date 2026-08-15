from pydantic import BaseModel





class UpdateContentFileRequest(BaseModel):
    content: str