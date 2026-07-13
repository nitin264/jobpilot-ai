# Coding Standards

## Goals

Coding standards should make the codebase predictable, strongly typed, and easy to test. The standards below apply once implementation begins.

## Python Version and Style

- Use modern Python with type hints throughout.
- Prefer explicit imports.
- Prefer small modules with focused responsibilities.
- Use dataclasses or typed value objects for domain concepts when appropriate.
- Avoid framework imports in domain code.
- Keep functions short enough to test and review.

## Typing

- All public functions and methods should have type annotations.
- Domain identifiers should use typed wrappers or strong conventions rather than passing raw strings everywhere.
- Avoid `Any` except at external boundaries.
- Validate external data before converting it into domain objects.

## Clean Architecture Rules

- Domain layer contains business rules and no framework dependencies.
- Application layer coordinates use cases and transaction boundaries.
- Infrastructure layer implements adapters.
- API layer maps HTTP requests to application commands and queries.

Dependency violations should be treated as architecture bugs.

## Dependency Injection

Use dependency injection for:

- Repositories.
- Unit of work.
- AI providers.
- ATS registry.
- Browser automation.
- Clock.
- ID generation.
- Settings.

Do not instantiate infrastructure clients deep inside domain or application services.

## Error Handling

- Raise typed domain or application errors.
- Convert errors to HTTP responses only at the API boundary.
- Preserve original provider and infrastructure error details in logs where safe.
- Avoid broad exception swallowing.
- Mark retryable and non-retryable failures explicitly.

## Logging

Use structured logging. Include correlation fields consistently. Never log:

- API keys.
- Passwords.
- Full resumes unless explicitly redacted.
- Full LLM prompts containing sensitive candidate data.
- Browser session secrets.

## AI Usage Standards

- Treat model output as untrusted.
- Validate structured output.
- Store provider metadata.
- Version prompts.
- Keep prompts close to the use case that owns them.
- Require human review for generated content that will be submitted externally.

## Database Standards

- Keep SQLAlchemy models in infrastructure.
- Use migrations for all schema changes.
- Avoid business logic in ORM models.
- Use repositories for persistence operations.
- Use explicit transaction boundaries.
- Avoid long transactions around external calls.

## Browser Automation Standards

- All Playwright use belongs behind automation adapters or ATS plugins.
- Capture step logs and artifacts for debugging.
- Prefer robust selectors and semantic cues.
- Support manual pause or review for uncertain actions.
- Do not submit applications without approval.

## API Standards

- Routes should be thin.
- Request and response DTOs should be separate from domain and persistence models.
- API errors should be consistent.
- Pagination should be used for list endpoints.
- Idempotency keys should be supported for commands that create long-running work.

## Documentation Standards

- Update architecture docs when boundaries or major decisions change.
- Document provider and plugin capabilities.
- Keep trade-off notes for irreversible or expensive decisions.
- Prefer diagrams when behavior spans multiple modules.

