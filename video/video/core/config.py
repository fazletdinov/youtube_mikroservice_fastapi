from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__name__).parent.parent.parent


class AppSettings(BaseSettings):
    app_name: str = "Microservice video"
    API_V1_STR: str = "/api/v1/"


class DBSettings(BaseSettings):
    host: str
    name: str
    port: int
    user: str
    password: SecretStr
    echo: bool = True

    model_config = SettingsConfigDict(env_prefix="db_", env_file=BASE_DIR / ".env", extra="ignore")

    def _url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:"
            f"{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    @property
    def async_url(self) -> str:
        return self._url()


class RedisDBSettings(BaseSettings):
    host: str
    port: int
    password: SecretStr
    expire_in_sec: int
    retry: int

    def _url(self):
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/0"

    @property
    def backend_url(self):
        return self._url()

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_prefix="redis_", extra="ignore")


class RabbitmqSettings(BaseSettings):
    host: str
    user: str
    port1: int
    port2: int
    password: SecretStr
    hostname: str
    vhost: str

    def _url(self) -> str:
        return f"amqp://{self.user}:{self.password.get_secret_value()}@" f"{self.host}:{self.port1}/{self.vhost}"

    @property
    def broker_url(self):
        return self._url()

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_prefix="rabbitmq_", extra="ignore")


class Settings:
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    redis: RedisDBSettings = RedisDBSettings()
    rabbitmq: RabbitmqSettings = RabbitmqSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
