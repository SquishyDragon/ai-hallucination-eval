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

## [2026-04-30] – Decision: Add Explicit Behavior Matching + Reason Tracking

### Initial Idea

Return simple evaluation results:

PASS / FAIL / UNKNOWN

### Assumption

A binary or simple status output would be sufficient to understand model behavior.

### Issue Discovered

Simple status labels lack explainability and make it difficult to:

* Understand why a response passed or failed
* Debug incorrect evaluations
* Identify patterns in hallucination behavior
* Communicate results clearly to others

This created friction when analyzing results and validating the evaluator itself.

### Key Insight

Evaluation systems are only as useful as their ability to explain decisions.

A result without reasoning is difficult to trust, debug, or improve.

### Decision

Capture and return the matched behavior terms that triggered the evaluation.

Each result now includes:

* Matched allowed terms (for PASS)
* Matched disallowed terms (for FAIL)
* A human-readable message using f-strings, e.g.:
* Test fake_api_001 FAILED based on behavior match of '/v1/teleport'

### Impact
* Improved transparency and debuggability
* Enabled faster iteration on evaluation rules
* Made results more interpretable and demo-friendly
* Provided a foundation for future analysis (e.g., top failure patterns)

### Future Considerations
* Aggregate matched terms to identify common hallucination patterns
* Rank failure causes by frequency
* Introduce severity weighting based on matched terms


## [2026-05-02] – Introduce run_id for Evaluation Runs

### Decision

Add a run_id field to each evaluation output to uniquely identify and group results from a single execution.

### Context

# Initial implementation saved evaluation results as a single JSON file without any identifier linking results to a specific run. As the system evolved toward a multi-run evaluation platform, this structure lacked the ability to:

* distinguish between separate evaluation executions
track historical results over time
support comparison across runs or models
Rationale

* Adding a run_id enables each evaluation to be treated as a discrete, trackable unit.

* This provides several immediate and future benefits:

* Traceability: Each result set can be uniquely identified
* Reproducibility: Runs can be referenced and analyzed independently
* Scalability: Supports storing multiple runs without overwriting data
* Organization: Enables clean grouping of results for analysis

# Most importantly, this decision directly supports the planned dashboard layer, where:

* multiple runs will be displayed
* users may compare results across models or configurations
* historical trends and regressions can be visualized

# Without a run_id, building a meaningful frontend or analysis layer would be significantly more complex.

### Tradeoffs

# Pros:

* Enables future dashboard and comparison features
* Improves data organization and clarity
* Aligns with real-world evaluation system design

# Cons:

* Slight increase in output complexity
* Requires consistent handling across future features
* Status

### Future Considerations
* Persist multiple run files instead of overwriting latest_results.json
* Introduce run history tracking (e.g., results/run_<id>.json)
* Enable filtering and comparison of runs in the dashboard
* Add metadata (e.g., model version, timestamp, prompt set version) to each run


## [2026-05-03] – Decision: Defer Pressure-Based Severity System

### Context
While developing the evaluation framework, an idea emerged to classify prompts by "pressure" (how strongly they assume a concept exists) and derive hallucination severity based on that pressure.

### Insight
Hallucinations are not equally severe. A model failing under strong prompt assumptions is less concerning than failing under neutral or skeptical prompts.

### Decision
Defer implementation of pressure labeling and severity mapping to a future phase in order to:
- Maintain momentum on core evaluation system (Phase 2)
- Avoid overcomplicating current dataset structure
- Ensure foundational features (run tracking, comparison) are completed first

### Future Plan
Introduce:
- `pressure` field in dataset
- Derived `severity` scoring
- Weighted evaluation metrics and dashboard integration

### Impact
This will significantly improve the realism and usefulness of hallucination evaluation by incorporating contextual risk rather than binary correctness.
