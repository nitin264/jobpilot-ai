# Folder Structure

## Goals

The folder structure should make current responsibilities obvious without creating empty layers. JobPilot AI should grow toward Clean Architecture, but the repository should only contain directories that provide value today.

Guiding rules:

- Prefer a small number of clear directories over deep placeholder trees.
- Add feature modules only when those features exist.
- Add infrastructure subpackages only when there are real adapters to isolate.
- Keep the backend approachable for a two-person engineering team.
- Preserve a natural path to domain, application, worker, scheduler, and infrastructure layers later.

## Current Repository Layout

```text
jobpilot-ai/
  backend/
    Dockerfile
    app/
      main.py              # FastAPI composition root
      api/                 # HTTP routes, request middleware, HTTP error mapping
      core/                # settings and runtime cross-cutting utilities
  frontend/                # future React dashboard
  infra/                   # future deployment and operational assets
  scripts/                 # future developer and operational scripts
  tests/                   # future test suites
  docs/
```

## Current Backend Layout

```text
backend/app/
  main.py
  api/
    health.py              # /health and /ready endpoints
    errors.py              # central HTTP exception handling
    request_logging.py     # request/correlation logging middleware
  core/
    config.py              # Pydantic Settings and environment loading
    logging.py             # structured logging setup
```

## Current Directory Responsibilities

### `app`

Contains the backend Python package. `main.py` is the composition root: it creates the FastAPI app, configures logging, registers middleware, registers exception handlers, and includes API routes.

### `api`

Contains HTTP interface concerns that exist today:

- Health and readiness endpoints.
- HTTP exception mapping.
- Request logging middleware.

Future request and response DTOs can live here when non-trivial API surfaces exist. Do not create nested `routers`, `dependencies`, or `dto` packages until there are enough files to justify them.

### `core`

Contains cross-cutting runtime concerns used by the application foundation:

- Configuration loading.
- Structured logging.

This is intentionally not a dumping ground for business logic. Domain rules, use cases, repositories, provider clients, ATS plugins, and browser automation do not belong here.

## Future Growth Path

Add directories when they solve a present problem:

- Add `domain/` when business entities, value objects, domain services, or domain events are implemented.
- Add `application/` when use cases or orchestration logic exists.
- Add `infrastructure/` when concrete adapters exist, such as SQLAlchemy, AI providers, storage, browser automation, or ATS plugin implementations.
- Add `workers/` when background processing exists.
- Add `scheduler/` when scheduled dispatch exists.
- Split `api/health.py` into `api/routers/` only after there are multiple route modules.
- Split `core/config.py` or `core/logging.py` into packages only when each area has multiple cohesive files.

## Import Direction Rules

Current allowed dependencies:

```text
main -> api/core
api -> core
core -> standard library and runtime dependencies
```

Future intended dependency direction:

```text
api -> application -> domain
workers -> application -> domain
scheduler -> application -> domain
infrastructure -> application/domain
```

Disallowed now and later:

- Business logic in `api` or `core`.
- Framework imports in future domain code.
- SQLAlchemy models used directly as API response models.
- Provider SDKs, Playwright, or ATS-specific logic imported into domain code.

## Naming Guidance

- Use names from the business domain once domain code exists.
- Use `core` only for foundation-level runtime concerns.
- Use `infrastructure` only for concrete external adapters.
- Use `repository`, `provider`, `plugin`, and `service` only when those concepts are actually implemented.
