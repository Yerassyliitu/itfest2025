from celery import Celery
from typing import Any, Optional
from .task_queue_abs import TaskQueueAbs
from singleton_decorator import singleton


@singleton
class CeleryTaskQueue(TaskQueueAbs):
    """
    Concrete implementation of TaskIntegrationAbs using Celery for asynchronous task queuing.
    """

    def __init__(self, broker_url: str = "redis://localhost:6379/0", backend_url: str = "redis://localhost:6379/0"):
        """
        Initializes the Celery app with a broker URL and backend URL.
        """
        self.celery_app = Celery(
            "tasks",
            broker=broker_url,
            backend=backend_url,
        )
        # Example configuration, adjust as needed
        self.celery_app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
            broker_connection_retry_on_startup=True
        )

    async def enqueue(
        self, task_name: str, args: Optional[list] = None, kwargs: Optional[dict] = None
    ) -> str:
        """
        Enqueues a task into Celery.
        Returns the task ID.
        """
        args = args or []
        kwargs = kwargs or {}
        task = self.celery_app.send_task(task_name, args=args, kwargs=kwargs)
        return task.id

    async def get_task_status(self, task_id: str) -> str:
        """
        Retrieves the status of a task by its ID.
        """
        task = self.celery_app.AsyncResult(task_id)
        return task.status

    async def get_task_result(self, task_id: str) -> Any:
        """
        Retrieves the result of a task after it has completed.
        """
        task = self.celery_app.AsyncResult(task_id)
        if task.state == "SUCCESS":
            return task.result
        elif task.state == "FAILURE":
            raise Exception(f"Task {task_id} failed with error: {task.info}")
        else:
            raise Exception(
                f"Task {task_id} is not completed yet. Current state: {task.state}"
            )

    def add_task(self, task_name: str, func):
        """
        Registers a task with the Celery app.
        """
        self.celery_app.task(name=task_name)(func)

