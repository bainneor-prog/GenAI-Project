"""Load approved deterministic evidence and enforce Phase 9 eligibility."""
from pathlib import Path
from io import BytesIO
import base64
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = Path(r"C:\crop-yield-genai-main")

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

def load_source_dataset() -> pd.DataFrame:
    """Load the canonical dataset, using authenticated transport parts on hosted copies."""
    parts_dir = ROOT / "data" / "source_parts"
    parts = sorted(parts_dir.glob("Crop_Yield_original.part*.b64"))
    if parts:
        encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
        return pd.read_csv(BytesIO(base64.b64decode(encoded, validate=True)))
    return pd.read_csv(ROOT / "data" / "Crop_Yield_original.csv")

