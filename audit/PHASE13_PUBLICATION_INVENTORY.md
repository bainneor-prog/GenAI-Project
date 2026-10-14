# Phase 13 publication inventory (pre-push)

Prepared from the local repository on 2026-10-14. No Git remote or Git history is present in this checkout, so no branch or commit has been created and nothing has been pushed.

## Proposed inclusion

- `AGENTS.md`, `docs/`, `requirements.in`, `requirements.txt`, `.python-version`
- `data/Crop_Yield_original.csv` and `results/dataset_manifest.json` (approved checksum retained)
- `analysis/`, `dataset_validation.py`, `tests/`
- `dashboard/`
- deterministic `results/` outputs, Phase 9 decisions and evidence records
- approved `audit/` evidence packages and Phase 12 reports
- `README.md`

## Exclusion

- `.venv/`, Python caches and `.pytest_cache/`
- local logs and temporary files
- `.env` files, Streamlit secrets and credentials
- OS/editor metadata

## Verification observations

- Dataset SHA-256: `58D1866B7A01519593B68C9C929007D10051D070AA957773589F136065CC5F1C`
- Python: `3.12.14`
- Required pins confirmed: `packaging==25.0`, `pandas==2.3.3`, `matplotlib==3.11.2`
- No files larger than 50 MB were found.
- No credentials or key files were found by the initial filename scan.
- Dashboard source contains historical explanatory references to OneDrive; runtime deployment paths must be reviewed before deployment.

## Gate status

GitHub repository preparation is not complete because no suitable remote exists. The project owner has specified `felipemontelles-lgtm/GenAI-Project`, public visibility and `main`. Duplicate evidence trees will be retained as requested. The first push remains blocked until the security gate is completed and explicitly approved.

