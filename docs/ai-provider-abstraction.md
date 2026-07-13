# AI Provider Abstraction

## Goals

The AI layer should let JobPilot AI use Ollama by default while allowing OpenAI-compatible providers later. Product use cases should depend on provider-neutral capabilities rather than provider SDKs.

## Provider Capabilities

The abstraction should represent capabilities, not vendors. Initial capabilities:

- Text generation.
- Structured JSON generation.
- Embedding generation if needed for matching or search.
- Model listing and health checks.
- Token or context estimation when available.

Future capabilities:

- Tool calling.
- Document understanding.
- Reranking.
- Multimodal inputs.

## Provider Interface Concepts

Provider-neutral request metadata should include:

- Capability requested.
- Model preference.
- System instructions.
- User content.
- Structured output schema when needed.
- Temperature or determinism settings.
- Timeout.
- Retry policy.
- Correlation ID.
- Safety classification.

Provider-neutral response metadata should include:

- Provider name.
- Model name.
- Request ID when available.
- Latency.
- Token counts when available.
- Finish reason.
- Raw provider metadata reference.
- Generated timestamp.

## Default Provider: Ollama

Ollama should be the default local provider.

Why:

- Works well for local Windows development through Docker or local runtime.
- Reduces external service dependency.
- Supports privacy-sensitive development with candidate data.

Constraints:

- Model availability depends on local installation.
- Performance varies by machine.
- Token accounting and structured output behavior may differ from hosted providers.

Design implication:

- The provider adapter must expose capability discovery and health checks.
- Application services should not assume a specific model is always available.

## Optional OpenAI-Compatible Providers

OpenAI-compatible adapters should be supported through the same provider interface.

Why:

- Production deployments may require stronger model quality or hosted reliability.
- Many providers expose OpenAI-compatible APIs.
- Switching should be configuration-driven, not use-case-driven.

Constraints:

- Privacy and data processing requirements must be reviewed.
- Costs and rate limits must be tracked.
- Provider-specific behavior should not leak into domain logic.

## Prompt Ownership

Prompts should be owned by application capabilities, not provider adapters.

Examples:

- Matching prompts belong to matching application services.
- Resume tailoring prompts belong to resume application services.
- Screening answer prompts belong to screening services.
- Provider adapters only translate provider-neutral requests.

Prompt templates should be versioned so generated artifacts can record which version produced them.

## Structured Output

For high-value workflows, prefer structured output with validation:

- Job normalization.
- Match explanations.
- Resume tailoring plan.
- Screening answer drafts.
- Interview preparation sections.

The application layer should validate provider output against schemas or domain policies before persisting it as trusted state.

## Provider Selection

Provider selection should be resolved by an AI provider router.

Selection inputs:

- Capability.
- Environment configuration.
- Candidate data sensitivity.
- Model availability.
- Cost policy.
- Latency requirement.
- Explicit user or operator preference.

Recommended default:

- Use Ollama for local development and privacy-sensitive workflows.
- Allow OpenAI-compatible providers for production-quality generation when configured.

## Testing

Use fake providers for unit tests. Fake providers should support deterministic responses and failure modes.

Use contract tests for real adapters:

- Health check.
- Text generation.
- Structured JSON generation.
- Timeout handling.
- Provider error mapping.

## Safety

AI outputs must be treated as untrusted until validated. The system should:

- Avoid fabricating candidate experience.
- Preserve truthful screening answers.
- Redact sensitive data from logs.
- Store generation metadata.
- Flag low-confidence outputs for review.
- Defend against prompt injection from job descriptions and career pages.

