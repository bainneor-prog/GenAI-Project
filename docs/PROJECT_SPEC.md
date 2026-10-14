# Crop Yield GenAI Analytics — Project Specification

## 1. Project Overview

This project extends a previous Business Intelligence crop-yield analysis
that used traditional analytical methods and Power BI.

The purpose of the new project is to evaluate whether a Generative
AI-assisted analytics workflow can improve analytical depth,
development efficiency, reproducibility and communication while
maintaining statistical validity, transparency and human oversight.

The project therefore has two related purposes:

1. Produce an expanded analysis of the crop-yield dataset.
2. Evaluate the benefits and limitations of using Generative AI within
   a Business Intelligence and Data Analytics workflow.

The original traditional BI project will remain the comparison baseline.

---

## 2. Previous Project

The original project analysed a dataset containing approximately
10,000 crop observations.

Variables include agricultural and environmental information such as:

- crop type;
- fertiliser use;
- nitrogen, phosphorus and potassium;
- irrigation;
- soil characteristics;
- rainfall;
- soil moisture;
- environmental variables;
- crop yield.

The original workflow included:

- data preparation;
- exploratory data analysis;
- descriptive statistics;
- correlation analysis;
- ANOVA;
- regression;
- Excel-based analysis;
- Power BI visualisation.

The original analysis is preserved in the `/baseline` directory.

Previous results must be treated as a benchmark rather than assumed
to be correct.

---

## 3. Revised Project Scope

The revised project will extend the original analysis using a
GenAI-assisted Python analytics workflow.

The project will investigate:

- descriptive patterns;
- crop-specific relationships;
- interactions between variables;
- potentially nonlinear relationships;
- predictive modelling;
- model performance;
- analytical reproducibility;
- GenAI efficiency;
- GenAI reliability;
- human verification requirements.

---

## 4. Generative AI Role

Generative AI may assist with:

- analytical planning;
- Python code generation;
- exploratory analysis;
- identification of candidate relationships;
- statistical workflow development;
- predictive modelling development;
- visualisation;
- dashboard development;
- interpretation of deterministic results;
- documentation;
- code review;
- identification of possible analytical weaknesses.

Generative AI is NOT the numerical source of truth.

All formal numerical results must originate from executable,
reproducible analytical code.

---

## 5. Technology

Primary development environment:

- Python
- Pandas
- NumPy
- SciPy
- statsmodels
- scikit-learn
- Plotly
- Streamlit

Primary GenAI development assistant:

- Codex

Independent AI reviewer:

- A separate LLM/provider where practical.

Exact model names and versions used during the project should be
recorded in the AI experiment log.

---

## 6. Major Deliverables

The project should produce:

1. Validated source dataset and dataset manifest.
2. Reproducible Python analytical pipeline.
3. Reproduction of selected traditional BI analyses.
4. Expanded descriptive and diagnostic analysis.
5. Interaction analysis.
6. Predictive modelling.
7. Analysis Register.
8. Finding/Claim Register.
9. Interactive Streamlit dashboard.
10. Analyst/Audit interface.
11. Independent AI audit package.
12. Human verification records.
13. GenAI experiment log.
14. Traditional BI versus GenAI comparison.
15. Documentation required to reproduce the analysis.

---

## 7. Dashboard

The application should provide two levels of access.

### Business View

Designed for straightforward interpretation:

- Overview
- Yield Drivers
- Interactions
- Prediction
- Verified Findings

### Analyst/Audit View

Designed for analytical transparency:

- Analysis ID
- question being investigated
- variables
- filters
- sample size
- analytical method
- deterministic results
- visual evidence
- underlying records where appropriate
- code/method reference
- AI interpretation
- independent review status
- human verification status

---

## 8. Out of Scope

Unless supported by additional appropriate data, the project will NOT:

- claim causal agricultural effects;
- determine optimal fertiliser application;
- make agronomic prescriptions;
- calculate profitability;
- estimate long-term environmental effects;
- manufacture missing information;
- present AI-generated numbers as analytical evidence.

---

## 9. Success Criteria

The project will be considered successful if it can:

- reproduce important baseline analyses;
- expand the analytical depth of the original project;
- generate reproducible statistical results;
- provide transparent evidence for important findings;
- compare predictive models appropriately;
- identify both useful and incorrect GenAI contributions;
- demonstrate human oversight;
- provide a usable interactive dashboard;
- provide evidence allowing traditional and GenAI-assisted workflows
  to be compared.

Success does NOT require GenAI to outperform the traditional workflow.

Finding limitations or failures of GenAI is a valid project outcome.
