# Data Visualization and Communication

## Learning objectives

- Match chart form to analytical question and data type.
- Encode comparisons honestly with readable scales and uncertainty.
- Produce accessible, reproducible graphics and a decision-focused narrative.

## A chart is an argument with geometry

Use position on a common scale for precise comparison. Bars suit magnitudes and normally start at zero; lines suit ordered time; dots often compare categories more efficiently; scatterplots show two quantitative variables; histograms/ECDFs show distributions; box/violin plots summarize groups but should not hide small sample sizes. Pie and 3D charts make comparison harder and can distort area or perspective.

Choose the denominator and aggregation before colors. Show counts with rates when sample sizes differ. Label units, population, window, source, and relevant exclusions. A truncated axis can be appropriate for small changes in a line chart if clearly marked, but truncating bars changes their visual ratio. Avoid dual axes unless the relationship is unavoidable and unmistakably labeled.

Uncertainty is part of the result. Use intervals, bands, or distributions and explain what they represent. Do not imply precision through too many decimals. Use direct labels where possible, colorblind-compatible palettes, adequate contrast, and redundant shape/line style when color carries meaning. Provide concise alternative text and a data table or long description for complex charts.

Separate analysis code from editorial decisions but keep both versioned. Export at stable dimensions with readable text; never rely on viewport-scaled font to fix a crowded figure.

## Free local practice

Create four figures from course data:

1. weekly enrollment and completion counts;
2. completion-rate dot plot by platform with confidence intervals and sample sizes;
3. ECDF of completion time by cohort;
4. scatterplot of lessons attempted versus completion time, faceted by experience level.

Use Matplotlib/Seaborn and save each as PNG plus SVG/PDF when appropriate. Write a one-sentence title stating the finding, not "Chart 1." Include source and transformation note. Create a misleading version of one plot using a bad denominator, truncated bar axis, or missing subgroup; annotate why it misleads, then correct it.

Write alternative text that states chart type, population, main pattern, material exception, and where exact data are available. Check figures in grayscale and at their intended display size.

## Completion criteria

- Chart choice, denominator, scale, units, and sample sizes match the question.
- Uncertainty is shown and defined where estimates are compared.
- A documented misleading chart is corrected with an explanation.
- Every final figure has provenance, readable labels, alternative text, and access to underlying summary data.

## References

- [Matplotlib quick start](https://matplotlib.org/stable/users/explain/quick_start.html) - figures, axes, scales, labels, and layouts.
- [Seaborn statistical visualization tutorial](https://seaborn.pydata.org/tutorial.html) - relationships, distributions, categorical data, estimation, and uncertainty.
- [W3C complex images guidance](https://www.w3.org/WAI/tutorials/images/complex/) - accessible summaries and long descriptions for charts and diagrams.
- [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/) - free full manuscript on honest, readable, and effective visualization.
