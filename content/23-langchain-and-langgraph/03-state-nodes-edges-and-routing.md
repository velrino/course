# State, Nodes, Edges, and Routing

## Learning objectives

Build a small deterministic LangGraph, reason about state ownership, and test branches before adding a model.

## Graph model

LangGraph represents a workflow with three core elements:

- **State** is the current application snapshot.
- **Nodes** perform computation or controlled side effects and return state updates.
- **Edges** choose the next node, either directly or conditionally.

Use the smallest state that supports decisions and audit. Do not copy entire database records or unlimited conversation history into every step. Name fields by domain meaning, define who may update each field, and distinguish input facts from derived decisions.

This model-free example routes an amount to approval:

```python
from typing import Literal, TypedDict
from langgraph.graph import END, START, StateGraph

class RequestState(TypedDict):
    amount: float
    route: str

def classify(state: RequestState):
    route = "review" if state["amount"] >= 500 else "automatic"
    return {"route": route}

def next_step(state: RequestState) -> Literal["review", "automatic"]:
    return state["route"]

builder = StateGraph(RequestState)
builder.add_node("classify", classify)
builder.add_node("review", lambda state: {})
builder.add_node("automatic", lambda state: {})
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", next_step)
builder.add_edge("review", END)
builder.add_edge("automatic", END)
graph = builder.compile()
```

Keeping the first graph deterministic makes routing errors visible. Add a model only to a node where language interpretation is necessary, and validate its output before an edge consumes it.

## State design rules

- Prefer identifiers over copied objects.
- Make status values an explicit finite set.
- Record errors as data when the graph must route on them.
- Keep sensitive values out unless a node truly needs them.
- Treat concurrent updates and retries as normal, not exceptional.

## Free local practice

Run the graph for amounts below, equal to, and above the threshold. Add a branch for invalid negative amounts and a terminal rejection node. Write unit tests for the routing function without compiling the graph. Finally, replace the amount example with a state model from your own case study.

## Completion criteria

- The graph runs without an LLM.
- Every branch has at least one test.
- State fields have clear ownership and bounded size.
- Invalid state reaches a safe terminal outcome.

## References

- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [LangGraph: Use the Graph API](https://docs.langchain.com/oss/python/langgraph/use-graph-api)
- [LangGraph install guide](https://docs.langchain.com/oss/python/langgraph/install)
