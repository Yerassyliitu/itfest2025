import logging
from typing import Any
from .logger_abs import LoggerAbs


class PythonLogger(LoggerAbs):
    """Реализация логирования с использованием стандартного логгера Python."""

    def __init__(self, logger_name: str = "FastAPIApp"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Настройка обработчика для вывода логов в консоль
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Формат логов
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def info(self, message: str, **kwargs: Any):
        """Логирование информационного сообщения."""
        self.logger.info(message, extra=kwargs)

    def error(self, message: str, **kwargs: Any):
        """Логирование сообщения об ошибке."""
        self.logger.error(message, extra=kwargs)

    def debug(self, message: str, **kwargs: Any):
        """Логирование отладочного сообщения."""
        self.logger.debug(message, extra=kwargs)

    def warning(self, message: str, **kwargs: Any):
        """Логирование предупреждения."""
        self.logger.warning(message, extra=kwargs)

    def critical(self, message: str, **kwargs: Any):
        """Логирование критического сообщения."""
        self.logger.critical(message, extra=kwargs)
