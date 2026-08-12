# Evaluate Models and Generalization

## Learning objectives

By the end of this lesson, you will be able to:

- separate training, validation, and test roles;
- compute and interpret classification metrics;
- choose metrics from error costs rather than habit; and
- plan monitoring for changed data and behavior.

## Generalization is the real target

A model generalizes when it performs usefully on relevant examples not used to fit it. **Underfitting** occurs when a model or representation cannot capture enough useful structure. **Overfitting** occurs when it fits training particulars that do not transfer.

A common data split uses:

- a **training set** to fit parameters;
- a **validation set** to choose features, thresholds, or other design decisions; and
- a **test set** for a final, less-biased estimate after choices are fixed.

Repeatedly consulting the test set turns it into another validation set. Also split according to the deployment problem. If tomorrow is the target, a random split that leaks future patterns into training may give an unrealistic estimate. Related records from one person or event may need to stay in one split.

## Start from the confusion matrix

For a binary decision:

- true positive (`TP`): predicted positive and actually positive;
- false positive (`FP`): predicted positive but actually negative;
- false negative (`FN`): predicted negative but actually positive; and
- true negative (`TN`): predicted negative and actually negative.

Useful metrics include:

```text
precision = TP / (TP + FP)
recall    = TP / (TP + FN)
accuracy  = (TP + TN) / all examples
```

Accuracy can be misleading with rare outcomes. A system that always predicts "not fraud" can be 99.9% accurate in a dataset with 0.1% fraud while detecting none of it. Precision answers how often positive predictions are right. Recall answers how much of the actual positive class is found.

The decision threshold trades error types. The right tradeoff depends on impact, review capacity, and the availability of a human fallback.

## Evaluate slices and the whole system

Aggregate metrics can hide failures. Measure relevant slices such as language, device type, region, document source, or high-impact user group, while respecting privacy and statistical uncertainty.

Also evaluate more than the model:

- input validation and missing-data behavior;
- latency, cost, and availability;
- calibration and confidence handling;
- user overrides and escalation;
- logging and incident response; and
- drift after deployment.

Data drift means input distributions change. Concept drift means the relationship between inputs and desired outputs changes. Monitoring detects signals; it does not automatically explain causes.

## Free local practice

Run this standard-library calculation:

```bash
python3 - <<'PY'
actual    = [1, 0, 1, 1, 0, 0, 1, 0, 0, 0]
predicted = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0]

tp = sum(a == 1 and p == 1 for a, p in zip(actual, predicted))
fp = sum(a == 0 and p == 1 for a, p in zip(actual, predicted))
fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))
tn = sum(a == 0 and p == 0 for a, p in zip(actual, predicted))

safe_div = lambda n, d: n / d if d else 0
print({"tp": tp, "fp": fp, "fn": fn, "tn": tn})
print({
    "accuracy": safe_div(tp + tn, len(actual)),
    "precision": safe_div(tp, tp + fp),
    "recall": safe_div(tp, tp + fn),
})
PY
```

Verify the counts by hand. Then describe two applications: one where the false positive is worse and one where the false negative is worse. Choose a primary metric for each and explain why no single metric is sufficient.

## Completion criteria

- [ ] You explain the distinct role of each data split.
- [ ] You reproduced `TP`, `FP`, `FN`, and `TN` by hand.
- [ ] You calculated accuracy, precision, and recall.
- [ ] Your metric choices follow documented error costs.
- [ ] Your monitoring plan includes slices and post-deployment change.

## References

- [Classification: Accuracy, Recall, Precision, and Related Metrics](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall) - free explanation and exercises for confusion-matrix metrics.
- [Datasets, Generalization, and Overfitting](https://developers.google.com/machine-learning/crash-course/overfitting) - official lessons on dataset properties and performance on unseen data.
- [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) - practical Google guidance emphasizing pipelines, simple baselines, metrics, and training-serving consistency.
- [NIST AI RMF: Measure](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) - public framework outcomes for testing, evaluation, verification, and validation in context.

## Continue

Next: [Distinguish Agents from Models and Workflows](04-distinguish-agents-from-models-and-workflows.md)
