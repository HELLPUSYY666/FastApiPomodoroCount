from typing import Optional

from pydantic import BaseModel


class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    access_token: str


class YandexUserData(BaseModel):
    id: int
    login: str
    real_name: Optional[str] = None
    display_name: Optional[str] = None
    default_email: Optional[str] = None
    access_token: str

    @property
    def name(self) -> str:
        return self.real_name or self.display_name or self.login

    @property
    def email(self) -> str:
        if self.default_email:
            return self.default_email
        return f"{self.login}@yandex.ru"
