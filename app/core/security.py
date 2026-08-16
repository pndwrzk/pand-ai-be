from datetime import datetime, timedelta, timezone
from app.constants.entry_point import EntryPoint

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash plain password menggunakan bcrypt
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
   
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def _get_jwt_config(entry_point: int) -> tuple[str, int]:
   
    if entry_point == EntryPoint.APP:
        return settings.JWT_SECRET_APP, settings.ACCESS_TOKEN_EXPIRE_MINUTES_APP
    else:
        return settings.JWT_SECRET_INTERNAL, settings.ACCESS_TOKEN_EXPIRE_MINUTES_INTERNAL


def create_access_token(
    data: dict,
    expires_minutes: int | None = None,
    entry_point: int = EntryPoint.INTERNAL,
) -> str:

    to_encode = data.copy()
    secret_key, default_expires_minutes = _get_jwt_config(entry_point)

    expire_minutes = (
        expires_minutes
        if expires_minutes is not None
        else default_expires_minutes
    )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expire_minutes
    )

    to_encode.update(
        {
            "exp": expire,
            "entry_point": entry_point,
        }
    )

    return jwt.encode(
        to_encode,
        secret_key,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(
    token: str,
    entry_point: int = EntryPoint.INTERNAL ,
) -> dict:
   
    secret_key, _ = _get_jwt_config(entry_point)

    return jwt.decode(
        token,
        secret_key,
        algorithms=[
            settings.ALGORITHM
        ],
    )