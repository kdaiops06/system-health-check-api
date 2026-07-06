from __future__ import annotations

from pydantic import BaseModel
from tabulate import tabulate

from app.logger import get_logger
from app.metrics import healthy_components, unhealthy_components
from app.models import ComponentHealth, HealthCheckResponse

logger = get_logger("aggregator")


class Summary(BaseModel):
    """Aggregate component health counts."""

    total_components: int
    healthy_components: int
    unhealthy_components: int


class HealthAggregator:
    """Aggregate component health results into summary output."""

    def summarize(self, results: list[ComponentHealth]) -> Summary:
        healthy = sum(result.status == "healthy" for result in results)
        return Summary(total_components=len(results), healthy_components=healthy, unhealthy_components=len(results) - healthy)

    def aggregate(self, results: list[ComponentHealth]) -> HealthCheckResponse:
        summary = self.summarize(results)
        healthy_components.set(summary.healthy_components)
        unhealthy_components.set(summary.unhealthy_components)
        overall_status = "healthy" if summary.unhealthy_components == 0 else "unhealthy"
        logger.info("summary total=%s healthy=%s unhealthy=%s", summary.total_components, summary.healthy_components, summary.unhealthy_components)
        return HealthCheckResponse(overall_status=overall_status, components=results, summary=summary.model_dump())

    def table(self, results: list[ComponentHealth]) -> str:
        rows = [[r.id, r.name, r.status, r.response_time_ms] for r in results]
        return tabulate(rows, headers=["ID", "Name", "Status", "Response Time (ms)"], tablefmt="github")