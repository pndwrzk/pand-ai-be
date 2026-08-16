import time

from sqlalchemy.exc import OperationalError, DBAPIError

from app.db.qdrant import Qdrant
from app.repositories.vector_repository import VectorRepository
from app.db.session import SessionLocal

from app.messaging.consumer import Consumer
from app.messaging.rabbitmq import RabbitMQ
from app.messaging.exchanges import Exchange, RoutingKey
from app.messaging.queues import Queue

from app.repositories.file_repository import FileRepository
from app.repositories.file_content_repository import FileContentRepository

from app.services.llm_service import LLMService
from app.services.storage_service import StorageService
from app.services.document_service import DocumentService


MAX_RETRIES = 3
RETRY_DELAY = 2


def create_document_service(db):
    return DocumentService(
        file_repository=FileRepository(db),
        file_content_repository=FileContentRepository(db),
        storage_service=StorageService(),
        vector_repository=VectorRepository(Qdrant()),
        llm_service=LLMService(),
    )


def extract_document_contents_with_retry(*args, **kwargs):
    for attempt in range(1, MAX_RETRIES + 1):
        db = SessionLocal()

        try:
            document_service = create_document_service(db)

            return document_service.extract_document_contents(
                *args,
                **kwargs,
            )

        except (OperationalError, DBAPIError) as e:
            db.rollback()

            print(
                f"[DOCUMENT OCR] Attempt "
                f"{attempt}/{MAX_RETRIES} failed: {e}"
            )

            if attempt >= MAX_RETRIES:
                print(
                    "[DOCUMENT OCR] Max retries reached."
                )
                raise

            delay = RETRY_DELAY * (2 ** (attempt - 1))

            print(
                f"[DOCUMENT OCR] Retrying in {delay}s..."
            )

            time.sleep(delay)

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


consumer = Consumer(
    RabbitMQ()
)

consumer.consume(
    exchange=Exchange.FILE,
    queue=Queue.DOCUMENT_OCR,
    routing_key=RoutingKey.OCR_PROCESS,
    callback=extract_document_contents_with_retry,
)