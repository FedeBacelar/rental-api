import asyncio
import logging
from datetime import datetime, time, timedelta

from fastapi import FastAPI

from app.core.config import settings
from app.db.session import SessionLocal
from app.services.rental.rental_service import RentalService


logger = logging.getLogger(__name__)


def _parse_daily_time(value: str) -> time:
    try:
        return time.fromisoformat(value)
    except ValueError as exc:
        raise RuntimeError("OVERDUE_WORKER_DAILY_TIME debe tener formato HH:MM") from exc


def _seconds_until_next_run(daily_time: str) -> float:
    now = datetime.now()
    target_time = _parse_daily_time(daily_time)
    next_run = datetime.combine(now.date(), target_time)

    if next_run <= now:
        next_run += timedelta(days=1)

    return (next_run - now).total_seconds()


def run_overdue_rental_worker_once() -> dict[str, int]:
    db = SessionLocal()
    try:
        result = RentalService(db).mark_overdue_rentals()
        logger.info(
            "Overdue rental worker finished: %s rentals, %s details updated",
            result["updated_rentals"],
            result["updated_details"],
        )
        return result
    except Exception:
        db.rollback()
        logger.exception("Overdue rental worker failed")
        raise
    finally:
        db.close()


async def _run_once_safely() -> None:
    try:
        await asyncio.to_thread(run_overdue_rental_worker_once)
    except Exception:
        logger.exception("Overdue rental worker run was skipped because it failed")


async def overdue_rental_worker_loop() -> None:
    if settings.overdue_worker_run_on_startup:
        await _run_once_safely()

    while True:
        seconds_to_sleep = _seconds_until_next_run(settings.overdue_worker_daily_time)
        logger.info(
            "Next overdue rental worker run in %.0f seconds at %s",
            seconds_to_sleep,
            settings.overdue_worker_daily_time,
        )
        await asyncio.sleep(seconds_to_sleep)
        await _run_once_safely()


def start_overdue_rental_worker(app: FastAPI) -> None:
    if not settings.overdue_worker_enabled:
        logger.info("Overdue rental worker is disabled")
        return

    app.state.overdue_rental_worker_task = asyncio.create_task(overdue_rental_worker_loop())


async def stop_overdue_rental_worker(app: FastAPI) -> None:
    task = getattr(app.state, "overdue_rental_worker_task", None)
    if task is None:
        return

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Overdue rental worker stopped")
