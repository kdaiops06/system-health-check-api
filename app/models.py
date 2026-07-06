from pydantic import BaseModel, HttpUrl


class Node(BaseModel):
    """Graph node in a health check request."""

    id: str
    name: str
    endpoint: HttpUrl


class Edge(BaseModel):
    """Directed dependency between nodes."""

    from_node: str
    to_node: str


class HealthCheckRequest(BaseModel):
    """Input payload for a health check run."""

    nodes: list[Node]
    edges: list[Edge]


class ComponentHealth(BaseModel):
    """Health details for a single component."""

    id: str
    name: str
    endpoint: HttpUrl
    status: str
    response_time_ms: int


class HealthCheckResponse(BaseModel):
    """Aggregated health check output."""

    overall_status: str
    components: list[ComponentHealth]
    summary: dict[str, int]