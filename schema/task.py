from pydantic import BaseModel, Field, model_validator


class TaskSchema(BaseModel):
    name: str
    pomodoro_count: int | None = None
    category_id: int | None = None
    user_id: int
    model_config = {"from_attributes": True}

    @model_validator(mode='before')
    @classmethod
    def check_name_not_none(cls, values):
        if values.get("name") is None:
            raise ValueError("Name cannot be None")
        return values


class TaskCreateSchema(BaseModel):
    name: str
    pomodoro_count: int | None = None
    category_id: int | None = None
