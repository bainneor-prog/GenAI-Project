# AGENTS.md

You are working on a university Generative AI in Business Intelligence
and Data Analytics project.

Read these documents BEFORE making analytical or architectural changes:

- docs/PROJECT_SPEC.md
- docs/METHODOLOGY.md
- docs/BUSINESS_QUESTIONS.md
- docs/ANALYSIS_RULES.md
- docs/HUMAN_VERIFICATION.md
- docs/DECISIONS.md

## Non-negotiable rules

1. Python calculations are the numerical source of truth.
2. Never fabricate, manually insert or infer statistical results.
3. Never convert association into causation.
4. Preserve the original dataset unchanged.
5. Every formal analysis must have an Analysis ID.
6. Every formal finding must link to analytical evidence.
7. AI interpretations remain unverified until reviewed.
8. Separate exploratory dashboard analysis from validated findings.
9. Avoid cherry-picking significant results.
10. Report negative/non-significant findings where relevant.
11. For predictive models, prevent leakage and preserve train/test
    separation.
12. Use fixed random seeds where applicable.
13. Report comparable model metrics using identical evaluation data.
14. Consider effect size and practical significance, not p-values alone.
15. Dashboard statistics must originate from generated result files,
    never hard-coded values.
16. Preserve auditability and reproducibility.
17. Do not silently change the methodology.
18. If methodology appears statistically inappropriate, flag the issue
    for human review rather than silently replacing it.
19. Document significant GenAI contributions and corrections.
20. Human verification is the final authority for findings.

When uncertain, prefer transparency over automation.

