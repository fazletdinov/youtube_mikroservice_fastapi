from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__name__).parent.parent.parent


class AppSettings(BaseSettings):
    app_name: str = "Проект Youtube"
    API_V1_STR: str = "/api/v1/"


class DBSettings(BaseSettings):
    host: str
    name: str
    port: int
    user: str
    password: SecretStr
    echo: bool = True

    model_config = SettingsConfigDict(env_prefix="db_", env_file=BASE_DIR / ".env")

    def _url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:"
            f"{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    @property
    def async_url(self) -> str:
        return self._url()


class Settings:
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
