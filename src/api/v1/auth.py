import random
from typing import Annotated
from fastapi import APIRouter, Depends

from src.schemas.auth import EmailInput, EmailCodeInput
from src.services.user import UserService
from src.api.exceptions.auth import (
    InvalidAccessTokenException,
    UserAlreadyExistsException,
    CacheServiceException,
    ServerErrorException,
    CodeExpiredException,
    EmailServiceUnavailableException,
    InvalidCodeException
)
from src.api.v1.dependencies import get_auth_service, get_user_service

from src.integrations import logger

from fastapi import APIRouter, Depends
from src.integrations import cache_service, task_queue_service
from src.services.auth_service import AuthService


auth_router = APIRouter(prefix="/v1/auth", tags=["auth"])


@auth_router.post(
    "/email/send-code/",
    status_code=200,
    summary="Отправка кода на email.",
)
async def email_send_code(
    email_input: EmailInput,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        logger.info(f"Получен запрос на отправку кода на email {email_input.email}.")

        # Проверка существования пользователя
        user_exists = await user_service.get_entity(email=email_input.email)
        # Генерация случайного кода
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])

        # Сохранение кода в кэш
        key = f"email_code:{email_input.email}"
        ttl = 1200
        try:
            await cache_service.set_value(key, random_code, ttl=ttl)
        except Exception as e:
            logger.error(
                f"Ошибка при сохранении кода в кэш для email {email_input.email}: {str(e)}"
            )
            raise CacheServiceException

        # Отправка email
        try:
            await task_queue_service.enqueue(
                task_name="send_email",
                args=[
                    email_input.email,
                    f"Код подтверждения: {random_code}. Никому не сообщайте.",
                ],
            )
        except Exception as e:
            logger.error(
                f"Ошибка при отправке email для {email_input.email}: {str(e)}"
            )
            raise EmailServiceUnavailableException

        logger.info(f"Код успешно отправлен на email {email_input.email}.")
        return {"message": "Код успешно отправлен", "code": random_code}

    except UserAlreadyExistsException as e:
        logger.error(f"Пользователь уже существует: {email_input.email}")
        raise e
    except CacheServiceException as e:
        logger.error(f"Ошибка кэша: {email_input.email}")
        raise e
    except EmailServiceUnavailableException as e:
        logger.error(f"Ошибка email-сервиса: {email_input.email}")
        raise e
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {email_input.email}: {str(e)}")
        raise ServerErrorException


@auth_router.post(
    "/email/confirm-code/",
    status_code=200,
    summary="Подтверждение кода с email.",
)
async def email_confirm_code(
    email_code_input: EmailCodeInput,
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        email = email_code_input.email

        logger.info(
            f"Получен запрос на подтверждение кода для email {email_code_input.email}."
        )

        # Проверяем наличие кода в кэше
        key = f"email_code:{email_code_input.email}"
        stored_code = await cache_service.get_value(key)

        if not stored_code:
            logger.warning(
                f"Код для email {email_code_input.email} недействителен или истёк."
            )
            raise CodeExpiredException

        # Проверяем корректность кода
        if email_code_input.code != stored_code:
            logger.warning(f"Неверный код для email {email_code_input.email}.")
            raise InvalidCodeException

        # Удаляем использованный код
        await cache_service.delete_value(key)

        user_exists = await user_service.get_entity(email=email)
        if user_exists is not None:
            data = {"id": str(user_exists.id)}

            token = auth_service.create_access_token(data=data)

            return {"token": token}

        created_user = await user_service.create_entity({"email": email})
        data = {"id": str(created_user.id)}
        token = auth_service.create_access_token(data=data)
        logger.info(
            f"Код для email {email_code_input.email} успешно подтверждён. Токен для регистрации создан."
        )
        return {
            "token": token
        }
    except CodeExpiredException as e:
        logger.error(f"Код истёк: {email_code_input.email}")
        raise e
    except InvalidCodeException as e:
        logger.error(f"Неверный код: {email_code_input.email}")
        raise e
    except Exception as e:
        logger.error(
            f"Неизвестная ошибка: {email_code_input.email}: {str(e)}"
        )
        raise ServerErrorException


@auth_router.post(
    "/current-user/",
    status_code=200,
    summary="Возвращает пользователя.",
    description="Возвращает пользователя.",
)
async def get_user(
    user: Annotated[dict, Depends(get_auth_service().get_current_user)],
):
    try:
        logger.info("Запрос текущего пользователя.")
        return user
    except InvalidAccessTokenException:
        logger.warning("Неверный access токен.")
        raise
    except Exception as e:
        logger.error(f"Ошибка сервера при запросе текущего пользователя: {str(e)}")
        raise ServerErrorException