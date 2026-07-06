# Architecture

## Overview

The System Health Check API is a FastAPI service that accepts a dependency graph, validates it, traverses component relationships, performs asynchronous health checks, and returns an aggregated JSON response.

## Application Flow

```text
Client
  ↓
FastAPI
  ↓
Request Validation
  ↓
DependencyGraph
  ↓
Breadth First Search
  ↓
Async Health Checker
  ↓
Health Aggregator
  ↓
JSON Response
```

### Flow Notes

- **FastAPI** handles request routing and schema validation.
- **DependencyGraph** validates DAG structure, detects cycles, and identifies root nodes.
- **Breadth First Search** preserves dependency order while avoiding duplicate execution.
- **Async Health Checker** performs concurrent HTTP checks using `httpx.AsyncClient`.
- **Health Aggregator** summarizes component results and produces the final response.

## Google Cloud Deployment

```text
GitHub
  ↓
GitHub Actions
  ↓
Artifact Registry
  ↓
Cloud Run
  ↓
Cloud Logging
  ↓
Cloud Monitoring
```

### Deployment Notes

- **GitHub Actions** builds and validates the application in CI.
- **Artifact Registry** stores the container image produced by the build.
- **Cloud Run** deploys the container as a managed, stateless HTTP service.
- **Cloud Logging** captures application logs from standard output.
- **Cloud Monitoring** provides operational visibility and alerting.

## Why Cloud Run Instead of Kubernetes

Cloud Run was selected because the workload is a stateless REST API with a small operational footprint. It provides managed autoscaling, simple deployment, and lower maintenance overhead than Kubernetes.

Kubernetes would introduce additional cluster management, networking, and platform complexity without delivering meaningful value for this assignment. Cloud Run better matches the goal of demonstrating platform engineering on Google-managed services while keeping the solution concise, production-ready, and easy to review.
