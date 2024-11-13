import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


BASE_DIR = Path(__file__).parent.parent


class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: Literal[
        'debug',
        'info',
        'warning',
        'error',
        'critical',
    ] = 'info'
    log_format: str = LOG_DEFAULT_FORMAT


class AppSettings(BaseSettings):
    model_config = {
        "case_sensitive": False,
        "env_nested_delimiter": "__",
        "env_prefix": "APP_CONFIG__",
    }
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()


app_settings = AppSettings()
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
API_ADMIN_PWD = os.environ.get("API_ADMIN_PWD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    f"postgresql+asyncpg://"
    f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


@dataclass(frozen=True)
class DatabaseConfig:
    db_uri: str

    @staticmethod
    def from_env() -> "DatabaseConfig":
        uri = os.getenv("DATABASE_URI", DATABASE_URI)

        if not uri:
            raise RuntimeError("Missing DATABASE_URI environment variable")

        return DatabaseConfig(uri)


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


@dataclass(frozen=True)
class RedisConfig:
    rd_uri: str

    @staticmethod
    def from_env() -> "RedisConfig":
        uri = os.environ.get("REDIS_URI", f"redis://{REDIS_HOST}:{REDIS_PORT}")

        if not uri:
            raise RuntimeError("Missing REDIS_URI environment variable")

        return RedisConfig(uri)


class MinIOConfig(BaseModel):
    endpoint_url: str = os.getenv("MINIO_ENDPOINT_URL")
    access_key: str = os.getenv("MINIO_ACCESS_KEY")
    secret_key: str = os.getenv("MINIO_SECRET_KEY")


class JWTSettings(BaseModel):
    private_key_path: Path = (
        Path(__file__).parent.parent / "certs" / "jwt-private.pem"
    )
    public_key_path: Path = (
        Path(__file__).parent.parent / "certs" / "jwt-public.pem"
    )
    algorithm: str = "RS512"
    access_token_expire_minutes: int = 1500
    refresh_token_expire_days: int = 30
    refresh_token_by_user_limit: int = 5

    _private_key: str = None
    _public_key: str = None

    def __post_init__(self):
        if self._private_key is None:
            self._private_key = self.private_key_path.read_text()
        if self._public_key is None:
            self._public_key = self.public_key_path.read_text()

    @property
    def private_key(self) -> str:
        if self._private_key is None:
            self._private_key = self.private_key_path.read_text()
        return self._private_key

    @property
    def public_key(self) -> str:
        if self._public_key is None:
            self._public_key = self.public_key_path.read_text()
        return self._public_key
