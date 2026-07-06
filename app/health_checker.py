from __future__ import annotations

import asyncio
import time
from typing import ClassVar

import httpx

from app.config import get_settings
from app.logger import get_logger
from app.metrics import health_check_duration_seconds, health_checks_total
from app.models import ComponentHealth, Node

logger = get_logger("health_checker")


class HealthChecker:
    """Run asynchronous HTTP health checks for components."""

    _client: ClassVar[httpx.AsyncClient | None] = None

    def __init__(self) -> None:
        settings = get_settings()
        self.timeout = httpx.Timeout(settings.request_timeout)
        if HealthChecker._client is None:
            HealthChecker._client = httpx.AsyncClient(timeout=self.timeout)

    @property
    def client(self) -> httpx.AsyncClient:
        assert HealthChecker._client is not None
        return HealthChecker._client

    async def check_component(self, component: Node) -> ComponentHealth:
        """Check one component endpoint and return a health record."""
        start = time.perf_counter()
        status = "unhealthy"
        try:
            response = await self.client.get(str(component.endpoint))
            status = "healthy" if response.status_code == 200 else "unhealthy"
        except Exception:
            pass
        latency = int((time.perf_counter() - start) * 1000)
        logger.info("component=%s endpoint=%s latency_ms=%s status=%s", component.id, component.endpoint, latency, status)
        return ComponentHealth(id=component.id, name=component.name, endpoint=component.endpoint, status=status, response_time_ms=latency)

    async def check(self, components: list[Node]) -> list[ComponentHealth]:
        """Check all components concurrently."""
        health_checks_total.inc(len(components))
        with health_check_duration_seconds.time():
            return await asyncio.gather(*(self.check_component(component) for component in components))