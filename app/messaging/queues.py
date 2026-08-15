from enum import StrEnum


class Queue(StrEnum):
    DOCUMENT_OCR = "document.ocr.queue"
    CONTENT_VECTOR = "content.vector.queue"
    CONTENT_REMOVE_VECTOR = "remove.vector.queue"
    CONVERSATION_TITLE = "conversation.title.queue"