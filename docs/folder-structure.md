# Folder Structure

## Goals

The folder structure should make boundaries visible. A developer should know where a use case, domain rule, plugin, provider adapter, database implementation, or API interface belongs without guessing.

## Target Repository Layout

```text
jobpilot-ai/
  backend/
    app/
      main.py                  # FastAPI composition root only
      api/                     # HTTP interface layer
      application/             # use cases and orchestration
      domain/                  # business model and domain services
      infrastructure/          # adapters for DB, AI, browser, ATS, storage
      workers/                 # background worker entrypoints and handlers
      scheduler/               # scheduled job dispatch
      shared/                  # cross-cutting primitives with no business logic
    migrations/                # Alembic migrations
  frontend/                    # future React dashboard
  infra/                       # deployment, compose, and operational assets
  scripts/                     # developer and operational scripts
  tests/
    unit/
    integration/
    contract/
    e2e/
  docs/
```

This document describes the intended layout. It does not require all folders to exist before implementation.

## Backend Package Layout

```text
backend/app/
  api/
    dependencies/
    dto/
    routers/
    error_handlers/

  application/
    companies/
    discovery/
    ats/
    jobs/
    candidates/
    matching/
    resumes/
    screening/
    applications/
    interviews/
    pipelines/

  domain/
    companies/
    discovery/
    ats/
    jobs/
    candidates/
    matching/
    resumes/
    screening/
    applications/
    interviews/
    automation/
    ai/

  infrastructure/
    database/
      repositories/
      models/
      unit_of_work/
    ai/
      providers/
    ats/
      plugins/
    browser/
    storage/
    logging/
    settings/

  workers/
    handlers/
    runtime/

  scheduler/
    jobs/

  shared/
    errors/
    ids/
    time/
    typing/
```

## Layer Responsibilities

### `domain`

Contains framework-independent business rules:

- Entities.
- Value objects.
- Domain services.
- Domain events.
- Domain errors.
- Policy objects.

Domain code must not import FastAPI, SQLAlchemy, Playwright, Ollama clients, HTTP SDKs, or environment settings.

### `application`

Contains use cases and orchestration:

- Commands and queries.
- Application services.
- Pipeline coordinators.
- Transaction boundaries.
- Authorization checks delegated from API context.
- Calls to repository, provider, and plugin interfaces.

Application code may define interfaces that infrastructure implements.

### `infrastructure`

Contains adapters:

- SQLAlchemy models and repositories.
- Alembic integration.
- Ollama and OpenAI-compatible clients.
- Playwright browser automation.
- ATS plugin implementations.
- File or object storage.
- Logging setup.
- Settings loading.

Infrastructure depends on application and domain contracts, not the reverse.

### `api`

Contains the HTTP interface:

- FastAPI routers.
- Request and response DTOs.
- Dependency wiring.
- Authentication extraction.
- Error mapping.

API routes should be thin and delegate to application services.

### `workers`

Contains background execution entrypoints and task handlers. Worker handlers should delegate business decisions to application services and pipeline orchestrators.

### `scheduler`

Contains scheduled dispatch logic. Scheduler jobs should create pipeline runs or enqueue tasks, not perform extraction or AI work directly.

### `shared`

Contains primitives with no business-specific dependencies:

- Typed IDs.
- Clock abstractions.
- Base error classes.
- Result helpers.
- Serialization helpers.

Do not turn `shared` into a dumping ground for domain logic.

## Import Direction Rules

Allowed dependency direction:

```text
api -> application -> domain
workers -> application -> domain
scheduler -> application -> domain
infrastructure -> application/domain
```

Disallowed:

- `domain` importing from `application`, `api`, or `infrastructure`.
- `application` importing concrete SQLAlchemy models or provider SDK clients.
- `api` directly importing SQLAlchemy models for response serialization.
- ATS plugins mutating job records without going through application contracts.

## Naming Guidance

- Prefer domain language over technical shortcuts.
- Use `service` for use-case orchestration only when a more specific name is not available.
- Use `policy` for business decision objects.
- Use `adapter` for infrastructure implementations of external contracts.
- Use `repository` only for persistence abstractions.
- Use `plugin` only for ATS integration modules registered through the ATS plugin registry.

