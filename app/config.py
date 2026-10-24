import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data"

load_dotenv(dotenv_path=BASE_DIR / ".env")


class ConfigError(RuntimeError):
    """Ошибка конфигурации приложения."""


def get_gigachat_credentials() -> str:
    creds = os.getenv("GIGACHAT_CREDENTIALS")
    if not creds:
        raise ConfigError("GIGACHAT_CREDENTIALS не найден в .env")
    return creds


def get_gigachat_scope() -> str:
    return os.getenv("GIGACHAT_SCOPE") or "GIGACHAT_API_PERS"


def get_forced_model() -> str | None:
    return os.getenv("GIGACHAT_MODEL") or None