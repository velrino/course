# Sampling, Uncertainty, and Hypothesis Tests

## Learning objectives

- Distinguish population, sample, parameter, estimator, and sampling distribution.
- Interpret confidence intervals and p-values without common overclaims.
- Choose and check a test based on design and assumptions.

## Inference depends on how data were generated

A large biased sample can estimate the wrong population very precisely. State the target population, sampling/assignment mechanism, dependence structure, and missingness before using formulas. Repeated events from the same student are clustered, not independent observations.

A confidence interval describes uncertainty from a specified repeated-sampling procedure under its assumptions. It does not mean there is a 95% probability that a fixed parameter lies inside one frequentist interval. A p-value is the probability, assuming the null model and other assumptions, of a result at least as incompatible with that model as observed. It is not the probability the null hypothesis is true and does not measure effect importance.

Report an effect size and uncertainty, not only a thresholded p-value. Practical significance depends on the decision. Testing many outcomes/subgroups raises false positives; pre-specify a primary outcome and use adjustment or clearly label exploration. "Fail to reject" is not proof of no effect; an equivalence or non-inferiority design is needed for a bounded no-important-difference claim.

Choose methods from the design. Paired observations require paired analysis. Proportions, means, ranks, and time-to-event outcomes differ. Check distribution, variance, independence, and sample-size assumptions. Permutation and bootstrap methods can be useful, but resampling units must reflect clusters and the design.

## Free local practice

Simulate completion outcomes for 2,000 students with a fixed NumPy random generator. Draw 1,000 repeated samples and plot the sampling distribution of a completion-rate difference. Show how standard error changes with sample size.

For one fixed sample, calculate a difference in proportions and confidence interval. Run an appropriate two-sided test with SciPy. Report group counts, rates, difference in percentage points, interval, test statistic, p-value, assumptions, and practical threshold. Rewrite three incorrect claims: "95% probability," "p proves," and "not significant means equal."

Create 20 unrelated null outcomes and test all at 0.05. Repeat the simulation many times to estimate how often at least one false positive appears. Apply a false-discovery-rate correction and compare. Do not use this simulation to justify post-hoc fishing; use it to understand multiplicity.

## Completion criteria

- Population, sampling/assignment, unit, independence, and missingness are stated.
- Reports include effect size, interval, p-value when used, sample sizes, and assumptions.
- Simulations demonstrate sampling variability and multiple-testing risk with a saved seed.
- Interpretations avoid probability-of-hypothesis and "no significance equals no effect" errors.

## References

- [SciPy statistical functions](https://docs.scipy.org/doc/scipy/reference/stats.html) - tests, confidence intervals, bootstrap, permutation, and false-discovery control.
- [SciPy resampling tutorial](https://docs.scipy.org/doc/scipy/tutorial/stats/resampling.html) - bootstrap, permutation, and Monte Carlo methods.
- [American Statistical Association statement on p-values](https://doi.org/10.1080/00031305.2016.1154108) - six principles for valid interpretation.
- [NIST confidence limits](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm) - confidence interval fundamentals for the mean.
- [NumPy random sampling](https://numpy.org/doc/stable/reference/random/index.html) - reproducible generators and distributions.
