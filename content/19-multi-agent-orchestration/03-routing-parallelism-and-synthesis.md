# Routing, Parallelism, and Synthesis

## Learning objectives

- Implement deterministic routing before model-based routing.
- Run independent workers concurrently with bounded resource use.
- Synthesize evidence while retaining disagreement and provenance.

## Routing is a decision with a fallback

Use rules when categories are stable and observable: file type, authenticated role, language setting, or explicit command. Use a classifier when wording is ambiguous, but constrain its output to known routes and include `unknown`. Record the router version and confidence/evidence. A failed classifier must not default to the most privileged worker.

Parallelism helps independent work, such as searching different approved sources. It hurts when workers depend on each other's results or share a rate-limited side effect. Bound concurrency, set per-worker and global deadlines, cancel work that no longer matters, and decide whether partial results are acceptable.

Synthesis is not concatenation. Normalize worker results, validate citations, group claims, surface conflicts, rank evidence by authority/freshness, and state missing coverage. A synthesizer must not turn two uncertain opinions into a fact. Where a deterministic reducer can combine numbers or deduplicate sources, use code.

## Free local practice

Implement an asynchronous Python orchestrator with three fake workers: policy search, technical documentation search, and citation verification. Use `asyncio.TaskGroup` (Python 3.11+) and `asyncio.timeout`. Each worker sleeps for a seeded random duration and returns structured claims, sometimes failing or disagreeing.

The router uses explicit keywords first and returns `unknown` otherwise. Fan out only the required workers. Limit concurrent external calls with `asyncio.Semaphore(2)`. Give each worker a timeout and the whole task a stricter global budget. Store start, finish, cancellation, and result events.

Write a reducer that:

1. rejects malformed records;
2. canonicalizes and deduplicates URLs;
3. groups identical normalized claims;
4. preserves contradictory claims and sources;
5. returns `partial` when a required worker failed;
6. never invents a citation.

Test all-success, one timeout, global timeout, unknown route, conflicting claims, and duplicate sources. Compare sequential and parallel elapsed time, but also verify that concurrency never exceeds two.

## Completion criteria

- Routing has a safe `unknown` path and no privileged default.
- Worker/global deadlines, cancellation, and concurrency limits are tested.
- Partial and conflicting results are explicit in the final structured output.
- Every synthesized claim retains its originating worker and source IDs.

## References

- [Python asyncio task groups](https://docs.python.org/3/library/asyncio-task.html#task-groups) - structured concurrency and cancellation behavior.
- [LangGraph parallel execution](https://docs.langchain.com/oss/python/langgraph/use-graph-api#run-graph-nodes-in-parallel) - graph fan-out and reducer patterns.
- [LangChain router documentation](https://docs.langchain.com/oss/python/langchain/multi-agent/router) - single-route and parallel multi-route designs.
- [AutoGen Selector Group Chat](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/selector-group-chat.html) - model-selected speakers, termination, and team state.
