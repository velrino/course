# Portfolio and Presentation

## Objectives

Present work honestly, protect sensitive information, and make technical and business decisions inspectable by another person.

## Portfolio structure

For each project, lead with the problem, users, baseline, and result, not a list of fashionable tools. A strong case study includes:

1. Problem and why it mattered.
2. Current process and non-AI alternatives.
3. Constraints, affected people, and success measures.
4. Architecture and trust boundaries.
5. Key decisions and rejected alternatives.
6. Evaluation design and representative failures.
7. Safety, privacy, operations, and governance.
8. Measured result, limitations, and next decision.

Link to a reproducible repository when licensing and privacy permit. Include setup, sample data, test command, expected output, and cleanup. Pin versions and remove secrets, credentials, personal data, internal hostnames, and proprietary documents from history, not only from the latest commit.

## Demonstration

A ten-minute demonstration should show:

- the normal path;
- a boundary or malicious case that safely fails;
- a tool or model outage and recovery;
- evaluation results and one error you did not solve;
- how to disable and clean up the system.

Do not stage a flawless path while hiding manual intervention. Label synthetic results and estimated costs. Do not claim "production ready," "secure," "compliant," or "accurate" without a defined standard and matching evidence.

## Interview narrative

Prepare concise explanations of one architecture tradeoff, one debugging investigation, one risk you reduced, one feature you removed, and one result that changed your decision. Employers can evaluate judgment more reliably from these specifics than from framework names.

## Practice

Run a portfolio review using the capstone rubric. Ask a reviewer to reproduce one project and locate the evidence for three claims. Record every point of confusion. Revise the project, then present it once to a technical audience and once to a business audience without changing the underlying evidence.

## Completion criteria

- Every material claim links to reproducible evidence.
- Public artifacts contain no unauthorized data or secrets.
- The demo includes safe failure and recovery.
- Limitations and rejected options are concrete.

## References

- [GitHub: About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Diataxis documentation framework](https://diataxis.fr/)
- [W3C Web Accessibility Initiative: Presentations](https://www.w3.org/WAI/teach-advocate/accessible-presentations/)
