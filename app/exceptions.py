from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse


class BaseDatabaseException(Exception):
    def __init__(self, model, message) -> None:
        self.model = model
        self.message = message

    def __str__(self) -> str:
        return f"{self.model} - {self.message}"

class ResourceNotFound(BaseDatabaseException):
    def __init__(self, model) -> None:
        self.model = model
        self.message = 'Resource not found'

class ResourceAlreadyExists(BaseDatabaseException):
    def __init__(self, model) -> None:
        self.model = model
        self.message = 'Resource already exists'

class BaseHTTPException(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        return f"{self.status_code}: {self.message}"

class Unauthorized(BaseHTTPException):
    def __init__(self, message: str = None) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = f'Unauthorized - {message}' if message else 'Unauthorized'

class Forbidden(BaseHTTPException):
    def __init__(self, message: str = None) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.message = f'Forbidden - {message}' if message else 'Forbidden'


def parse_response(status_code: int, error: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": error, "user_friendly": True } )

def init_error_handling(app: FastAPI) -> None:
    @app.exception_handler(Unauthorized)
    async def unauthorized_exception_handler(request: Request, exc: Unauthorized):
        return parse_response(status.HTTP_401_UNAUTHORIZED, str(exc))

    @app.exception_handler(Forbidden)
    async def forbidden_exception_handler(request: Request, exc: Forbidden):
        return parse_response(status.HTTP_403_FORBIDDEN, str(exc))
    
    @app.exception_handler(ResourceNotFound)
    async def resource_not_found_exception_handler(request: Request, exc: ResourceNotFound):
        return parse_response(status.HTTP_404_NOT_FOUND, str(exc)) 
       
    @app.exception_handler(ResourceAlreadyExists)
    async def resource_already_exists_exception_handler(request: Request, exc: ResourceAlreadyExists):
        return parse_response(status.HTTP_409_CONFLICT, str(exc))