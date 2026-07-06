from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from app.models import ComponentHealth, Node


@pytest.fixture
def node() -> Node:
    return Node(id="a", name="A", endpoint="http://a.local")


@pytest.fixture
def client() -> Mock:
    mock_client = Mock()
    mock_client.get = AsyncMock()
    return mock_client


@pytest.fixture
def checker(client: Mock):
    with patch("app.health_checker.HealthChecker._client", client), patch("app.health_checker.get_settings", return_value=Mock(request_timeout=5)):
        from app.health_checker import HealthChecker

        yield HealthChecker()


@pytest.mark.asyncio
async def test_successful_http_200_returns_healthy(checker, client: Mock, node: Node) -> None:
    client.get.return_value = Mock(status_code=200)
    result = await checker.check_component(node)
    assert result.status == "healthy"


@pytest.mark.asyncio
async def test_http_500_returns_unhealthy(checker, client: Mock, node: Node) -> None:
    client.get.return_value = Mock(status_code=500)
    result = await checker.check_component(node)
    assert result.status == "unhealthy"


@pytest.mark.asyncio
async def test_timeout_returns_unhealthy(checker, client: Mock, node: Node) -> None:
    client.get.side_effect = httpx.TimeoutException("timeout")
    result = await checker.check_component(node)
    assert result.status == "unhealthy"


@pytest.mark.asyncio
async def test_multiple_components_are_checked_concurrently(checker, monkeypatch) -> None:
    started = []
    gate = AsyncMock()
    gate.wait = AsyncMock()

    async def fake_check(component: Node) -> ComponentHealth:
        started.append(component.id)
        return ComponentHealth(id=component.id, name=component.name, endpoint=component.endpoint, status="healthy", response_time_ms=1)

    components = [Node(id="a", name="A", endpoint="http://a.local"), Node(id="b", name="B", endpoint="http://b.local")]
    monkeypatch.setattr(checker, "check_component", AsyncMock(side_effect=fake_check))

    results = await checker.check(components)

    assert started == ["a", "b"]
    assert [result.id for result in results] == ["a", "b"]
