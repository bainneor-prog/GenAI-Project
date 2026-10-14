# Business Questions

## Purpose

These questions define the analytical objectives of the project.

Formal analyses should normally relate to one of these questions.
Exploratory analyses may investigate additional patterns but must be
identified as exploratory.

---

# BQ1 — Yield Relationships and Interactions

## Question

Which crop-specific relationships and interactions between fertiliser,
irrigation, soil and environmental conditions are most strongly
associated with crop yield?

## Why this matters

The previous analysis demonstrated that aggregated analysis can hide
important crop-specific relationships.

The revised analysis should therefore investigate whether relationships
differ according to crop or agricultural/environmental conditions.

## Candidate areas

Examples include:

- Crop × Fertiliser
- Crop × Rainfall
- Crop × Soil
- Crop × Irrigation
- Rainfall × Irrigation
- Soil × Fertiliser
- Soil Moisture × Irrigation

These are candidate analyses, not predetermined findings.

## Expected output

Identify:

- strength of relationships;
- uncertainty;
- statistical significance where appropriate;
- effect size;
- differences between relevant groups;
- limitations;
- practical interpretation.

Do not assume that a statistically significant relationship is
agriculturally important.

---

# BQ2 — Crop Yield Prediction

## Question

How accurately can crop yield be predicted using the variables available
in the dataset, and which variables contribute most to predictive
performance?

## Expected analysis

Compare appropriate predictive approaches including:

- baseline prediction;
- linear regression;
- Random Forest;
- gradient boosting.

Use consistent evaluation data and methodology.

## Evaluation

Report appropriate metrics including:

- MAE
- RMSE
- R²

Where appropriate, examine model performance by important subgroups such
as crop type.

Consider both predictive performance and interpretability.

---

# BQ3 — Additional GenAI-Assisted Insights

## Question

Which additional findings identified through the GenAI-assisted
workflow are sufficiently reliable, reproducible and interpretable to
support further agricultural investigation?

## Important distinction

An AI-generated observation is not automatically a business finding.

Candidate findings require deterministic analytical evidence and
verification before acceptance.

---

# Project Evaluation Question

## EQ1

Does a GenAI-assisted analytics workflow improve analytical depth,
efficiency, reproducibility and communication compared with the
traditional BI workflow, and what additional risks or verification
requirements does it introduce?

## Evaluation dimensions

Where evidence is available, compare:

- development time;
- analytical breadth;
- number of analyses;
- additional verified insights;
- reproducibility;
- AI errors;
- correction/rejection rates;
- independent replication;
- human verification effort;
- dashboard usability.

Do not invent historical measurements that were not recorded.

Clearly distinguish measured values from estimates.
