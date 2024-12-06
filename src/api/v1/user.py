import random
from typing import Annotated
from fastapi import APIRouter, Depends

from src.services.user import UserService
from src.api.exceptions.auth import (
    UserNotFoundException
)
from src.api.v1.dependencies import get_auth_service, get_user_service

from src.integrations import logger

from fastapi import APIRouter, Depends



user_router = APIRouter(prefix="/v1/user", tags=["user"])

@user_router.get(
    "/me/",
    status_code=200,
    summary="Получения пользователя"
)
async def get_user_me(
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_token: Annotated[dict, Depends(get_auth_service().get_current_user)],
):
    try:
        user_id = user_token["id"]
        user = await user_service.get_entity(id=user_id)
        if not user:
            raise UserNotFoundException
        return user
    except UserNotFoundException:
        logger.warning("Такого пользователя нет в базе.")
        raise
    except Exception as e:
        logger.error(f"Ошибка сервера при запросе текущего пользователя: {str(e)}")
