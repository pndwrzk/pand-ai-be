from app.constants.vector_collections import VectorCollection
from app.constants.conversation_role import ConversationRole
from app.messaging.exchanges import Exchange, RoutingKey
from app.messaging.publisher import Publisher
from app.models.conversation import Conversation
from app.models.conversation_message import ConversationMessage
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.vector_repository import VectorRepository
from app.schemas.requests.create_conversation_request import CreateConversationRequest
from app.services.llm_service import LLMService


class ConversationService:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        llm_service: LLMService,
        publisher: Publisher,
        vector_repository: VectorRepository,
    ):
        self.conversation_repository = conversation_repository
        self.llm_service = llm_service
        self.publisher = publisher
        self.vector_repository = vector_repository

    def _search_contexts(self, query: str, limit: int = 5):
        results = self.vector_repository.search(
            collection_name=VectorCollection.DOCUMENTS,
            query=query,
            limit=limit,
        )
        return [document for document, score in results]
    
    
    
    def get_conversations(self):
        return self.conversation_repository.get_all_conversation();
    
    
    
    def get_conversation_by_id(self, conversation_id: str):
         conversation_data =  self.conversation_repository.get_conversation_detail_by_id(conversation_id=conversation_id);
         if not conversation_data:
                     raise ValueError(f"Conversation not found")
         return conversation_data



    def create_conversation(self, request: CreateConversationRequest):
        conversation_data = self.conversation_repository.createConversationWithMessage(
            conversation=Conversation(),
            message_content=request.message,
            role=ConversationRole.HUMAN,
        )


        self.publisher.publish(
            exchange=Exchange.CHAT,
            routing_key=RoutingKey.CONVERSATION_TITLE_PROCESS,
            message={"conversation_id": str(conversation_data.id)},
        )

        return {
            "conversation_id": conversation_data.id
        }

    def reply_conversation_stream(self, conversation_id: str, message_content: str):

        conversation = self.conversation_repository.get_conversation_by_id(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with id {conversation_id} not found")
        history = self.conversation_repository.get_conversation_messages(conversation_id)

        self.conversation_repository.create_conversation_message(
            ConversationMessage(
                conversation_id=conversation.id,
                content=message_content,
                role=ConversationRole.HUMAN,
            )
        )

        contexts = self._search_contexts(message_content)

        response_parts = []
        for chunk in self.llm_service.generate_response_stream(message_content, history, contexts):
            response_parts.append(chunk)
            yield chunk

        response_message = "".join(response_parts)
        suggested_questions = self.llm_service.generate_suggested_questions(message_content)

        self.conversation_repository.create_conversation_message(
            ConversationMessage(
                conversation_id=conversation.id,
                content=response_message,
                role=ConversationRole.SYSTEM,
            )
        )

        return {
            "conversation_id": conversation.id,
            "conversation_title": conversation.title,
            "message": message_content,
            "response": response_message,
            "suggested_questions": suggested_questions,
        }

    def generate_conversation_title(self, message: dict):
        conversation_id = message.get("conversation_id")
        if not conversation_id:
            raise ValueError("conversation_id is required in the message")

        conversation = self.conversation_repository.get_conversation_by_id(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with id {conversation_id} not found")

        first_message = self.conversation_repository.get_first_message_of_conversation(conversation_id)
        if not first_message:
            raise ValueError(f"No messages found for conversation with id {conversation_id}")

        conversation.title = self.llm_service.generate_title(first_message.content)
        self.conversation_repository.update_conversation(conversation)