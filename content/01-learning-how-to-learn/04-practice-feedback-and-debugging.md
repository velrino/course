# Practice, Feedback, and Debugging

## Learning objectives

By the end of this lesson, you will be able to:

- design practice that targets a specific subskill;
- use worked examples without copying them blindly;
- turn errors into hypotheses and diagnostic experiments; and
- request feedback that leads to an actionable revision.

## Practice needs a target and a feedback channel

"Build a large project" sounds practical, but it can hide weak skills. You may spend most of the time on setup or follow instructions without making decisions. Focused practice isolates a bottleneck while preserving a realistic context.

Use this loop:

1. State the subskill: "interpret an HTTP error from observable evidence."
2. Define success: "identify whether the failure is transport, authentication, authorization, or application validation."
3. Attempt a task just beyond current reliability.
4. Collect feedback from output, tests, documentation, or a reviewer.
5. Change one thing and try a related task.

Practice should vary the input while holding the target skill stable. Three nearly identical copied commands are repetition; three failures that require choosing different diagnostics are practice.

## Fade worked examples

A worked example reduces cognitive load by showing both the steps and reasoning. Use it in three passes:

- **Explain:** annotate why every step exists and predict the next step before revealing it.
- **Complete:** hide selected steps and reconstruct them.
- **Transfer:** solve a changed problem without the example.

If you cannot explain a line, treat it as an open question. Copying a correct program can produce no usable mental model.

## Debug with hypotheses

Random edits produce noise. A diagnostic cycle is:

```text
Observation -> competing hypotheses -> discriminating test -> result -> updated model
```

Example observation: `curl` connects to a server but receives `401 Unauthorized`.

Possible hypotheses:

- the credential is absent;
- the credential format is wrong;
- the credential is expired; or
- the server expects a different authentication scheme.

A useful test distinguishes hypotheses. Printing the exact request headers (with secrets redacted) is more informative than retrying the same request. Change one variable when possible and preserve the failing example as a regression test.

## Ask for high-quality feedback

"Is this good?" gives a reviewer no target. Ask:

> The intended behavior is X. Here is the artifact and the evidence I collected. Check specifically for Y and Z. Point to the first counterexample or unsupported assumption. Do not rewrite it yet.

When feedback arrives, classify it as correctness, clarity, maintainability, security, or scope. Revise the artifact, then rerun the original completion test. Feedback is not complete until it changes work or is rejected with a reason.

## Free local practice

Choose any command you know, such as `ls`, `git status`, or `curl --version`.

1. Write a correct worked example and annotate every token.
2. Introduce one deliberate error.
3. Record the exact observed output.
4. Write at least two hypotheses before changing anything.
5. Choose one command or inspection that separates the hypotheses.
6. Fix the error and rerun both the failing and successful cases.
7. Write one retrieval prompt based on the error.

The artifact is a one-page diagnostic record, not merely a corrected command.

## Completion criteria

- [ ] Your practice targets one named subskill.
- [ ] You explained a worked example before completing a changed version.
- [ ] You wrote competing hypotheses before applying a fix.
- [ ] Your diagnostic test could make at least one hypothesis less likely.
- [ ] You saved the error as a future retrieval or regression exercise.

## References

- [Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/WWC/Docs/PracticeGuide/20072004.pdf) - guidance supporting alternating worked examples with independent problem solving.
- [How Learning Works](https://firstliteracy.org/wp-content/uploads/2015/07/How-Learning-Works.pdf) - free text explaining goal-directed practice, targeted feedback, prior knowledge, and self-directed learning.
- [The Debugging Mindset](https://queue.acm.org/detail.cfm?id=3068754) - free ACM Queue article on disciplined causal reasoning during software debugging.

## Continue

Next: [Run a Sustainable Weekly Learning Loop](05-run-a-sustainable-weekly-learning-loop.md)
