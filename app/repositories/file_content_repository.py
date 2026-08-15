from uuid import UUID

from app.models.file_content import FileContent


class FileContentRepository:

    def __init__(
        self,
        db,
    ):
        self.db = db


    def create_bulk(
        self,
        file_id: UUID,
        contents: list[dict],
    ):

        file_contents = []


        for content in contents:

            file_contents.append(
                FileContent(
                    file_id=file_id,
                    page_number=content["page_number"],
                    content=content["content"],
                    content_original=content["content_original"],
                    status=content["status"],
                )
            )


        self.db.add_all(
            file_contents
        )

        self.db.commit()


        return file_contents

    def update(
        self,
        file_content: FileContent,
    ):
        self.db.commit()
        self.db.refresh(file_content)

        return file_content

    def find_by_id(
        self,
        file_content_id: UUID,
    ):
        return (
            self.db.query(FileContent)
            .filter(
                FileContent.id == file_content_id
            )
            .first()
        )

        file_content.content = content
        self.db.commit()
        self.db.refresh(file_content)

        return file_content