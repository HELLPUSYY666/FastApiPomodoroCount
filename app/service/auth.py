import datetime
import uuid
from dataclasses import dataclass
from datetime import timedelta

from fastapi import HTTPException
from jose import JWTError, jwt

from app.client import GoogleClient, YandexClient
from app.exception import (
    TokenExpiredException,
    TokenNotCorrectException,
    UserNotCorrectPasswordException,
    UserNotFoundException,
)
from app.models import UserProfile
from app.repository import UserRepository
from app.schema import UserCreateSchema, UserLoginSchema
from app.settings import settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code)
        user = await self.user_repository.get_user_by_email(email=user_data.email)

        if user:
            token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=token)

        username = user_data.email.split("@")[0] + "_" + uuid.uuid4().hex[:6]
        create_user_data = UserCreateSchema(
            username=username,
            password=None,
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name,
        )
        created = await self.user_repository.create_user(create_user_data)
        token = self.generate_access_token(user_id=created.id)
        return UserLoginSchema(user_id=created.id, access_token=token)

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        user_data = self.yandex_client.get_user_info(code)

        email = user_data.default_email or f"{user_data.login}@yandex.ru"
        name = user_data.name or user_data.login

        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Yandex")

        user = await self.user_repository.get_user_by_email(email=email)
        if user:
            token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=token)

        username = email.split("@")[0] + "_" + uuid.uuid4().hex[:6]
        create_user_data = UserCreateSchema(
            username=username,
            password=None,
            yandex_access_token=user_data.access_token,
            email=email,
            name=name,
        )
        created = await self.user_repository.create_user(create_user_data)
        token = self.generate_access_token(user_id=created.id)
        return UserLoginSchema(user_id=created.id, access_token=token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (datetime.datetime.utcnow() + timedelta(days=7)).timestamp()
        return jwt.encode(
            {"user_id": user_id, "expire": expires_date_unix},
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ENCODE_ALGORITHM,
        )

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ENCODE_ALGORITHM],
            )
        except JWTError:
            raise TokenNotCorrectException

        if payload["expire"] < datetime.datetime.utcnow().timestamp():
            raise TokenExpiredException

        return payload["user_id"]
