from typing import Any

from fastapi import status


class AppException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int,
        errors: Any | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors

        super().__init__(message)


class UnauthorizedException(AppException):

    def __init__(
        self,
        message="Unauthorized",
        errors=None,
    ):
        super().__init__(
            message,
            status.HTTP_401_UNAUTHORIZED,
            errors,
        )


class ForbiddenException(AppException):

    def __init__(
        self,
        message="Forbidden",
        errors=None,
    ):
        super().__init__(
            message,
            status.HTTP_403_FORBIDDEN,
            errors,
        )


class NotFoundException(AppException):

    def __init__(
        self,
        message="Not Found",
        errors=None,
    ):
        super().__init__(
            message,
            status.HTTP_404_NOT_FOUND,
            errors,
        )


class ConflictException(AppException):

    def __init__(
        self,
        message="Conflict",
        errors=None,
    ):
        super().__init__(
            message,
            status.HTTP_409_CONFLICT,
            errors,
        )