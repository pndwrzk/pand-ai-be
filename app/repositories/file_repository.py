from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.file import File


class FileRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, file: File):
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)

        return file

    def find_by_id(
        self,
        file_id: UUID,
    ):
        return (
            self.db.query(File)
            .filter(
                File.id == file_id
            )
            .first()
        )
        
    def find_All_by_module_id(
        self,
        module_id: UUID,
    ):
        return (
            self.db.query(File)
            .filter(
                File.module_id == module_id
            )
            .all()
        )

    def find_by_id_with_contents(
        self,
        file_id: UUID,
    ):

        return (
            self.db.query(File)
            .options(
                joinedload(File.contents)
            )
            .filter(
                File.id == file_id
            )
            .first()
        )

    def update_status(
        self,
        file_id: UUID,
        status: int,
    ):
        file = self.find_by_id(file_id)
        if not file:
            return None

        file.status = status
        self.db.commit()
        self.db.refresh(file)

        return file


    def find_by_key(
        self,
        key: str,
    ):
        return (
            self.db.query(File)
            .filter(
                File.key == key
            )
            .first()
        )
        
    def delete(
        self,
        file: File,
    ):
        self.db.delete(file)
        self.db.commit()

   