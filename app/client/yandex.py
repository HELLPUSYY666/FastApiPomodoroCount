from dataclasses import dataclass

import httpx

from app.schema import YandexUserData
from app.settings import settings


@dataclass
class YandexClient:
    settings: settings  # type: ignore
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = self._get_user_access_token(code)
        async with self.async_client() as client:
            response = await client.get(
                "https://login.yandex.ru/info?format=json",
                headers={"Authorization": f"OAuth {access_token}"},
            )
        response.raise_for_status()
        return YandexUserData(**response.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_CLIENT_SECRET,
            "redirect_uri": self.settings.YANDEX_REDIRECT_URL,
            "grant_type": "authorization_code",
        }
        async with self.async_client() as client:
            response = await client.post(self.settings.YANDEX_TOKEN_URL, data=data)
        response.raise_for_status()

        token_data = response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("Yandex did not return an access token")

        return access_token
