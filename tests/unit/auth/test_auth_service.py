from app.dependecy import get_auth_service
from app.service.auth import AuthService


async def get_google_redirect_url__success():
    auth_service = await get_auth_service()
    assert isinstance(auth_service, AuthService)


async def get_google_redirect_url__fail():
    pass
