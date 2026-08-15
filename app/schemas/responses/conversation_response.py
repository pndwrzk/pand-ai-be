from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateConversationResponse(BaseModel):
    conversation_id: UUID
  
    
    
class GetConversationsResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    

