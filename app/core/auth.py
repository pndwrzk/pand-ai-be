from collections.abc import Generator
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.constants.user_role import UserRole
from app.constants.user_status import UserStatus
from app.core.security import decode_access_token
from app.db.base import clear_current_user_id
from app.exceptions.exceptions import ForbiddenException, UnauthorizedException
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Generator[dict, None, None]:
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except Exception:
        clear_current_user_id()
        raise UnauthorizedException("Invalid token")

    try:
        yield payload
    finally:
        clear_current_user_id()


def _get_user_repository() -> Generator[UserRepository, None, None]:
    # Import lokal untuk menghindari circular import dengan
    # app.core.dependency (yang meng-assemble repository & service,
    # dan pada akhirnya mengimpor router-router yang memakai module ini).
    from app.core.dependency import get_db

    db_gen = get_db()
    db = next(db_gen)

    try:
        yield UserRepository(db)
    finally:
        next(db_gen, None)


def get_current_active_user(
    payload: dict = Depends(get_current_user),
    repository: UserRepository = Depends(_get_user_repository),
) -> User:
    """
    Mengambil data user yang sedang login secara utuh dari database
    (bukan hanya dari isi JWT), supaya role/status yang dipakai untuk
    otorisasi selalu yang terbaru, bukan yang ter-cache di dalam token.
    """

    user_id = payload.get("sub")

    if not user_id:
        raise UnauthorizedException("Invalid token: missing user ID")

    user = repository.find_by_id(UUID(user_id))

    if user is None:
        raise UnauthorizedException("User not found")

    if user.status != UserStatus.ACTIVE:
        raise UnauthorizedException("User is inactive")

    return user


def require_superadmin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dependency guard: hanya boleh dilanjutkan jika user yang sedang
    login memiliki role SUPERADMIN.
    """

    if current_user.role != UserRole.SUPERADMIN:
        raise ForbiddenException(
            message="Only superadmin can perform this action"
        )

    return current_user