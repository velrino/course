# Review Interfaces, Feedback, and Escalation

## Learning objectives

- Build review information that supports attention rather than automation bias.
- Capture feedback as structured operational data.
- Measure reviewer agreement, overrides, delays, and downstream outcomes.

## Design for a decision, not a demo

Reviewers tend to accept plausible defaults under time pressure. Reduce anchoring by presenting source facts before the proposed conclusion when risk is high. Clearly distinguish user input, retrieved evidence, model output, and deterministic policy checks. Show known limitations and the consequence of approval.

A reviewer should never need hidden model reasoning. Provide observable evidence instead: citations, input fields, diffs, validation failures, tool arguments, and relevant history. For an edited proposal, display a semantic or text diff. Require a reason for overrides and rejection, but keep the taxonomy short enough to use: `incorrect_fact`, `missing_context`, `policy_violation`, `unsafe_action`, `wrong_recipient`, `other`.

Feedback is not ground truth automatically. A hurried approval, malicious reviewer, or disagreement between experts may be wrong. Preserve reviewer identity/role, displayed version, decision, reason, time spent, and later outcome. Use adjudication for high-impact labels and measure inter-rater agreement on a sample.

Operational metrics should reveal system and process failures:

- approval, edit, rejection, and escalation rates by action type;
- queue age and decision-time percentiles;
- override reason distribution;
- disagreement between reviewers;
- incidents after approval;
- false escalation and missed escalation samples.

A low rejection rate is not proof of quality; it may show inattentive review.

## Free local practice

Build a static HTML page or terminal interface for ten synthetic approval packets. Include one normal case and nine edge cases such as stale evidence, an inaccessible source, a changed recipient, a large amount, ambiguous identity, and a policy exception.

Ask two people, or run two blinded passes yourself at different times, to review the packets. Do one pass with only the model recommendation and another with sources-first ordering. Record decision, reason, confidence, and elapsed time in CSV. Compare:

1. override rate;
2. errors against a prewritten answer key;
3. median decision time;
4. percent agreement between passes or reviewers.

Inspect disagreements rather than compressing everything into one score. Revise the packet for cases where material evidence was overlooked. Define an escalation service level and a safe behavior when the queue exceeds it.

## Completion criteria

- The interface labels evidence, model output, and policy checks separately.
- Review actions include edit, reject, and escalate with structured reasons.
- A small blinded study produces recorded accuracy and timing evidence.
- Queue overload and reviewer disagreement have explicit operational responses.

## References

- [Microsoft Guidelines for Human-AI Interaction project](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/) - guidance across initial use, routine use, errors, and adaptation.
- [Amershi et al. CHI 2019 paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf) - research method and validated guidelines.
- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) - suggested actions for governing, mapping, measuring, and managing risk.
- [Krippendorff's alpha overview and implementation](https://github.com/pln-fing-udelar/fast-krippendorff) - open implementation for agreement measurement across several data types.
