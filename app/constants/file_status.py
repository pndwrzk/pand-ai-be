# app/constants/status.py
from enum import IntEnum


class FileStatus(IntEnum):
    PENDING = 0
    PROCESS = 1
    COMPLETED = 2
    FAILED= -1
    
class FileContentStatus(IntEnum):
    UNSAVED = 0
    PROCESS =1
    SAVED = 2