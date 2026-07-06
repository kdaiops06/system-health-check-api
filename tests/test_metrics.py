from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_metrics_endpoint_returns_metrics() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text
    assert "health_checks_total" in response.text
