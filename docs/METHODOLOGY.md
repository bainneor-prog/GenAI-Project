# Project Methodology

## Project purpose

This project evaluates whether a Generative AI-assisted analytics
workflow can improve the depth, efficiency, reproducibility and
communication of a previous traditional BI crop-yield analysis while
maintaining statistical validity, transparency and human oversight.

This is both:

1. an agricultural data analytics project; and
2. an experiment evaluating Generative AI in a BI workflow.

The previous project used Excel/statistical analysis and Power BI.
The new project must preserve the original project as the traditional
BI benchmark.

---

# Core analytical principle

Generative AI is an analytical assistant, NOT the source of
statistical truth.

AI may:
- propose analyses;
- generate Python;
- suggest interactions;
- generate visualisations;
- develop predictive models;
- help build the dashboard;
- generate candidate interpretations;
- review findings.

AI must NOT:
- invent numerical results;
- manually supply dashboard statistics;
- claim a finding is validated merely because an LLM produced it;
- make causal claims unsupported by the dataset.

All numerical analytical results must be calculated deterministically
from the source dataset using executable Python.

SOURCE OF TRUTH:

Original data
    ↓
Python calculation
    ↓
Structured deterministic result
    ↓
Candidate interpretation
    ↓
AI review
    ↓
Human verification
    ↓
Verified finding

---

# Business Questions

BQ1:
Which crop-specific relationships and interactions between fertiliser,
irrigation, soil and environmental conditions are most strongly
associated with crop yield?

BQ2:
How accurately can crop yield be predicted using the available
variables, and which variables contribute most to predictive
performance?

BQ3:
Which additional findings produced through the GenAI-assisted workflow
are sufficiently reliable and interpretable to support further
agricultural investigation?

PROJECT EVALUATION QUESTION:

Does a GenAI-assisted analytics workflow improve analytical depth,
efficiency, reproducibility and communication compared with the
original traditional BI workflow, and what additional risks or
verification requirements does it introduce?

---

# Dataset limitations

The dataset is static and observational.

Therefore:

- association must not be described as causation;
- statistical significance must not automatically be interpreted as
  practical/business significance;
- the analysis cannot establish long-term agricultural effects;
- profitability cannot be calculated without appropriate financial data;
- missing information cannot be invented or inferred by GenAI.

Preferred language:

"associated with"
"within this dataset"
"the analysis indicates"
"predictive relationship"

Avoid unsupported language:

"causes"
"will increase"
"optimal"
"best management practice"
"proves"

---

# Workflow

## Phase 1 — Dataset validation

Validate the original dataset before analysis.

Record:
- SHA-256 hash;
- row count;
- column count;
- column names;
- data types;
- missing values;
- duplicate records;
- invalid values;
- validation timestamp.

Generate:

results/dataset_manifest.json

The original source dataset must never be silently modified.

---

## Phase 2 — Reproduce traditional analysis

Before conducting new analyses, reproduce important analyses from the
previous BI project.

This establishes a baseline and tests the new Python pipeline.

Record comparisons between:
- previous result;
- new Python result;
- difference;
- validation status.

Do not alter the new calculation simply to make it agree with the
previous result.

Disagreement must be investigated and documented.

---

## Phase 3 — Descriptive and diagnostic analysis

Perform appropriate:
- descriptive statistics;
- distributions;
- correlations;
- ANOVA where appropriate;
- regression;
- effect sizes;
- confidence intervals.

Do not rely only on p-values.

Report practical magnitude as well as statistical significance.

---

## Phase 4 — Interaction analysis

Systematically investigate relevant interactions including:

- Crop × Fertiliser
- Crop × Rainfall
- Crop × Soil
- Crop × Irrigation
- Rainfall × Irrigation
- Soil × Fertiliser
- Soil Moisture × Irrigation

Additional interactions may be proposed but must be documented as
exploratory.

Avoid cherry-picking only significant relationships.

---

## Phase 5 — Non-linear relationships

Investigate whether important relationships are non-linear rather than
assuming linear relationships automatically.

