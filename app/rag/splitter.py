from langchain_experimental.text_splitter import SemanticChunker
from app.rag.embedding import Embedding

class Splitter:
    def __init__(self):
        self._chunker = SemanticChunker(
            embeddings=Embedding().model,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=90,
        )

    def split(self, text: str) -> list[str]:
        return self._chunker.split_text(text)