
from app.messaging.publisher import Publisher
from app.repositories.conversation_repository import ConversationRepository

from app.db.session import SessionLocal
from app.db.qdrant import Qdrant
from app.messaging.consumer import Consumer
from app.messaging.rabbitmq import RabbitMQ
from app.messaging.exchanges import Exchange, RoutingKey
from app.messaging.queues import Queue

from app.repositories.vector_repository import VectorRepository
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.storage_service import StorageService


def create_conversation_service():

    db = SessionLocal()

    return ConversationService(
      conversation_repository=ConversationRepository(db),
        llm_service=LLMService(),
        publisher=Publisher(RabbitMQ()),
        vector_repository=VectorRepository(qdrant=Qdrant()),
        storage_service=StorageService()
    )


conversation_service = create_conversation_service()


consumer = Consumer(
    RabbitMQ()
)


consumer.consume(
    exchange=Exchange.CHAT,
    queue=Queue.CONVERSATION_TITLE,
    routing_key=RoutingKey.CONVERSATION_TITLE_PROCESS,
    callback=conversation_service.generate_conversation_title,
)