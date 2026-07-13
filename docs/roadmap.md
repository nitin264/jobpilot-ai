# Roadmap

## Phase 0: Architecture Foundation

Goals:

- Establish documentation.
- Confirm module boundaries.
- Define domain model.
- Define database design.
- Define pipeline, AI provider, and ATS plugin architecture.

Exit criteria:

- Architecture docs are reviewed.
- Initial implementation plan is agreed.
- No source implementation is required for this phase.

## Phase 1: Backend Skeleton

Goals:

- Create FastAPI application shell.
- Add settings validation.
- Add structured logging.
- Add database connection and Alembic baseline.
- Add repository and unit-of-work interfaces.
- Add test scaffolding.

Exit criteria:

- API starts locally.
- Database migrations run locally.
- Unit tests and formatting run in CI.

## Phase 2: Company and Discovery Core

Goals:

- Implement company registry.
- Implement career page discovery.
- Implement basic ATS detection.
- Persist discovery runs and audit events.

Exit criteria:

- A company can be registered.
- Career pages can be discovered and scored.
- ATS detection records evidence and confidence.

## Phase 3: Job Extraction and Normalization

Goals:

- Implement ATS plugin registry.
- Add generic extraction plugin.
- Add first dedicated ATS plugin.
- Implement job normalization and deduplication.

Exit criteria:

- Jobs can be extracted from supported career pages.
- Raw and normalized job data are persisted.
- Duplicate jobs are handled predictably.

## Phase 4: Candidate, Matching, and AI Provider Layer

Goals:

- Implement candidate profile.
- Implement Ollama provider adapter.
- Implement fake provider for tests.
- Implement job matching pipeline.

Exit criteria:

- Candidate profiles can be matched against jobs.
- Match scores include explanations and provider metadata.
- Matching tests are deterministic.

## Phase 5: Resume Tailoring and Screening

Goals:

- Add resume records and parsed facts.
- Generate tailored resume variants.
- Generate screening question answer drafts.
- Add human review states.

Exit criteria:

- Application packages can be prepared but not automatically submitted.
- Generated content stores prompt and provider metadata.
- Review gates are enforced.

## Phase 6: Browser Automation

Goals:

- Add Playwright automation adapter.
- Add automation run tracking.
- Add ATS-specific application workflow support.
- Capture screenshots and step logs.

Exit criteria:

- Automation can navigate supported test workflows.
- Submission requires explicit approval.
- Failures produce useful diagnostic artifacts.

## Phase 7: Application Tracking and Interview Prep

Goals:

- Implement application lifecycle.
- Add interview preparation generation.
- Add application status history.
- Add reminders or scheduled checks if needed.

Exit criteria:

- Candidates can track applications across statuses.
- Interview prep is generated from candidate, job, and company context.

## Phase 8: React Dashboard

Goals:

- Build dashboard for companies, jobs, matches, applications, resumes, and interview prep.
- Add review workflows for generated content.
- Add pipeline run visibility.

Exit criteria:

- Users can operate primary workflows without direct API calls.
- Review gates are usable from the UI.

## Phase 9: Production Hardening

Goals:

- Add authentication and authorization.
- Add monitoring, alerting, and error tracking.
- Add backup and restore processes.
- Add provider cost controls.
- Add privacy and retention workflows.

Exit criteria:

- Staging environment is production-like.
- Production readiness checklist is complete.
- Operational runbooks exist.

## Phase 10: Scale and Extensibility

Goals:

- Add more ATS plugins.
- Introduce queue infrastructure if needed.
- Add search improvements.
- Add OpenAI-compatible provider support.
- Add plugin contract documentation for contributors.

Exit criteria:

- New ATS support can be added with minimal core changes.
- Worker throughput can scale independently.
- Provider selection is configuration-driven.

