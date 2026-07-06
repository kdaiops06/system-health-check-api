from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_valid_dag_returns_http_200() -> None:
    payload = {"nodes": [{"id": "a", "name": "A", "endpoint": "http://a.local"}], "edges": []}
    with patch("app.api.HealthChecker") as mock_checker, patch("app.api.HealthAggregator") as mock_aggregator:
        mock_checker.return_value.check = AsyncMock(return_value=[])
        mock_aggregator.return_value.aggregate.return_value = {"overall_status": "healthy", "components": [], "summary": {"total_components": 0, "healthy_components": 0, "unhealthy_components": 0}}
        response = client.post("/health-check", json=payload)
    assert response.status_code == 200


def test_cyclic_dag_returns_http_400() -> None:
    payload = {"nodes": [{"id": "a", "name": "A", "endpoint": "http://a.local"}, {"id": "b", "name": "B", "endpoint": "http://b.local"}], "edges": [{"from_node": "a", "to_node": "b"}, {"from_node": "b", "to_node": "a"}]}
    assert client.post("/health-check", json=payload).status_code == 400


def test_invalid_request_returns_http_422() -> None:
    assert client.post("/health-check", json={"nodes": "invalid", "edges": []}).status_code == 422
