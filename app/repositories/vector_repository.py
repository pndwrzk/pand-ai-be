from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
    PayloadSchemaType,
)

from app.db.qdrant import Qdrant
from app.rag.embedding import Embedding


class VectorRepository:

    def __init__(self, qdrant: Qdrant):
        self.client = qdrant.client
        self.embedding = Embedding().model

    def _ensure_index(self, collection_name: str, field_name: str = "file_content_id"):
       
            self.client.create_payload_index(
                collection_name=collection_name,
                field_name=field_name,
                field_schema=PayloadSchemaType.KEYWORD,
            )
     

    def _vector_store(self, collection_name: str) -> QdrantVectorStore:

        store = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.embedding,
        )

        self._ensure_index(collection_name)

        return store

    def save(self, collection_name: str, documents: list[Document]):
        self._vector_store(collection_name).add_documents(documents)

    def search(self, collection_name: str, query: str, limit: int = 5):
        return self._vector_store(collection_name).similarity_search_with_score(
            query=query,
            k=limit,
        )

    def delete(self, collection_name: str, key: str, value):
        self._ensure_index(collection_name, key)

        self.client.delete(
            collection_name=collection_name,
            points_selector=Filter(
                must=[FieldCondition(key=key, match=MatchValue(value=value))]
            ),
        )
        
    def search_by_metadata(
        self,
        collection_name: str,
        key: str,
        value: str,
        limit: int = 100,
    ):
        self._ensure_index(collection_name, key)

        points, _ = self.client.scroll(
            collection_name=collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value),
                    )
                ]
            ),
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        return points