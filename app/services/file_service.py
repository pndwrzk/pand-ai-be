from pathlib import Path
from uuid import UUID

from app.constants.file_extensions import FILE_EXTENSION_MAPPING
from app.constants.file_status import FileContentStatus, FileStatus
from app.constants.vector_collections import VectorCollection
from app.repositories.vector_repository import VectorRepository
from app.schemas.responses.file_response import FileWithFileContentAndVectorInfoResponse
from app.services.storage_service import StorageService
from app.exceptions import ConflictException
from app.repositories.file_content_repository import FileContentRepository
from app.exceptions import NotFoundException
from app.messaging.exchanges import Exchange, RoutingKey
from app.messaging.publisher import Publisher
from app.models.file import File
from app.repositories.file_repository import FileRepository
from app.repositories.module_repository import ModuleRepository
from app.schemas.requests.create_file_request import CreateFileRequest




class FileService:

    def __init__(
        self,
        file_repository: FileRepository,
        module_repository: ModuleRepository,
        file_content_repository: FileContentRepository,
        publisher: Publisher,
        vector_repository : VectorRepository,
        storage_service: StorageService
    ):
        self.file_repository = file_repository
        self.module_repository = module_repository
        self.publisher = publisher
        self.file_content_repository = file_content_repository
        self.vector_repository = vector_repository
        self.storage_service = storage_service
        
        
    def get_by_module_id(
        self,
        module_id: UUID,
    ):
        files = self.file_repository.find_All_by_module_id(
            module_id
        )

        return files

    def create(
        self,
        module_id: UUID,
        request: CreateFileRequest,
    ) -> File:

        module = self.module_repository.find_by_id(module_id)

        if module is None:
            raise NotFoundException("Module not found")

        
        existing_file = self.file_repository.find_by_key(request.key)
        if existing_file is not None:
            raise ConflictException("File already exists")

        key_path = Path(request.key)
        file_type = key_path.parent.name    
        file_name = key_path.name  
        file_url =  self.storage_service.get_file_url(request.key)  
        file_size = self.storage_service.get_file_size(request.key) 

        file = File(
            module_id=module_id,
            name=file_name,
            key=request.key,
            url=file_url,
            type=file_type,
            size=file_size,
            status=FileStatus.PENDING,
        )

      
        file = self.file_repository.create(file)

        self.publisher.publish(
            exchange=Exchange.FILE,
            routing_key=RoutingKey.OCR_PROCESS,
            message={
                "file_id": file.id,
            },
        )

        return file

    
    def get_by_id_with_contents(
        self,
        file_id: UUID,
    ):

        file = self.file_repository.find_by_id_with_contents(file_id)
        
        
        data_vector = self.vector_repository.search_by_metadata(
             collection_name=VectorCollection.DOCUMENTS,
            key="metadata.file_id",
            value=str(file_id),
             limit=1
        )
        

        if file is None:
            raise NotFoundException("File not found")

        return FileWithFileContentAndVectorInfoResponse(
        id=file.id,
        module_id=file.module_id,
        name=file.name,
        key=file.key,
        url=file.url,
        type=file.type,
        size=file.size,
        status=file.status,
        total_contents=len(file.contents or []),
        is_available_vector=bool(data_vector),
        contents=file.contents,
    )

    def get_file_content_by_id(
        self,
        file_content_id: UUID,
    ):
        file_content = self.file_content_repository.find_by_id(file_content_id)

        if file_content is None:
            raise NotFoundException("File content not found")

        return file_content

    def update_content(
        self,
        file_content_id: UUID,
        content: str,
    ):
        
        file_content = self.file_content_repository.find_by_id(file_content_id)

        if file_content is None:
            raise NotFoundException("File content not found")

        if file_content.status  == FileContentStatus.SAVED:
            raise ConflictException(f"File content status is already {FileContentStatus.SAVED}")   

        file_content.content = content
        self.file_content_repository.update(file_content)

        return file_content

    def update_content_status(self,
        file_content_id: UUID,
        status: int,
    ) -> File:
        
        file_content = self.file_content_repository.find_by_id(file_content_id)
        
        if file_content is None:
            raise NotFoundException("File content not found")
        
        file = self.file_repository.find_by_id(file_content.file_id)
        
        if file is None:
            raise NotFoundException("File not found")
        
        if file.status != FileStatus.COMPLETED:
            raise ConflictException("File is not completed")



        if file_content.status == status:
            raise ConflictException(f"File content status is already {status}")

        if status == FileContentStatus.SAVED:
            self.publisher.publish(
            exchange=Exchange.FILE,
            routing_key=RoutingKey.VECTOR_PROCESS,
            message={
                "file_content_id": file_content_id,
            },
        )
            file_content.status = FileContentStatus.PROCESS
        elif status == FileContentStatus.UNSAVED:
            self.vector_repository.delete(
            collection_name=VectorCollection.DOCUMENTS,
            key="metadata.file_content_id",
            value=file_content_id,
        )
            file_content.status =  FileContentStatus.UNSAVED
            
        
        self.file_content_repository.update(file_content)
        

      

        return file_content
    
    def delete_by_file_id(
        self,
        file_id: UUID,
    ):
        file = self.file_repository.find_by_id(file_id)

        if file is None:
            raise NotFoundException("File not found")
        
        
        self.storage_service.delete_by_key(
            file.key
        )
        
        self.vector_repository.delete(
              collection_name=VectorCollection.DOCUMENTS,
               key="metadata.file_id",
              value=str(file.id)
        )
        

        self.file_repository.delete(file)

    