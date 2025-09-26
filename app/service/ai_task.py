import datetime as dt
from typing import Dict

import httpx
import requests

from app.models.user import UserProfile
from app.repository.task import TaskRepository
from app.repository.user import UserRepository
from app.settings import settings
from prompt_create_task_plan import USER_TASK_PROMPT


class AIService:
    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository) -> None:
        self.task_repo = task_repo
        self.user_repo = user_repo

    async def generate_task_plan(self, user: UserProfile) -> Dict:
        tasks = await self.task_repo.get_user_tasks(user_id=user.id)
        for task in tasks:
            user = await self.user_repo.get_user_by_id(task.user_id)

            prompt = USER_TASK_PROMPT.format(
                tasks_data={
                    "name": task.name,
                    "priority": task.priority,
                    "status": task.status,
                    "description": task.description,
                    "deadline": task.deadline,
                    "progress": task.progress,
                },
                requirements=user.prompts.prompt,
                progress_data=task.progress,
                priority=task.priority,
                status=task.status,
                today=dt.datetime.today(),
                deadline=task.deadline,
            )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.AI_API_URL,
                headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
                json={
                    "model": "grok-4",
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"},
                },
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]
