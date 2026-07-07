# System Health Check API

A production-oriented FastAPI service for evaluating the health of dependent components represented as a Directed Acyclic Graph. The repository is intentionally scoped as a polished take-home submission for a Senior Google Cloud Platform Engineering / AI SRE interview.

## Executive Summary

The application validates a dependency graph, traverses it with Breadth First Search, runs concurrent HTTP health checks, aggregates component health, and exposes Prometheus metrics for review in Grafana. It is designed for Cloud Run and delivered with Docker, Terraform, and GitHub Actions.

## Problem Statement

Accept a graph of dependent services, verify that it is valid, evaluate the health of each reachable component, and return a concise operational view of system health with low operational overhead.

## Solution Overview

The API accepts a `HealthCheckRequest`, builds and validates the DAG, discovers root nodes, traverses the dependency tree with BFS, resolves nodes to `Node` objects, performs asynchronous health checks, and returns a `HealthCheckResponse` with aggregated health data.

## Architecture Overview

- FastAPI handles request routing and validation.
- NetworkX models and traverses the DAG.
- `asyncio` and `httpx.AsyncClient` execute component checks concurrently.
- `HealthAggregator` combines the results into the final response.
- Prometheus exposes request, latency, and health metrics for operational visibility.

## Technology Stack

- FastAPI
- Pydantic
- NetworkX
- asyncio
- httpx
- Prometheus
- Docker
- Terraform
- Cloud Run
- Artifact Registry
- GitHub Actions
- Structured Logging

## Repository Structure

- `app/` - API, graph engine, async health checker, aggregation, logging, and metrics
- `tests/` - pytest unit, integration, and endpoint coverage
- `terraform/` - Google Cloud provider, Cloud Run, and Artifact Registry resources
- `monitoring/` - local Prometheus and Grafana stack
- `grafana/` - dashboard JSON for manual review or provisioning reference
- `docs/` - architecture, design decisions, and platform considerations
- `scripts/` - bootstrap helper
- `examples/` - sample request payloads

## Request Processing Flow

1. Receive and validate the `HealthCheckRequest`.
2. Build the dependency graph.
3. Validate the graph and detect cycles.
4. Identify root nodes and traverse with BFS.
5. Execute asynchronous health checks in dependency order.
6. Aggregate the component results.
7. Return a `HealthCheckResponse`.

## Deployment Architecture

- GitHub hosts the source code.
- GitHub Actions runs linting, tests, Terraform validation, and Docker builds.
- Artifact Registry stores the container image.
- Cloud Run runs the service as a managed stateless HTTP workload.
- Cloud Logging and Cloud Monitoring provide the Google Cloud operational path.

## Infrastructure

Terraform provisions only the resources required for the assignment:

- Google provider configuration
- Artifact Registry Docker repository
- Cloud Run service
- Public invoker access for unauthenticated requests

## Observability

- Structured logging with a stable `component` field
- Health endpoints: `/health`, `/live`, `/ready`
- Prometheus metrics at `/metrics`
- Request rate, latency, component health, and error ratio visibility

## Monitoring

The repository includes a local monitoring stack under `monitoring/`.

- Prometheus scrapes `http://host.docker.internal:8080/metrics`
- Grafana is auto-provisioned with the dashboard JSON from this repository
- The stack is intended for local validation of the exposed metrics

## Testing

The test suite uses pytest and covers DAG validation, BFS traversal, async health checks, aggregation, metrics exposure, and FastAPI endpoint behavior.

## Docker

Build the application image with:

```bash
make docker
```

Run the image locally with:

```bash
docker run --rm -p 8080:8080 system-health-check-api
```

## Terraform Deployment

Set the required variables and run Terraform from the `terraform/` directory:

```bash
export TF_VAR_project_id=<your-project-id>
export TF_VAR_region=us-central1
cd terraform
terraform init
terraform validate
terraform plan
terraform apply
```

## GitHub Actions Pipeline

The CI pipeline checks out the repository, sets up Python 3.12, installs dependencies, runs Ruff, runs pytest, builds the Docker image, and validates Terraform when the Terraform directory is present.

## Assumptions

- The dependency graph is a DAG.
- Execution is request-scoped and stateless.
- Cloud Run is the deployment target.
- Google-managed services are preferred over self-managed infrastructure.
- Persistent history and retry semantics are intentionally out of scope.

## Design Decisions

Key engineering decisions are documented in [`docs/design-decisions.md`](docs/design-decisions.md).

## Tradeoffs

- Cloud Run reduces operational overhead but provides less infrastructure control than Kubernetes.
- In-memory aggregation keeps the implementation simple but does not retain historical health trends.
- BFS improves execution clarity, while DFS would also satisfy the graph traversal requirement.

## AI Usage

GitHub Copilot:
- Boilerplate
- Refactoring
- Tests

ChatGPT:
- Architecture review
- Platform engineering review
- Terraform review
- Documentation
- Observability review
- Code review guidance

All AI generated code and recommendations were manually reviewed, tested, modified where appropriate and fully understood before being committed.

## Future Enhancements

- Retry policies and circuit breakers
- Distributed tracing
- OpenTelemetry
- Cloud Trace
- Cloud Monitoring dashboards
- SLOs, SLIs, and error budgets
- Vertex AI root cause analysis
- AI incident summaries
- AI runbooks
- Multi-region deployment

## Local Development

```bash
make bootstrap
source .venv/bin/activate
make run
```

Helpful commands:

```bash
make test
make docker
```

## Running the Monitoring Stack

```bash
cd monitoring
docker compose up -d
```

Open Grafana at http://localhost:3000 with `admin` / `admin`, and open Prometheus at http://localhost:9090.

Generate traffic with:

```bash
for i in {1..100}; do
curl -s http://localhost:8080/health-check \
  -H "Content-Type: application/json" \
  -d @examples/sample_request.json >/dev/null
done
```

## Cleanup

Stop the local monitoring stack and remove volumes with:

```bash
cd monitoring
docker compose down -v
```

If needed, destroy the Cloud Run deployment with Terraform:

```bash
cd terraform
terraform destroy
```
