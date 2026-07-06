from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.models import ComponentHealth

client = TestClient(app)


def test_metrics_endpoint_returns_metrics() -> None:
    payload = {"nodes": [{"id": "a", "name": "A", "endpoint": "http://localhost:8080/health"}], "edges": []}
    with patch("app.api.HealthChecker") as mock_checker:
        mock_checker.return_value.check = AsyncMock(return_value=[ComponentHealth(id="a", name="A", endpoint="http://localhost:8080/health", status="healthy", response_time_ms=1)])
        assert client.post("/health-check", json=payload).status_code == 200

    response = client.get("/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text
    assert "health_checks_total" in response.text
    assert "healthy_components" in response.text
    assert "unhealthy_components" in response.text
