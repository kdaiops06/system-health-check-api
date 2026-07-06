from fastapi import FastAPI
from prometheus_client import make_asgi_app

from app.api import router
from app.config import get_settings
from app.logger import configure_logging

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(router)
app.mount("/metrics", make_asgi_app())


@app.on_event("startup")
def startup() -> None:
	configure_logging()


@app.get("/")
def root() -> dict[str, str]:
	return {"application": settings.app_name, "version": settings.app_version, "status": "ok"}


@app.get("/health")
@app.get("/live")
@app.get("/ready")
def status() -> dict[str, str]:
	return {"status": "ok"}