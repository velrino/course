# Pilot, Rollout, and Operations

## Learning objectives

Design a limited pilot, define go/no-go evidence, operate safely, and prepare rollback and retirement before release.

## A pilot tests the service

A pilot is not merely a smaller production launch. It tests user fit, workflow, data, controls, support, monitoring, and incident response in a bounded environment. Define who participates, what data and actions are allowed, how long it runs, what comparison exists, and what would stop it immediately.

Use synthetic data first, then shadow mode where the system produces recommendations without affecting outcomes. Move to assisted mode with explicit human action before considering narrower automation. Do not increase autonomy and user population simultaneously; changing one dimension at a time makes failures easier to attribute.

## Release evidence

Before a limited live release, require:

- approved scope, risk assessment, and data-flow diagram;
- versioned evaluation with quality and safety thresholds;
- access control, secret handling, and dependency inventory;
- monitoring, alerts, audit, and retention settings;
- human fallback and accessible user support;
- incident roles, kill switch, rollback, and restoration test;
- vendor outage, model change, and contract exit plans.

## Operating model

Name a service owner and on-call or support responsibilities. Define severity levels, response targets, communication templates, and post-incident learning. Monitor distribution shift, permission changes, source freshness, cost, latency, refusal, unsafe actions, reviewer overrides, and user complaints.

Retirement is an operation: disable credentials and triggers, export or delete required records, remove stale indexes, communicate alternatives, and verify that downstream integrations no longer call the system.

## Free local practice

Write a pilot protocol for a capstone with at most ten synthetic users and no real external side effects. Define baseline, duration, entry and exit criteria, five stop triggers, monitoring dashboard, incident drill, rollback command, and retirement checklist. Run one tabletop incident and revise the protocol.

## Completion criteria

- Scope, autonomy, users, data, and duration are bounded.
- Stop triggers and decision authority are explicit.
- Rollback and restoration have been tested.
- Vendor exit and final retirement remove active access.

## References

- [GOV.UK: How the beta phase works](https://www.gov.uk/service-manual/agile-delivery/how-the-beta-phase-works)
- [GOV.UK: How the live phase works](https://www.gov.uk/service-manual/agile-delivery/how-the-live-phase-works)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
