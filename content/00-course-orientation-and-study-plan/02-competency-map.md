# Competency Map

## Objectives

Use this map to understand dependencies, choose an entry point, and identify the evidence expected at each stage.

## Five stages

### Stage 1: Foundations

Modules 01-08 cover learning methods, digital systems, AI and LLM concepts, context engineering, HTTP, containers, and MCP. Completion evidence is a set of small local experiments: an HTTP request, a containerized service, a structured prompt test, and an MCP architecture diagram.

### Stage 2: Automation design

Modules 09-14 move from business process discovery to implementation. You will prioritize opportunities, define success and risk, express logic as algorithms, build n8n workflows, integrate APIs, and separate deterministic workflow steps from agent decisions.

### Stage 3: Reliable agent systems

Modules 15-19 cover retrieval, memory, multimodal inputs, human approval, security, evaluation, and multi-agent coordination. The central competency is not making a demo answer once; it is controlling what the system may do, measuring how often it succeeds, and recovering safely when it fails.

### Stage 4: Code and data

Modules 20-25 add Python, SQL, analysis, LangChain, LangGraph, CrewAI, and model adaptation. Module 29 adds a parallel Node.js automation path. These modules let you inspect and test behavior that no-code tools may conceal. Fine-tuning comes last because many apparent model problems are actually data, retrieval, tool, context, or evaluation problems.

### Stage 5: Responsible delivery

Modules 26-28 integrate ethics, governance, impact assessment, project delivery, adoption, and capstones. Completion evidence includes a risk register, system card, evaluation report, operating procedure, rollback plan, and portfolio demonstration.

## Dependency shortcuts

- A business specialist may start at modules 01-05, then study 09-19 before learning Python.
- A programmer may test out of modules 02, 06, 07, 20, and 21, but should still complete their security and failure exercises.
- A data analyst may start with modules 03-06, continue through 15-18, then take 20-23.
- A JavaScript developer may take module 29 after modules 06 and 11, while retaining module 20 before the Python-based data-analysis work.
- Anyone deploying an agent that can change external systems must complete modules 16-18 and 26 before deployment.

## Self-assessment scale

Score every competency from 0 to 3:

| Score | Evidence |
|---:|---|
| 0 | I cannot yet explain it. |
| 1 | I can explain it with notes. |
| 2 | I can build or apply it independently. |
| 3 | I can test it, explain tradeoffs, and help another person debug it. |

Do not average away a critical gap. A score of 3 in prompt writing does not compensate for a score of 0 in access control when an agent can send email or update records.

## Practice

Create a table with one row per module and columns for current score, target score, artifact, and review date. Re-score after each capstone using only evidence you can show.

## Completion criteria

- You can describe the five stages and their dependencies.
- You identified modules you may test out of and defined a practical test for each.
- You recorded at least three safety-critical competencies that cannot be skipped.

## References

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI Resource Center](https://airc.nist.gov/)
- [Google People + AI Guidebook](https://pair.withgoogle.com/guidebook-v2/)
