# Analysis Rules

These rules apply to all formal analytical work in this repository.

---

## 1. Source of Truth

All formal numerical results must be calculated from the source data
using executable analytical code.

The LLM is not a numerical source of truth.

Never:

- fabricate results;
- manually enter statistics into the dashboard;
- use an LLM estimate as a calculated result;
- change a calculation to match an expected result.

---

## 2. Preserve Source Data

The original source dataset must remain unchanged.

Cleaning and transformations must:

- occur programmatically;
- be documented;
- be reproducible.

Derived datasets should be stored separately.

---

## 3. Association Is Not Causation

The dataset is observational/static.

Do not describe statistical associations as causal effects.

Preferred language:

- associated with
- relationship
- within this dataset
- the analysis indicates
- predictive relationship

Avoid unsupported terms:

- causes
- proves
- results in
- will increase
- optimal
- best management practice

---

## 4. Statistical Significance Is Not Business Significance

Do not use p-values alone to determine importance.

Where appropriate report:

- effect size;
- confidence intervals;
- magnitude;
- sample size;
- practical interpretation.

Large samples can produce statistically significant results with
negligible practical importance.

---

## 5. Analysis Identification

Every formal analysis receives an Analysis ID:

A001, A002, A003...

Record:

- business question;
- purpose;
- variables;
- filters;
- sample size;
- method;
- assumptions;
- code location;
- output;
- result;
- limitations.

---

## 6. Exploratory Analysis

Exploration is encouraged but must be labelled exploratory.

Do not selectively promote only statistically significant exploratory
results.

An exploratory observation must undergo formal analysis and validation
before becoming a verified finding.

---

## 7. Statistical Method Selection

Methods must be appropriate for:

- variable types;
- distributions;
- sample structure;
- analytical question.

Check relevant assumptions.

If a planned method appears inappropriate:

DO NOT silently replace it.

Document:

1. original proposed method;
2. identified problem;
3. recommended alternative;
4. reason;
5. whether human approval is required.

---

## 8. Multiple Testing

When many relationships are explored, acknowledge the increased
probability of false-positive findings.

Where appropriate:

- distinguish confirmatory from exploratory analysis;
- use appropriate multiple-comparison controls;
- report the number of comparisons;
- avoid selecting findings solely because p < 0.05.

---

## 9. Aggregation

Always consider whether aggregated analysis hides meaningful subgroup
differences.

Crop type is particularly important.

Where relevant compare:

- overall result;
- crop-specific result.

Do not assume an overall relationship applies equally to every crop.

---

## 10. Missing Data

Report missingness before analysis.

Do not silently:

- remove observations;
- impute values;
- replace values.

Any treatment of missing data must be documented.

---

## 11. Outliers

Do not automatically delete outliers.

Investigate whether they represent:

- legitimate observations;
- data errors;
- influential observations.

Any exclusion must have a documented analytical reason.

---

## 12. Predictive Modelling

Maintain strict separation between training and evaluation data.

Prevent:

- target leakage;
- preprocessing leakage;
- test-set contamination.

Use reproducible random seeds.

Where appropriate use cross-validation.

Compare models using the same evaluation methodology.

At minimum consider:

- baseline;
- linear regression;
- Random Forest;
- gradient boosting.

Report all relevant model results rather than only the best result.

---

## 13. Model Evaluation

Use appropriate metrics such as:

- MAE
- RMSE
- R²

Training performance alone is insufficient.

Evaluate unseen-data performance.

Where relevant examine performance by crop or other meaningful groups.

---

## 14. Model Interpretability

Predictive accuracy does not automatically make a model useful.

Consider:

- interpretability;
- stability;
- complexity;
- subgroup performance;
- practical usefulness.

Feature importance indicates predictive contribution, not necessarily
causal importance.

---

## 15. Reproducibility

Use fixed seeds where stochastic methods are used.

Record:

- dependency versions;
- configuration;
- dataset hash;
- execution timestamp;
- pipeline version where practical.

Repeated execution should reproduce deterministic results within
appropriate numerical tolerance.

---

## 16. Negative Results

Non-significant or contradictory findings must not be hidden merely
because they are less interesting.

The project is an analytical investigation, not an attempt to prove
predetermined conclusions.

---

## 17. Dashboard Results

Formal dashboard statistics must originate from generated analytical
outputs.

Do not hard-code important analytical results into the application.

The dashboard is a presentation/exploration layer, not the calculation
authority.

---

## 18. AI-Generated Interpretations

AI interpretations are candidate interpretations.

Every formal claim must link to analytical evidence.

No AI-generated statement becomes a verified finding without the
required review process.
