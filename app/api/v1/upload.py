from fastapi import APIRouter, Depends

from app.common.response import ApiResponse
from app.core.dependency import get_storage_service
from app.schemas.requests.presign_request import PresignRequest
from app.services.storage_service import StorageService

router = APIRouter(
    prefix="/internal/upload",
    tags=["Upload"],
)


@router.post("/presign")
def presign(
    request: PresignRequest,
    storage_service: StorageService = Depends(get_storage_service),
):
    result = storage_service.generate_presigned_upload(
        content_type=request.content_type,
    )

    return ApiResponse.success(
        message="Presigned URL generated successfully",
        data=result,
    )