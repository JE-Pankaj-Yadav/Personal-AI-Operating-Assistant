# PA NEXUS V3 — PROVIDER AND ROUTING SPEC

## Provider lifecycle

UNCONFIGURED
→ CONFIGURED
→ TESTING
→ HEALTHY
or
→ UNHEALTHY

## Provider record

- id
- user_id
- company
- provider_type
- display_name
- model
- base_url
- encrypted credential reference
- priority
- enabled
- preferred
- capabilities
- health
- last_tested_at
- latency
- usage source

## Health

Health must never be inferred solely from a saved key.

A provider is healthy only after:
- a successful test;
- or a recent validated production request under defined policy.

## Routing

Candidate filters:
- enabled;
- credential configured;
- required capabilities;
- healthy/recently validated;
- quota available;
- context window sufficient.

Score:
- priority;
- health;
- capability;
- quota;
- latency;
- cost;
- quality preference.

## Exact/estimated usage

Every usage record:
- source;
- exact boolean;
- timestamp.

## Switching

Threshold is configurable.

Default:
80/90/95.

Before switch:
- create/update capsule;
- select candidate;
- health check;
- persist event;
- continue same conversation.

## Idempotency

Switch event must be idempotent.

Do not switch twice for one trigger.

## Failure

If switch fails:
- preserve message;
- preserve conversation;
- attempt allowed fallbacks;
- create alert;
- return actionable state.

## Transparency

UI always knows:
- active provider;
- active model;
- usage certainty;
- last switch;
- reason.

Never hide a switch.
