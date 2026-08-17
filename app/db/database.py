from sqlalchemy import create_engine

from app.core.config import settings

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args={
        "prepare_threshold": None,
    },
)