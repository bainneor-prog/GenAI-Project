# Reproducibility report

Python 3.12.14 is recorded and requirements.in/requirements.txt are present. Matplotlib 3.11.2 is now declared directly and pinned in the regenerated lock. The local non-OneDrive environment installs the lock successfully and pip check reports no broken requirements. dashboard/app.py compiles successfully. The earlier OneDrive environment issue is retained as historical context; verification used the local copy.

The source data and deterministic outputs remain unchanged. Model configuration and random seeds are stored in results/model_configuration.json and results/model_metrics.csv. The full suite passes 49 tests when the temporary directory is writable. The Phase 4 script runs in an isolated output copy with exit code 0 and produces the preserved interaction-results hash. After dependency remediation, pip-audit 2.10.1 completed with exit code 0 and reported no known vulnerabilities; the JSON report is preserved.

## Phase 12 follow-up evidence

Phase 4 source search found analysis/phase4_interaction_nonlinear.py and its plan, tests, outputs and audit-package copies. No Git history is available in this checkout. The script is therefore recoverable as current project evidence and reproducible, but historical provenance of when it was originally created cannot be established. Human acceptance is required for this residual provenance limitation before any later phase.

