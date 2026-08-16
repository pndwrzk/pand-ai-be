
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from app.common.response import ApiResponse
from app.common.streaming import stream_response
from app.core.dependency import get_conversation_service
from app.schemas.requests.create_conversation_request import CreateConversationRequest
from app.schemas.responses.conversation_response import CreateConversationResponse, GetConversationsResponse
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["Conversations"])




@router.post("")
def create_conversation(
    request: CreateConversationRequest,
    service: ConversationService = Depends(get_conversation_service),
):
    response = service.create_conversation(request)
    return ApiResponse.success(
            message="Conversation created successfully",
            data=CreateConversationResponse.model_validate(
                response
            ),
        )


@router.post("/{conversation_id}/stream")
def create_conversation_message(
    conversation_id: str,
    request: CreateConversationRequest,
    service: ConversationService = Depends(get_conversation_service),
):
    generator = service.reply_conversation_stream(conversation_id, request.message)
    return StreamingResponse(stream_response(generator), media_type="text/event-stream")


@router.get("/history")
def get_conversation_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    service: ConversationService = Depends(get_conversation_service),
):
    response = service.get_conversations(page=page, per_page=per_page)
    return ApiResponse.success(
        message="Success",
        data=response["items"],
        meta=response["meta"],
    )
    
@router.get("/{conversation_id}/history")
def get_conversation_history_by_id(
    conversation_id: str,
    service: ConversationService = Depends(get_conversation_service),
):
    response = service.get_conversation_by_id(conversation_id)
    return ApiResponse.success(
        message="Success",
        data=response,
    )