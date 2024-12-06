from abc import ABC, abstractmethod


class MessageBrokerAbs(ABC):

    @abstractmethod
    async def connect(self):
        """Connect to the Redis instance for messaging (Celery)."""
        pass

    @abstractmethod
    async def publish_message(self, channel: str, message: str):
        """Publish a message to a Redis channel."""
        pass

    @abstractmethod
    async def close(self):
        """Close the Redis connection."""
        pass
