from uuid import UUID

from app.models.module import Module
from app.repositories.module_repository import ModuleRepository
from app.schemas.requests.create_module_request import CreateModuleRequest
from app.schemas.requests.update_module_request import UpdateModuleRequest
import time

from app.exceptions import (
    ConflictException,
    NotFoundException,
)


class ModuleService:


    def __init__(
        self,
        repository: ModuleRepository
    ):
        self.repository = repository


    def get_all(self):

        return self.repository.find_all()


    def get_by_id(
        self,
        id: UUID
    ):

        module = self.repository.find_by_id(id)

        if not module:
            raise NotFoundException(
                "Module not found"
            )

        return module



    def create(
        self,
        dto: CreateModuleRequest
    ):

        exists = self.repository.find_by_name(
            dto.name
        )

        if exists:
            raise ConflictException(
                "Module already exists"
            )

        module = Module(
            name=dto.name,
            description=dto.description,
        )

        return self.repository.create(module)


    def update(
        self,
        id: UUID,
        dto: UpdateModuleRequest
    ):

        module = self.get_by_id(id)

        module.name = dto.name
        module.description = dto.description

        return self.repository.update(module)


    def delete(
        self,
        id: UUID
    ):

        module = self.get_by_id(id)

        self.repository.delete(
            module
        )