from app.db.qdrant import Qdrant
from app.repositories.vector_repository import VectorRepository
from app.db.session import SessionLocal
from app.messaging.consumer import Consumer
from app.messaging.rabbitmq import RabbitMQ
from app.messaging.exchanges import Exchange, RoutingKey
from app.messaging.queues import Queue
from app.repositories.file_repository import FileRepository
from app.repositories.file_content_repository import FileContentRepository
from app.services.storage_service import StorageService
from app.services.document_service import DocumentService
from app.services.llm_service import LLMService


def create_document_service():

    db = SessionLocal()

    return DocumentService(
        file_repository=FileRepository(db),
        file_content_repository=FileContentRepository(db),
        storage_service=StorageService(),
        vector_repository=VectorRepository(Qdrant()),
        llm_service=LLMService(),
    )


document_service = create_document_service()


consumer = Consumer(
    RabbitMQ()
)


consumer.consume(
    exchange=Exchange.FILE,
    queue=Queue.CONTENT_VECTOR,
    routing_key=RoutingKey.VECTOR_PROCESS,
    callback=document_service.indexing_contents,
)