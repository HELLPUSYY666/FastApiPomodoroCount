from dataclasses import dataclass

from app.exception import TaskNotFound
from app.repository import TaskCacheRepository, TaskRepository
from app.schema.task import TaskCreateSchema, TaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCacheRepository

    async def get_tasks(self) -> list[TaskSchema]:
        tasks = await self.task_cache.get_all_tasks()

        if tasks:
            return tasks

        tasks = await self.task_repository.get_tasks()

        if tasks:
            task_schema = [TaskSchema.model_validate(task.__dict__) for task in tasks]
            await self.task_cache.set_all_tasks(task_schema)
            return task_schema
        else:
            return []

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task = await self.task_repository.create_task(body, user_id)
        return TaskSchema.model_validate(task.__dict__)

    async def update_task_name(
        self, task_id: int, name: str, user_id: int
    ) -> TaskSchema:
        task = await self.task_repository.get_user_task(task_id, user_id)
        if not task:
            raise TaskNotFound
        task = await self.task_repository.update_task_name(task_id, name)
        return TaskSchema.model_validate(task.__dict__)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(task_id, user_id)
        if not task:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)
