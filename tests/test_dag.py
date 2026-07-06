import pytest

from app.dag import DependencyGraph
from app.models import Edge, HealthCheckRequest, Node


def test_build_valid_dag() -> None:
    request = HealthCheckRequest(nodes=[Node(id="a", name="A", endpoint="http://a.local"), Node(id="b", name="B", endpoint="http://b.local")], edges=[Edge(from_node="a", to_node="b")])
    graph = DependencyGraph(request)
    assert graph.build().number_of_nodes() == 2
    assert graph.root_nodes() == ["a"]


def test_missing_node() -> None:
    request = HealthCheckRequest(nodes=[Node(id="a", name="A", endpoint="http://a.local")], edges=[Edge(from_node="a", to_node="b")])
    with pytest.raises(ValueError, match="unknown node"):
        DependencyGraph(request).build()


def test_cycle_detection() -> None:
    request = HealthCheckRequest(nodes=[Node(id="a", name="A", endpoint="http://a.local"), Node(id="b", name="B", endpoint="http://b.local")], edges=[Edge(from_node="a", to_node="b"), Edge(from_node="b", to_node="a")])
    with pytest.raises(ValueError, match="DAG|cycle"):
        DependencyGraph(request).build()


def test_root_nodes() -> None:
    request = HealthCheckRequest(nodes=[Node(id="a", name="A", endpoint="http://a.local"), Node(id="b", name="B", endpoint="http://b.local"), Node(id="c", name="C", endpoint="http://c.local"), Node(id="d", name="D", endpoint="http://d.local")], edges=[Edge(from_node="a", to_node="c"), Edge(from_node="b", to_node="d")])
    graph = DependencyGraph(request)
    graph.build()
    assert graph.root_nodes() == ["a", "b"]


def test_bfs_traversal() -> None:
    request = HealthCheckRequest(nodes=[Node(id="a", name="A", endpoint="http://a.local"), Node(id="b", name="B", endpoint="http://b.local"), Node(id="c", name="C", endpoint="http://c.local")], edges=[Edge(from_node="a", to_node="b"), Edge(from_node="b", to_node="c")])
    graph = DependencyGraph(request)
    graph.build()
    assert graph.bfs("a") == ["a", "b", "c"]
