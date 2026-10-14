# Project Decision Log

This document records important methodological, analytical and
governance decisions made during the project.

Routine coding and UI implementation decisions do not need to be
recorded unless they materially affect analytical results,
reproducibility or project methodology.

---

## D001 — Deterministic Python as Numerical Authority

Date: 2026-09-09

Decision:
All formal numerical analytical results will be calculated using
executable Python rather than supplied directly by a Generative AI
model.

Reason:
LLM-generated numerical responses may be incorrect or non-reproducible.
Separating AI reasoning/code generation from deterministic computation
improves reproducibility and auditability.

Decision owner:
Human analyst

Status:
APPROVED

---

## D022 — External Split-Seed Evidence

Decision:
External split-seed sensitivity evidence may be retained as advisory
evidence, clearly labelled as not independently reproduced within the
primary repository.

Status:
APPROVED

---

## D023 — Cotton Regression Specification Hold

Decision:
The original Cotton regression model will not be changed at this stage.
The D017 interpretation restriction remains in force, and Phase 8 will
assess robustness.

Status:
APPROVED

---

## D024 — Phase 8 Candidate Findings

Decision:
All seven candidate findings may enter blind replication in Phase 8,
with F005 and F006 prioritised.

Status:
APPROVED

---

## D025 — Finding Status Hold

Decision:
All candidate finding statuses remain UNVERIFIED until Phase 9 human
review.

Status:
APPROVED

---

## D002 — Separate Exploratory and Verified Findings

Date: 2026-09-09

Decision:
Interactive dashboard exploration will not automatically create formal
business findings.

Reason:
Unrestricted filtering and repeated testing may identify coincidental
patterns. Important observations must enter the formal analysis and
verification workflow before being reported as verified findings.

Decision owner:
Human analyst

Status:
APPROVED

---

## D003 — Independent AI Review

Date: 2026-09-09

Decision:
Important candidate findings will be reviewed by a separate LLM where
practical.

Reason:
The independent reviewer provides an adversarial check for analytical,
coding and interpretation errors.

AI agreement will not replace deterministic evidence or human
verification.

Decision owner:
Human analyst

Status:
APPROVED

---

## D004 — Preserve Non-Significant Results

Date: 2026-09-09

Decision:
Relevant non-significant and contradictory results will be retained.

Reason:
The project evaluates analytical evidence rather than attempting to
prove predetermined hypotheses.

Decision owner:
Human analyst

Status:
APPROVED

---

## D005 — Phase 1 Dataset Identity Reference

Date: 2026-09-13

Decision:
The SHA-256 checksum calculated during Phase 1 is the authoritative
source-data checksum for this project from Phase 1 onward. It is not
retrospective proof of the dataset's original provenance.

The raw worksheet in the baseline workbook is a secondary consistency
reference. It is not independent provenance evidence.

Reason:
These controls provide a reproducible project reference while avoiding
claims that are not supported by historical provenance records.

Decision owner:
Human analyst

Status:
APPROVED

---

## D006 — Metadata and Provenance Classification

Date: 2026-09-13

Decision:
A formal data dictionary will classify metadata as CONFIRMED, INFERRED,
or UNKNOWN. Undocumented units, measurement methods, and scientifically
valid ranges must not be inferred as facts.

Dataset provenance and whether the data are observed, synthetic,
simulated, augmented, or otherwise generated will remain UNKNOWN /
PROVENANCE NOT YET CONFIRMED until supported by documentary evidence.

Reason:
Explicit uncertainty prevents assumptions from becoming unsupported
project facts.

Decision owner:
Human analyst

Status:
APPROVED

---

## D007 — Python Dependency Management

Date: 2026-09-13

Decision:
The project will use pip-tools for reproducible Python dependency
management.

Direct project dependencies will be maintained in:

requirements.in

The complete resolved dependency environment will be locked in:

requirements.txt

using pip-compile.

The Python version used by the analytical environment will also be
recorded.

Reason:
This approach provides a human-readable list of intentional
dependencies while also preserving exact resolved package versions for
reproducibility.

Dependency changes must be made through requirements.in followed by
regeneration of requirements.txt and execution of the project tests.

Status:
APPROVED

---

## D008 — Phase 2 Approval Gate

Date: 2026-09-13

Decision:
Phase 2 is not authorised. Phase 1.5 reproducibility and metadata work
must be completed and returned for human review before analysis begins.

Reason:
Dependency, metadata, and provenance controls must be established before
analytical results are produced.

Decision owner:
Human analyst

