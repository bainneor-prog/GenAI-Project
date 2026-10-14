# Phase 12 audit report

This read-only audit covers Phases 0–11. Original datasets, frozen outputs, Phase 8 results, Phase 9 decisions and analytical methods were not modified.

## Results

- Dataset integrity: PASS. The authoritative SHA-256 matches, with 10,000 rows, 19 columns, six crop types, zero missing values and zero duplicate rows.
- Statistical and predictive reproducibility: PASS_WITH_QUALIFICATIONS. Deterministic outputs, configurations, seeds and limitations are present.
- Phase 4: PASS_WITH_QUALIFICATIONS. Matplotlib is now a direct pinned dependency (3.11.2). The recovered script ran in an isolated writable copy and reproduced the preserved interaction-results SHA-256 exactly. Historical creation provenance remains unauthenticated because no Git history is available.
- Phase 7 and Phase 8: evidence and limitations are preserved.
- Phase 9: all approved decisions remain unchanged; F005 remains DEFER and all technical statuses remain UNVERIFIED.
- Dashboard and Analysis Process: code compiles; governance downloads and reconstructed educational prompt downloads are present.
- Phase 11: comparative claims remain qualified where traditional-workflow evidence is incomplete.
- Security: no credentials or API keys were observed in inspected application and evidence files. After upgrading Pillow and Streamlit, pip-audit 2.10.1 completed with exit code 0 and reported no known vulnerabilities; the JSON report is preserved.

## Recommendation

READY_WITH_QUALIFICATIONS. The corrected dependency environment includes matplotlib==3.11.2, pillow==12.3.0 and streamlit==1.59.1, installs from the regenerated lock, passes pip check, passes all 49 automated tests, passes dataset and Phase 9 integrity checks, and compiles the dashboard. Browser acceptance was checked and approved by the human project owner. pip-audit now completes with exit code 0 and reports no known vulnerabilities. The recovered Phase 4 script is reproducible as current evidence, but its historical creation provenance cannot be authenticated.

## Follow-up investigation

Phase 4 files were found in the authoritative checkout: analysis/phase4_interaction_nonlinear.py, its prespecified plan, tests and deterministic outputs. No Git history exists to authenticate an original historical version. The direct dependency list now includes matplotlib and pip-compile regenerated requirements.txt without broad analytical changes; the lock retains packaging==25.0 and pandas==2.3.3 for Streamlit compatibility. The isolated Phase 4 run returned exit code 0 and generated the same interaction-results hash (01BB4B8553E2614A388258B21522002DDEE2692A764A28FD16A43BEE72FDB7BC). The human owner approved browser acceptance. After Pillow and Streamlit remediation, pip-audit 2.10.1 completed with exit code 0 and reported no known vulnerabilities; P12-007 is resolved.

