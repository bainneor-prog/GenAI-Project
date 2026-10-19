"""Load approved deterministic evidence and enforce Phase 9 eligibility."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = Path(r"C:\crop-yield-genai-main")


class DatasetValidationError(RuntimeError):
    """Raised when the dashboard source data do not match approved evidence."""

def load_evidence():
    manifest = json.loads((ROOT / "results/dataset_manifest.json").read_text(encoding="utf-8"))
    findings = json.loads((ROOT / "results/findings.json").read_text(encoding="utf-8"))
    decisions = pd.read_csv(ROOT / "results/PHASE9_REPORTING_ELIGIBILITY.csv")
    refs = pd.read_csv(ROOT / "results/PHASE9_EVIDENCE_REFERENCE_INDEX.csv")
    return manifest, findings, decisions, refs

def eligible_findings(decisions: pd.DataFrame) -> pd.DataFrame:
    """Only qualified human acceptances are eligible; technical status stays visible."""
    return decisions[decisions["Human_Decision"].eq("ACCEPT_WITH_QUALIFICATIONS") & decisions["Eligible_For_Dashboard"].eq("YES")].copy()

def required_files_exist(refs: pd.DataFrame) -> tuple[bool, list[str]]:
    missing = [p for p in refs["Repository_Relative_Path"] if not (ROOT / p).exists()]
    return not missing, missing

def load_csv(relative: str) -> pd.DataFrame:
    path = ROOT / relative
    try:
        return pd.read_csv(path)
    except pd.errors.ParserError as exc:
        # Some legacy baseline exports contain descriptive commas that were not
        # CSV-quoted. Preserve the source file and expose only parseable rows.
        # The dashboard is a communication layer, not a repair of evidence.
        try:
            frame = pd.read_csv(path, engine="python", on_bad_lines="skip")
        except Exception:
            frame = pd.DataFrame()
            frame.attrs["evidence_warning"] = f"Evidence file could not be parsed: {exc}"
            return frame
        frame.attrs["evidence_warning"] = f"Legacy CSV parsing warning: {exc}"
        return frame

    except OSError as exc:
        # OneDrive may temporarily expose an offline/placeholder file. A local
        # project copy is used only as an explicitly disclosed read-only fallback.
        alternate = LEGACY_ROOT / relative
        if alternate.exists():
            try:
                frame = pd.read_csv(alternate, engine="python", on_bad_lines="skip")
                frame.attrs["evidence_warning"] = (
                    f"Primary OneDrive evidence was unavailable ({exc}). Displaying the accessible "
                    "local project copy for review; no source file was replaced."
                )
                return frame
            except Exception:
                pass
        frame = pd.DataFrame()
        frame.attrs["evidence_warning"] = f"Evidence file is currently unavailable: {exc}"
        return frame

def load_source_dataset(root: Path = ROOT) -> pd.DataFrame:
    """Load the single canonical CSV only after validating it against the manifest."""
    try:
        manifest = json.loads((root / "results/dataset_manifest.json").read_text(encoding="utf-8"))
        source = manifest["source_dataset"]
        dataset_path = root / source["relative_path"]
        payload = dataset_path.read_bytes()
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        raise DatasetValidationError(
            "The approved source dataset or its validation manifest is unavailable."
        ) from exc

    actual_size = len(payload)
    expected_size = int(source["size_bytes"])
    if actual_size != expected_size:
        raise DatasetValidationError(
            f"Source dataset size mismatch: expected {expected_size:,} bytes, found {actual_size:,}."
        )

    actual_hash = hashlib.sha256(payload).hexdigest()
    expected_hash = str(source["sha256"]).lower()
    if actual_hash != expected_hash:
        raise DatasetValidationError(
            "Source dataset checksum does not match the approved validation manifest."
        )

    try:
        frame = pd.read_csv(BytesIO(payload))
    except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as exc:
        raise DatasetValidationError("The approved source dataset could not be parsed safely.") from exc

    expected_shape = (int(manifest["shape"]["row_count"]), int(manifest["shape"]["column_count"]))
    if frame.shape != expected_shape:
        raise DatasetValidationError(
            f"Source dataset shape mismatch: expected {expected_shape}, found {frame.shape}."
        )
    if frame.columns.tolist() != manifest["column_names"]:
        raise DatasetValidationError("Source dataset columns do not match the approved validation manifest.")

    actual_missing = frame.isna().sum().astype(int).to_dict()
    expected_missing = {key: int(value) for key, value in manifest["missing_values"].items()}
    if actual_missing != expected_missing:
        raise DatasetValidationError("Source dataset missing-value counts do not match the approved manifest.")

    actual_duplicates = int(frame.duplicated().sum())
    if actual_duplicates != int(manifest["duplicate_rows"]):
        raise DatasetValidationError("Source dataset duplicate count does not match the approved manifest.")
    return frame


def load_crop_yield_summary(root: Path = ROOT) -> pd.DataFrame:
    """Load the approved A002 crop summary used for formal dashboard statistics."""
    summary = pd.read_csv(root / "results/baseline_details/A002_crop_yield_summary.csv")
    return summary.rename(columns={"crop": "Crop_Type", "standard_deviation": "sd"})
