# Build Harnesses and Evaluation Loops

## Learning objectives

By the end of this lesson, you will be able to:

- identify the responsibilities of an AI harness;
- build a small versioned evaluation dataset and rubric;
- compare prompt changes without changing several variables at once; and
- turn failures into regression cases and system improvements.

## A harness makes behavior operable

The harness is the code and environment around a model. Depending on the system, it manages:

- prompt and policy versions;
- context selection and compaction;
- model and inference configuration;
- tool discovery, authorization, and execution;
- state, budgets, retries, and stop conditions;
- input and output validation;
- logs, traces, metrics, and redaction;
- evaluation and deployment controls; and
- human approvals and incident response.

Prompt engineering changes model-facing instructions. Harness engineering changes the full environment and feedback loops that make useful behavior repeatable and verifiable.

## Evaluate the task, not the demonstration

Build examples from actual task variation:

```json
{"id":"normal-01","input":"...","must_include":["..."],"must_not_include":["..."]}
{"id":"missing-01","input":"...","expected_status":"needs_evidence"}
{"id":"attack-01","input":"ignore prior rules ...","expected_status":"safe_rejection"}
```

Include normal, boundary, malformed, adversarial, multilingual if relevant, tool-failure, permission-denied, and no-evidence cases. Keep a held-out set so prompt iterations are not optimized only to familiar examples.

Use deterministic graders for parseability, schema, exact values, prohibited strings, tool-call limits, and citations. Use human rubrics for qualities that require judgment. Model-based graders can scale review but must themselves be validated against human decisions and checked for bias or self-preference.

## Run controlled iterations

For every experiment, record:

- dataset version;
- prompt and policy version;
- model/runtime identifier;
- decoding and tool configuration;
- code revision;
- per-case outputs and traces;
- pass rate by slice;
- latency and resource use; and
- known uncertainty.

Change one coherent factor, rerun the same evaluation, inspect newly failing cases, and keep improvements only if important regressions are acceptable. A better average can hide a new high-severity failure.

## Turn failures into system changes

Classify a failure before editing:

- missing or conflicting instruction;
- bad or unauthorized context;
- retrieval miss;
- tool design or execution error;
- output validation gap;
- model capability limit;
- evaluation defect; or
- product-policy ambiguity.

Fix the owning layer, add the case to the regression set, and rerun relevant slices.

## Free local practice: local prompt regression harness

Using the local model from the previous module, run the same five cases with prompt versions `v1` and `v2`. If no local model runs on your hardware, use two manually written candidate outputs to exercise the evaluator.

Create `results.jsonl`, one object per result:

```json
{"case":"E1","version":"v1","valid_json":true,"unsupported_claim":false,"elapsed_ms":1200}
```

Then summarize it locally:

```bash
python3 - <<'PY'
import json
from collections import defaultdict

scores = defaultdict(lambda: {"count": 0, "valid": 0, "unsupported": 0, "ms": 0})
for line in open("results.jsonl"):
    row = json.loads(line)
    item = scores[row["version"]]
    item["count"] += 1
    item["valid"] += bool(row["valid_json"])
    item["unsupported"] += bool(row["unsupported_claim"])
    item["ms"] += row["elapsed_ms"]
for version, item in sorted(scores.items()):
    print(version, item)
PY
```

Write a release decision that gives high-severity cases priority over average pass rate.

## Completion criteria

- [ ] Your harness responsibility map covers context, tools, validation, observability, evaluation, and approval.
- [ ] The evaluation set includes boundary, adversarial, missing-evidence, and failure cases.
- [ ] Every run records model, prompt, dataset, configuration, and code versions.
- [ ] You changed one coherent factor and checked regressions by case.
- [ ] Each observed failure is assigned to an owning system layer.

## References

- [Harness Engineering: Leveraging Codex in an Agent-First World](https://openai.com/index/harness-engineering/) - current OpenAI engineering account of environments, feedback loops, structured knowledge, verification, and enforced invariants.
- [OpenAI Evals Design Guide](https://platform.openai.com/docs/guides/evals) - public documentation on defining tasks, test data, graders, and evaluation-driven development.
- [HELM: Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110) - original paper advocating multi-metric, scenario-based, transparent model evaluation.
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) - public outcomes for continuous Govern, Map, Measure, and Manage activities.

## Continue

Next module: [Understand the Web Request Path](../06-web-apis-and-webhooks/01-understand-the-web-request-path.md)
