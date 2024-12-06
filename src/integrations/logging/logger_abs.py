from abc import ABC, abstractmethod
from typing import Any

class LoggerAbs(ABC):
    """Абстрактный класс для логирования."""

    @abstractmethod
    def info(self, message: str, **kwargs: Any):
        """Логирование информационного сообщения."""
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any):
        """Логирование сообщения об ошибке."""
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs: Any):
        """Логирование отладочного сообщения."""
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any):
        """Логирование предупреждения."""
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs: Any):
        """Логирование критического сообщения."""
        pass
