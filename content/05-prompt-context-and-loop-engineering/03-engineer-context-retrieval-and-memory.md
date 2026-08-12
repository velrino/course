# Engineer Context, Retrieval, and Memory

## Learning objectives

By the end of this lesson, you will be able to:

- distinguish model parameters, request context, retrieval, and application memory;
- allocate a context budget by relevance and provenance;
- design a basic retrieval pipeline with citations; and
- compact long sessions without silently changing requirements.

## Context engineering is selection and control

The context presented for one model call may contain system instructions, user messages, examples, retrieved passages, tool definitions, tool results, and prior conversation. More is not automatically better. Context competes for a finite window, affects latency and cost, and can contain conflicting or hostile text.

Separate four mechanisms:

- **parametric knowledge:** patterns represented in trained weights;
- **request context:** tokens supplied for this call;
- **retrieval:** selecting external items relevant to the current need; and
- **memory:** application-managed state saved and reintroduced later.

A chat product saying "I remember" does not reveal which mechanism was used.

## Budget context deliberately

Reserve space for:

```text
stable instructions
current user task
authoritative evidence
relevant tool definitions and results
compact state summary
output allowance
safety margin
```

Rank candidate context by authority, relevance, freshness, sensitivity, and token cost. Remove duplicates and stale material. Keep critical constraints close to the task and test placement: research shows models can use long input unevenly, including degraded use of information in the middle.

## Retrieval is a pipeline

A minimal retrieval-augmented generation pipeline:

1. ingest approved sources and record provenance;
2. split them into meaningful chunks;
3. create searchable representations;
4. retrieve candidates for a query;
5. optionally rerank and filter by permissions or freshness;
6. provide selected passages with stable identifiers; and
7. require the answer to cite supporting identifiers.

Evaluate retrieval separately from generation. If the needed passage was not returned, rewriting the answer prompt cannot recover it. Measure whether relevant evidence appears in top results and whether irrelevant or unauthorized evidence leaks in.

## Memory needs policy

Do not append an entire conversation forever. Maintain an explicit state object:

```json
{
  "goal": "classify support tickets",
  "confirmed_constraints": ["no automatic refunds"],
  "decisions": [{"id":"D1","value":"three categories","source":"user"}],
  "open_questions": ["Which timezone defines business hours?"],
  "completed_steps": ["schema drafted"]
}
```

When compacting, preserve source and distinguish facts, user decisions, model proposals, and unresolved assumptions. Let users inspect, correct, and delete persistent memory. Do not store secrets or personal information without purpose and policy.

## Free local practice

Take any three short public documents already on your device. Assign IDs `D1`, `D2`, and `D3` and split each into paragraph-sized chunks.

For the query "What evidence supports the action limit?" create a table with:

- chunk ID;
- exact supporting sentence;
- source authority;
- freshness;
- relevance from 0 to 3;
- sensitivity; and
- include or exclude decision.

Compose a context packet capped at 300 words. Answer using only that packet and cite chunk IDs. Then delete the best chunk and confirm that the correct behavior changes to abstention.

## Completion criteria

- [ ] You distinguish parameters, context, retrieval, and memory.
- [ ] Your context budget reserves output and safety margin.
- [ ] Every retrieved chunk has source identity and an access decision.
- [ ] You tested a missing-evidence case that requires abstention.
- [ ] Your state summary separates confirmed facts from proposals and open questions.

## References

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) - original RAG paper combining parametric generation with retrieved non-parametric memory.
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) - original study showing that long-context models can use information differently depending on position.
- [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) - current engineering account emphasizing structured, repository-local context and progressive disclosure rather than one giant instruction document.
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework) - public framework for managing privacy risk when collecting and retaining context or memory.

## Continue

Next: [Design Bounded Tool and Human Loops](04-design-bounded-tool-and-human-loops.md)
