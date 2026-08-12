# Experiments, Regression, and Reproducible Reporting

## Learning objectives

- Design a randomized experiment with a pre-specified analysis.
- Fit and diagnose a regression without turning association into causation.
- Deliver a reproducible analysis package and decision memo.

## Design carries more causal weight than the model

Random assignment makes treatment groups comparable in expectation; observational regression does not recreate randomization automatically. Before an experiment, specify unit and mechanism of randomization, eligibility, treatment, control, primary outcome, minimum meaningful effect, sample-size rationale, duration, exclusions, stopping rule, and analysis. Guard against interference when one student's treatment affects another, and analyze assignment (intention to treat) unless a different estimand was pre-specified.

Check allocation and instrumentation, but avoid repeated unplanned peeking and stopping on a favorable p-value. Track attrition and missing outcomes by group. Report harms and operational metrics alongside the primary outcome.

Regression estimates conditional associations under a model. Inspect functional form, residuals, heteroskedasticity, influential observations, multicollinearity, and dependence. Encode categorical variables intentionally and choose a meaningful reference. Adding every available covariate can introduce leakage, post-treatment bias, or collider bias. A good predictive model is not necessarily a valid causal estimate.

Reproducibility means raw immutable data (or a generation script), environment/dependency record, deterministic pipeline, seed, validation report, analysis code, figures/tables, and a narrative that states limitations. A notebook can explore, but the final result should run top-to-bottom from a clean environment without hidden state.

## Free local practice

Simulate a randomized experiment for a reminder feature with student-level assignment and a binary 28-day completion outcome. Prewrite `analysis-plan.md`, then generate data with a saved seed. Include noncompliance and missing outcomes but never modify rules after seeing results.

Produce:

1. a CONSORT-style flow count from eligible to analyzed;
2. balance diagnostics without significance-test gatekeeping;
3. intention-to-treat difference with confidence interval;
4. sensitivity analysis for missing outcomes;
5. logistic or linear-probability regression with pre-specified baseline covariates;
6. residual/specification diagnostics appropriate to the model;
7. subgroup estimates labeled exploratory unless pre-specified.

Package source data generator, `pyproject.toml` or lock file, scripts, tests for cohort/outcome logic, manifest hashes, and a short decision memo: recommendation, effect and uncertainty, operational tradeoffs, limitations, and follow-up. Run from a clean environment and compare output hashes or documented nondeterministic fields.

## Completion criteria

- The analysis plan predates generated outcomes and defines one primary decision.
- Main analysis follows assignment and reports attrition/missingness transparently.
- Regression diagnostics and causal limitations are explicit.
- A single documented command regenerates validated tables, figures, and memo inputs.

## References

- [NIST Engineering Statistics Handbook: design of experiments](https://www.itl.nist.gov/div898/handbook/pri/pri.htm) - experimental objectives, designs, analysis, and assumptions.
- [statsmodels getting started](https://www.statsmodels.org/stable/gettingstarted.html) - model fitting, summaries, diagnostics, and graphics.
- [statsmodels regression diagnostics](https://www.statsmodels.org/stable/examples/notebooks/generated/regression_diagnostics.html) - specification, normality, autocorrelation, and influence checks.
- [CONSORT 2025 statement](https://www.consort-spirit.org/) - current reporting framework for randomized parallel-group trials; adapt relevant transparency principles outside health research.
- [The Turing Way reproducible research guide](https://book.the-turing-way.org/reproducible-research/reproducible-research) - open guidance on environments, workflows, versioning, and computational reproducibility.
