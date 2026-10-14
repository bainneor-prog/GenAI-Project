# Independent AI Audit Report: Crop Yield GenAI Analytics

**Status:** Advisory audit recommendations. No human-verification status has been changed. All seven candidate findings remain UNVERIFIED for the human analyst.
**Dataset checked:** `Crop_Yield_original.csv`, SHA-256 `58d1866b7a01519593b68c9c929007d10051d070aa957773589f136065cc5f1c`, matches the approved checksum.
**Method note:** Every numerical check here is non-blind. I had already seen the primary outputs before recalculating. Blind replication belongs to Phase 8 and is planned separately in `PHASE8_BLIND_REPLICATION_PLAN.md`.

---

## 1. Executive summary

The numerical base is sound. Of 81 independent checks, 75 reproduced exactly, 1 reproduced with a specification caveat, 0 failed, and 5 could not be compared because no primary value exists. The dataset is intact, the leakage controls are correctly implemented, and no finding rests on an arithmetic error.

The main problems are interpretive:

1. **F006 (predictive performance) is framed against a weak benchmark.** The global-mean baseline gives a holdout RMSE of 23.99. A crop-mean lookup, which the package does not include, gives 1.68. Gradient boosting gives 1.03 to 1.09 across split seeds. The models add about 0.6 RMSE over crop identity. Within-crop holdout R² is only 0.52 to 0.60. (AUD-01, HIGH)
2. **F005 interprets Cotton coefficients while a D017 gate is open.** Cotton's RESET p is 0.0186, which I reproduced. D017 requires interpretation to be withheld until that is resolved. (AUD-02, HIGH)

Verdicts: 5 SUPPORTED, 2 CORRECTION_REQUIRED, 0 REJECTED, 0 UNABLE_TO_VERIFY. Issues: 0 CRITICAL, 2 HIGH, 3 MEDIUM, 10 LOW, 2 INFORMATIONAL.

**Readiness for Phase 8:** Remediation is needed first. Fix AUD-01 and AUD-02, and resolve the F005 wording, before blind replication. The numerical results themselves do not need rework.

---

## 2. Materials examined

I read every file in `AI_Audit_Package.zip` (41 files), including:

- Governance: `PROJECT_SPEC.md`, `METHODOLOGY.md`, `DECISIONS.md` (D001–D017), `HUMAN_VERIFICATION.md`, `ANALYSIS_RULES.md`, `AUDIT_INSTRUCTIONS.md`, `README.md`, `MISSING_EVIDENCE.md`.
- Data: `Crop_Yield_original.csv`, `dataset_manifest.json`, `DATA_DICTIONARY.md`, `DATA_PROVENANCE.md`.
- Outputs: `baseline_reproduction.csv`, `baseline_methodology_review.md/.csv`, `interaction_results.csv`, `phase4_interaction_summary.json`, `cotton_fertiliser_spline_*`, `model_metrics.csv`, `model_configuration.json`, `analysis_register.csv`, `findings.json`, `claim_register.csv`.
- Code (read, not executed by the audit): the relevant sections of `reproduce_baseline.py`, `phase4_interaction_nonlinear.py`, `cotton_fertiliser_spline_sensitivity.py` and `phase5_bq2_modelling.py`. I did not read `validate_baseline_methods.py` or the test files in full.
- Plans: Phase 2.5, Phase 4, Phase 5, and the spline sensitivity plan.

I did not run the project's own scripts. Every recalculation was written independently in `audit_work/recalc.py` and `audit_work/extra_checks.py`, using scipy, statsmodels and scikit-learn in an isolated venv. The package and the original data were not modified.

---

## 3. Scope and limitations

- **In scope:** dataset integrity, baseline ANOVA and OLS, Pearson correlations, Phase 4 interaction and nonlinear tests (partly), Phase 5 predictive models and permutation importance, and all seven candidate findings.
- **Partly in scope:** the Phase 4 omnibus interactions A046–A051. I reviewed their specifications and correction logic by reading the code, but did not recompute them. The A052 synthesis was also not recomputed.
- **Not in scope:** the spline sensitivity A055 beyond the linear RESET test. The exact linear specification is not fully recoverable from the package (19 parameters recovered vs 20 reported).
- **Provenance:** UNKNOWN. Nothing here establishes whether the data are observed, synthetic or simulated. Any statement about real-world agriculture is out of scope.
- **Environment:** Python 3.13.16 with scikit-learn 1.9.1, statsmodels 0.15.0, scipy 1.18.1 and pandas 3.0.6. The manifest specifies Python 3.12.14. Results did not depend on this in my runs.

