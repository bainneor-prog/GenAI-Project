# Phase 8 Unblinding and Independent Replication Comparison

The frozen ZIP was preserved unchanged. SHA-256: `E5E1C18F1B76BF7CC06FD7B18078CBC330BC32B2EBD4C2E9E9C2059C3C043F3F`. Its dataset hash matches the authoritative source hash `58d1866b7a01519593b68c9c929007d10051d070aa957773589f136065cc5f1c`.

## Plain-English summary

The independent replication reproduces the main correlation, irrigation, rainfall, and feature-importance patterns. Differences are generally small and arise from explicit methodological choices such as split seeds, model configurations, bootstrap intervals, and broader specifications. The independent five-seed predictive analysis ranks linear regression best on average, whereas the primary fixed configuration ranks gradient boosting best. This is a model-configuration and evaluation-design difference, not evidence that either result should be overwritten.

The independent report marks A1, A4 and A5 partially completed because the original analysis register and exact fixed specifications were unavailable to the blind reviewer. Those comparisons are therefore incomplete, not successful replications.

## Finding assessment recommendations

- F001: supports the descriptive crop-yield differences; independent package confirms crop counts and dataset integrity.
- F002: supports the crop-specific fertiliser correlations; Q1 values reproduce the primary A004-A009 values to displayed precision.
- F003: supports the pooled-versus-within-crop rainfall contrast; A7 reproduces pooled r≈0.0312 and crop-specific values. The within-centred result is additional independent evidence, not a replacement.
- F004: supports the non-significant irrigation interpretation; classical ANOVA statistics agree and independent Welch/Holm checks remain non-significant.
- F005: partially supports model fit magnitude, but does not clear D017. Independent A4 is partially completed and uses an expanded operational specification; coefficient interpretation remains withheld.
- F006: partially supports strong predictive performance and the crop-mean benchmark. Model ranking differs because Phase 8 used five seeds, different gradient-boosting/RF configurations, and a documented standardized linear pipeline. No real-world generalisation claim is justified.
- F007: supports the broad ranking that Crop_Type dominates, followed by Fertilizer_Used and Rainfall. Independent permutation importance used three permutation seeds and 20 repeats; values are close but not identical.

All recommendations are comparison results only. All findings remain `UNVERIFIED`.

