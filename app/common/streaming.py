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


def stream_response(generator, chunk_size: int = 32):
    try:
        while True:
            chunk = next(generator)
            if isinstance(chunk, str):
                for i in range(0, len(chunk), chunk_size):
                    yield format_sse({"delta": chunk[i:i + chunk_size]})
            else:
                yield format_sse({"delta": serialize_for_json(chunk)})
    except StopIteration as exc:
        yield format_sse({"event": "done", "payload": serialize_for_json(exc.value)})
    except ValueError as exc:
        yield format_sse({"event": "error", "message": str(exc)})
        
