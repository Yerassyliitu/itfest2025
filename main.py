from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.integrations import cache_service

from src.api.v1.routers import all_routers
from src.api.exceptions.auth import (
    InvalidAccessTokenException,
    UserAlreadyExistsException,
    CodeExpiredException,
    InvalidCodeException,
    CacheServiceException,
    ServerErrorException,
    EmailServiceUnavailableException,
)

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Обработчики исключений
@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsException
):
    return JSONResponse(
        status_code=400,
        content={"detail": "UserAlreadyExists"},
    )


@app.exception_handler(CodeExpiredException)
async def code_expired_exception_handler(request: Request, exc: CodeExpiredException):
    return JSONResponse(
        status_code=400,
        content={"detail": "CodeExpired"},
    )


@app.exception_handler(InvalidCodeException)
async def invalid_code_exception_handler(request: Request, exc: InvalidCodeException):
    return JSONResponse(
        status_code=400,
        content={"detail": "InvalidCode"},
    )


@app.exception_handler(CacheServiceException)
async def cache_service_exception_handler(request: Request, exc: CacheServiceException):
    return JSONResponse(
        status_code=500,
        content={"detail": "CacheServiceError"},
    )


@app.exception_handler(ServerErrorException)
async def server_error_exception_handler(request: Request, exc: ServerErrorException):
    return JSONResponse(
        status_code=500,
        content={"detail": "ServerError"},
    )


@app.exception_handler(EmailServiceUnavailableException)
async def server_error_exception_handler(request: Request, exc: ServerErrorException):
    return JSONResponse(
        status_code=500,
        content={"detail": "EmailServiceUnavailableException"},
    )

@app.exception_handler(InvalidAccessTokenException)
async def server_error_exception_handler(request: Request, exc: InvalidAccessTokenException):
    return JSONResponse(
        status_code=500,
        content={"detail": "InvalidAccessTokenException"},
    )

@app.on_event("startup")
async def on_startup():
    """Создание всех таблиц в базе данных при запуске приложения."""
    await cache_service.connect()


@app.get("/")
def hello():
    return {"Details": "Add /docs"}


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}
    )


for router in all_routers:
    app.include_router(router, prefix="/api")
