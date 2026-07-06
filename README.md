# System Health Check API

A production-oriented Python REST API that evaluates the health of interconnected system components represented as a Directed Acyclic Graph (DAG).

This project was developed as part of a Platform Engineering / AI SRE take-home assignment with a focus on software engineering quality, cloud-native architecture, observability, developer experience, and maintainability.

---

# Executive Summary

The objective is to build a REST API capable of evaluating the health of systems composed of multiple dependent services.

Each service is represented as a node in a Directed Acyclic Graph (DAG), where dependency relationships are modeled as graph edges.

The API validates the graph, traverses it using Breadth First Search (BFS), performs asynchronous health checks, aggregates overall system health, and returns both machine-readable and human-readable results.

The implementation intentionally emphasizes production engineering principles rather than unnecessary architectural complexity.

---

# Problem Statement

Implement a REST API that:

- Accepts a JSON representation of a dependency graph
- Validates graph correctness
- Detects dependency cycles
- Traverses the graph using Breadth First Search (BFS)
- Executes asynchronous health checks
- Aggregates overall system health
- Returns JSON and table-based results
- Demonstrates production-ready engineering practices

---

# Current Implementation Status

## ✅ Phase 0 – Project Foundation

Completed

- Project structure
- Bootstrap script
- Makefile
- Dockerfile
- GitHub Actions CI
- Terraform scaffold
- CODEOWNERS
- Pull Request template
- Python package structure

---

## ✅ Phase 1 – FastAPI Foundation

Completed

- FastAPI application
- Configuration management
- Structured logging
- Application startup
- Health endpoints

Available endpoints

- GET /
- GET /health
- GET /live
- GET /ready

---

## ✅ Phase 2 – Domain Models

Completed

- Request models
- Response models
- Pydantic validation
- Unit tests

---

## ✅ Phase 3 – Dependency Graph Engine

Completed

Features

- Directed graph construction
- DAG validation
- Cycle detection
- Root node discovery
- Breadth First Search traversal
- NetworkX integration
- Unit tests

---

## 🚧 Phase 4 – Async Health Checker

In Progress

Implementation

- asyncio
- httpx.AsyncClient
- Concurrent health checks
- Configurable timeout
- Response latency measurement

---

## ⏳ Remaining Milestones

- Health aggregation
- Human-readable table output
- API orchestration
- Prometheus metrics
- Cloud Run deployment
- Terraform completion
- Documentation
- Optional DAG visualization

---

# Current Architecture

```
                    Client
                       │
                       ▼
                 FastAPI API
                       │
                       ▼
            HealthCheckService
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
 DependencyGraph              HealthChecker
         │                           │
         └─────────────┬─────────────┘
                       ▼
              HealthAggregator
                       │
                       ▼
          JSON + Human Readable Table
```

---

# Technology Stack

## Application

- Python 3.12
- FastAPI
- Pydantic v2
- NetworkX
- asyncio
- httpx
- tabulate

## Platform Engineering

- Docker
- Terraform
- GitHub Actions
- Cloud Run
- Artifact Registry

## Observability

Current

- Structured logging
- Health endpoints

Planned

- Prometheus metrics
- Cloud Monitoring
- Cloud Logging
- OpenTelemetry (future)

---

# Engineering Principles

This implementation intentionally prioritizes

- Simplicity
- Maintainability
- Production readiness
- Google Cloud managed services
- Developer Experience
- Infrastructure as Code
- Observability
- Platform Engineering best practices

---

# Features Implemented

- FastAPI REST API
- Configuration management
- Structured logging
- Health endpoints
- Request validation
- Dependency graph construction
- DAG validation
- Cycle detection
- Breadth First Search traversal
- Docker support
- GitHub Actions CI
- Terraform project scaffold

---

# Features Planned

- Concurrent asynchronous health checks
- Health aggregation
- Human-readable table output
- Prometheus metrics
- Cloud Run deployment
- Artifact Registry deployment
- End-to-end API workflow
- Optional DAG visualization

---

# Assumptions

- Input graph must be a Directed Acyclic Graph (DAG).
- Cyclic graphs return HTTP 400.
- Health checks are request scoped.
- No persistence is required.
- Cloud Run is the target runtime environment.
- Google managed services are preferred over self-managed infrastructure.

---

# Features Intentionally Excluded

To keep the implementation focused within the assignment time constraints, the following capabilities are intentionally excluded:

- Authentication
- Authorization
- Database persistence
- Kubernetes (GKE)
- Retry policies
- Circuit breakers
- Distributed cache
- Multi-region deployment
- AI Root Cause Analysis
- AI Agents
- OpenTelemetry implementation

These are documented as future enhancements.

---

# Observability

Current implementation

- Structured application logging
- Health endpoints
- Cloud Logging compatible output

Planned

- Prometheus metrics
- Request latency metrics
- Health check latency metrics
- Component health metrics

Future

- OpenTelemetry
- Cloud Trace
- SLO dashboards
- Error budgets

---

# AI Usage

AI tools were used to improve developer productivity while maintaining engineering ownership.

GitHub Copilot

- Boilerplate generation
- Test generation
- Async implementation
- Terraform scaffolding

ChatGPT

- Architecture review
- Platform engineering guidance
- Design decisions
- Documentation
- CI/CD review
- Code review

All AI-generated code and recommendations were manually reviewed, tested, modified where appropriate, and fully understood before being committed.

---

# Project Status

Current Progress

```
████████████░░░░░░░░ 60%

✅ Foundation
✅ FastAPI
✅ Configuration
✅ Logging
✅ Models
✅ Dependency Graph
🚧 Async Health Checker
⬜ Aggregator
⬜ Service
⬜ API
⬜ Metrics
⬜ Terraform
⬜ Documentation
```

The remaining work focuses on integrating asynchronous health evaluation, system health aggregation, observability, deployment, and final documentation.

## Current Progress

- ✅ Foundation
- ✅ FastAPI
- ✅ Configuration
- ✅ Logging
- ✅ API Models
- ⏳ DAG Engine
- ⏳ Async Health Checks
- ⏳ Aggregation
- ⏳ Metrics
- ⏳ Terraform Deployment

Current

- Structured logging
- Health endpoints
- Prometheus metrics
- Cloud Logging compatible

Future

- Managed Prometheus
- Cloud Monitoring dashboards
- Alert Policies
- Cloud Trace
- OpenTelemetry

