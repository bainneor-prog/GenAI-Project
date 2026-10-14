# Phase 2.5 Baseline Methodology Review

Status: **UNVERIFIED — human review required**

This review validates only the ANOVA and OLS methods already reproduced in Phase 2. It does not introduce new exploratory questions or replace an approved baseline method.

## Scope and evidence

- Canonical source: `data/Crop_Yield_original.csv` (SHA-256 `58d1866b7a01519593b68c9c929007d10051d070aa957773589f136065cc5f1c`).
- A038 covers A010–A015 and A023–A028; A039 covers A029–A034.
- Independence, sampling, representativeness and temporal ordering remain unable to be verified because provenance is unknown.

## ANOVA review

| ID | Crop | Grouping | N | Classical p | Welch p | Brown–Forsythe p | Holm p | Eta² | Classification |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| A010 | Cotton | Irrigation_Type | 1666 | 0.872191 | 0.872573 | 0.764068 | 1 | 0.000423552 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A011 | Maize | Irrigation_Type | 1658 | 0.654824 | 0.654191 | 0.984971 | 1 | 0.000978773 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A012 | Potato | Irrigation_Type | 1670 | 0.621377 | 0.602028 | 0.250749 | 1 | 0.00106184 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A013 | Rice | Irrigation_Type | 1702 | 0.387333 | 0.358979 | 0.218733 | 1 | 0.00178114 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A014 | Sugarcane | Irrigation_Type | 1633 | 0.833514 | 0.833093 | 0.904067 | 1 | 0.00053159 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A015 | Wheat | Irrigation_Type | 1671 | 0.105062 | 0.118579 | 0.640972 | 0.630369 | 0.00367451 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A023 | Cotton | Soil_Type | 1666 | 0.0118678 | 0.00833424 | 0.0387928 | 0.0593388 | 0.00657912 | ALTERNATIVE RECOMMENDED |
| A024 | Maize | Soil_Type | 1658 | 0.880437 | 0.874198 | 0.357164 | 1 | 0.000404357 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A025 | Potato | Soil_Type | 1670 | 0.00337472 | 0.00267007 | 0.0922787 | 0.0202483 | 0.00817522 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A026 | Rice | Soil_Type | 1702 | 0.947021 | 0.945567 | 0.914485 | 1 | 0.000215906 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A027 | Sugarcane | Soil_Type | 1633 | 0.533894 | 0.530026 | 0.568698 | 1 | 0.00134315 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A028 | Wheat | Soil_Type | 1671 | 0.12075 | 0.119164 | 0.681677 | 0.482999 | 0.00348365 | METHOD ACCEPTABLE WITH LIMITATIONS |

Classical one-way ANOVA is limited by unverified independence. Unequal-variance flags lead to a recommendation for Welch ANOVA in later formal mean comparisons. Kruskal–Wallis may be considered for a rank/distribution question, but it is not a direct substitute for equality of means.

Holm adjustment is shown separately for the six irrigation tests and six soil tests. All raw results, including non-significant results, are retained.

## Regression review

| ID | Crop | N | BP p | JB p | RESET p | Max VIF | Cook > 4/N | Classification |
|---|---|---:|---:|---:|---:|---:|---:|---|
| A029 | Cotton | 1666 | 0.495243 | 0.32657 | 0.0185558 | 1.014 | 78.0 | ALTERNATIVE RECOMMENDED |
| A030 | Maize | 1658 | 0.684387 | 0.59868 | 0.678681 | 1.017 | 73.0 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A031 | Potato | 1670 | 0.422785 | 0.240688 | 0.744722 | 1.018 | 76.0 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A032 | Rice | 1702 | 0.559991 | 0.63927 | 0.395115 | 1.013 | 82.0 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A033 | Sugarcane | 1633 | 0.351678 | 0.0150341 | 0.642996 | 1.010 | 84.0 | METHOD ACCEPTABLE WITH LIMITATIONS |
| A034 | Wheat | 1671 | 0.237388 | 0.780894 | 0.437995 | 1.010 | 78.0 | METHOD ACCEPTABLE WITH LIMITATIONS |

The full canonical crop samples are authoritative under D009. The legacy Potato, Rice, Sugarcane and Wheat workbook regressions used truncated input ranges; their historical values remain evidence but are not authoritative.

Breusch–Pagan tests heteroscedasticity; Jarque–Bera flags residual non-normality; RESET flags possible functional-form misspecification. Cook's threshold is a screening flag only. Durbin–Watson is recorded in the CSV but cannot be given a time-series interpretation because row order and temporal coverage are unknown.

## Interpretation audit

- The baseline statement that irrigation is ‘underperforming’ because yield relates to rainfall and soil moisture but not irrigation is not supported. A non-significant irrigation ANOVA does not establish underperformance, and the design does not support causation.
- Regression coefficients support conditional association only. Model fit and significant coefficients do not establish agronomic effects, intervention benefits, external validity, or predictive performance.
- Negative and non-significant irrigation findings remain preserved. Soil and coefficient findings must not be selected without their testing-family context.

## Multiple testing

The baseline contains two families of six crop-level ANOVAs and 84 coefficient tests across six regressions. Selective use of unadjusted p-values inflates false-positive risk. For later confirmatory analysis, pre-specify families and primary outcomes, retain all tests, and use Holm control for a small confirmatory family. Benjamini–Hochberg may be proposed for a clearly labelled broader discovery family, subject to human approval.

## Human decisions

All four Phase 2.5 recommendations were approved on 2026-09-13:

1. Welch ANOVA will be primary for later formal mean comparisons where unequal variance is flagged; classical baseline results remain preserved (D014).
2. HC3 robust standard errors are approved, and RESET warnings require investigation (D015).
3. Confirmatory testing families must be defined in advance and use Holm correction; a documented discovery family may use Benjamini–Hochberg control (D016).
4. Regression interpretation will be withheld while a material specification warning remains unresolved (D017).

