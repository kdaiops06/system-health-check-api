# Design Decisions

This document captures the key architectural and engineering decisions made during the implementation of the System Health Check API.

The goal was to deliver a production-oriented MVP within the assignment time constraints while demonstrating sound software engineering, platform engineering, and AI SRE practices.

---

# DD-001: FastAPI as the REST Framework

## Decision

Use FastAPI to implement the REST API.

## Rationale

- Native asynchronous support
- Excellent Pydantic integration
- Automatic OpenAPI documentation
- High performance for I/O-bound workloads
- Excellent developer experience

## Tradeoff

FastAPI is slightly more opinionated than Flask but significantly reduces boilerplate and improves maintainability.

---

# DD-002: Google Cloud Run for Deployment

## Decision

Target Google Cloud Run as the deployment platform.

## Rationale

- Fully managed serverless runtime
- Automatic scaling
- Native integration with Cloud Logging and Cloud Monitoring
- Lower operational overhead than Kubernetes
- Well suited for stateless REST APIs

## Tradeoff

Provides less infrastructure control than GKE but greatly simplifies operations for this assignment.

---

# DD-003: Pydantic for API Contracts

## Decision

Use Pydantic models for request and response validation.

## Rationale

- Strong type validation
- Automatic serialization
- Automatic OpenAPI schema generation
- Improved developer experience

## Tradeoff

Small runtime validation overhead, acceptable for API workloads.

---

# DD-004: Dependency Graph Validation

## Decision

Validate the dependency graph before executing any health checks.

## Rationale

- Fail fast
- Prevent invalid execution plans
- Detect configuration errors early
- Improve API reliability

## Tradeoff

Adds a small validation step before execution.

---

# DD-005: NetworkX for Graph Processing

## Decision

Use NetworkX to represent and traverse the dependency graph.

## Rationale

- Mature graph library
- Reliable DAG validation
- Built-in traversal algorithms
- Reduces custom implementation complexity

## Tradeoff

Introduces a lightweight dependency but significantly improves correctness and maintainability.

---

# DD-006: Breadth First Search (BFS)

## Decision

Use Breadth First Search to traverse the dependency graph.

## Rationale

- Deterministic traversal order
- Easy to understand
- Suitable for dependency-level processing
- Simplifies operational troubleshooting

## Tradeoff

Depth First Search would also satisfy the assignment, but BFS provides a more intuitive execution order for dependency graphs.

---

# DD-007: Separation of Responsibilities

## Decision

Separate graph construction, validation, and traversal into independent methods.

## Rationale

- Easier unit testing
- Better maintainability
- Cleaner architecture
- Reusable graph engine independent of API transport

## Tradeoff

Slightly more code but significantly clearer responsibilities.

---

# DD-008: Developer Experience First

## Decision

Invest in developer tooling early.

## Rationale

The project includes:

- Bootstrap script
- Makefile
- Docker
- GitHub Actions
- Terraform scaffold

This allows contributors to bootstrap the project quickly while ensuring consistent local development and CI execution.

## Tradeoff

A small upfront investment in tooling significantly improves maintainability and onboarding.

---

# DD-009: Platform Engineering Approach

## Decision

Prefer managed Google Cloud services over self-managed infrastructure.

## Rationale

The objective is to demonstrate platform engineering principles rather than infrastructure management.

Examples include:

- Cloud Run
- Artifact Registry
- GitHub Actions
- Cloud Logging
- Cloud Monitoring

## Tradeoff

Reduced infrastructure flexibility in exchange for lower operational complexity.

---

# DD-010: Observability by Design

## Decision

Build observability into the application from the beginning.

## Rationale

The application includes:

- Structured logging
- Health endpoints
- Prometheus metrics (planned)
- Cloud Logging compatibility

Future enhancements include:

- OpenTelemetry
- Cloud Trace
- Managed Prometheus
- SLO dashboards

## Tradeoff

Only foundational observability is implemented to remain within the assignment time budget.

# DD-011: Asynchronous Health Checks

## Decision

Execute component health checks concurrently using `asyncio` and `httpx.AsyncClient`.

## Rationale

Health checks are network-bound, I/O-intensive operations. Running them concurrently significantly reduces total evaluation time compared to sequential execution while improving throughput and resource utilization.

Using `httpx.AsyncClient` provides efficient connection management and aligns with FastAPI's asynchronous execution model.

## Tradeoff

Concurrent execution introduces additional complexity around timeout handling and exception management. However, the performance benefits outweigh the implementation complexity for dependency-based health evaluation services.

Future production enhancements may include configurable retry policies, exponential backoff, adaptive concurrency, and circuit breaker patterns.

# DD-012: Request-Scoped Aggregation

### Decision

Aggregate health results entirely in memory for each request.

### Rationale

The assignment does not require persistence. Request-scoped aggregation keeps the implementation stateless, simplifies deployment on Cloud Run, and avoids unnecessary operational complexity.

### Tradeoff

Historical health trends are not retained. A production implementation could persist results to BigQuery, Cloud SQL, or Firestore for analytics and reporting.