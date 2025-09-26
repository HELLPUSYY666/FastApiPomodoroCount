from dataclasses import dataclass
from typing import Dict, List

import requests

from app.repository.cache_task import TaskCacheRepository
from app.repository.task import TaskRepository
from app.settings import settings
from prompt_create_task_plan import USER_TASK_PROMPT
from worker.celery import generate_ai_plan_task


@dataclass
class AIService:
    task_repository: TaskRepository
    task_cache: TaskCacheRepository

    def generate_task_plan(self, user_id: int) -> Dict:
        tasks = self.task_repository.get_user_tasks(user_id)
        generate_ai_plan_task.delay()

        tasks_data = [
            {
                "name": task.name,
                "description": task.description,
                "priority": task.priority,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "status": task.status,
            }
            for task in tasks
        ]
        prompt = USER_TASK_PROMPT.format(
            tasks_data=tasks_data,
            requirements=requirements,
            progress_data=progress_data,
        )

        response = requests.post(
            settings.AI_API_URL,
            headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
            json={
                "model": "grok-4",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
