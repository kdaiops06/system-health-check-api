# Design Decisions

This document records the key engineering choices made for the System Health Check API.

## FastAPI

**Decision:** Use FastAPI for the REST API.

**Rationale:** It provides async-native request handling, strong Pydantic integration, and a clean developer experience for a small production-oriented service.

**Tradeoff:** FastAPI is more opinionated than lighter frameworks, but the reduced boilerplate and built-in validation are worth it.

## Pydantic

**Decision:** Use Pydantic for request and response models.

**Rationale:** It enforces schema validation, simplifies serialization, and keeps API contracts explicit.

**Tradeoff:** Validation adds a small runtime cost, which is acceptable for this workload.

## NetworkX

**Decision:** Use NetworkX to represent and validate dependency graphs.

**Rationale:** It provides reliable DAG handling, cycle detection, and graph traversal without custom graph-engine code.

**Tradeoff:** It adds an external dependency, but it improves correctness and reduces implementation risk.

## Breadth First Search

**Decision:** Traverse dependency graphs with Breadth First Search.

**Rationale:** BFS provides a predictable execution order for dependency trees and is easy to reason about during debugging.

**Tradeoff:** DFS could also work, but BFS is more intuitive for component-level evaluation.

## asyncio

**Decision:** Execute health checks concurrently with `asyncio`.

**Rationale:** Health checks are network-bound, so concurrency reduces total request time and improves throughput.

**Tradeoff:** Async orchestration is slightly more complex than sequential code, but the performance benefit is significant.

## httpx.AsyncClient

**Decision:** Use `httpx.AsyncClient` for outbound component checks.

**Rationale:** It is a modern async HTTP client with good timeout handling and connection reuse.

**Tradeoff:** It requires careful timeout and exception handling, but it fits the asynchronous API model well.

## Stateless Request Processing

**Decision:** Keep aggregation and orchestration request-scoped and in memory.

**Rationale:** The assignment does not require persistence, and stateless processing fits Cloud Run well.

**Tradeoff:** The service does not retain historical health data, which would require external storage in a production expansion.

## Prometheus Metrics

**Decision:** Expose application metrics with Prometheus.

**Rationale:** Metrics provide visibility into request volume, latency, and component health, and integrate well with Google Cloud observability.

**Tradeoff:** Only core metrics are implemented to keep the solution focused.

## Cloud Run

**Decision:** Deploy the application to Google Cloud Run.

**Rationale:** Cloud Run provides managed scaling, low operational overhead, and a strong fit for stateless HTTP services.

**Tradeoff:** It offers less infrastructure control than Kubernetes, but that is a benefit here because the assignment favors simplicity.

## Docker

**Decision:** Package the application as a container image.

**Rationale:** Containers provide reproducible builds and make the service portable across local development and Cloud Run.

**Tradeoff:** Containerization adds a small build step, but it standardizes runtime behavior and deployment.

## GitHub Actions

**Decision:** Use GitHub Actions for CI.

**Rationale:** It provides a straightforward, repository-native pipeline for tests, linting, and image builds.

**Tradeoff:** It is less customizable than a full internal CI platform, but it is sufficient for a take-home assignment and easy to review.
