from pydantic import BaseModel


class CreateConversationRequest(BaseModel):
    message: str