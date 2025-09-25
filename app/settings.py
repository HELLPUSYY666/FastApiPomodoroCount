from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123"
    DB_NAME: str = "fast_api_db"
    DB_DRIVER: str = "postgresql+asyncpg"
    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 1
    JWT_SECRET_KEY: str = "secret_key"
    JWT_ENCODE_ALGORITHM: str = "HS256"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URL: str = ""
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"

    YANDEX_CLIENT_ID: str = ""
    YANDEX_CLIENT_SECRET: str = ""
    YANDEX_REDIRECT_URL: str = ""
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"

    CELERY_REDIS_URL: str = "redis://:your_strong_password@localhost:6379/1"

    from_email: str = "pzakariya@mail.ru"
    SMTP_PORT: int = 465
    SMTP_HOST: str = "smtp.mail.ru"
    SMTP_PASSWORD: str = "57ZdNKZrJR5wEBXEIlA8"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def google_redirect_url(self) -> str:
        return (
            f"https://accounts.google.com/o/oauth2/auth"
            f"?response_type=code"
            f"&client_id={self.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={self.GOOGLE_REDIRECT_URL}"
            f"&scope=openid%20profile%20email"
            f"&access_type=offline"
        )

    @property
    def yandex_redirect_url(self) -> str:
        return (
            f"https://oauth.yandex.ru/authorize?"
            f"client_id={self.YANDEX_CLIENT_ID}&"
            f"redirect_uri={self.YANDEX_REDIRECT_URL}&"
            f"response_type=code"
            f"&access_type=offline"
        )


settings = Settings()
