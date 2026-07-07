# Design Decisions

This document summarizes the core engineering choices made for the System Health Check API.

## FastAPI

**Decision:** Use FastAPI for the REST API.

**Reason:** It provides async-native request handling, strong validation support, and a concise programming model for a small production MVP.

**Tradeoff:** FastAPI is more opinionated than a minimal framework, but it reduces boilerplate and improves maintainability.

## Pydantic

**Decision:** Use Pydantic for request and response models.

**Reason:** It gives explicit contracts, schema validation, and predictable serialization for API payloads.

**Tradeoff:** Validation adds a small runtime cost, which is acceptable for this service.

## NetworkX

**Decision:** Use NetworkX for DAG modeling and validation.

**Reason:** It provides reliable graph primitives, cycle detection, and traversal without custom graph-engine code.

**Tradeoff:** It adds an external dependency, but it reduces implementation risk.

## Breadth First Search

**Decision:** Traverse the graph with Breadth First Search.

**Reason:** BFS provides a clear and deterministic order for dependency evaluation.

**Tradeoff:** DFS would also work, but BFS is easier to reason about when validating dependency trees.

## asyncio

**Decision:** Run health checks concurrently with asyncio.

**Reason:** Component checks are network-bound, so concurrency improves throughput and reduces total request time.

**Tradeoff:** Async orchestration is slightly more complex than sequential code.

## httpx

**Decision:** Use httpx.AsyncClient for outbound checks.

**Reason:** It is a modern async HTTP client with connection pooling and straightforward timeout handling.

**Tradeoff:** It requires explicit timeout and exception management.

## Cloud Run

**Decision:** Deploy the application on Cloud Run.

**Reason:** It is a managed, stateless HTTP runtime that fits the assignment’s operational scope and keeps the platform surface small.

**Tradeoff:** It offers less infrastructure control than Kubernetes, which is acceptable for this workload.

## Terraform

**Decision:** Manage infrastructure with Terraform.

**Reason:** It makes the deployment reproducible, reviewable, and easy to understand in a platform engineering review.

**Tradeoff:** It introduces a small amount of IaC overhead, which is worth the clarity it provides.

## Docker

**Decision:** Package the service in Docker.

**Reason:** Containers make local execution and Cloud Run deployment consistent.

**Tradeoff:** It adds a build step, but it standardizes the runtime environment.

## Prometheus

**Decision:** Expose metrics with Prometheus.

**Reason:** It is a simple and widely used metrics format for request volume, latency, and component health.

**Tradeoff:** The implementation intentionally stays minimal and does not include advanced telemetry pipelines.

## Grafana

**Decision:** Use Grafana for dashboard visualization.

**Reason:** It provides a clear operational view of the application metrics and supports reviewer-friendly observability.

**Tradeoff:** A dashboard adds a small amount of setup, but it improves the submission significantly.

## GitHub Actions

**Decision:** Use GitHub Actions for CI.

**Reason:** It is easy to review, repository-native, and sufficient for linting, tests, Docker builds, and Terraform validation.

**Tradeoff:** It is not as customizable as a larger internal CI platform, but it is appropriate for this project.
