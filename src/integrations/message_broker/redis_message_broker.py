import aioredis
from .message_broker_abs import MessageBrokerAbs
from singleton_decorator import singleton


@singleton
class RedisMessageBroker(MessageBrokerAbs):
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 1):
        self.host = host
        self.port = port
        self.db = db
        self.redis = None

    async def connect(self):
        """Connect to Redis for message brokering (Celery)"""
        self.redis = await aioredis.create_redis_pool(
            (self.host, self.port),
            db=self.db,
        )

    async def publish_message(self, channel: str, message: str):
        """Publish message to a Redis channel"""
        await self.redis.publish(channel, message)

    async def close(self):
        """Close Redis connection"""
        self.redis.close()
        await self.redis.wait_closed()
