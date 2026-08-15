from collections.abc import Generator

from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.db.qdrant import Qdrant
from app.db.session import SessionLocal

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.module_repository import ModuleRepository
from app.repositories.file_repository import FileRepository

from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.module_service import ModuleService
from app.services.file_service import FileService
from app.services.storage_service import StorageService
from app.services.document_service import DocumentService
from app.repositories.file_content_repository import FileContentRepository
from app.messaging.publisher import Publisher
from app.messaging.rabbitmq import RabbitMQ
from app.repositories.vector_repository import VectorRepository


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()




def get_user_repository(
    db: Session = Depends(get_db),
):
    return UserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
):
    return UserService(repository)




def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
):
    return AuthService(repository)


def get_llm_service():
    return LLMService()



def get_rabbitmq(
    request: Request,
) -> RabbitMQ:
    return request.app.state.rabbitmq

def get_publisher(
    rabbitmq: RabbitMQ = Depends(get_rabbitmq),
):
    return Publisher(rabbitmq)


def get_conversation_repository(
    db: Session = Depends(get_db),
):
    return ConversationRepository(db)



def get_qdrant(request: Request) -> Qdrant:
    return request.app.state.qdrant




def get_vector_repository(
    qdrant: Qdrant = Depends(get_qdrant),
):
    return VectorRepository(
        qdrant=qdrant,
    )



def get_storage_service():
    return StorageService()



def get_conversation_service(
    repository: ConversationRepository = Depends(get_conversation_repository),
    llm_service: LLMService = Depends(get_llm_service),
    publisher: Publisher = Depends(get_publisher),
    vector_repository: VectorRepository = Depends(get_vector_repository),
    storage_service: StorageService = Depends(get_storage_service)
):
    return ConversationService(
        conversation_repository=repository,
        llm_service=llm_service,
        publisher=publisher,
        vector_repository=vector_repository,
        storage_service=storage_service,
    )

def get_module_repository(
    db: Session = Depends(get_db),
):
    return ModuleRepository(db)


def get_module_service(
    repository: ModuleRepository = Depends(get_module_repository),
):
    return ModuleService(repository)






def get_file_repository(
    db: Session = Depends(get_db),
):
    return FileRepository(db)






def get_file_content_repository(
    db: Session = Depends(get_db),
):
    return FileContentRepository(db)







def get_file_service(
    file_repository: FileRepository = Depends(get_file_repository),
    module_repository: ModuleRepository = Depends(get_module_repository),
    file_content_repository: FileContentRepository = Depends(get_file_content_repository),
    publisher: Publisher = Depends(get_publisher),
    vector_repository: VectorRepository = Depends(get_vector_repository),
    storage_service : StorageService = Depends(get_storage_service)
):
    return FileService(
        file_repository=file_repository,
        module_repository=module_repository,
        publisher=publisher,
        file_content_repository=file_content_repository,
        vector_repository=vector_repository,
        storage_service=storage_service,
    )



def get_document_service(
    file_repository: FileRepository = Depends(get_file_repository),
    file_content_repository: FileContentRepository = Depends(get_file_content_repository),
    storage_service: StorageService = Depends(get_storage_service),
    vector_repository: VectorRepository = Depends(get_vector_repository),
):
    return DocumentService(
        file_repository=file_repository,
        file_content_repository=file_content_repository,
        storage_service=storage_service,
        vector_repository=vector_repository,
    )