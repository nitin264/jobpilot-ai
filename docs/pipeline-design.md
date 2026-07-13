# Pipeline Design

## Purpose

Pipelines coordinate long-running, retryable workflows such as discovery, job extraction, matching, resume tailoring, screening generation, automation, and interview preparation.

Pipelines should be durable: progress, inputs, outputs, errors, and artifacts must survive process restarts.

## Pipeline Principles

- Keep stages small and idempotent.
- Persist state between external operations.
- Do not hold database transactions during network calls, browser automation, or LLM generation.
- Record enough metadata to debug failures.
- Make retry policy explicit per stage.
- Prefer resumable workflows over one large job.

## Core Pipeline Types

### Company Discovery Pipeline

Purpose:

- Discover career pages for registered companies.

Stages:

1. Load company.
2. Generate candidate career URLs.
3. Probe URLs.
4. Score discovered pages.
5. Persist career pages.
6. Trigger ATS detection when appropriate.

### ATS Detection Pipeline

Purpose:

- Identify the ATS used by a career page.

Stages:

1. Fetch career page metadata.
2. Run plugin detection probes.
3. Score evidence.
4. Persist ATS detection.
5. Select extraction strategy.

### Job Extraction Pipeline

Purpose:

- Extract jobs from career pages or ATS APIs.

Stages:

1. Resolve ATS plugin or generic extractor.
2. Fetch listing data.
3. Extract raw job records.
4. Normalize fields.
5. Deduplicate jobs.
6. Persist new and updated jobs.
7. Mark missing jobs as stale when appropriate.

### Job Matching Pipeline

Purpose:

- Evaluate jobs against candidate profiles.

Stages:

1. Load candidate profile and job.
2. Validate required data.
3. Run deterministic pre-score checks.
4. Call AI provider for qualitative reasoning when needed.
5. Persist match score and explanation.

### Resume Tailoring Pipeline

Purpose:

- Generate a tailored resume variant for a target job.

Stages:

1. Load candidate, base resume, and target job.
2. Build tailoring context.
3. Generate tailored content through AI provider.
4. Validate output against resume policy.
5. Persist artifact and metadata.
6. Mark application package readiness.

### Screening Generation Pipeline

Purpose:

- Generate or draft answers for screening questions.

Stages:

1. Load job, candidate, and known application context.
2. Detect or receive questions.
3. Generate answer drafts.
4. Apply safety and truthfulness checks.
5. Persist question set and answers.

### Browser Automation Pipeline

Purpose:

- Execute controlled application workflows using Playwright.

Stages:

1. Verify application package approval.
2. Resolve ATS automation plugin.
3. Start browser context.
4. Execute workflow steps.
5. Capture screenshots and step logs.
6. Pause for manual review when required.
7. Persist outcome and update application status.

### Interview Preparation Pipeline

Purpose:

- Generate candidate-specific interview prep materials.

Stages:

1. Load candidate, job, company, and application state.
2. Summarize company and role context.
3. Generate likely questions and talking points.
4. Generate gap-specific preparation plan.
5. Persist interview preparation artifact.

## Pipeline State Model

Recommended statuses:

- `pending`
- `running`
- `waiting_for_review`
- `succeeded`
- `failed`
- `cancelled`
- `retry_scheduled`

Each stage should record:

- Stage name.
- Start and completion time.
- Status.
- Retry count.
- Error category.
- Input reference.
- Output reference.
- Artifact references.

## Idempotency

Every pipeline run should have an idempotency key derived from intent. Examples:

- Company discovery: company ID plus requested scan date or manual run ID.
- Job extraction: career page ID plus scan window.
- Matching: candidate ID plus job ID plus profile version plus job version.
- Resume tailoring: candidate ID plus base resume ID plus job ID plus tailoring strategy version.

Idempotency prevents duplicate records when retries occur.

## Retry Policy

Retryable:

- Network timeouts.
- Browser startup failures.
- Provider rate limits.
- Temporary ATS unavailability.
- Serialization conflicts.

Not retryable without intervention:

- Missing required candidate data.
- Unsupported ATS workflow.
- Invalid application status transition.
- Provider output that violates policy repeatedly.
- Authentication or permission failures.

Use exponential backoff with capped retries for infrastructure failures.

## Human Review Gates

Human review should be required before:

- Submitting a job application.
- Sending generated answers to an external form.
- Using a tailored resume for submission.
- Proceeding after browser automation detects uncertainty.

The domain should represent review state explicitly rather than encoding it as a worker flag.

## Observability

Each pipeline should emit:

- Structured logs.
- Pipeline run events.
- Stage duration metrics.
- Provider call metadata.
- Artifact references.
- Audit events for user-visible outcomes.

