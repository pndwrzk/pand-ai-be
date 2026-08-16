from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    APP_NAME : str = ""
    APP_VERSION:str = ""
    JWT_SECRET_INTERNAL: str = ""
    JWT_SECRET_APP: str = ""
    ALGORITHM: str = "HS256"
    RABBITMQ_HOST: str = ""
    RABBITMQ_PORT: int = 0
    RABBITMQ_USERNAME: str = ""
    RABBITMQ_PASSWORD: str = ""
    RABBITMQ_VHOST: str = ""
    QDRANT_HOST: str = ""
    QDRANT_PORT: int = 6333
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_TOKEN_EXPIRE_MINUTES_INTERNAL: int = 30
    ACCESS_TOKEN_EXPIRE_MINUTES_APP: int = 60
    GROQ_API_KEY: SecretStr = SecretStr("")
    S3_ACCESS_KEY_ID: str = ""
    S3_SECRET_ACCESS_KEY: str = ""
    S3_ENDPOINT_URL: str = ""
    S3_REGION: str = ""
    S3_BUCKET_NAME: str = ""


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()