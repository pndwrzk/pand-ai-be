from typing import Optional

from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
import torch


class Reranker:

    _instance = None
    _model: Optional[CrossEncoder] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            Reranker._model = CrossEncoder(
                "cross-encoder/ms-marco-MiniLM-L-2-v2",
                max_length=512,
            )

    def rerank(self, query: str, documents: list[Document], top_k: int = 5) -> list[Document]:
        ranked = self.rerank_with_scores(query, documents, top_k)
        return [doc for doc, score in ranked]

    def rerank_with_scores(
        self, query: str, documents: list[Document], top_k: int = 5
    ) -> list[tuple[Document, float]]:
        if not documents:
            return []

        assert self._model is not None

        pairs = [(query, doc.page_content) for doc in documents]
        raw_scores = self._model.predict(pairs)
        scores = torch.sigmoid(torch.tensor(raw_scores)).tolist()   # normalisasi ke 0-1

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return [(doc, float(score)) for doc, score in ranked[:top_k]]