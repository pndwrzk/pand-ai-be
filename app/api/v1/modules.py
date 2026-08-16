from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.dependency import get_module_service

from app.services.module_service import ModuleService

from app.schemas.requests.create_module_request import CreateModuleRequest
from app.schemas.requests.update_module_request import UpdateModuleRequest

from app.common.response import ApiResponse


router = APIRouter(
    prefix="/internal/modules",
    tags=["Modules"]
)


@router.get("")
def get_modules(
    service: ModuleService = Depends(get_module_service),
):

    modules = service.get_all()

    return ApiResponse.success(
        message="Success",
        data=modules
    )



@router.post("")
def create_module(
    request: CreateModuleRequest,
    service: ModuleService = Depends(get_module_service),
):

    module = service.create(request)

    return ApiResponse.success(
        message="Module created",
        data=module
    )



@router.get("/{id}")
def get_module(
    id: UUID,
    service: ModuleService = Depends(get_module_service),
):

    module = service.get_by_id(id)

    return ApiResponse.success(
        message="Success",
        data=module
    )



@router.put("/{id}")
def update_module(
    id: UUID,
    request: UpdateModuleRequest,
    service: ModuleService = Depends(get_module_service),
):

    module = service.update(
        id,
        request
    )

    return ApiResponse.success(
        message="Module updated",
        data=module
    )



@router.delete("/{id}")
def delete_module(
    id: UUID,
    service: ModuleService = Depends(get_module_service),
):

    service.delete(id)

    return ApiResponse.success(
        message="Module deleted"
    )