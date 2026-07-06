from __future__ import annotations

import networkx as nx

from app.logger import get_logger
from app.models import HealthCheckRequest

logger = get_logger("dag")


class DependencyGraph:
    """Build and inspect a health-check dependency graph."""

    def __init__(self, request: HealthCheckRequest) -> None:
        self.request = request
        self.graph = nx.DiGraph()
        self._built = False

    def build(self) -> nx.DiGraph:
        """Build a directed graph from request nodes and edges."""
        logger.info("building graph with %s nodes and %s edges", len(self.request.nodes), len(self.request.edges))
        self.graph.clear()
        self.graph.add_nodes_from((node.id, {"name": node.name, "endpoint": str(node.endpoint)}) for node in self.request.nodes)
        self.graph.add_edges_from((edge.from_node, edge.to_node) for edge in self.request.edges)
        self._built = True
        self.validate()
        return self.graph

    def validate(self) -> None:
        """Validate node references and ensure the graph is acyclic."""
        logger.info("validating graph with %s nodes and %s edges", self.graph.number_of_nodes(), self.graph.number_of_edges())
        node_ids = {node.id for node in self.request.nodes}
        missing = [name for edge in self.request.edges for name in (edge.from_node, edge.to_node) if name not in node_ids]
        if missing:
            raise ValueError(f"Edge references unknown node(s): {', '.join(sorted(set(missing)))}")
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Dependency graph must be acyclic (DAG)")

    def root_nodes(self) -> list[str]:
        """Return nodes with no incoming edges."""
        logger.info("collecting root nodes from %s nodes and %s edges", self.graph.number_of_nodes(), self.graph.number_of_edges())
        return [node for node, degree in self.graph.in_degree() if degree == 0]

    def bfs(self, start_node: str) -> list[str]:
        """Traverse the graph from a start node using breadth-first search."""
        if not self._built:
            raise ValueError("graph has not been built")
        logger.info("running bfs traversal from %s over %s nodes and %s edges", start_node, self.graph.number_of_nodes(), self.graph.number_of_edges())
        if start_node not in self.graph:
            raise ValueError("start node does not exist")
        return list(nx.bfs_tree(self.graph, start_node).nodes)


DAGBuilder = DependencyGraph