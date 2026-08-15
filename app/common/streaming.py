import json
from uuid import UUID

from langchain_core.messages import HumanMessage

from langchain_core.messages import HumanMessage


def serialize_for_json(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, dict):
        return {key: serialize_for_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [serialize_for_json(item) for item in value]
    return value


def format_sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, default=str)}\n\n"


def stream_response(generator):
    try:
        while True:
            chunk = next(generator)
            yield format_sse({"delta": serialize_for_json(chunk)})
    except StopIteration as exc:
        yield format_sse({"event": "done", "payload": serialize_for_json(exc.value)})
    except ValueError as exc:
        yield format_sse({"event": "error", "message": str(exc)})
        
