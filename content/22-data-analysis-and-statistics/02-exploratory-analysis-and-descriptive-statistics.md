# Exploratory Analysis and Descriptive Statistics

## Learning objectives

- Use distributions and robust summaries instead of relying on averages.
- Explore relationships while checking data-generating assumptions.
- Separate exploratory findings from confirmatory claims.

## Describe shape, spread, and structure

Begin with row/column counts, types, unique values, missingness, ranges, and time coverage. For numeric variables, inspect median, quantiles, interquartile range, minimum/maximum, and mean/standard deviation. A mean is sensitive to skew and outliers; a median can hide bimodality. Always look at the distribution and the raw scale.

An outlier may be an error, a rare valid event, fraud, or the most important observation. Investigate its provenance before removing it. Report results with and without influential observations when the decision is sensitive. Use domain limits and robust methods rather than automatic z-score deletion.

For relationships, compare within meaningful groups and over time. Aggregation can reverse a pattern (Simpson's paradox), and repeated observations from one person are not independent rows. Correlation measures association, not causation; time trends, selection, and shared causes can create it.

Exploratory data analysis generates hypotheses and discovers assumptions. If you select a surprising subgroup after viewing the data and then compute a p-value on the same data, the result is not a clean confirmation. Label it exploratory and validate on new or held-out data.

## Free local practice

Using the cleaned synthetic course data, produce one table per variable with missingness, cardinality, range, and robust summaries. Plot completion time with histogram and empirical cumulative distribution. Compare completion by platform and enrollment week.

Create a deliberate Simpson's paradox example: mobile has lower completion within both beginner and advanced cohorts, but appears higher overall because it has more advanced students. Calculate the overall and stratified rates, then explain which comparison answers which question.

Investigate the five most extreme completion times. For each, label valid, data error, or unresolved with evidence. Recompute key summaries under at least two defensible treatments and record sensitivity. Finish with an EDA memo: established data facts, anomalies, candidate explanations, and questions requiring new data.

## Completion criteria

- Summaries include distribution, spread, missingness, and time/group structure.
- Outliers are investigated and sensitivity is reported before exclusion.
- Overall and stratified results expose a constructed aggregation reversal.
- Exploratory hypotheses are labeled and not presented as confirmed causal effects.

## References

- [NIST: What is exploratory data analysis?](https://www.itl.nist.gov/div898/handbook/eda/section1/eda11.htm) - goals, philosophy, and graphical emphasis of EDA.
- [NIST EDA techniques](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3.htm) - graphical and quantitative technique catalog.
- [pandas descriptive statistics](https://pandas.pydata.org/docs/user_guide/basics.html#descriptive-statistics) - summary operations and behavior.
- [NumPy statistics routines](https://numpy.org/doc/stable/reference/routines.statistics.html) - array-level means, quantiles, variance, and related functions.
