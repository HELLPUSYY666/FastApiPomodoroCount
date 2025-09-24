import json
from typing import List

import redis.asyncio as redis

from app.schema.task import TaskSchema


class TaskCacheRepository:
    def __init__(self, cache_session: redis.Redis) -> None:
        self.cache_session = cache_session

    async def get_all_tasks(self, key: str = "all_tasks") -> List[TaskSchema]:
        tasks_json = await self.cache_session.get(key)
        if tasks_json is None:
            return []
        return [TaskSchema.model_validate(task) for task in json.loads(tasks_json)]

    async def set_all_tasks(
        self, tasks: list[TaskSchema], key: str = "all_tasks"
    ) -> None:
        tasks_json = json.dumps(
            [task.model_dump() for task in tasks], ensure_ascii=False
        )
        await self.cache_session.set(key, tasks_json, ex=60)
