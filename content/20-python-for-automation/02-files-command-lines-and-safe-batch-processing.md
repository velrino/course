# Files, Command Lines, and Safe Batch Processing

## Learning objectives

- Build a predictable command-line interface for batch automation.
- Process CSV/JSON/files with explicit encoding, validation, and atomic output.
- Add dry-run, idempotency, and path-safety controls.

## File automation is state management

Use `pathlib.Path` instead of assembling paths with string concatenation. Resolve an allowed root and reject inputs/outputs that escape it. Do not trust file extensions alone when security matters. Set text encoding explicitly, usually UTF-8, and use `newline=""` with the CSV module.

Never overwrite the only copy of an input. Write output to a temporary file in the same filesystem, flush and close it, then atomically replace the destination. For multi-file workflows, create a manifest that records input hashes, configuration, output hashes, status, and errors. On rerun, an idempotency rule decides whether to skip an identical completed item or produce a new version.

A usable CLI has help text, validated arguments, meaningful exit codes, logs on stderr, data on stdout where appropriate, and a `--dry-run` mode that shows planned changes without performing them. A dry run must execute the same discovery and validation paths as the real run; otherwise it provides false confidence.

For large inputs, stream rows rather than loading everything. Decide whether one invalid row fails the batch or moves to a quarantine file. Silent skipping is usually the worst choice.

## Free local practice

Extend `invoice_audit` with:

```text
invoice-audit INPUT.csv --output findings.jsonl
  [--dry-run] [--on-error fail|quarantine] [--force]
```

Use `argparse`, `csv.DictReader`, and `json`. Validate headers before rows. Stream findings to a temporary JSON Lines file. Calculate SHA-256 for the input and write a manifest beside the output. If the same hash/configuration already succeeded, exit successfully without duplicating work unless `--force` is supplied.

Create fixtures for empty file, missing header, invalid UTF-8, duplicate ID, quoted comma, very long field, partial old output, and a symlink/path traversal attempt. In dry run, print counts and intended destinations but create no result or manifest. Send malformed rows to a quarantine JSONL file with row number and error, never raw secrets.

## Completion criteria

- Help, exit codes, stderr/stdout behavior, and dry-run semantics are documented and tested.
- Output publication is atomic; a simulated exception leaves the prior output intact.
- Identical reruns are safe and recorded by hash/configuration.
- Invalid paths, encodings, schemas, and row policies have explicit behavior.

## References

- [argparse documentation](https://docs.python.org/3/library/argparse.html) - standard command-line parsing.
- [pathlib documentation](https://docs.python.org/3/library/pathlib.html) - object-oriented and safer path handling.
- [csv documentation](https://docs.python.org/3/library/csv.html) - dialects, quoting, and newline requirements.
- [json documentation](https://docs.python.org/3/library/json.html) - serialization limits and command-line validation.
- [Python tempfile documentation](https://docs.python.org/3/library/tempfile.html) - secure temporary files and directories.
