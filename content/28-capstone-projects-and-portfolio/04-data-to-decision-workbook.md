# Capstone: Data-to-Decision Workbook

## Objective

Turn a public dataset into a reproducible analysis that answers a business question without overstating causality or hiding data quality problems.

## Scenario

Choose a public dataset with a documented license and data dictionary. Define a fictional stakeholder and one decision they need to make. Examples include service demand planning, inventory patterns, public transport reliability, or support workload. Avoid sensitive person-level prediction.

## Required analysis

1. Write the question, decision, baseline, and limitations before exploring.
2. Create a data manifest and quality profile.
3. Load raw data without manual spreadsheet edits.
4. Clean through reproducible transformations.
5. Use SQL for at least one aggregation and Python for analysis.
6. Report distributions and uncertainty, not only averages.
7. Create accessible visualizations with units and sources.
8. Test how missing data and alternative definitions change the result.
9. Separate descriptive findings from causal claims.

An optional natural-language layer may propose SQL against a read-only copy, but every query must be validated, limited, logged, and compared with a hand-written result.

## Evaluation

Add automated checks for schema, range, uniqueness, missingness, row counts, and reconciliation totals. Create at least three sensitivity analyses. Ask another person to interpret each chart without your explanation; revise misleading encodings.

## Deliverables

- Data and source manifest, or a download script when redistribution is prohibited.
- SQL schema and queries.
- Reproducible notebook or Python package.
- Data-quality report, charts, and decision memo.
- Tests, environment file, and limitations statement.

## Completion criteria

- Raw data can be reconstructed and is never silently edited.
- Claims match the analysis design and uncertainty.
- Charts are labeled, accessible, and reproducible.
- The decision memo identifies what additional evidence would change the recommendation.

## References

- [pandas user guide](https://pandas.pydata.org/docs/user_guide/)
- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [SciPy statistics documentation](https://docs.scipy.org/doc/scipy/tutorial/stats.html)
- [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)
