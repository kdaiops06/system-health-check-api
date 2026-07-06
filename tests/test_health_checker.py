import asyncio
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from app.health_checker import HealthChecker
from app.models import ComponentHealth, Node


@pytest.fixture
def node() -> Node:
    return Node(id="a", name="A", endpoint="http://a.local")


@pytest.fixture
def checker() -> HealthChecker:
    original = HealthChecker._client
    client = Mock()
    client.get = AsyncMock()
    HealthChecker._client = client
    try:
        yield HealthChecker()
    finally:
        HealthChecker._client = original


@pytest.mark.asyncio
async def test_successful_http_200_returns_healthy(checker: HealthChecker, node: Node) -> None:
    checker.client.get.return_value = httpx.Response(200)
    result = await checker.check_component(node)
    assert result.status == "healthy"


@pytest.mark.asyncio
async def test_http_500_returns_unhealthy(checker: HealthChecker, node: Node) -> None:
    checker.client.get.return_value = httpx.Response(500)
    result = await checker.check_component(node)
    assert result.status == "unhealthy"


@pytest.mark.asyncio
async def test_timeout_returns_unhealthy(checker: HealthChecker, node: Node) -> None:
    checker.client.get.side_effect = httpx.TimeoutException("timeout")
    result = await checker.check_component(node)
    assert result.status == "unhealthy"


@pytest.mark.asyncio
async def test_multiple_components_are_checked_concurrently(checker: HealthChecker) -> None:
    gate = asyncio.Event()
    started: list[str] = []

    async def fake_check(component: Node) -> ComponentHealth:
        started.append(component.id)
        if len(started) == 2:
            gate.set()
        await gate.wait()
        return ComponentHealth(id=component.id, name=component.name, endpoint=component.endpoint, status="healthy", response_time_ms=1)

    components = [
        Node(id="a", name="A", endpoint="http://a.local"),
        Node(id="b", name="B", endpoint="http://b.local"),
    ]
    checker.check_component = AsyncMock(side_effect=fake_check)

    results = await checker.check(components)

    assert started == ["a", "b"]
    assert [result.id for result in results] == ["a", "b"]
