from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FileResponse(BaseModel):
    id: UUID
    module_id: UUID
    name: str
    key: str
    url: str
    type: str
    size: int
    status: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class FileContentResponse(BaseModel):
    id: UUID
    page_number: int
    content: str
    content_original: str
    status: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )

class FileWithFileContentResponse(BaseModel):

    id: UUID
    module_id: UUID
    name: str
    key: str
    url: str
    type: str
    size: int
    status: int
    contents: list[FileContentResponse] = []


    model_config = {
        "from_attributes": True
    }


class FileWithFileContentAndVectorInfoResponse(BaseModel):
    id: UUID
    module_id: UUID
    name: str
    key: str
    url: str
    type: str
    size: int
    status: int
    is_available_vector: bool = False
    contents: list[FileContentResponse] = []

    model_config = ConfigDict(
        from_attributes=True,
    )