from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from settings.auth_config import ALGORITHM, SECRET


class AuthService:
    def __init__(self):
        self._bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")

    def _get_secret_key(self) -> str:
        """Возвращает секретный ключ."""
        return SECRET

    def _get_algorithm(self) -> str:
        """Возвращает алгоритм шифрования."""
        return ALGORITHM

    def create_access_token(
        self, data: Dict[str, int], token_expiry_minutes: int = 14400
    ) -> str:
        """Создание access-токена с указанными данными."""
        expiry = datetime.now(timezone.utc) + timedelta(minutes=token_expiry_minutes)
        # Преобразуем время в метку времени (float)
        expiry_timestamp = expiry.timestamp()
        encode = {"id": int(data["id"]), "exp": expiry_timestamp}

        return jwt.encode(
            encode, self._get_secret_key(), algorithm=self._get_algorithm()
        )

    def create_refresh_token(
        self, data: Dict[str, int], refresh_token_expiry_minutes: int = 14400
    ) -> str:
        """Создание refresh-токена с указанными данными."""
        expiry = datetime.now(timezone.utc) + timedelta(minutes=refresh_token_expiry_minutes)
        # Преобразуем время в метку времени (float)
        expiry_timestamp = expiry.timestamp()
        encode = {"id": int(data["id"]), "exp": expiry_timestamp}
        return jwt.encode(
            encode, self._get_secret_key(), algorithm=self._get_algorithm()
        )

    def decode_token(self, token: str) -> Dict[str, Optional[int]]:
        """Декодирование токена."""
        try:
            payload = jwt.decode(
                token, self._get_secret_key(), algorithms=[self._get_algorithm()]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/"))) -> Dict[str, int]:
        """Получение текущего пользователя из токена."""
        payload = self.decode_token(token)
        id: int = payload.get("id")

        return {"id": int(id)}