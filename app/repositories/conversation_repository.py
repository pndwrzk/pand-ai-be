

from uuid import UUID

from sqlalchemy.orm import joinedload

from app.models import conversation_message
from app.models.conversation import Conversation
from app.models.conversation_message import ConversationMessage

class ConversationRepository:
    def __init__(self, db):
        self.db = db

    def createConversationWithMessage(
        self,
        conversation: Conversation,
        message_content: str,
        role: int,
    ):
        self.db.add(conversation)
        self.db.flush() 

        conversation_message = ConversationMessage(
            conversation_id=conversation.id,
            content=message_content,
            role=role,
        )
        self.db.add(conversation_message)

        self.db.commit()
        self.db.refresh(conversation)
        self.db.refresh(conversation_message)

        return conversation
    
    
    def get_all_conversation(self):
        return (
            self.db.query(Conversation)
            .order_by(Conversation.created_at.desc())
            .all()
        )
    
    def get_conversation_by_id(self, conversation_id: str):
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    def get_conversation_detail_by_id(self, conversation_id: str):
        return (
        self.db.query(Conversation)
        .options(joinedload(Conversation.messages))
        .filter(Conversation.id == conversation_id)
        .first()
    )
    
    
    def get_first_message_of_conversation(self, conversation_id: str):
        return self.db.query(ConversationMessage).filter(ConversationMessage.conversation_id == conversation_id).order_by(ConversationMessage.created_at.asc()).first()
    
    def get_conversation_messages(self, conversation_id: str):
        return self.db.query(ConversationMessage).filter(ConversationMessage.conversation_id == conversation_id).order_by(ConversationMessage.created_at.asc()).all()
    
    def update_conversation(self, conversation: Conversation):
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def create_conversation_message(self, conversation_message: ConversationMessage):
        self.db.add(conversation_message)
        self.db.commit()
        self.db.refresh(conversation_message)
        return conversation_message
    
    
    
    
    