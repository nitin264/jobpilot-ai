# Testing Strategy

## Testing Goals

Testing should protect domain behavior, module boundaries, provider contracts, ATS plugin behavior, database mappings, and browser automation workflows. Tests should be fast by default and realistic where risk requires it.

## Test Pyramid

Recommended mix:

- Many unit tests.
- Focused integration tests.
- Contract tests for providers and plugins.
- A smaller set of end-to-end tests.
- Manual exploratory testing for unstable third-party ATS behavior.

## Unit Tests

Unit tests should cover:

- Domain policies.
- Application use cases with fake repositories.
- Application status transitions.
- Job normalization rules.
- Duplicate detection.
- Match scoring policy.
- Resume tailoring validation.
- Screening answer validation.
- Pipeline stage orchestration with fake adapters.

Unit tests should not require PostgreSQL, Ollama, Playwright, or network access.

## Integration Tests

Integration tests should cover:

- SQLAlchemy repositories against PostgreSQL.
- Unit-of-work transaction behavior.
- Alembic migration compatibility.
- API dependency wiring.
- Worker handler persistence behavior.
- Artifact storage adapters.

Use Docker Compose or test containers when practical.

## Contract Tests

Contract tests are required for:

- AI provider adapters.
- ATS plugins.
- Browser automation adapters.
- Repository implementations.

Contract tests verify that each adapter follows the interface expected by application services.

## ATS Plugin Tests

Each ATS plugin should include:

- Detection tests from URL and HTML fixtures.
- Extraction tests from stored listing fixtures.
- Job detail parsing tests.
- Error mapping tests.
- Capability declaration tests.

Live ATS tests should be limited, rate-controlled, and not required for every local test run.

## AI Provider Tests

Use three levels:

- Fake provider tests for application logic.
- Contract tests for adapter behavior.
- Optional smoke tests for real Ollama and OpenAI-compatible providers.

Provider tests should verify:

- Timeouts.
- Error mapping.
- Structured output validation.
- Metadata capture.
- Retry handling.

## Browser Automation Tests

Playwright tests should cover:

- Stable internal test pages.
- Generic workflow execution.
- Pause and review behavior.
- Screenshot and artifact capture.
- Error handling.

Do not rely on live job application pages for routine tests. Use local fixture pages and selected manual smoke checks for real ATS platforms.

## End-to-End Tests

End-to-end tests should validate critical workflows:

- Register company, discover career page, detect ATS, extract jobs.
- Create candidate, match job, generate resume tailoring plan.
- Prepare application package and stop before external submission.
- Generate interview prep from existing job and candidate data.

E2E tests should run in CI after unit and integration tests.

## Test Data

Use deterministic fixture data:

- Company samples.
- Career page HTML.
- ATS listing responses.
- Job descriptions.
- Candidate profiles.
- Resume text.
- AI provider fake responses.

Sensitive real resumes or personal data should not be committed.

## CI Strategy

GitHub Actions should eventually run:

1. Formatting checks.
2. Static typing.
3. Linting.
4. Unit tests.
5. Integration tests.
6. Contract tests.
7. E2E tests where environment allows.

Tests that require real provider credentials should be opt-in and skipped by default.

## Quality Gates

Before production release:

- Domain logic coverage for critical policies.
- Repository integration coverage for all aggregates.
- Contract coverage for supported ATS plugins.
- AI output validation coverage.
- Browser automation review-gate coverage.
- Migration upgrade and downgrade checks where practical.

