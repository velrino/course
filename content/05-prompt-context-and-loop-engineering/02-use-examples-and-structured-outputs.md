# Use Examples and Structured Outputs

## Learning objectives

By the end of this lesson, you will be able to:

- choose when zero-shot instructions are sufficient and when examples help;
- design representative few-shot examples without leaking answers;
- define and validate structured output; and
- test boundary, adversarial, and malformed cases.

## Examples communicate a decision boundary

Zero-shot prompting supplies instructions without demonstrations. Few-shot prompting includes example input-output pairs in context. Examples are valuable when a verbal rule leaves a decision boundary or format ambiguous.

Do not add examples merely because more context feels safer. Each example consumes space and can introduce accidental patterns. Select a small set covering:

- a normal positive case;
- a normal negative case;
- a boundary case;
- missing or malformed input; and
- a case where the system should abstain.

Use correct, independently reviewed outputs. A model can imitate mistakes and irrelevant correlations in demonstrations. Keep example labels separate from the real input so the expected answer is not leaked.

## Define data contracts precisely

"Return JSON" is incomplete. Define field names, types, required fields, allowed values, null behavior, nesting, and whether extra properties are permitted.

```json
{
  "type": "object",
  "properties": {
    "category": {"enum": ["billing", "technical", "other"]},
    "urgency": {"type": "integer", "minimum": 1, "maximum": 3},
    "evidence": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["category", "urgency", "evidence"],
  "additionalProperties": false
}
```

Native schema-constrained generation, when supported by a runtime, can improve syntactic and structural reliability. It still cannot guarantee that `category` is semantically correct or that evidence is truthful.

## Validate at the boundary

Treat model output as untrusted input:

1. parse using a real JSON parser;
2. validate against the schema;
3. check domain rules and authorization;
4. reject or repair through a bounded path; and
5. record the invalid case in the evaluation set.

Do not extract JSON from arbitrary prose with fragile string slicing when the runtime offers a structured response. Never execute generated code or queries merely because they parsed successfully.

## Free local practice

Save three candidate outputs to `outputs.jsonl`:

```jsonl
{"category":"technical","urgency":2,"evidence":["connection times out"]}
{"category":"sales","urgency":1,"evidence":[]}
{"category":"billing","urgency":"high","evidence":["charged twice"],"reply":"refund sent"}
```

Run a dependency-free validator:

```bash
python3 - <<'PY'
import json

allowed = {"billing", "technical", "other"}
required = {"category", "urgency", "evidence"}

for line_number, line in enumerate(open("outputs.jsonl"), 1):
    errors = []
    try:
        item = json.loads(line)
        if set(item) != required: errors.append("fields")
        if item.get("category") not in allowed: errors.append("category")
        if type(item.get("urgency")) is not int or item.get("urgency") not in range(1, 4): errors.append("urgency")
        if not isinstance(item.get("evidence"), list) or not all(isinstance(x, str) for x in item.get("evidence", [])): errors.append("evidence")
    except json.JSONDecodeError:
        errors.append("json")
    print(line_number, "PASS" if not errors else errors)
PY
```

Add malformed JSON, `null`, an empty object, and a valid structure with an unsupported claim. Note which failures structural validation cannot detect.

## Completion criteria

- [ ] Your examples cover normal, boundary, invalid, and abstention behavior.
- [ ] Expected answers are independently checked and not leaked into real inputs.
- [ ] The schema defines types, allowed values, required fields, and extra-field policy.
- [ ] You ran parsing and validation on at least seven cases.
- [ ] You distinguish structural validity from semantic correctness and authorization.

## References

- [Language Models Are Few-Shot Learners](https://arxiv.org/abs/2005.14165) - original GPT-3 paper studying zero-, one-, and few-shot task behavior from in-context demonstrations.
- [JSON Schema: Getting Started](https://json-schema.org/learn/getting-started-step-by-step) - free introduction to a standard vocabulary for validating JSON structure.
- [JSON Schema Specification](https://json-schema.org/specification) - normative and supporting documents for the standard.
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) - practical guidance for syntactic and semantic validation at trust boundaries.

## Continue

Next: [Engineer Context, Retrieval, and Memory](03-engineer-context-retrieval-and-memory.md)
