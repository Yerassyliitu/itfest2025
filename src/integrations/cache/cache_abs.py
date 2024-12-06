from abc import ABC, abstractmethod
from typing import Any


class CacheAbs(ABC):
    """Абстрактный класс для работы с кэшем."""

    @abstractmethod
    async def connect(self):
        """Подключение к Кэшу."""
        pass

    @abstractmethod
    async def set_value(self, key: str, value: Any, ttl: int = None):
        """Установить значение в кэш с необязательным временем жизни."""
        pass

    @abstractmethod
    async def get_value(self, key: str) -> Any:
        """Получить значение из кэша по ключу."""
        pass

    @abstractmethod
    async def delete_value(self, key: str):
        """Удалить значение из кэша по ключу."""
        pass

    @abstractmethod
    async def close(self):
        """Закрыть соединение с Кэшем."""
        pass
