# Testing, Logging, and Automation Capstone

## Learning objectives

- Test decision logic, adapters, failure paths, and command-line behavior.
- Produce structured, privacy-aware operational logs.
- Deliver a resumable end-to-end automation with a runbook.

## Test the properties that make automation trustworthy

Unit-test pure functions with small explicit examples. Test adapters at their boundary using temporary directories, mock HTTP transports, and temporary databases. Contract tests verify assumptions about an external schema. End-to-end tests execute the CLI in an isolated workspace. Include negative cases: timeouts, invalid records, disk failure, interruption, duplicate run, expired credential, and partial remote response.

Avoid mocks that merely repeat implementation details. Assert observable outcomes and invariants: no output published on failure, one side effect per idempotency key, checkpoint after commit, no secret in logs, and stable exit-code categories. Use property-based testing optionally for parsers and invariants.

Use the standard `logging` module or a structured wrapper. Include timestamp, level, event name, run/trace ID, item ID, component, duration, status, and safe error class. Keep human message and machine fields separate. Redact credentials and minimize personal content. Logs should answer what happened without becoming a second uncontrolled dataset.

## Free local practice

Finish `invoice_audit` as a scheduled-style workflow:

1. discover CSV inputs under an allowed root;
2. validate and audit rows;
3. optionally enrich product codes through the local mock API;
4. atomically publish JSONL findings and a manifest;
5. checkpoint per input hash in SQLite;
6. quarantine bad rows and retry only transient API failures;
7. expose `--dry-run`, `--resume`, and bounded concurrency.

Write pytest coverage for domain rules, malformed CSV, path escape, atomic publication, HTTP timeout/429, token redaction, duplicate rerun, crash/resume, and two concurrent runners. Use `tmp_path`, `monkeypatch`, and a mock transport. Add a `pyproject.toml` test dependency group and a single test command.

Create a runbook covering setup, configuration, input/output contract, exit codes, scheduling, log location, retry/quarantine handling, safe replay, credential rotation, rollback, and deletion. Run the capstone twice and after a simulated crash; compare hashes and audit events.

## Completion criteria

- Tests cover business rules, boundaries, failures, security controls, and recovery.
- Logs correlate a run without exposing fixture secrets or unnecessary record content.
- Fresh, repeated, concurrent, and resumed executions have documented deterministic outcomes.
- Another person can operate and recover the job from the runbook alone.

## References

- [pytest documentation](https://docs.pytest.org/en/stable/) - fixtures, parametrization, assertions, and command-line testing.
- [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) - safely replacing environment, functions, and paths in tests.
- [Python logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html) - structured context, handlers, and production patterns.
- [Hypothesis documentation](https://hypothesis.readthedocs.io/en/latest/) - optional property-based testing for generated edge cases.
- [Python dependency groups specification](https://packaging.python.org/en/latest/specifications/dependency-groups/) - standardized development/test dependency declaration.
