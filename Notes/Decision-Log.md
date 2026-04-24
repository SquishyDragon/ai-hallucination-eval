## [2026-04-21] – Moving Away from AI-as-Judge as Primary Evaluator

### Initial Idea

Use an AI model to evaluate responses from another AI model to detect hallucinations.

### Assumption

A sufficiently capable model should be able to identify incorrect or hallucinated outputs from another model.

### Issue Discovered

The evaluator model may share the same knowledge gaps or hallucination tendencies as the model being evaluated.
This creates a risk of:

* False negatives (hallucinations not detected)
* False positives (correct answers flagged incorrectly)
* Inconsistent evaluations depending on model version

### Key Insight

AI models are not reliable sources of **ground truth**.
They are probabilistic systems that can reproduce the same errors they are supposed to detect.

### Decision

Shifted to a **known-truth, rule-based evaluation system** as the primary method for scoring responses.

AI-based evaluation may still be used later as a **secondary signal**, not as the source of truth.

### Impact

* Increased evaluation reliability and consistency
* Reduced dependence on subjective or unstable judgments
* Made results more explainable and defensible

### Future Considerations

* Introduce hybrid evaluation (rule-based + AI judge for edge cases)
* Add confidence scoring to capture uncertainty in borderline cases
* Explore disagreement detection between rule-based and AI-based evaluations
