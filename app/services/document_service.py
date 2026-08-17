from app.constants.file_status import FileContentStatus, FileStatus
from app.models import file, file_content
from app.repositories.vector_repository import VectorRepository
from pathlib import Path

from langchain_core.documents import Document

from app.db.qdrant import Qdrant
from app.rag.extractor import Extractor
from app.rag.splitter import Splitter

from app.repositories.file_repository import FileRepository
from app.repositories.file_content_repository import FileContentRepository
from app.services.llm_service import LLMService
from app.services.storage_service import StorageService
from app.constants.vector_collections import VectorCollection


class DocumentService:

    def __init__(
        self,
        file_repository: FileRepository,
        file_content_repository: FileContentRepository,
        storage_service: StorageService,
        vector_repository : VectorRepository,
        llm_service: LLMService, 
    ):

        self.file_repository = file_repository
        self.file_content_repository = file_content_repository
        self.storage_service = storage_service
        self.vector_repository=  vector_repository
        self.extractor = Extractor()
        self.llm_service = llm_service


    def extract_document_contents(
        self,
        message: dict,
    ):

        file_id = message.get("file_id")

        if not file_id:
            return


        file = self.file_repository.find_by_id(
            file_id
        )


        if file is None:
            print(
                f"File {file_id} not found"
            )
            return
        
        
        self.file_repository.update_status(
                        file_id=file.id,
                        status=FileStatus.PROCESS,
                    )


        file_path = None


        try:

            print(
                f"Processing {file.name}"
            )


            file_path = self.storage_service.download(
                file.key
            )


            pages = self.extractor.extract(
                file_path
            )


            contents = []

            for page in pages:

                contents.append(
                    {
                        "file_id": file.id,
                        "page_number": page["page_number"],
                        "content": page["text"],
                        "content_original": page["text"],
                        "status": FileContentStatus.UNSAVED,
                    }
                )

            self.file_content_repository.create_bulk(
                file_id=file.id,
                contents=contents,
            )

            self.file_repository.update_status(
                file_id=file.id,
                status=FileStatus.COMPLETED,
            )
        


            print(
                f"Saved {len(contents)} pages"
            )


        finally:

            if file_path:
                Path(file_path).unlink(
                    missing_ok=True,
                )

    def indexing_contents(
        self,
        message: dict,
    ):

        file_content_id = message.get("file_content_id")

        if not file_content_id:
            return

        file_content = self.file_content_repository.find_by_id(
            file_content_id
        )
        
        file_content.status = FileContentStatus.PROCESS
        self.file_content_repository.update(
                    file_content
        )

        if file_content is None:
            print(
                f"File content {file_content_id} not found"
            )
            return

        print(
            f"Indexing content for {file_content.file_id}"
        )

        self.vector_repository.delete(
                        collection_name=VectorCollection.DOCUMENTS,
                        key="metadata.file_content_id",
                        value=file_content_id,
                    )   
        
        splitter = Splitter()
        chunks = splitter.split(file_content.content)
        file = self.file_repository.find_by_id(file_content.file_id)
        
        if file is None:
            print(
                f"File {file_content.file_id} not found"
            )
            return
        
        if file.key is None:
            print(
                f"File {file_content.file_id} has no key"
            )
            return

        splitter = Splitter()
        chunks = splitter.split(file_content.content)

        documents = []
        for i, chunk in enumerate(chunks):
            context = self.llm_service.generate_chunk_context(file_content.content, chunk)
            enriched_content = f"{context}\n\n{chunk}"

            documents.append(
                Document(
                    page_content=enriched_content,     
                    metadata={
                        "file_id": file_content.file_id,
                        "file_content_id": file_content.id,
                        "file_key": file.key,
                        "page_number": file_content.page_number,
                        "chunk_number": i,
                        "original_content": chunk,     
                    },
                )
            )

        if documents:
            self.vector_repository.save(collection_name=VectorCollection.DOCUMENTS,documents=documents)
            
       

        file_content.status = FileContentStatus.SAVED
        self.file_content_repository.update(
            file_content
        )

        print(
            "indexing succesfully"
        )
        
    def remove_indexing_contents(
        self,
        message: dict,
    ):

        file_content_id = message.get("file_content_id")

        if not file_content_id:
            return

        file_content = self.file_content_repository.find_by_id(
            file_content_id
        )

        if file_content is None:
            print(
                f"File content {file_content_id} not found"
            )
            return

        print(
            f"Removing indexing for {file_content.id}"
        )

        self.vector_repository.delete(
                        collection_name=VectorCollection.DOCUMENTS,
                        key="metadata.file_content_id",
                        value=file_content_id,
                    )
        


    
        


