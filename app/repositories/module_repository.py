from uuid import UUID

from sqlalchemy.orm import Session

from app.models.module import Module


class ModuleRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db


    def find_all(self):

        return self.db.query(
            Module
        ).all()


    def find_by_id(
        self,
        id: UUID
    ):

        return self.db.query(
            Module
        ).filter(
            Module.id == id
        ).first()


    def find_by_name(
        self,
        name: str
    ):

        return self.db.query(
            Module
        ).filter(
            Module.name == name
        ).first()


    def create(
        self,
        module: Module
    ):

        self.db.add(module)
        self.db.commit()
        self.db.refresh(module)

        return module


    def update(
        self,
        module: Module
    ):

        self.db.commit()
        self.db.refresh(module)

        return module


    def delete(
        self,
        module: Module
    ):

        self.db.delete(module)
        self.db.commit()