from typing import Any
from redis.asyncio import Redis
from singleton_decorator import singleton
from .cache_abs import CacheAbs


@singleton
class RedisCache(CacheAbs):
    """Реализация кэша на базе Redis."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str = None,
    ):
        self.host = host
        self.port = port
        self.db = db
        self.redis: Redis = None
        self.password = password

    async def connect(self):
        """Подключение к Redis."""
        self.redis = Redis(
            host=self.host, port=self.port, db=self.db, password=self.password
        )

    async def set_value(self, key: str, value: Any, ttl: int = None):
        """Установить значение в Redis."""
        if isinstance(value, (dict, list)):
            value = str(value)  # Преобразуем сложные структуры в строку
        if ttl:
            await self.redis.set(key, value, ex=ttl)  # `ex` задаёт TTL в секундах
        else:
            await self.redis.set(key, value)

    async def get_value(self, key: str) -> Any:
        """Получить значение из Redis."""
        value = await self.redis.get(key)
        if value is not None:
            return value.decode("utf-8")  # Декодируем значение в строку
        return None

    async def delete_value(self, key: str):
        """Удалить ключ из Redis."""
        await self.redis.delete(key)

    async def close(self):
        """Закрыть соединение с Redis."""
        if self.redis:
            await self.redis.close()
