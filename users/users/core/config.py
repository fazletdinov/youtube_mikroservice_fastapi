import os
from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(os.path.abspath("users")).parent


class AppSettings(BaseSettings):
    app_name: str = "Проект Youtube"
    API_V1_STR: str = "/api/v1/"

    model_config = SettingsConfigDict(extra="ignore")


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


class TokenAuthSettings(BaseSettings):
    access_expire: int
    refresh_expire: int
    refresh_cookie_name: str
    algorithm: str

    private_key_path: Path = BASE_DIR / "users" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "users" / "certs" / "jwt-public.pem"

    model_config = SettingsConfigDict(env_prefix="token_", env_file=BASE_DIR / ".env", extra="ignore")


class Settings:
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    token: TokenAuthSettings = TokenAuthSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

if __name__ == "__main__":
    import os
    from pathlib import Path

    print(Path(__name__).parent.parent.parent)
