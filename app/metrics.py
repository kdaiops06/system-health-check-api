"""Reusable Prometheus metrics for API and health-check observability."""

from prometheus_client import Counter, Gauge, Histogram

api_requests_total = Counter("api_requests", "Total API requests")
health_checks_total = Counter("health_checks", "Total health checks")
api_request_duration_seconds = Histogram("api_request_duration_seconds", "API request duration in seconds")
health_check_duration_seconds = Histogram("health_check_duration_seconds", "Health check duration in seconds")
healthy_components = Gauge("healthy_components", "Number of healthy components")
unhealthy_components = Gauge("unhealthy_components", "Number of unhealthy components")
