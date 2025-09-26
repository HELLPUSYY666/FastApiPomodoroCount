from typing import Any, Dict, cast

from fastapi import status
from httpx import Headers


class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "Password not correct"


class TokenExpiredException(Exception):
    detail = "Token expired"


class TokenNotCorrectException(Exception):
    detail = "Token not correct"


class TaskNotFound(Exception):
    detail = "Task not found"


class AlreadyExists(Exception):
    def __init__(
        self, model_name: str, headers: Dict[str, Any] | Headers | None = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{model_name.capitalize()} already exists",
            headers=cast(dict[str, Any], headers),
        )


class EmailNotGiven(Exception):
    detail = "Email not given"
