from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.core.exceptions import (
    AuthenticationError,
    DatabaseConnectionError,
    DataNotFoundError,
    DataConflictError,
    InvalidJsonFormatError
)

def register_exception_handlers(app: FastAPI):
    def error_response(status_code: int, message: str, errors: list = None):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "message": message,
                "errors": errors if errors else []
            }
        )

    @app.exception_handler(AuthenticationError)
    async def auth_exception_handler(request: Request, exc: AuthenticationError):
        return error_response(401, exc.message)

    @app.exception_handler(DatabaseConnectionError)
    async def db_exception_handler(request: Request, exc: DatabaseConnectionError):
        return error_response(500, exc.message)

    @app.exception_handler(DataNotFoundError)
    async def data_not_found_handler(request: Request, exc: DataNotFoundError):
        return error_response(404, exc.message)

    @app.exception_handler(DataConflictError)
    async def data_conflict_handler(request: Request, exc: DataConflictError):
        return error_response(409, exc.message)

    @app.exception_handler(InvalidJsonFormatError)
    async def invalid_json_format_handler(request: Request, exc: InvalidJsonFormatError):
        return error_response(400, exc.message)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        error_details = [
            {
                "field": ".".join(str(part) for part in err.get("loc", [])),
                "error": err.get("msg", "")
            }
            for err in exc.errors()
        ]
        return error_response(422, "요청한 데이터 형식이 잘못되었습니다.", error_details)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return error_response(500, "서버 내부 오류가 발생했습니다.")