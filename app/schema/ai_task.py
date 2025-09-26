from typing import Dict

from pydantic import BaseModel


class AIPlanRequest(BaseModel):
    requirements: str
    progress_data: Dict[str, any]


class AIPlanResponse(BaseModel):
    plan: Dict[str, any]
