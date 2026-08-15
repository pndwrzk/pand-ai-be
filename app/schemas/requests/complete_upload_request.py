from uuid import UUID

from pydantic import BaseModel


class CompleteUploadRequest(BaseModel):
    module_id: UUID
    key: str
    file_name: str
    type: str