from uuid import UUID

from app.schemas.requests.update_status_file_content_request import UpdateStatusFileContentRequest
from app.schemas.requests.update_content_file_request import UpdateContentFileRequest
from fastapi import APIRouter, Depends

from app.common.response import ApiResponse
from app.core.dependency import get_file_service
from app.schemas.requests.create_file_request import CreateFileRequest
from app.schemas.responses.file_response import FileContentResponse, FileResponse, FileWithFileContentAndVectorInfoResponse
from app.services.file_service import FileService
from app.schemas.responses.file_response import FileWithFileContentResponse

router = APIRouter(
    tags=["Files"],
)



@router.get("/internal/modules/{module_id}/files")
def get_files_by_module_id(
    module_id: UUID,
    service: FileService = Depends(get_file_service),
):
    files = service.get_by_module_id(
        module_id=module_id
    )

    return ApiResponse.success(
        message="Files retrieved successfully",
        data=[FileResponse.model_validate(file) for file in files],
    )


@router.post("/internal/modules/{module_id}/files")
def create_file(
    module_id: UUID,
    request: CreateFileRequest,
    service: FileService = Depends(get_file_service),
):
    file = service.create(
        module_id=module_id,
        request=request,
    )

    return ApiResponse.success(
        message="File uploaded successfully",
        data=FileResponse.model_validate(file),
    )

@router.get("/internal/files/{file_id}")
def get_file_detail(
    file_id: UUID,
    service: FileService = Depends(get_file_service),
):

    file = service.get_by_id_with_contents(
        file_id
    )

    return ApiResponse.success(
        message="File retrieved successfully",
        data=FileWithFileContentAndVectorInfoResponse.model_validate(
            file
        ),
    )


@router.get("/internal/files/content/{content_id}")
def get_file_content_detail(
    content_id: UUID,
    service: FileService = Depends(get_file_service),
):
    file_content = service.get_file_content_by_id(
        file_content_id=content_id,
    )

    return ApiResponse.success(
        message="File content retrieved successfully",
        data=FileContentResponse.model_validate(file_content),
    )

@router.patch("/internal/files/content/{file_content_id}")
def update_file_content(
    file_content_id: UUID,
    request: UpdateContentFileRequest,
    service: FileService = Depends(get_file_service),
):
    file_content = service.update_content(
        file_content_id=file_content_id,
        content=request.content,
    )

    return ApiResponse.success(
        message="File content updated successfully",
        data=FileContentResponse.model_validate(
            file_content
        ),
    )

@router.patch("/internal/files/content/{file_content_id}/status")
def update_file_status_approve(
    file_content_id: UUID,
    request: UpdateStatusFileContentRequest,
    service: FileService = Depends(get_file_service),
):

    service.update_content_status(
        file_content_id=file_content_id,
        status=request.status
    )

    return ApiResponse.success(
        message="File status updated successfully",
    )

@router.delete("/internal/modules/{module_id}/files/{file_id}")
def delete_file(
    file_id: UUID,
    service: FileService = Depends(get_file_service),
):
    service.delete_by_file_id(
        file_id=file_id
    )

    return ApiResponse.success(
        message="File deleted successfully",
    )
