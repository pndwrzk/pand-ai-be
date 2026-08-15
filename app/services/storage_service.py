import uuid
from pathlib import Path

import boto3
from botocore.client import Config

from app.constants.file_extensions import FILE_EXTENSION_MAPPING
from app.core.config import settings


class StorageService:

    def __init__(self):

        self.client = boto3.client(
            "s3",
            region_name=settings.S3_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        )


    def _get_folder(
        self,
        extension: str,
    ) -> str:
        return FILE_EXTENSION_MAPPING.get(
            extension.lower(),
            "others",
        )


    def generate_presigned_upload(
        self,
        content_type: str,
    ):

        extension = content_type.split("/")[-1]

        folder = self._get_folder(
            extension
        )

        key = f"{folder}/{uuid.uuid4()}.{extension}"

        upload_url = self.client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": settings.S3_BUCKET_NAME,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=600,
        )

        return {
            "key": key,
            "upload_url": upload_url,
            "url": f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{key}",
        }


    def download(
        self,
        key: str,
    ) -> str:

        extension = Path(key).suffix

        temp_dir = Path("storage/tmp")

        temp_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            temp_dir /
            f"{uuid.uuid4()}{extension}"
        )


        self.client.download_file(
            Bucket=settings.S3_BUCKET_NAME,
            Key=key,
            Filename=str(file_path),
        )


        return str(file_path)

    
    def get_file_size(self, key: str) -> int:
        response = self.client.head_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=key,
        )
        return response["ContentLength"]

    def get_file_url(self, key: str) -> str:
        return f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{key}"
    
    
    def delete_by_key(self, key: str) -> None:
        self.client.delete_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=key,
        )
        
    def get_by_name_by_key(self, key: str) -> str:
        return key.split("/")[-1]
        
        
    
  