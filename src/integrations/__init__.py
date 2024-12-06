import os
from .task_queue.celery_task_queue import CeleryTaskQueue
from .cache.redis_cache import RedisCache
from .logging.python_logger import PythonLogger
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_USER = os.getenv("REDIS_USER", "")  # Новый параметр для пользователя
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_CACHE_DB = int(os.getenv("REDIS_CACHE_DB", 0))
REDIS_BROKER_DB = int(os.getenv("REDIS_BROKER_DB", 1))

# Настройка RedisCache
cache_service = RedisCache(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_CACHE_DB,
    password=REDIS_PASSWORD  # Добавлено поле для пароля
)

# Формирование строки подключения для Redis Broker
broker_url = f"redis://{REDIS_USER + ':' if REDIS_USER else ''}{REDIS_PASSWORD + '@' if REDIS_PASSWORD else ''}{REDIS_HOST}:{REDIS_PORT}/{REDIS_BROKER_DB}"

# Настройка CeleryTaskQueue
task_queue_service = CeleryTaskQueue(broker_url=broker_url, backend_url=broker_url)

logger = PythonLogger()