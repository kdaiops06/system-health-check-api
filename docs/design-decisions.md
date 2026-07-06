DD-003

Decision:
Use Pydantic models for API contracts.

Why:
- Strong validation
- Automatic serialization
- OpenAPI generation
- Better developer experience

Tradeoff:
Slight runtime overhead compared to dataclasses, acceptable for API workloads.