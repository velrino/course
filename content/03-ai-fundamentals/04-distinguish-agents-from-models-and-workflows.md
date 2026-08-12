# Distinguish Agents from Models and Workflows

## Learning objectives

By the end of this lesson, you will be able to:

- separate a model, agent, tool, workflow, and environment;
- identify observations, actions, state, objectives, and stop conditions;
- choose an appropriate level of autonomy; and
- storyboard an agent interaction including failures and human control.

## A model is a component; an agent is a system

A model maps input to output. An **agent** operates in an environment over time: it observes state, selects actions toward an objective, receives new observations, and repeats until a stop condition. A language model can help choose actions, but the agent also needs a harness that manages tools, state, permissions, errors, budgets, and human interaction.

Useful distinctions:

- **Tool:** a bounded operation with a defined input and output, such as `get_order`.
- **Workflow:** a mostly predetermined sequence or graph of steps.
- **Agent:** selects some next steps dynamically from observations.
- **Environment:** systems and information affected or observed.
- **State:** information retained across steps.

An agent is not automatically better than a workflow. If the path and failure handling are known, an explicit workflow is easier to test and govern.

## Sensors, actuators, objectives

Classic agent language remains useful:

- **sensors/observations:** messages, files, API responses, clock, database results;
- **actuators/actions:** calls to tools that read, create, update, send, or delete;
- **objective:** the desired outcome and quality constraints;
- **policy:** how the next action is selected; and
- **environment:** everything outside the policy that supplies consequences.

"Resolve customer tickets" is not enough. Specify what counts as resolved, what must never happen, the allowed tools, maximum attempts and cost, and when a person must decide.

## Use an autonomy ladder

Choose the lowest level that meets the need:

1. model produces information only;
2. system proposes an action;
3. system acts after per-action approval;
4. system acts within narrow, reversible bounds and reports;
5. system acts more broadly with monitoring and emergency controls.

High-impact, irreversible, financial, legal, safety, or external-communication actions need stronger authorization and human oversight. Approval must show what will happen, on which target, using what data. A generic "allow" prompt is weak control.

## Storyboard normal and abnormal paths

For each frame, record:

```text
Observation -> internal state -> proposed action -> authorization -> tool result -> user-visible outcome
```

Include malformed input, unavailable tools, permission denial, conflicting instructions, repeated failure, duplicate requests, and user cancellation. Define terminal states such as `completed`, `needs_human`, `budget_exhausted`, and `failed_safely`.

## Free local practice

Storyboard a study-planning assistant. Its tools are only:

- `list_topics()` - read-only;
- `record_review(topic, score)` - changes local data; and
- `delete_history()` - irreversible.

Create eight frames covering a successful session. Then add:

- an invalid score;
- a missing topic;
- a repeated `record_review` call;
- a request to delete history; and
- a tool timeout.

For each action, mark whether it can run automatically, requires confirmation, or must be prohibited. Write exact stop conditions.

## Completion criteria

- [ ] You distinguish a model, workflow, tool, agent, and environment.
- [ ] Your storyboard includes observations, actions, state, and objectives.
- [ ] Every action has an autonomy level and authorization rule.
- [ ] You modeled at least four failure paths.
- [ ] The agent has bounded attempts and explicit terminal states.

## References

- [Artificial Intelligence: A Modern Approach, Chapter 2 slides](https://aima.cs.berkeley.edu/slides-pdf/chapter02.pdf) - public companion material on intelligent agents, environments, sensors, actuators, and rational behavior.
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) - original paper describing interleaved model reasoning and actions against external environments.
- [People + AI Guidebook: Feedback and Control](https://pair.withgoogle.com/guidebook-v2/chapter/feedback-controls/) - public design guidance for meaningful user control in AI-enabled systems.
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) - lifecycle outcomes organized under Govern, Map, Measure, and Manage.

## Continue

Next: [Use AI Responsibly and Critically](05-use-ai-responsibly-and-critically.md)
