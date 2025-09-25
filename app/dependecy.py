import httpx
from fastapi import Depends, HTTPException, Security, security
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.client import GoogleClient, YandexClient
from app.client.mail import MailClient
from app.exception import TokenExpiredException, TokenNotCorrectException
from app.infrastructure.cache import get_redis_connection
from app.infrastructure.database import get_session_maker
from app.repository import TaskCacheRepository, TaskRepository, UserRepository
from app.service import AuthService, TaskService, UserService
from app.settings import settings


async def get_task_repository(
    session_maker: async_sessionmaker[AsyncSession] = Depends(get_session_maker),
) -> TaskRepository:
    return TaskRepository(session_maker)


async def get_task_cache_repository() -> TaskCacheRepository:
    redis_connection = await get_redis_connection()
    return TaskCacheRepository(redis_connection)


def get_task_service(
    task_repository: TaskRepository = Depends(get_task_repository),
    task_cache: TaskCacheRepository = Depends(get_task_cache_repository),
) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=task_cache)


def get_user_repository(
    session_maker: async_sessionmaker[AsyncSession] = Depends(get_session_maker),
) -> UserRepository:
    return UserRepository(session_maker)


def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


def get_google_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> GoogleClient:
    return GoogleClient(settings=settings, async_client=async_client)


def get_yandex_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> YandexClient:
    return YandexClient(settings=settings, async_client=async_client)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        google_client=google_client,
        yandex_client=yandex_client,
    )


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrectException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