---

## 4. Dataset integrity findings

| Check | Result |
|---|---|
| SHA-256 matches approved checksum | Yes (verified) |
| Rows / columns | 10,000 / 19 (verified) |
| Missing values | 0 in all columns (verified) |
| Exact duplicate rows | 0 (verified) |
| Duplicates on 18 predictors, target excluded | 0 (verified) |
| Maximum absolute correlation among numeric predictors | 0.027 (verified) |
| Provenance, units, generation status | UNKNOWN (documented) |

**Finding:** Integrity controls are correct, and the checksum reference is used consistently. Provenance remains the main limitation, as the package itself states.

**Concern (AUD-04):** Within-crop SDs are nearly identical (Cotton 1.73, Maize 1.70, Potato 1.68, Rice 1.66, Sugarcane 1.64, Wheat 1.65), and crop identity explains about 99.5% of variance. These patterns are consistent with structured data generation. They do not establish it, and I do not infer it. Findings must stay within-dataset until provenance is documented.

**Legacy workbook discrepancy (AUD-10):** The baseline workbook used fewer rows for four crops than the canonical subsets (for example Rice 1,699 vs 1,702). D009 documents this, and the canonical rows are authoritative. The legacy values keep their MATERIAL DIFFERENCE status.

---

## 5. Statistical-methodology findings

**Verified and reproduced**

- **Pearson correlations (A004–A009, A016–A022).** All r values match to 1e-8. Fisher 95% CIs, not in the source output, are now computed (see AUD-06 and section 9).
- **Classical ANOVA for irrigation and soil (A010–A015, A023–A028).** All F statistics and p-values match. Welch p-values match the review table to 1e-5.
- **Brown-Forsythe screen.** No irrigation test is flagged, so classical ANOVA is consistent with D014. The Cotton soil test is flagged (Brown-Forsythe p = 0.039) and the review recommends Welch there. The review classifies the Potato soil test as acceptable.

**Concerns**

- **Non-significance language (F004).** The claim correctly states that non-significance is not evidence of no effect. However, its limitation text cites Welch as relevant for irrigation, which the screen does not support (AUD-07). No power or equivalence bound is given.
- **Pooled versus within-crop (F003).** The attenuation is real: pooled r = 0.031 (95% CI 0.012–0.051) against within-crop r of 0.40–0.48. The mechanism is plausible, but I did not test it (AUD-08).
- **Multiple testing.** The baseline has 84 coefficient tests. D016 requires Holm control for confirmatory families. These are descriptive analyses, but the family should be disclosed (AUD-03).

---

## 6. Interaction and nonlinear findings

I reproduced the Cotton fertiliser quadratic (A054) exactly, with HC3 standard errors and the Phase 4 covariate set:

| Quantity | Primary | Independent |
|---|---|---|
| Coefficient on z(Fertilizer_Used)² | −0.0513011 | −0.0513011 |
| HC3 p-value | 0.00579146 | 0.00579146 |
| Holm-adjusted p (×4 Cotton quadratics) | 0.0232 | 0.0232 |
| Incremental R² | 0.00203866 | 0.00203867 |

**Reading of the result.** The Holm adjustment is applied within four Cotton quadratic terms, and the result survives it at 0.05. However, the quadratic was added after the Cotton RESET flag, so it is diagnostic-triggered. It is in-sample, with adjusted R² gains of about 0.002. The global quadratic tests are not significant (Holm 0.52–0.89). The spline and quadratic fits pass RESET, and the linear fit does not (p = 0.0176, reproduced within 1e-5).

**Omnibus interactions (A046–A051).** I reviewed the code. The omnibus tests use HC3 Wald statistics, and the Holm correction is applied within each analysis. The lowest raw p-value is 0.0546 (Crop × Soil_Moisture), and no family survives correction. The global synthesis (A052) corrects across 9 omnibus p-values, more than the six families the plan declares. This is conservative and does not change the conclusion; the global minimum adjusted p is 0.49 (AUD-11).

**Verdict on the nonlinear result.** It is numerically correct and nominally supported, but it is not a candidate finding and should not be promoted without a human decision. It must not be used to infer an optimum or a fertiliser response (AUD-05).

---

## 7. Predictive-modelling findings

**Design (verified).** Split before preprocessing, with a stratified 80/20 split on Crop_Type. Preprocessing is inside pipelines. The target is excluded from predictors. Five-fold CV is run on the training partition only. There is no target-derived predictor and no duplicate across partitions.

