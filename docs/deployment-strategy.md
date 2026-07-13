# Deployment Strategy

## Goals

Deployment should support local Windows development first, then evolve toward production reliability without changing the core architecture.

## Local Development

Use Docker Compose for local services:

- PostgreSQL.
- Ollama.
- API service.
- Worker service.
- Scheduler service.
- Optional future frontend.

Developers should be able to run the platform from VS Code on Windows with consistent environment variables and mounted source directories.

## Environments

Recommended environments:

- Local: developer machine, local Docker Compose, local Ollama.
- CI: GitHub Actions, ephemeral database, fake or optional provider tests.
- Staging: production-like deployment with test data and limited external access.
- Production: managed infrastructure, backups, monitoring, secrets management, and access controls.

## Process Model

Separate runtime processes:

- API process handles HTTP requests.
- Worker process handles pipelines and long-running tasks.
- Scheduler process dispatches recurring work.

This separation prevents slow browser automation and LLM calls from blocking API responsiveness.

## Container Strategy

Use containers for deployable units. Build images should be reproducible and avoid embedding secrets.

Container responsibilities:

- API image contains the FastAPI application.
- Worker image can reuse the same codebase with a different entrypoint.
- Scheduler image can reuse the same codebase with a different entrypoint.
- Frontend image can be added when the React dashboard exists.

## Database Operations

PostgreSQL should have:

- Automated backups.
- Point-in-time recovery in production.
- Migration runbooks.
- Connection pooling strategy.
- Monitoring for locks, slow queries, and storage growth.

Migrations should be applied deliberately during deployment, not as a hidden side effect of application startup.

## Secrets

Secrets should include:

- Database credentials.
- Provider API keys.
- Session secrets.
- Encryption keys.
- External service credentials.

Local development can use `.env`, but staging and production should use a secret manager provided by the hosting environment.

## Observability

Production deployment should include:

- Structured log aggregation.
- Metrics for API latency, worker throughput, provider latency, pipeline failures, and browser automation failures.
- Error tracking.
- Health checks.
- Audit event review.

## Scaling

Initial scaling approach:

- Scale workers horizontally for extraction, matching, and preparation pipelines.
- Keep API stateless.
- Use database-backed task claiming initially.

Future scaling:

- Introduce a queue when database-backed task claiming becomes a bottleneck.
- Split heavy browser automation workers from AI generation workers.
- Introduce search infrastructure if job search becomes high volume.

## Production Readiness Checklist

Before production launch:

- Authentication and authorization are implemented.
- Sensitive data logging is blocked.
- Provider costs and rate limits are monitored.
- Application submission requires review gates.
- Backups and restore tests exist.
- Alembic migration process is documented.
- Worker retry behavior is bounded.
- Browser automation artifacts have retention policies.
- Security review covers prompt injection and data privacy.

## Trade-Offs

### Docker Compose First

Chosen for local simplicity and Windows developer support.

Alternative: Kubernetes from the start. Kubernetes is powerful but adds operational complexity before the product needs it.

### Database-Backed Work Queue Initially

Chosen for fewer moving parts.

Alternative: Redis, RabbitMQ, or cloud queues. These may be introduced when throughput or scheduling complexity requires them.

### Local Ollama Default

Chosen for privacy and offline-friendly development.

Alternative: hosted LLM by default. Hosted models can improve quality but add cost, network dependency, and privacy review requirements.

