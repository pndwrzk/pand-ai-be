from enum import StrEnum


class Exchange(StrEnum):
    FILE = "file"
    CHAT = "chat"
   


class RoutingKey(StrEnum):
    OCR_PROCESS = "file.ocr"
    VECTOR_PROCESS = "file.vector"
    REMOVE_VECTOR_PROCESS = "file.remove.vector"
    CONVERSATION_TITLE_PROCESS = "file.conversation.title"