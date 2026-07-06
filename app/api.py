from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.aggregator import HealthAggregator
from app.dag import DependencyGraph
from app.health_checker import HealthChecker
from app.logger import get_logger
from app.models import HealthCheckRequest, HealthCheckResponse

router = APIRouter()
logger = get_logger("api")


@router.post("/health-check", response_model=HealthCheckResponse)
async def health_check(request: HealthCheckRequest) -> HealthCheckResponse:
    """Run the full health-check workflow for a request."""
    logger.info("health check started")
    try:
        graph = DependencyGraph(request)
        graph.build()
        ordered_ids, seen = [], set()
        for root in graph.root_nodes():
            for node_id in graph.bfs(root):
                if node_id not in seen:
                    seen.add(node_id)
                    ordered_ids.append(node_id)
        node_map = {node.id: node for node in request.nodes}
        results = await HealthChecker().check([node_map[node_id] for node_id in ordered_ids])
        response = HealthAggregator().aggregate(results)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        logger.info("health check completed")
    return response