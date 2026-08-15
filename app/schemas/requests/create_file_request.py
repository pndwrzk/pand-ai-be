from pydantic import BaseModel


class CreateFileRequest(BaseModel):
    # name: str
    key: str
    # url: str
    # type: str
    # size: int