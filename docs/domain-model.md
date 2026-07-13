# Domain Model

## Domain Overview

The JobPilot AI domain is centered on helping candidates discover, evaluate, prepare for, and track job applications. The model should capture recruitment concepts independently from persistence, API payloads, or UI concerns.

## Aggregate Candidates

### Company

Represents an organization that may publish jobs.

Responsibilities:

- Store canonical company identity.
- Track known domains and career entry points.
- Maintain discovery status.
- Associate detected ATS platforms.

Key relationships:

- Company has many career pages.
- Company has many job postings.
- Company has many discovery runs.

### Career Page

Represents a company-owned or ATS-hosted page used to list roles.

Responsibilities:

- Store URL, page type, reachability status, and discovery confidence.
- Record whether page belongs to company domain, subdomain, or third-party ATS.
- Track last scan metadata.

### ATS Integration

Represents the detected applicant tracking system for a company or career page.

Responsibilities:

- Capture ATS type, detection evidence, confidence, and plugin capability.
- Determine which extractor or automation plugin should handle the page.

### Job Posting

Represents a specific employment opportunity.

Responsibilities:

- Hold source-specific raw job data.
- Hold normalized job attributes.
- Track source URL, external ID, status, and freshness.
- Connect to matching, tailoring, and application records.

The normalized job should include title, company, location, remote policy, employment type, seniority, department, description, requirements, responsibilities, salary range, benefits, skills, and application URL when available.

### Candidate Profile

Represents the user or candidate being matched to jobs.

Responsibilities:

- Store profile facts, preferences, skills, experience, education, target roles, location preferences, work authorization, and compensation expectations.
- Reference resumes and generated artifacts.

Sensitive fields must be handled with privacy controls.

### Resume

Represents a source or tailored resume.

Responsibilities:

- Store resume metadata and extracted structured profile data.
- Connect generated resume variants to the original source resume.
- Track tailoring rationale and target job.

The domain should distinguish between original uploaded resumes, parsed resume facts, and generated tailored documents.

### Job Match

Represents an evaluation of fit between a candidate and a job.

Responsibilities:

- Store match score, criteria-level explanations, gaps, strengths, and recommendation.
- Reference the matching strategy and AI provider version used.
- Allow recalculation when candidate or job data changes.

### Screening Question Set

Represents questions and suggested answers for a job application.

Responsibilities:

- Store detected or generated questions.
- Store candidate-specific answer drafts.
- Track confidence, source, and review status.

### Application

Represents an attempt or intent to apply for a job.

Responsibilities:

- Track lifecycle from saved job to submitted application.
- Store status, timestamps, target resume, screening answers, and submission evidence.
- Record manual and automated actions.

Recommended statuses:

- `saved`
- `matched`
- `prepared`
- `ready_to_apply`
- `in_progress`
- `submitted`
- `needs_review`
- `rejected`
- `interviewing`
- `offer`
- `closed`

### Automation Run

Represents a browser automation attempt.

Responsibilities:

- Track requested workflow, execution status, browser artifacts, step logs, screenshots, and failure reason.
- Associate with application, ATS plugin, or discovery run.

### Interview Preparation

Represents preparation artifacts for a candidate and job.

Responsibilities:

- Store likely interview topics, company research summary, behavioral question preparation, technical preparation, and tailored talking points.

## Supporting Concepts

### Pipeline Run

Represents a durable execution of a multi-stage process such as company discovery, job extraction, or application preparation.

Responsibilities:

- Track state, owner, idempotency key, stage outcomes, retries, and artifacts.

### Artifact

Represents generated or captured material.

Examples:

- Raw HTML snapshot.
- Extracted JSON.
- Resume variant.
- Prompt response.
- Screenshot.
- Interview prep notes.

Artifacts should have metadata for sensitivity, retention, and origin.

### Audit Event

Represents notable user-visible or security-relevant actions.

Examples:

- Job extracted.
- Resume tailored.
- Screening answer generated.
- Browser automation submitted an application.
- Provider call failed.

## Domain Service Candidates

Domain services should contain business rules that do not naturally belong to one entity:

- Company identity resolution.
- Career page URL ranking.
- ATS detection scoring.
- Job normalization.
- Duplicate job detection.
- Match scoring policy.
- Resume tailoring policy.
- Screening answer policy.
- Application status transition policy.
- Automation safety policy.

## Invariants

- A job posting must have a source company or source organization name.
- A normalized job must preserve a link to its raw source data.
- A tailored resume must reference both a candidate and a target job.
- An application must reference one job and one candidate.
- Automated submission must not occur without an explicit candidate-approved application package.
- Provider outputs used for user-visible decisions must store provider metadata and generation timestamp.
- Application status transitions must be validated by policy, not arbitrary writes.

## Domain Events

Domain events should be recorded when meaningful state changes occur:

- `CompanyRegistered`
- `CareerPageDiscovered`
- `AtsDetected`
- `JobExtracted`
- `JobNormalized`
- `JobMatched`
- `ResumeTailored`
- `ScreeningQuestionsGenerated`
- `ApplicationPrepared`
- `ApplicationSubmitted`
- `InterviewPrepGenerated`

Events can initially be stored in relational tables and processed in-process. A message broker can be introduced later if event volume or integration needs justify it.