Status:
APPROVED

---

## D009 — Canonical-Row Python Regressions

Date: 2026-09-13

Decision:
For Phase 2 baseline reproduction, Python regression results calculated
from the full canonical dataset are approved as the authoritative
reproduced results.

Historical Excel results remain preserved as baseline evidence but are
not treated as authoritative where inconsistent or truncated input
ranges were used.

Reason:
The new project requires reproducible analysis from the validated source
dataset and must not alter calculations to force agreement with legacy
workbook ranges.

Decision owner:
Human analyst

Status:
APPROVED

---

## D010 — Irreproducible Baseline Analyses

Date: 2026-09-13

Decision:
A003, A036 and A037 are accepted as UNABLE TO REPRODUCE unless
additional traceable numeric baseline evidence becomes available.

Reason:
The existing baseline materials do not contain sufficient numeric
evidence to reconstruct these analyses with confidence.

No reverse-engineering from qualitative prose is permitted.

Decision owner:
Human analyst

Status:
APPROVED

---

## D011 — Baseline Method Validation

Date: 2026-09-13

Decision:
Baseline ANOVA and regression methods will undergo methodological
validation before their interpretations are reused in the revised
analysis.

Reason:
Phase 2 established numerical reproduction where possible, but the
baseline does not document assumption checks, multiple-testing controls,
or consistent regression input ranges.

Decision owner:
Human analyst

Status:
APPROVED

---

## D012 — A001 Tied-Mode Difference

Date: 2026-09-13

Decision:
A001 will remain MATERIAL DIFFERENCE because the discrepancy is
attributable to differing tied-mode conventions rather than an
implementation error.

Reason:
Both calculations are internally valid under different mode
definitions. The difference remains explicit rather than being forced
into a MATCH classification.

Decision owner:
Human analyst

Status:
APPROVED

---

## D013 — Phase 2 Baseline Reproduction Authorisation

Date: 2026-09-13

Decision:
Phase 1 and Phase 1.5 were reviewed and approved. Phase 2 is authorised
only for reproduction of selected analyses from the traditional BI
baseline. New exploratory analysis, predictive modelling, dashboard
analysis, and new business findings remain outside the authorised scope.

Reason:
Baseline reproduction establishes whether the Python pipeline can
reproduce the prior work before the project proceeds to new analysis.

Decision owner:
Human analyst

Status:
APPROVED

---

## D014 — Welch ANOVA for Unequal Variance

Date: 2026-09-13

Decision:
For later formal mean comparisons, Welch ANOVA is approved as the
primary method when a documented unequal-variance diagnostic is
flagged. The corresponding classical ANOVA result will remain preserved
as baseline evidence.

Reason:
Welch ANOVA provides inference that does not require equal group
variances while preserving transparency about the originally reproduced
method.

Decision owner:
Human analyst

Status:
APPROVED

---

## D015 — Robust Regression Inference and Specification Review

Date: 2026-09-13

Decision:
HC3 heteroscedasticity-robust standard errors are approved for later
formal OLS inference. Documented Ramsey RESET warnings must be
investigated before the affected regression interpretation is reused.

The approved full-canonical-row model results and historical baseline
evidence will remain preserved; observations and model terms must not be
silently removed or changed.

Reason:
Robust standard errors reduce reliance on constant residual variance,
while RESET warnings require explicit investigation of possible
functional-form misspecification.

Decision owner:
Human analyst

Status:
APPROVED

---

## D016 — Multiple-Testing Control

Date: 2026-09-13

Decision:
Later confirmatory analyses must define their related testing families
in advance and apply Holm family-wise error control while retaining all
raw and adjusted results.

For a separately labelled broader exploratory or discovery family, a
Benjamini–Hochberg false-discovery-rate procedure may be used when the
family and purpose are documented before interpretation.

Reason:
The baseline contains multiple related ANOVA and regression coefficient
tests. Explicit families and suitable correction reduce selective
reporting and inflated false-positive risk.

Decision owner:
Human analyst

Status:
APPROVED

---

## D017 — Interpretation of Diagnostically Flagged Regressions

Date: 2026-09-13

Decision:
Interpretation of a regression with a documented specification warning
will be withheld until the warning has been investigated and the method
has been shown suitable for the intended question.

Diagnostic flags do not authorise automatic observation deletion,
unreported model replacement, or causal interpretation.

Reason:
Reusing an interpretation before resolving a material model-specification
concern could overstate what the fitted model supports.

Decision owner:
Human analyst

Status:
APPROVED

