# JobPilot AI Architecture

## Purpose

JobPilot AI is an AI-powered recruitment automation platform that discovers company career pages, detects applicant tracking systems, extracts and normalizes jobs, matches jobs against candidate profiles, supports resume tailoring, generates screening answers, automates browser workflows, tracks applications, and prepares candidates for interviews.

This document defines the target production architecture. It is intentionally implementation-free: it describes responsibilities, boundaries, dependencies, and trade-offs so implementation can proceed consistently.

## Architectural Style

JobPilot AI should use Clean Architecture with explicit boundaries between:

- Domain model: business concepts and rules that do not depend on frameworks.
- Application services: use cases, orchestration, transactions, and policies.
- Infrastructure adapters: database, browser automation, AI providers, ATS integrations, queues, file storage, and external APIs.
- Interface adapters: HTTP API, CLI tools, scheduled workers, and future React dashboard integration.

Dependencies must point inward. Domain code must not import FastAPI, SQLAlchemy, Playwright, provider SDKs, Docker concerns, or framework-specific configuration.

## High-Level Components

The system is organized around these components:

- API service: FastAPI application exposing authenticated use cases to clients and the future dashboard.
- Worker service: background execution for discovery, extraction, matching, resume tailoring, browser automation, and interview preparation.
- Scheduler: periodic dispatch for company scans, job refreshes, stale application checks, and provider health probes.
- Domain modules: company, career discovery, ATS detection, jobs, candidates, matching, resumes, applications, interviews, automation, and AI.
- Persistence layer: PostgreSQL via SQLAlchemy 2.x repositories and Alembic migrations.
- AI provider layer: provider-neutral interface with Ollama as the default provider and optional OpenAI-compatible adapters.
- ATS plugin layer: plugin registry and contract for ATS-specific discovery, extraction, and application workflows.
- Browser automation layer: Playwright-based workflow execution isolated behind automation service interfaces.
- Observability layer: structured logging, metrics, traces, audit events, and run history.

## Runtime Topology

The initial Docker Compose topology should eventually include:

- `api`: FastAPI process for synchronous request handling.
- `worker`: background worker process for long-running jobs.
- `scheduler`: lightweight process responsible for enqueueing planned work.
- `postgres`: primary relational database.
- `ollama`: local LLM runtime and default AI provider.
- Optional `frontend`: future React dashboard.

The API must not directly perform long-running browser automation or LLM-heavy batch processing. It should create commands, persist requested work, and return status. Workers should execute durable tasks.

## Request Flow

Typical synchronous API flow:

1. Client sends a request to the FastAPI API.
2. Interface layer validates request shape and authentication.
3. Application service executes a use case.
4. Use case calls domain services and repository interfaces.
5. Infrastructure repositories persist state through SQLAlchemy.
6. API returns a DTO, not database models or domain internals.

Typical asynchronous pipeline flow:

1. API, scheduler, or operator creates a pipeline run.
2. Worker claims pending work.
3. Application pipeline orchestrator executes stages.
4. Stages call domain services, ATS plugins, browser automation, and AI providers through interfaces.
5. Each stage records status, artifacts, errors, retry metadata, and audit events.

## Core Design Decisions

### Use Modular Monolith First

Chosen approach: start as a modular monolith with separate deployable API, worker, and scheduler processes sharing one codebase and one PostgreSQL database.

Why:

- The product domain is still evolving.
- Strong module boundaries can be enforced without operational overhead from microservices.
- Transactions across related recruitment entities are easier to reason about.
- Local Windows development with Docker Compose remains straightforward.

Alternative: microservices from the beginning. This increases deployment and observability complexity before module responsibilities are stable.

### Use Repository and Unit-of-Work Boundaries

Application services should depend on repository interfaces and a unit-of-work abstraction. SQLAlchemy implementations belong in infrastructure.

Why:

- Tests can use fakes without requiring PostgreSQL.
- Transaction boundaries are explicit.
- Domain rules remain persistence-independent.

Alternative: pass SQLAlchemy sessions through application and domain layers. This is simpler early but leaks persistence details into the core.

### Use Plugin-Based ATS Integrations

ATS integrations should be implemented as plugins behind a stable contract.

Why:

- ATS behavior varies widely.
- New ATS support can be added without changing core discovery and job logic.
- Fallback generic extraction remains available when no plugin matches.

Alternative: hard-code conditionals in extraction services. This becomes brittle as supported ATS count grows.

### Use Provider Abstraction for AI

The system should define provider-neutral AI capabilities, with Ollama as the default adapter and OpenAI-compatible providers as optional adapters.

Why:

- Local-first development works without cloud dependency.
- Provider changes do not rewrite use cases.
- Tests can use deterministic fake providers.

Alternative: call Ollama directly from use cases. This is fast initially but blocks portability and testability.

## Cross-Cutting Concerns

### Logging

Use structured logs with consistent fields:

- `request_id`
- `correlation_id`
- `actor_id`
- `pipeline_run_id`
- `task_id`
- `company_id`
- `job_id`
- `provider`
- `ats_type`
- `duration_ms`
- `status`

Logs must avoid storing full resumes, secrets, access tokens, or unredacted LLM prompts containing sensitive personal data.

### Errors

Use typed application errors. Distinguish:

- Validation errors.
- Not found errors.
- Permission errors.
- Provider errors.
- Browser automation errors.
- ATS extraction errors.
- Retryable infrastructure errors.
- Non-retryable domain errors.

### Configuration

Configuration should be loaded at process startup from environment variables and validated once. Application code should receive typed settings through dependency injection rather than reading environment variables directly.

### Security

Security concerns include:

- Secrets management.
- Provider API keys.
- User authentication.
- Row-level ownership checks.
- Prompt injection defenses.
- Browser automation sandboxing.
- Sensitive artifact retention.
- Audit history for user-visible actions.

### Data Privacy

Resumes, candidate profiles, generated answers, and interview notes are sensitive. Store only what is needed, encrypt secrets, redact logs, and define retention policies before production launch.

## Evolution Path

The architecture should support these phases:

1. Local prototype: single developer, local PostgreSQL, local Ollama, manual pipeline runs.
2. Private beta: authenticated API, durable workers, observability, selected ATS plugins.
3. Production launch: managed PostgreSQL, backups, secret manager, monitoring, rate limits, user dashboard.
4. Scale-out: horizontal workers, queue-backed pipelines, plugin marketplace-style registration, multi-tenant controls.

