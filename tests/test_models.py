from pydantic import ValidationError

from app.models import Edge, HealthCheckRequest, Node


def test_node_model_creation():
    node = Node(
        id="api",
        name="API",
        endpoint="https://example.com/health",
    )
    assert node.id == "api"


def test_invalid_endpoint():
    try:
        Node(
            id="api",
            name="API",
            endpoint="not-a-url",
        )
        assert False
    except ValidationError:
        assert True


def test_health_request_creation():
    request = HealthCheckRequest(
        nodes=[
            Node(
                id="api",
                name="API",
                endpoint="https://example.com/health",
            )
        ],
        edges=[
            Edge(
                from_node="api",
                to_node="db",
            )
        ],
    )

    assert len(request.nodes) == 1
    assert len(request.edges) == 1