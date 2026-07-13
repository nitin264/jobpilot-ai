# ATS Plugin Architecture

## Purpose

ATS plugins isolate ATS-specific behavior from the core product. They allow JobPilot AI to support platforms such as Greenhouse, Lever, Workday, Ashby, SmartRecruiters, and generic career pages without hard-coding each platform into core services.

## Plugin Responsibilities

An ATS plugin may provide:

- Detection probes.
- Career page URL parsing.
- Job listing extraction.
- Job detail extraction.
- Job application URL resolution.
- Screening question discovery.
- Browser automation workflow steps.
- Capability metadata.

Plugins should not own core application state or write directly to persistence.

## Plugin Contract Concepts

Each plugin should declare:

- Plugin name.
- ATS type.
- Supported URL patterns.
- Detection signals.
- Capabilities.
- Version.
- Known limitations.

Capabilities may include:

- `detect`
- `extract_listings`
- `extract_job_detail`
- `extract_screening_questions`
- `resolve_application_url`
- `automate_application`

## Detection

Detection should combine multiple evidence sources:

- URL patterns.
- HTML markers.
- Script sources.
- API endpoints.
- Form structure.
- Redirect behavior.

The ATS detection service should score evidence and select the best plugin. A low-confidence detection should use generic extraction or require review.

## Extraction Flow

Recommended extraction flow:

1. Core job extraction pipeline selects plugin by ATS detection.
2. Plugin fetches or receives source content through approved adapters.
3. Plugin returns provider-neutral raw job DTOs.
4. Core job module normalizes and persists jobs.
5. Plugin-specific evidence is stored as metadata, not as core state.

Plugins must not return SQLAlchemy models or domain entities directly.

## Browser Automation Flow

Recommended automation flow:

1. Application module verifies package readiness and approval.
2. Automation service starts a Playwright session.
3. ATS plugin supplies workflow actions or a workflow executor.
4. Automation service records steps, artifacts, and failures.
5. Application module updates application status through policy.

Automation plugins must support pausing when uncertainty is detected.

## Generic Plugin

A generic plugin should exist for unsupported career pages.

Capabilities:

- Basic career page detection.
- HTML job listing extraction.
- Link discovery.
- Heuristic job detail parsing.

Limitations:

- Lower confidence.
- More human review.
- No automated application submission by default.

## Plugin Registration

Use an explicit registry. Registration should capture:

- ATS type.
- Plugin instance or factory.
- Capability map.
- Detection priority.
- Version.

Avoid filesystem auto-loading for the first production version. Explicit registration is simpler, safer, and easier to test. Dynamic loading can be added later if a marketplace-style plugin system is needed.

## Error Handling

Plugin errors should be mapped to standard categories:

- Unsupported page.
- Detection inconclusive.
- Extraction failed.
- Structure changed.
- Authentication required.
- Rate limited.
- Automation blocked.
- Human review required.

Plugins should include evidence that helps maintainers update selectors or API parsing.

## Versioning

Plugin outputs should include plugin name and version. This allows:

- Debugging extraction regressions.
- Reprocessing jobs after plugin changes.
- Comparing output quality across versions.

## Testing

Each plugin should have:

- Unit tests for URL and HTML detection.
- Contract tests against stored fixtures.
- Extraction tests for representative job listings.
- Automation tests only where stable and safe.

Use captured fixtures rather than live ATS pages for most tests. Live smoke tests can be scheduled separately with rate limits.