Document the analytical method and justification.

---

## Phase 6 — Predictive modelling

Prediction must be separated conceptually from descriptive/diagnostic
analysis.

Compare models under equivalent conditions.

At minimum consider:
- simple baseline;
- linear regression;
- Random Forest;
- gradient boosting.

Use:
- train/test separation;
- consistent folds;
- fixed random seeds;
- cross-validation where appropriate.

Report:
- MAE;
- RMSE;
- R².

Check for:
- target leakage;
- train/test contamination;
- overfitting;
- inappropriate preprocessing;
- unfair model comparisons.

Do not report only the best model.

Consider interpretability as well as predictive performance.

---

# Analysis Register

Every formal analysis must receive a unique ID:

A001
A002
A003
...

Record:
- Analysis ID
- Business Question
- Analysis purpose
- Dataset
- Filters
- Variables
- Method
- N
- Code location
- Output location
- Statistical result
- Interpretation
- AI generated?
- Independent AI review
- Human verification
- Final status

Generate:

results/analysis_register.csv

---

# Finding Register

AI-generated interpretations are CANDIDATE FINDINGS until validated.

Finding IDs:

F001
F002
F003
...

Each finding must link to one or more Analysis IDs.

Statuses:

UNVERIFIED
VERIFIED
CORRECTION_REQUIRED
REJECTED
INCONCLUSIVE

No unverified finding may be presented as a verified business
conclusion.

---

# Independent AI Audit

Generate a portable audit package containing:

- dataset;
- data dictionary;
- methodology;
- analysis register;
- relevant Python code;
- deterministic results;
- candidate findings;
- audit instructions.

The package will be supplied to an independent LLM/provider.

The independent reviewer must check:
- data selection;
- methodology;
- calculations;
- interpretation;
- causal overreach;
- leakage;
- overfitting;
- unsupported claims.

Selected important findings will undergo blind replication.

---

# Human Verification

Human verification is the final authority.

For important findings check:

1. Data trace
2. Method appropriateness
3. Numerical spot-check
4. Visual inspection
5. Interpretation
6. Independent AI disagreements

Final human decisions:

ACCEPTED
CORRECTED
REJECTED
INCONCLUSIVE

Record verification time.

---

# Dashboard requirements

Build a Streamlit analytical application.

Business mode:

Overview
Drivers
Interactions
Prediction
Findings

Analyst/Audit mode must expose:

- deterministic results;
- Analysis ID;
- sample size;
- variables;
- filters;
- method;
- statistical outputs;
- interactive visual;
- underlying records;
- source result file;
- relevant Python method/code;
- AI interpretation;
- independent AI review;
- human verification.

Important dashboard numbers must be read from deterministic results.

Do NOT manually type analytical results into dashboard source code.

---

# Exploratory vs validated results

Interactive dashboard filtering is exploratory.

An interesting dashboard pattern does NOT automatically become a
formal finding.

To become a formal finding:

Exploratory observation
→ Analysis ID
→ deterministic analysis
→ candidate finding
→ independent review
→ human verification
→ final finding.

---

# GenAI Experiment

Record the use of GenAI throughout development.

For important GenAI tasks record:

- timestamp;
- model/tool;
- task;
- prompt or prompt reference;
- output;
- time taken;
- human intervention;
- accepted/corrected/rejected;
- reason.

Generate:

audit/ai_experiment_log.csv

The purpose is to compare GenAI-assisted analytics with the previous
traditional BI workflow.

Potential evaluation dimensions:

- development time;
- analytical breadth;
- number of analyses;
- additional verified insights;
- AI errors;
- correction rate;
- rejection rate;
- independent reproduction rate;
- human verification effort;
- reproducibility;
- dashboard usability.

Do not manufacture missing benchmark measurements.

Clearly distinguish measured values from estimates.

---

# Reproducibility

Running the pipeline again on the same dataset should reproduce
deterministic analytical results.

Lock random seeds where stochastic algorithms are used.

Store dependency versions.

Automated tests should verify important pipeline behaviour.
