from langchain_core.documents import Document

from app.constants.vector_collections import VectorCollection
from app.constants.conversation_role import ConversationRole
from app.messaging.exchanges import Exchange, RoutingKey
from app.messaging.publisher import Publisher
from app.models.conversation import Conversation
from app.models.conversation_message import ConversationMessage
from app.rag.reranker import Reranker
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.vector_repository import VectorRepository
from app.schemas.requests.create_conversation_request import CreateConversationRequest
from app.services.llm_service import LLMService
from app.services.storage_service import StorageService


class ConversationService:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        llm_service: LLMService,
        publisher: Publisher,
        vector_repository: VectorRepository,
        storage_service: StorageService,
        
    ):
        self.conversation_repository = conversation_repository
        self.llm_service = llm_service
        self.publisher = publisher
        self.vector_repository = vector_repository
        self.reranker = Reranker()
        self.storage_service = storage_service

    def _search_contexts(self, query: str, limit: int = 5, score_threshold: float = 0.5):
        results = self.vector_repository.search(
            collection_name=VectorCollection.DOCUMENTS,
            query=query,
            limit=20,
        )
        filtered_documents = [
            document for document, score in results if score >= score_threshold
        ]
        reranked = self.reranker.rerank_with_scores(query, filtered_documents, top_k=limit)
        return reranked  # list of (document, rerank_score)
    
    
    
    def get_conversations(self, page: int = 1, per_page: int = 10):
        if page < 1:
            raise ValueError("Page number must be greater than or equal to 1")
        if per_page < 1:
            raise ValueError("Per page number must be greater than or equal to 1")
        if per_page > 100:
            raise ValueError("Per page number must be less than or equal to 100")

        return self.conversation_repository.get_all_conversation(page=page, per_page=per_page)
    
    
    
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
        
    def _build_sources(self, reranked_contexts, score_threshold: float = 0.7) -> list[dict]:
        seen = set()
        sources = []
        for doc, score in reranked_contexts:
            if score < score_threshold:
                continue

            assert doc.metadata is not None
            file_key = doc.metadata.get("file_key", "Unknown document")
            if file_key in seen:
                continue
            seen.add(file_key)

            url = self.storage_service.get_file_url(file_key)
            file_name = self.storage_service.get_by_name_by_key(file_key)
            if url is None:
                print(f"File with key {file_key} not found in storage")
                continue

            sources.append({
                "file_key": file_key,
                "file_name": file_name,
                "url": url,
            })
        return sources

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

        search_query = self.llm_service.rewrite_query(message_content, history)

        reranked_contexts: list[tuple[Document, float]] = self._search_contexts(search_query)
        contexts: list[Document] = [doc for doc, score in reranked_contexts]
        sources = self._build_sources(reranked_contexts)

        response_parts = []
        for chunk in self.llm_service.generate_response_stream(message_content, history, contexts):
            response_parts.append(chunk)
            yield chunk

        response_message = "".join(response_parts)
        suggested_questions = []

        if len(sources) > 0:
            suggested_questions = self.llm_service.generate_suggested_questions(
                message_content=message_content,
                history=history,
                contexts=contexts,
            )

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
            "sources": sources,
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
        

