from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.common.response import ApiResponse
from app.exceptions import AppException


def register_exception_handlers(
    app: FastAPI
):

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):

        return ApiResponse.error(
            message=exc.message,
            status_code=exc.status_code,
            data=exc.errors,
        )


    @app.exception_handler(RequestValidationError)
    async def validation_handler(
        request: Request,
        exc: RequestValidationError,
    ):

        return ApiResponse.error(
            message="Validation Error",
            status_code=422,
            data=exc.errors(),
        )


    @app.exception_handler(Exception)
    async def exception_handler(
        request: Request,
        exc: Exception,
    ):

        return ApiResponse.error(
            message="Internal Server Error",
            status_code=500,
        )