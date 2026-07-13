# Database Design

## Database Choice

Use PostgreSQL as the system of record. SQLAlchemy 2.x should be used for ORM mapping and query construction. Alembic should manage schema migrations.

PostgreSQL is appropriate because JobPilot AI needs relational integrity, transactional updates, JSON support for external payloads, full-text search options, and mature operational tooling.

## Persistence Principles

- Keep domain entities independent from SQLAlchemy models.
- Use repositories to map between domain objects and persistence models.
- Use explicit transactions through a unit-of-work abstraction.
- Prefer normalized relational tables for core business state.
- Use JSONB for external raw payloads, provider metadata, plugin-specific evidence, and semi-structured artifacts.
- Store large binary files outside primary tables when possible and keep database rows as metadata.

## Conceptual Tables

### Companies

Purpose:

- Store canonical company identity and registry metadata.

Key fields:

- Stable internal ID.
- Canonical name.
- Display name.
- Website domain.
- Description.
- Status.
- Created and updated timestamps.

### Company Domains

Purpose:

- Track known domains, aliases, and career-related subdomains.

Key fields:

- Company ID.
- Domain.
- Domain type.
- Verification status.

### Career Pages

Purpose:

- Store discovered career URLs and scan state.

Key fields:

- Company ID.
- URL.
- Page type.
- Discovery source.
- Confidence score.
- Reachability status.
- Last scanned timestamp.

### ATS Detections

Purpose:

- Store detected ATS platform and evidence.

Key fields:

- Company ID.
- Career page ID.
- ATS type.
- Confidence score.
- Detection evidence as JSONB.
- Plugin name.
- Capability flags.

### Job Postings

Purpose:

- Store source-specific and normalized job records.

Key fields:

- Company ID.
- Career page ID.
- Source URL.
- External ID.
- Source payload JSONB.
- Normalized fields.
- Status.
- First seen and last seen timestamps.
- Content hash.

Recommended uniqueness:

- Company plus external ID when external ID exists.
- Company plus source URL.
- Content hash as a secondary duplicate signal.

### Candidates

Purpose:

- Store candidate profile metadata and preferences.

Key fields:

- User ID or candidate owner.
- Profile status.
- Location preferences.
- Target roles.
- Work authorization metadata.
- Preference JSONB.

### Resume Records

Purpose:

- Store resume metadata, parsed facts, and generated variants.

Key fields:

- Candidate ID.
- Resume type.
- Source resume ID for variants.
- Target job ID for tailored resumes.
- Storage reference.
- Parsed facts JSONB.
- Generation metadata JSONB.

### Job Matches

Purpose:

- Store candidate-job match outcomes.

Key fields:

- Candidate ID.
- Job ID.
- Score.
- Recommendation.
- Criteria breakdown JSONB.
- Provider metadata JSONB.
- Generated timestamp.

### Screening Question Sets

Purpose:

- Store screening questions and generated answers.

Key fields:

- Candidate ID.
- Job ID.
- Application ID when available.
- Questions JSONB.
- Answers JSONB.
- Review status.
- Provider metadata JSONB.

### Applications

Purpose:

- Store application lifecycle state.

Key fields:

- Candidate ID.
- Job ID.
- Status.
- Selected resume ID.
- Screening question set ID.
- Submission URL.
- Submitted timestamp.
- Status reason.

Recommended uniqueness:

- Candidate plus job should usually be unique unless multiple application attempts are explicitly supported.

### Automation Runs

Purpose:

- Store browser automation execution history.

Key fields:

- Application ID.
- Workflow type.
- ATS plugin name.
- Status.
- Started and completed timestamps.
- Step log JSONB.
- Artifact references JSONB.
- Error category.
- Retry count.

### Pipeline Runs

Purpose:

- Store durable multi-stage work.

Key fields:

- Pipeline type.
- Status.
- Idempotency key.
- Current stage.
- Input JSONB.
- Output JSONB.
- Error metadata JSONB.
- Started and completed timestamps.

### Artifacts

Purpose:

- Store metadata about generated or captured artifacts.

Key fields:

- Artifact type.
- Owner type and owner ID.
- Storage reference.
- MIME type.
- Sensitivity classification.
- Retention policy.
- Created timestamp.

### Audit Events

Purpose:

- Store significant system and user-visible events.

Key fields:

- Actor ID.
- Event type.
- Entity type.
- Entity ID.
- Correlation ID.
- Metadata JSONB.
- Created timestamp.

## Indexing Strategy

Recommended indexes:

- Company canonical name and domain.
- Career page company ID and URL.
- ATS detection company ID and ATS type.
- Job company ID, status, external ID, source URL, content hash, and last seen timestamp.
- Candidate owner ID.
- Job match candidate ID plus score.
- Application candidate ID plus status.
- Pipeline status plus created timestamp.
- Automation run application ID plus status.
- Audit event entity and timestamp.

Use PostgreSQL full-text search or a dedicated search service later if job search becomes a primary product surface.

## JSONB Use

Use JSONB for data that is:

- Provider-specific.
- ATS-specific.
- Semi-structured.
- Useful for audit or debugging.
- Not heavily filtered by core queries.

Do not hide core business state in JSONB if it is frequently queried, joined, validated, or indexed.

## Migration Policy

Alembic migrations should be:

- Small.
- Reversible when practical.
- Reviewed with data migration risk in mind.
- Paired with compatibility changes for deployed services.

Production migrations should avoid long blocking locks. Backfills should be staged for large tables.

## Data Retention

Define retention separately for:

- Raw HTML snapshots.
- Browser screenshots.
- LLM prompts and responses.
- Resume artifacts.
- Audit events.
- Pipeline logs.

Sensitive candidate data should have explicit deletion and export workflows before production launch.

