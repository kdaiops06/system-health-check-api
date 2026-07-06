# Design Decisions

## DD-001: FastAPI

### Decision

Use FastAPI as the REST framework.

### Rationale

- Native async support
- Excellent Pydantic integration
- Automatic OpenAPI documentation
- High performance for I/O workloads

### Tradeoff

Slightly more opinionated than Flask but significantly better suited for asynchronous APIs.

---

## DD-002: Cloud Run

### Decision

Deploy on Google Cloud Run.

### Rationale

- Fully managed
- Serverless
- Integrated with Cloud Logging and Monitoring
- Minimal operational overhead

### Tradeoff

Less infrastructure control than GKE, but a much better fit for the assignment scope.

---

## DD-003: Pydantic Models

### Decision

Use Pydantic models for API contracts.

### Rationale

- Strong validation
- Type safety
- Automatic serialization
- Better developer experience

### Tradeoff

Small runtime validation cost.

## DD-004

### Decision:
Validate DAG before traversal.

### Reason:
Fail fast and prevent invalid health check execution.

### Tradeoff:
Small validation overhead before processing.

## DD-005
### Decision

Use Breadth First Search (BFS) to traverse the dependency graph.

### Rationale

BFS processes services level by level, making dependency relationships easier to understand and providing a deterministic traversal order for health evaluation.

### Tradeoff

DFS is equally valid for traversal, but BFS provides a more intuitive execution order for dependency graphs and operational troubleshooting.