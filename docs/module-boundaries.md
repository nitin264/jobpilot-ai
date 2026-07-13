# Module Boundaries

## Boundary Philosophy

Modules should own business capabilities, not technical layers alone. Each domain module may have domain, application, infrastructure, and API pieces, but dependency direction must still follow Clean Architecture.

## Core Modules

### Companies

Owns:

- Company registry.
- Company identity and canonical naming.
- Company domains.
- Company lifecycle metadata.

Does not own:

- Job extraction.
- ATS-specific scraping.
- Candidate matching.

Collaborates with discovery to find career pages.

### Discovery

Owns:

- Career page search strategy.
- URL candidate evaluation.
- Reachability checks.
- Discovery confidence scoring.

Does not own:

- ATS parsing details.
- Job normalization.

Collaborates with ATS detection and browser automation.

### ATS

Owns:

- ATS type detection.
- Plugin contracts.
- Plugin registry.
- ATS capability reporting.

Does not own:

- Core job matching.
- Candidate data.
- Application lifecycle status.

Collaborates with jobs and automation.

### Jobs

Owns:

- Raw job capture.
- Normalized job representation.
- Duplicate detection.
- Freshness and status.

Does not own:

- Candidate-specific scoring.
- Resume tailoring.
- Browser submission.

Collaborates with ATS, matching, and applications.

### Candidates

Owns:

- Candidate profile.
- Preferences.
- Skills and experience facts.
- User-owned job search criteria.

Does not own:

- Job extraction.
- ATS plugins.

Collaborates with matching, resumes, screening, and interviews.

### Matching

Owns:

- Fit evaluation between candidate and job.
- Match explanations.
- Matching strategies.
- Score recalculation policy.

Does not own:

- Candidate profile storage.
- Job extraction.
- Resume generation.

Collaborates with AI providers through application interfaces.

### Resumes

Owns:

- Resume metadata.
- Resume parsing results.
- Tailored resume variants.
- Resume-to-job tailoring policy.

Does not own:

- Application status transitions.
- Screening questions.

Collaborates with AI providers and applications.

### Screening

Owns:

- Screening question detection.
- Candidate-specific answer generation.
- Review status of generated answers.

Does not own:

- Browser form submission.
- Resume document storage.

Collaborates with AI providers and applications.

### Applications

Owns:

- Application lifecycle.
- Application package readiness.
- Submission state.
- Manual and automated action history.

Does not own:

- Browser automation implementation.
- ATS plugin internals.
- Job extraction.

Collaborates with automation, resumes, screening, and interviews.

### Automation

Owns:

- Browser workflow execution abstraction.
- Run history.
- Step outcomes.
- Safety and approval policy.

Does not own:

- Application business status policy.
- ATS extraction semantics.

Collaborates with ATS plugins and applications.

### AI

Owns:

- Provider-neutral generation contracts.
- Prompt template ownership rules.
- Provider metadata.
- Safety and retry policies.

Does not own:

- Domain-specific matching or resume decisions.

Collaborates with matching, resumes, screening, and interviews.

### Interviews

Owns:

- Interview prep generation.
- Company and job research synthesis.
- Candidate-specific talking points.

Does not own:

- Application lifecycle.
- Job extraction.

Collaborates with AI, jobs, candidates, and applications.

## Boundary Enforcement

Use these enforcement mechanisms:

- Import linting once the codebase exists.
- Module-level public contracts.
- Contract tests for provider and plugin interfaces.
- Narrow DTOs between API and application layers.
- Repository interfaces in application or domain-adjacent ports.
- Code review checklist focused on dependency direction.

## Shared Data Rules

Modules should not share mutable persistence models as their main integration mechanism. Instead:

- Read data through repositories or query services.
- Change another module's state through application use cases.
- Communicate meaningful changes through domain events.
- Keep internal module data structures private unless explicitly declared as public contracts.

## Transaction Boundaries

Use cases should define transaction boundaries. Avoid transactions that span slow operations such as:

- LLM generation.
- Browser automation.
- Network discovery.
- ATS page scraping.

Recommended pattern:

1. Persist intent or pending run.
2. Commit.
3. Perform external operation.
4. Persist result with idempotency key.

## Anti-Corruption Layers

External systems should be isolated behind anti-corruption layers:

- ATS plugins convert ATS-specific data into JobPilot AI job extraction DTOs.
- AI provider adapters convert provider responses into provider-neutral result objects.
- Browser automation converts Playwright steps into workflow events and artifacts.