**Reproduced exactly.** Baseline holdout RMSE 23.9955; linear 1.1197; Random Forest 1.1662; gradient boosting 1.0899; gradient boosting holdout R² 0.9979. Five-fold CV and holdout MAE also match, and so do all within-crop holdout R² values.

**Robustness across split seeds (new check, seeds 1–5):**

| Seed | Linear RMSE | Gradient boosting RMSE | Crop-mean RMSE |
|---|---|---|---|
| 1 | 1.0869 | 1.0478 | 1.6837 |
| 2 | 1.0585 | 1.0478 | 1.6474 |
| 3 | 1.0749 | 1.0590 | 1.6951 |
| 4 | 1.0776 | 1.0322 | 1.6657 |
| 5 | 1.0923 | 1.0629 | 1.7021 |

Gradient boosting beats linear regression on all five seeds, by 0.01 to 0.05 RMSE. So "gradient boosting best" is supported as a comparative claim. The margin is small.

**The main concern (AUD-01).** The global-mean benchmark exaggerates the gain. Crop identity alone gives holdout R² 0.9951. The models improve RMSE over that by about 0.6, and within-crop holdout R² is 0.52–0.60. The claim that models "substantially outperform the mean baseline" is correct but incomplete. A crop-mean benchmark should be the headline comparison.

**Limitations to keep.** Single split and single model seed per comparison; no hyperparameter-selection history (AUD-12); "synthetic structure" is noted as a possibility but not established (AUD-04).

---

## 8. Feature-importance findings

**Reproduced exactly (RF, holdout, 10 repeats, RMSE scoring):** Crop_Type 32.5964 (SD 0.293), Fertilizer_Used 0.4828 (SD 0.0185), Rainfall 0.3506 (SD 0.0085), Soil_Moisture 0.1275.

**Stability.** The top-four ranking is identical under a second permutation seed (Crop_Type, Fertilizer_Used, Rainfall, Soil_Moisture).

**Interpretation.** The ranking is predictive, as the claim says. Crop_Type's dominance reflects the between-crop structure already discussed. The collinearity caveat in F007 does not apply materially, since predictors are essentially uncorrelated (max |r| = 0.027). The claim should drop that caveat and mention Soil_Moisture as third (AUD-09).

---

## 9. AI-specific risks

**Risks observed**

- **Benchmark selection (AUD-01).** A weak comparator makes a true result look more impressive than it is.
- **Diagnostic-triggered interpretation (AUD-02, AUD-05).** Interpreting a model after a specification warning is an overreach that D017 is designed to prevent.
- **Declared-versus-implemented mismatches (AUD-11, AUD-13).** Code does not always match the plan's family structure, and the package is not self-contained.
- **Stale documentation (AUD-14).** The README still lists the Phase 4 file as missing.

**Risks checked and not found**

- No fabricated statistics: every numerical claim traced to a deterministic output and reproduced.
- No target leakage, no duplicate-driven inflation, and no preprocessing before the split.
- No causal language in the candidate findings. "Associated with" and "conditional association" wording is used.

**Workflow controls that worked**

- The Phase 2.5 review rejected the baseline statement that irrigation is "underperforming", on the grounds that a non-significant test does not establish it (AUD-17).
- Decisions D014–D017 gated specific analyses before they could be reported.
- Non-significant and contrary results (for example Potato soil, AUD-15) were retained.

---

## 10. Finding-by-finding verdicts

| Finding | Analyses | Verdict | Severity | Main reason |
|---|---|---|---|---|
| F001 Crop means | A002 | SUPPORTED | NONE | Reproduced; descriptive; scope limited by provenance |
| F002 Fertiliser correlations | A004–A009 | SUPPORTED | LOW | Reproduced; CIs should be added (AUD-06) |
| F003 Rainfall correlations | A016–A022 | SUPPORTED | LOW | Reproduced; mechanism untested (AUD-08) |
| F004 Irrigation ANOVA | A010–A015 | SUPPORTED | LOW | Reproduced; limitation text needs correction (AUD-07) |
| F005 Crop OLS | A029–A034 | CORRECTION_REQUIRED | HIGH | Cotton interpreted despite open RESET flag (AUD-02); covariate set and HC3 (AUD-03) |
| F006 Predictive models | A056–A059 | CORRECTION_REQUIRED | HIGH | Benchmark framing overstates gain (AUD-01) |
| F007 Permutation importance | A060 | SUPPORTED | LOW | Reproduced and stable; caveat overstated (AUD-09) |

Full detail is in `FINDING_AUDIT_REGISTER.csv`.

---

## 11. Independently reproduced numerical checks

