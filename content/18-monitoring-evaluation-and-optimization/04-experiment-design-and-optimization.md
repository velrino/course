# Experiment Design and Optimization

## Learning objectives

- Compare configurations with paired, uncertainty-aware experiments.
- Optimize quality, latency, and cost without contaminating a held-out set.
- Avoid false wins caused by sampling noise or repeated testing.

## Define the decision before running variants

Write the primary metric, safety floors, latency/cost budgets, slices, sample, and decision rule first. For example: "Ship B if paired task success improves by at least 3 percentage points, the 95% bootstrap interval excludes -1 point, no critical safety case regresses, p95 latency stays below 4 seconds, and cost rises no more than 10%."

Use paired evaluation: run A and B on the same case IDs and compare per-case outcomes. Pairing reduces noise from case difficulty. Preserve raw outputs and randomize blinded human comparison order. When model sampling is material, repeat each case and report distribution or pass probability; do not cherry-pick the best response.

Optimize one component at a time when diagnosing: retrieval `k`, chunking, reranking, prompt, model, tool policy, or temperature. Factorial designs can reveal interactions, but the number of comparisons grows quickly. Repeatedly tuning against the test set overfits it; use development data for search and a held-out set once for confirmation.

Quality is constrained optimization, not a single leaderboard number. Plot a Pareto frontier of quality against cost and latency. Remove dominated variants that are worse on all relevant dimensions. Always inspect critical slices even when the overall score improves.

## Free local practice

Take stored outputs from two RAG or agent configurations on at least 30 identical cases. Create a CSV with case ID, tags, score A/B, latency A/B, cost A/B, and safety pass A/B.

Use NumPy with a fixed `default_rng` seed to bootstrap the mean paired quality difference 10,000 times. Report the median and 2.5/97.5 percentiles. Calculate p95 latency per variant and slice-level changes. Plot quality versus cost using Matplotlib and label nondominated variants.

Write a one-page decision record that includes the preregistered rule, result, critical regressions, uncertainty, limitations, and decision. Then reveal one withheld slice. If the conclusion changes, document why rather than moving the threshold after seeing results.

## Completion criteria

- The decision rule and constraints are written before examining comparison results.
- Variants use identical case IDs and paired analysis.
- Uncertainty, tails, cost, and safety slices are reported with the average.
- Development tuning and held-out confirmation are separated.

## References

- [SciPy bootstrap documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) - reproducible bootstrap confidence intervals.
- [NumPy random Generator](https://numpy.org/doc/stable/reference/random/generator.html) - explicit random state for repeatable simulation.
- [NIST Engineering Statistics Handbook: comparison of two processes](https://www.itl.nist.gov/div898/handbook/prc/section3/prc3.htm) - statistical comparison foundations.
- [MLflow evaluation quickstart](https://mlflow.org/docs/latest/genai/eval-monitor/quickstart/) - recording runs and comparing evaluation results against a baseline.
