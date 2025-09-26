from fastapi import APIRouter, Depends, HTTPException

from app.dependecy import get_request_user_id
from app.schema.ai_task import AIPlanRequest, AIPlanResponse
from app.service.ai_task import AIService

router = APIRouter(prefix="/ai-tasks", tags=["AI Tasks"])


@router.post("/{user_id}/generate-plan", response_model=AIPlanResponse)
async def generate_ai_plan(
    user_id: int,
    request: AIPlanRequest,
    current_user: int = Depends(get_request_user_id),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    plan = AIService.generate_task_plan(
        user_id, request.requirements, request.progress_data
    )
    return {"plan": plan}
