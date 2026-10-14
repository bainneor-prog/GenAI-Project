# Human Verification Protocol

## Purpose

Human verification provides the final analytical control over
AI-assisted findings.

AI agreement does not constitute human verification.

The human analyst remains responsible for deciding whether a finding is
accepted into the final analysis.

---

# Verification Levels

## Level 1 — Routine Verification

For routine descriptive results:

Check:

1. correct dataset;
2. correct variables;
3. expected sample size;
4. deterministic result exists;
5. interpretation matches the result.

---

## Level 2 — Important Finding Verification

For findings likely to appear prominently in the report/dashboard:

Check:

1. Data Trace
2. Method
3. Numerical Result
4. Visual Evidence
5. Interpretation
6. Independent AI Review

Perform an independent numerical spot-check where practical.

---

## Level 3 — High-Risk Verification

Required when:

- AI reviewers disagree;
- result is unexpected;
- result drives an important business conclusion;
- predictive performance appears unusually strong;
- causal interpretation is possible;
- methodology is disputed;
- result materially contradicts previous analysis.

Perform independent recalculation.

Where possible, use a calculation that does not depend on the primary
analysis implementation.

---

# Human Verification Checklist

## 1. Data Trace

Verify:

- correct source dataset;
- correct variables;
- correct filters;
- correct groups;
- sample size;
- exclusions.

Question:

"Was the intended data actually analysed?"

---

## 2. Method Check

Determine whether the analytical method is appropriate for the
question and data.

Consider:

- variable types;
- assumptions;
- sample structure;
- statistical test;
- model evaluation approach.

Question:

"Does this method actually answer the question?"

---

## 3. Numerical Check

For important findings, reproduce one or more important values using:

- Excel;
- calculator;
- separate Python calculation;
- other independent analytical method.

Do not use the same primary pipeline function when claiming independent
replication.

Question:

"Can I independently reproduce the important number?"

---

## 4. Visual Check

Inspect appropriate plots and/or underlying observations.

Look for:

- outliers;
- unexpected distributions;
- subgroup differences;
- nonlinear patterns;
- misleading aggregation;
- results dominated by a small number of observations.

Question:

"Does the underlying data visually support the statistical result?"

---

## 5. Interpretation Check

Check whether the wording accurately reflects the evidence.

Specifically look for:

- causal claims;
- exaggerated conclusions;
- confusion between statistical and practical significance;
- generalisation beyond the dataset;
- ignored uncertainty;
- unsupported recommendations.

Question:

"Does the claim say more than the evidence supports?"

---

## 6. Independent AI Review

Review any issues raised by the independent AI auditor.

AI disagreement does not determine the answer.

Resolve disagreements using:

- source data;
- analytical method;
- deterministic calculation;
- statistical reasoning.

---

# Final Human Decision

Every reviewed formal finding receives one of:

## ACCEPTED

Evidence and interpretation are sufficiently supported.

## CORRECTED

Underlying analysis is substantially valid but the result,
methodology or interpretation required correction.

Record what changed.

## REJECTED

The proposed finding is unsupported, incorrect or methodologically
invalid.

Record the reason.

## INCONCLUSIVE

Available evidence is insufficient to make a reliable conclusion.

---

# Verification Record

Record at minimum:

- Finding ID
- Analysis ID(s)
- Verification level
- Date
- Data trace status
- Method status
- Numerical check status
- Visual check status
- Independent AI status
- Final decision
- Corrections
- Reason
- Verification time

Store records in:

audit/human_verification_register.csv

---

# Human Verification Metrics

Where sufficient records exist, calculate:

Acceptance Rate =
Accepted unchanged / Findings reviewed

Correction Rate =
Corrected / Findings reviewed

Rejection Rate =
Rejected / Findings reviewed

Human Intervention Rate =
(Corrected + Rejected) / Findings reviewed

Record verification time so that the human cost of AI-assisted
analytics can also be evaluated.

Do not manufacture metrics where insufficient observations exist.
