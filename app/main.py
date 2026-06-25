from pathlib import Path
import os
import time
import webbrowser

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.controller.catalog.catalog_controller import router as catalog_router
from app.controller.customer.customer_controller import router as customer_router
from app.controller.health_controller import router as health_router
from app.controller.inventory.inventory_controller import router as inventory_router
from app.controller.rental.rental_controller import router as rental_router
from app.controller.security.auth_controller import router as auth_router
from app.controller.security.user_controller import router as user_router
from app.workers.overdue_rental_worker import (
    start_overdue_rental_worker,
    stop_overdue_rental_worker,
)


def run_migrations() -> None:
    base_path = Path(__file__).resolve().parent.parent
    alembic_cfg = Config(str(base_path / "alembic.ini"))
    last_error = None

    for _ in range(15):
        try:
            command.upgrade(alembic_cfg, "head")
            return
        except OperationalError as exc:
            last_error = exc
            time.sleep(2)

    raise RuntimeError("Database connection failed while running migrations") from last_error


app = FastAPI(title="RentalApi", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    run_migrations()
    start_overdue_rental_worker(app)
    if os.getenv("OPEN_SWAGGER_ON_STARTUP") == "1":
        webbrowser.open("http://127.0.0.1:8000/docs")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await stop_overdue_rental_worker(app)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(customer_router)
app.include_router(inventory_router)
app.include_router(rental_router)
app.include_router(user_router)
