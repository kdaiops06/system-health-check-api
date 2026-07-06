# Platform Engineering Considerations

## Objective

This implementation intentionally focuses on a production-oriented MVP suitable for deployment on Google Cloud while minimizing operational complexity.

---

## Runtime Platform

- Google Cloud Run
- Artifact Registry
- GitHub Actions
- Terraform

Reason

Cloud Run provides:

- fully managed infrastructure
- automatic scaling
- integrated logging
- integrated monitoring
- reduced operational overhead

For the scope of this assignment, Cloud Run was preferred over GKE.

---

## CI/CD

Source Control

GitHub

↓

GitHub Actions

↓

Unit Tests

↓

Lint

↓

Docker Build

↓

Artifact Registry

↓

Cloud Run

Future

Cloud Deploy
Progressive Delivery
Blue/Green Deployment

---

## Observability

Current

- Application logging
- Health endpoints
- Prometheus metrics

Future

- Google Managed Prometheus
- Cloud Monitoring
- Cloud Logging dashboards
- Alert Policies
- SLOs
- Error Budgets

---

## Security

Current

- Environment variables
- Input validation

Future

- Secret Manager
- IAM
- Binary Authorization
- Workload Identity
- VPC Connector
- Private Service Connect

---

## Reliability

Current

- DAG validation
- Cycle detection
- Async execution

Future

- Retry policies
- Circuit breakers
- Exponential backoff
- Timeouts
- Rate limiting

---

## AI SRE Evolution

Future capabilities

- Vertex AI Root Cause Analysis
- AI Incident Summary
- AI Runbook Generation
- AI Platform Gateway
- AI Policy Engine
- Prompt Guardrails
- Hallucination Detection
- AI Observability