import json
from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import SecretStr
from redis import asyncio as aioredis  # type: ignore
from redis.backoff import ExponentialBackoff  # type: ignore
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError  # type: ignore
from redis.retry import Retry  # type: ignore

from video.core.config import settings

JSON_TYPE = TypeVar("JSON_TYPE", bound=json)  # type: ignore
KEY_STR = TypeVar("KEY_STR", bound=str)


class RedisDBBase(metaclass=ABCMeta):
    @abstractmethod
    async def set_key(self, key: KEY_STR, value: JSON_TYPE) -> None:
        pass

    @abstractmethod
    async def set_all(self, key: KEY_STR, values: list[JSON_TYPE]) -> None:
        pass

    @abstractmethod
    async def get_value(self, key: KEY_STR) -> JSON_TYPE:
        pass

    @abstractmethod
    async def is_exists(self, key: KEY_STR) -> bool:
        pass

    @abstractmethod
    async def delete_key(self, key: KEY_STR) -> Any:
        pass


class RedisDB(RedisDBBase):
    def __init__(
        self,
        host: str,
        port: int,
        password: SecretStr,
        expire_in_sec: int,
        retry: Retry,
        errors: list,
    ) -> None:
        self.redis = aioredis.Redis(
            host=host,
            port=port,
            password=password.get_secret_value(),
            retry=retry,
            retry_on_error=errors,
        )
        self.expire_in_sec: int = expire_in_sec

    async def set_key(self, key: KEY_STR, value: JSON_TYPE) -> None:
        data: str = json.dumps(jsonable_encoder(value))
        return await self.redis.set(key, data, ex=self.expire_in_sec)

    async def set_all(self, key: KEY_STR, values: list[JSON_TYPE]) -> None:
        datas: str = json.dumps(jsonable_encoder(values))
        return await self.redis.set(key, datas, ex=self.expire_in_sec)

    async def get_value(self, key: KEY_STR) -> Any:
        data = await self.redis.get(key)
        return json.loads(data)

    async def is_exists(self, key: KEY_STR) -> bool:
        return await self.redis.exists(key)

    async def delete_key(self, key: KEY_STR) -> None:
        return await self.redis.delete(key)

    async def delete_all(self) -> None:
        return await self.redis.flushall(asynchronous=True)


async def get_redis() -> RedisDB:
    return RedisDB(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
        expire_in_sec=settings.redis.expire_in_sec,
        retry=Retry(ExponentialBackoff(), settings.redis.retry),
        errors=[TimeoutError, ConnectionError, BusyLoadingError],
    )
