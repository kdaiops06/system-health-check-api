# System Health Check API
## End-to-End Demo Guide

**Author:** Dinesh Kumar

**Role Target:** Google Cloud Platform Engineering / AI SRE

**Estimated Demo Time:** 12–15 minutes

---

# Demo Objectives

Demonstrate an end-to-end production-oriented Platform Engineering solution including:

- Python API
- DAG Processing
- Breadth-First Search
- Async Health Checks
- Observability
- Docker
- Terraform
- Cloud Run
- Prometheus
- Grafana
- CI/CD
- Documentation

---

# Demo 1 — Repository Overview (1 minute)

## Command

```bash
tree -L 2
```

## Explain

Repository organization

```
app/
tests/
terraform/
monitoring/
grafana/
docs/
examples/
```

Highlight:

- Clean separation of concerns
- Infrastructure as Code
- Monitoring
- Documentation
- Tests

---

# Demo 2 — Code Quality (30 seconds)

## Commands

```bash
ruff check .

pytest -v
```

Explain

- Static analysis passes
- Unit tests validate the complete application

Coverage includes:

- Models
- DAG
- API
- Metrics
- Aggregator
- Health Checker

---

# Demo 3 — Run the Application (30 seconds)

```bash
make run
```

Open

```
http://localhost:8080/docs
```

Explain

FastAPI automatically generates OpenAPI documentation.

---

# Demo 4 — Health Endpoints (30 seconds)

```bash
curl localhost:8080/
```

```bash
curl localhost:8080/health
```

```bash
curl localhost:8080/live
```

```bash
curl localhost:8080/ready
```

Explain

These endpoints support:

- Cloud Run
- Kubernetes
- Load Balancers

---

# Demo 5 — Core Assignment (2 minutes)

```bash
curl -X POST \
http://localhost:8080/health-check \
-H "Content-Type: application/json" \
-d @examples/sample_request.json | jq
```

Explain request flow

```
Client

↓

FastAPI

↓

Pydantic Validation

↓

Dependency Graph

↓

Validate DAG

↓

Breadth First Search

↓

Async Health Checks

↓

Health Aggregator

↓

JSON Response
```

Mention

- DAG validation
- BFS traversal
- Async execution
- Concurrent health checks

---

# Demo 6 — Logging (30 seconds)

Show logs

Example

```
building graph

validating graph

running bfs traversal

checking service-a

checking service-b

aggregating results

request completed
```

Explain

- Structured logging
- Cloud Logging compatible

---

# Demo 7 — Prometheus Metrics (1 minute)

```bash
curl -Ls http://localhost:8080/metrics | grep api
```

```bash
curl -Ls http://localhost:8080/metrics | grep health
```

Highlight

```
api_requests_total

health_checks_total

healthy_components

unhealthy_components

api_request_duration_seconds

health_check_duration_seconds
```

Explain

These metrics are scraped by Prometheus.

---

# Demo 8 — Monitoring Stack (2 minutes)

Start monitoring

```bash
cd monitoring

docker compose up -d
```

Open

```
http://localhost:9090
```

Prometheus

Open

```
http://localhost:3000
```

Grafana

Login

```
admin

admin
```

Generate traffic

```bash
for i in {1..20}; do
curl -s http://localhost:8080/health-check \
-H "Content-Type: application/json" \
-d @../examples/sample_request.json >/dev/null
done
```

Refresh dashboard.

Show

- API Request Rate
- Average Latency
- P95 Latency
- Healthy Components
- Error Ratio

---

# Demo 9 — Docker (1 minute)

```bash
docker build -t system-health-check-api .
```

```bash
docker run -p 8080:8080 system-health-check-api
```

Explain

Containerized application

Production-ready image

---

# Demo 10 — Terraform (2 minutes)

```bash
cd terraform

terraform validate
```

```bash
terraform plan
```

Explain

Terraform provisions

- Artifact Registry
- Cloud Run
- IAM

Infrastructure is declarative.

---

# Demo 11 — Cloud Run (2 minutes)

Get URL

```bash
terraform output
```

Health

```bash
curl https://<cloud-run-url>/health
```

Run API

```bash
curl -X POST \
https://<cloud-run-url>/health-check \
-H "Content-Type: application/json" \
-d @examples/sample_request.json
```

Explain

Docker

↓

Artifact Registry

↓

Cloud Run

↓

Production API

---

# Demo 12 — Documentation (1 minute)

Walk through

```
README.md

architecture.md

design-decisions.md

platform-considerations.md
```

Explain

- Assumptions
- Tradeoffs
- AI Usage
- Future Enhancements

---

# Demo 13 — Architecture Diagram (1 minute)

Open

```
docs/architecture.md
```

Explain

```
GitHub

↓

GitHub Actions

↓

Docker Build

↓

Artifact Registry

↓

Cloud Run

↓

Prometheus

↓

Grafana
```

Then explain application architecture

```
Client

↓

FastAPI

↓

Dependency Graph

↓

BFS

↓

Async Health Checker

↓

Aggregator

↓

JSON
```

---

# Demo 14 — Infrastructure Cleanup (30 seconds)

```bash
terraform destroy
```

Explain

Infrastructure lifecycle is fully automated.

No orphaned cloud resources.

---

# Demo 15 — Closing Summary (1 minute)

Summarize

This solution demonstrates:

✅ FastAPI

✅ Pydantic

✅ DAG Construction

✅ Breadth-First Search

✅ Async Health Checks

✅ Docker

✅ Terraform

✅ Cloud Run

✅ Artifact Registry

✅ GitHub Actions

✅ Prometheus

✅ Grafana

✅ Structured Logging

✅ Documentation

---

# Common Interview Questions

### Why FastAPI?

- Automatic validation
- Async support
- OpenAPI generation

---

### Why NetworkX?

- Mature graph library
- DAG validation
- BFS support
- Easy extensibility

---

### Why BFS?

- Dependency-aware traversal
- Natural processing order
- Easy to parallelize by levels

---

### Why Cloud Run instead of Kubernetes?

- Fully managed
- Lower operational overhead
- Auto-scaling
- Cost effective for APIs

---

### Why Prometheus?

- Cloud native
- CNCF standard
- Google Managed Prometheus compatible

---

### Future Improvements

- Retry Policies
- Circuit Breakers
- OpenTelemetry
- Cloud Trace
- SLO
- Error Budgets
- AI Incident Summaries
- Vertex AI Root Cause Analysis
- Multi-region deployment

---

# Final Statement

This project demonstrates an end-to-end Platform Engineering solution covering application development, Infrastructure as Code, deployment, observability, testing, and documentation using Google Cloud managed services and production-oriented engineering practices.