**Totals:** 81 checks. 75 REPRODUCED. 1 PARTIAL_SPEC_CAVEAT (A055 linear RESET p matches to 1e-5, but parameter count is 19 vs 20 in the primary). 0 NOT_REPRODUCED. 5 UNABLE_TO_ASSESS (no primary comparator: A054 Rainfall, Soil_Moisture and Wind_Speed quadratics, the new crop-mean benchmark, and split-seed sensitivity).

**Key checks**

| Check | Primary | Independent |
|---|---|---|
| Holdout RMSE, gradient boosting | 1.0899 | 1.0899 (within 1e-6) |
| Holdout RMSE, Random Forest | 1.1662 | 1.1662 |
| Holdout RMSE, linear | 1.1197 | 1.1197 |
| Holdout RMSE, baseline | 23.9955 | 23.9955 |
| Permutation importance, Crop_Type | 32.5964 | 32.5964 |
| Cotton quadratic p (HC3) | 0.00579146 | 0.00579146 |
| Irrigation ANOVA p, Sugarcane | 0.8335 | 0.8335 |
| Pooled rainfall r | 0.031213 | 0.031213 |

The complete list is in `INDEPENDENT_RECALCULATIONS.csv`.

---

## 12. Prioritised corrective actions

1. **(HIGH, AUD-02)** Withhold Cotton coefficient interpretation in F005 until the RESET warning is resolved, as D017 requires. Keep Cotton adjusted R² as descriptive only.
2. **(HIGH, AUD-01)** Add a crop-mean benchmark and within-crop metrics to F006. Reword the headline as incremental improvement over crop means, and report split-seed spread.
3. **(HIGH, AUD-14, AUD-13, AUD-16)** Fix the stale README, state the Python version and run instructions, and run a near-duplicate check across partitions.
4. **(HIGH, AUD-17 practice)** Keep the Phase 2.5-style interpretation review for all future candidate findings.
5. **(MEDIUM, AUD-03)** State the covariate set in F005, run HC3 for all coefficients, and disclose the 84-test family.
6. **(MEDIUM, AUD-04)** Keep all wording within-dataset. Require documented provenance before any real-world claim.
7. **(MEDIUM, AUD-05)** Do not promote the Cotton curvature without a human decision. If promoted, label it in-sample and diagnostic-triggered, and make no optimum claim.
8. **(MEDIUM, AUD-11, AUD-12)** Align the A052 synthesis with the six declared families. Document any holdout use in hyperparameter choice.
9. **(LOW)** Add CIs to F002, correct the F004 limitation text, reword F003 and F007 as indicated, and record A025 in the register.

---

## 13. Unresolved questions

1. **Provenance.** Who generated or collected the data, and how? Until this is answered, no real-world claim is supportable.
2. **Cotton RESET.** What is the functional-form problem in the Cotton regression, and does the quadratic term resolve it?
3. **Hyperparameters.** Were any Phase 5 hyperparameters chosen on holdout data?
4. **Holm families.** Should A052 use the declared six families or the nine omnibus p-values?
5. **Soil_Type Potato (A025).** Should this significant-after-Holm soil result become a candidate finding?
6. **Near-duplicates.** Are there near-duplicate observations across train and holdout at any tolerance?
7. **Spline specification.** What exact design produced the 20-parameter linear model in A055?

---

## 14. Final assessment of analytical reliability

**Numerically:** reliable. Every checked output reproduced, and the leakage controls are correctly implemented.

**Methodologically:** mostly sound. The main gaps are the benchmark choice in F006 and the open D017 gate in F005.

**Interpretively:** needs correction before the findings are presented. The numbers are right, but the framing overstates what is known.

**Overall:** the project is suitable for internal review and correction. It is not yet ready for Phase 8 blind replication. I have not approved Phase 8, and this audit does not change any human-verification status.

---

## 15. Required summary counts

| Item | Count |
|---|---|
| Candidate findings reviewed | 7 |
| SUPPORTED | 5 |
| CORRECTION_REQUIRED | 2 |
| REJECTED | 0 |
| UNABLE_TO_VERIFY | 0 |
| CRITICAL issues | 0 |
| HIGH issues | 2 |
| MEDIUM issues | 3 |
| LOW issues | 10 |
| INFORMATIONAL observations | 2 |
| Independent numerical checks attempted | 81 |
| Reproduced successfully | 75 |
| Reproduced with specification caveat | 1 |
| Not reproduced | 0 |
| Unable to assess | 5 |

**Recommendation:** Remediate AUD-01 and AUD-02 before Phase 8. Then re-run this audit's checks on the corrected wording. Do not approve Phase 8 automatically.

