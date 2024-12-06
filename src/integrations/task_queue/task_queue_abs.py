from abc import ABC, abstractmethod
from typing import Any, Optional


class TaskQueueAbs(ABC):
    """
    Abstract class for asynchronous task integration using a task queue system like Celery.
    Defines the basic operations for handling tasks.
    """

    @abstractmethod
    async def enqueue(self, task_name: str, args: Optional[list] = None, kwargs: Optional[dict] = None) -> str:
        """
        Enqueues a task into the task queue.
        Returns the task ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_task_status(self, task_id: str) -> str:
        """
        Gets the status of a task by its ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_task_result(self, task_id: str) -> Any:
        """
        Retrieves the result of a completed task.
        """
        raise NotImplementedError
