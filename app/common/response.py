from typing import Any

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class ApiResponse:

    @staticmethod
    def success(
        message: str = "Success",
        data: Any = None,
        meta: Any = None,
        status_code: int = 200,
    ):

        content = {
            "message": message,
            "data": jsonable_encoder(data),
        }

        if meta is not None:
            content["meta"] = jsonable_encoder(meta)

        return JSONResponse(
            status_code=status_code,
            content=content,
        )


    @staticmethod
    def error(
        message: str,
        data: Any = None,
        status_code: int = 400,
        meta: Any = None,
    ):

        content = {
            "message": message,
            "data": jsonable_encoder(data),
        }

        if meta is not None:
            content["meta"] = jsonable_encoder(meta)

        return JSONResponse(
            status_code=status_code,
            content=content,
        )