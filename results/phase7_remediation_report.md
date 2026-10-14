# Phase 7 Independent Audit Remediation

## F006 predictive benchmark

Added A061, a crop-mean benchmark fitted on the training partition only and evaluated on the unchanged stratified holdout. Global-mean A056 remains historical context. Model outputs now include overall and crop-specific holdout metrics for the benchmarks and fitted models. No independently supplied split-seed sensitivity file was present in the repository; any such auditor result remains external evidence and is not represented as a Python calculation.

## F005 Cotton regression

Original A029 remains unchanged. F005 wording now withholds coefficient interpretations under D017 until the Cotton RESET/specification concern is resolved. The baseline covariates and HC3/multiple-testing limitations remain documented. No model replacement was performed.

## F001-F004 and F007

Claims were tightened to distinguish descriptive, diagnostic, and predictive evidence, preserve non-significant results, and avoid causal or real-world generalisation language.

## Evidence consistency and A055

The earlier missing Phase 4 report referred to the current checkout, while the independent auditor saw files available in the older checkout. The older files were recovered, hash-matched, and restored. A055 reports parameter counts 20 (linear), 21 (quadratic), and 23 (natural cubic spline); the difference is attributable to model specification and is documented, not corrected by changing results.

## Remaining limitations and human decisions

All findings remain UNVERIFIED. Human review is required before any finding is accepted. Human approval is required before changing the Cotton specification or treating external split-sensitivity evidence as repository-derived.

## Approved follow-up decisions

External split-seed evidence is retained as advisory and is not treated as independently reproduced. The original Cotton model remains unchanged under D017, with robustness assessment deferred to Phase 8. All seven findings may enter blind replication, prioritising F005 and F006. All statuses remain UNVERIFIED until Phase 9 human review.

