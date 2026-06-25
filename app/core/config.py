import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str
    overdue_worker_enabled: bool
    overdue_worker_run_on_startup: bool
    overdue_worker_daily_time: str


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_settings() -> Settings:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    return Settings(
        database_url=database_url,
        overdue_worker_enabled=_get_bool_env("OVERDUE_WORKER_ENABLED", True),
        overdue_worker_run_on_startup=_get_bool_env("OVERDUE_WORKER_RUN_ON_STARTUP", True),
        overdue_worker_daily_time=os.getenv("OVERDUE_WORKER_DAILY_TIME", "00:00"),
    )


settings = get_settings()
