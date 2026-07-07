# Design Decisions

This document captures the key engineering decisions, assumptions, tradeoffs, and scope choices made while implementing the **System Health Check API**. The assignment was intentionally open-ended, so several implementation decisions were made to balance correctness, maintainability, and delivery within the expected time.

---

# Engineering Assumptions

The following assumptions were made while interpreting the problem statement.

## Graph Assumptions

- The input represents a valid Directed Acyclic Graph (DAG).
- Each component has a unique identifier.
- All dependency edges reference existing nodes.
- Cyclic graphs are considered invalid and are rejected during validation.

## Health Check Assumptions

- Every component exposes an HTTP endpoint that can be queried.
- HTTP 200 indicates a healthy component.
- Any non-200 response, timeout, or network failure is considered unhealthy.
- Health evaluation is request-scoped and does not rely on historical state.

## Platform Assumptions

- The service is stateless.
- Cloud Run is the preferred deployment target.
- Google-managed services are preferred over self-managed infrastructure.
- Prometheus is used for metrics collection and Grafana for visualization.

---

# Scope Decisions

The assignment was intentionally scoped to deliver a production-oriented MVP.

The following capabilities were intentionally excluded:

- Authentication and authorization
- Persistent storage
- Historical health reporting
- Retry policies
- Circuit breakers
- Distributed tracing
- Background scheduling
- Service discovery
- Multi-region deployment
- AI-assisted remediation

These capabilities are documented as future enhancements rather than implemented to keep the solution focused on the assignment objectives.

---

# Design Decisions

## FastAPI

**Decision**

Use FastAPI for the REST API.

**Reason**

FastAPI provides asynchronous request handling, automatic OpenAPI documentation, and strong request validation with minimal boilerplate.

**Tradeoff**

FastAPI is more opinionated than lightweight frameworks but significantly improves maintainability and developer productivity.

---

## Pydantic

**Decision**

Use Pydantic models for request and response validation.

**Reason**

Explicit schemas improve API correctness, simplify serialization, and automatically generate OpenAPI documentation.

**Tradeoff**

Validation introduces a small runtime overhead that is acceptable for this workload.

---

## NetworkX

**Decision**

Use NetworkX to model and validate the dependency graph.

**Reason**

It provides mature graph algorithms, DAG validation, cycle detection, and traversal utilities without requiring custom graph implementations.

**Tradeoff**

Adds a dependency but significantly reduces implementation complexity and risk.

---

## Breadth-First Search (BFS)

**Decision**

Traverse dependencies using Breadth-First Search.

**Reason**

BFS evaluates dependencies in a deterministic level-by-level order, making execution flow easier to understand and extend.

**Tradeoff**

Depth-First Search would also satisfy the assignment, but BFS provides clearer execution ordering for dependency graphs.

---

## asyncio

**Decision**

Execute health checks concurrently using asyncio.

**Reason**

Component health checks are network-bound operations. Asynchronous execution reduces total request latency without increasing infrastructure complexity.

**Tradeoff**

Async programming introduces additional complexity compared to sequential execution.

---

## httpx

**Decision**

Use httpx.AsyncClient for outbound HTTP requests.

**Reason**

Provides native async support, connection pooling, configurable timeouts, and a clean API.

**Tradeoff**

Requires explicit timeout configuration and exception handling.

---

## Cloud Run

**Decision**

Deploy the application on Google Cloud Run.

**Reason**

Cloud Run is a fully managed serverless platform that aligns well with the stateless nature of the application while minimizing operational overhead.

**Tradeoff**

Provides less infrastructure control than Kubernetes but significantly reduces operational complexity for this use case.

---

## Terraform

**Decision**

Provision infrastructure using Terraform.

**Reason**

Infrastructure as Code provides repeatable, version-controlled deployments and aligns with Platform Engineering best practices.

**Tradeoff**

Adds Infrastructure as Code maintenance but greatly improves reproducibility and reviewability.

---

## Docker

**Decision**

Package the application as a Docker container.

**Reason**

Containers provide a consistent runtime across development, testing, and production while simplifying Cloud Run deployments.

**Tradeoff**

Introduces an image build step but standardizes execution environments.

---

## Prometheus

**Decision**

Expose operational metrics using Prometheus.

**Reason**

Prometheus is the industry standard for cloud-native metrics and integrates naturally with Grafana and Google Managed Prometheus.

**Tradeoff**

The implementation focuses on core operational metrics and intentionally excludes advanced telemetry pipelines.

---

## Grafana

**Decision**

Provide a Grafana dashboard for operational visualization.

**Reason**

Dashboards improve observability by visualizing request throughput, latency, and component health during local validation.

**Tradeoff**

Requires additional setup but significantly improves the reviewer experience and operational visibility.

---

## GitHub Actions

**Decision**

Use GitHub Actions for Continuous Integration.

**Reason**

GitHub Actions is repository-native and provides sufficient capabilities for linting, testing, Docker builds, and Terraform validation.

**Tradeoff**

Less customizable than enterprise CI platforms but appropriate for the assignment scope.

---

# Key Tradeoffs

Several tradeoffs were made intentionally.

| Decision | Benefit | Tradeoff |
|-----------|---------|----------|
| Cloud Run | Minimal operational overhead | Less infrastructure control than Kubernetes |
| BFS | Simple and deterministic traversal | DFS could also satisfy the requirement |
| In-memory aggregation | Simpler implementation | No historical persistence |
| Async HTTP | Better performance for I/O workloads | Increased implementation complexity |
| Prometheus | Standard cloud-native metrics | No distributed tracing |

---

# Production Considerations

For a production deployment, the following enhancements would be considered:

- Retry policies with exponential backoff
- Circuit breakers
- OpenTelemetry
- Google Cloud Trace
- Google Cloud Monitoring dashboards
- Alerting policies
- SLOs, SLIs, and Error Budgets
- AI-assisted incident summarization
- Vertex AI-based root cause analysis
- Multi-region deployment
- Service-to-service authentication
- Historical health persistence