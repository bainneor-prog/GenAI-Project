import hashlib
import json

import pandas as pd
import pytest

from dashboard.evidence import (
    ROOT,
    DatasetValidationError,
    eligible_findings,
    load_crop_yield_summary,
    load_evidence,
    load_source_dataset,
    required_files_exist,
)

def test_dashboard_evidence_and_eligibility():
    manifest, findings, decisions, refs = load_evidence()
    assert manifest["source_dataset"]["sha256"]
    assert len(findings) == 7
    eligible = eligible_findings(decisions)
    assert set(eligible.Finding_ID) == {"F001", "F002", "F003", "F004", "F006", "F007"}
    assert "F005" not in set(eligible.Finding_ID)
    assert required_files_exist(refs)[0]

def test_technical_status_is_not_human_decision():
    _, _, decisions, _ = load_evidence()
    assert set(decisions.Status) == {"UNVERIFIED"}
    assert set(decisions.Human_Decision) == {"ACCEPT_WITH_QUALIFICATIONS", "DEFER"}


def test_canonical_dashboard_dataset_matches_manifest_and_a002():
    data = load_source_dataset()
    manifest, _, _, _ = load_evidence()
    assert data.shape == (10000, 19)
    assert data.columns.tolist() == manifest["column_names"]
    assert int(data.isna().sum().sum()) == 0
    assert int(data.duplicated().sum()) == 0
    assert hashlib.sha256((ROOT / "data/Crop_Yield_original.csv").read_bytes()).hexdigest() == manifest["source_dataset"]["sha256"]

    calculated = data.groupby("Crop_Type")["Crop_Yield_ton_per_hectare"].agg(
        count="size", mean="mean", median="median", sd="std"
    ).reset_index().sort_values("Crop_Type").reset_index(drop=True)
    stored = load_crop_yield_summary().sort_values("Crop_Type").reset_index(drop=True)
    pd.testing.assert_frame_equal(
        calculated[["Crop_Type", "count", "mean", "median", "sd"]],
        stored[["Crop_Type", "count", "mean", "median", "sd"]],
        check_dtype=False,
        rtol=1e-12,
    )


def _write_test_dataset(root, frame, *, declared_payload=None):
    (root / "data").mkdir(parents=True)
    (root / "results").mkdir(parents=True)
    payload = frame.to_csv(index=False).encode("utf-8")
    (root / "data/source.csv").write_bytes(payload)
    reference = payload if declared_payload is None else declared_payload
    manifest = {
        "source_dataset": {
            "relative_path": "data/source.csv",
            "size_bytes": len(reference),
            "sha256": hashlib.sha256(reference).hexdigest(),
        },
        "shape": {"row_count": len(frame), "column_count": len(frame.columns)},
        "column_names": frame.columns.tolist(),
        "missing_values": frame.isna().sum().astype(int).to_dict(),
        "duplicate_rows": int(frame.duplicated().sum()),
    }
    (root / "results/dataset_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def test_loader_rejects_truncated_or_checksum_mismatched_data(tmp_path):
    frame = pd.DataFrame({"crop": ["Cotton", "Rice"], "yield": [7.4, 9.4]})
    _write_test_dataset(tmp_path, frame)
    dataset = tmp_path / "data/source.csv"
    dataset.write_bytes(dataset.read_bytes()[:-3])
    with pytest.raises(DatasetValidationError, match="size mismatch"):
        load_source_dataset(tmp_path)

    _write_test_dataset(tmp_path / "checksum", frame)
    checksum_dataset = tmp_path / "checksum/data/source.csv"
    corrupted = checksum_dataset.read_bytes().replace(b"Cotton", b"Potato")
    checksum_dataset.write_bytes(corrupted)
    with pytest.raises(DatasetValidationError, match="checksum"):
        load_source_dataset(tmp_path / "checksum")


def test_loader_rejects_missing_values_even_with_matching_hash(tmp_path):
    frame = pd.DataFrame({"crop": ["Cotton", "Rice"], "yield": [7.4, 9.4]})
    _write_test_dataset(tmp_path, frame)
    dataset = tmp_path / "data/source.csv"
    altered = b"crop,yield\nCotton,\nRice,9.4\n"
    dataset.write_bytes(altered)
    manifest_path = tmp_path / "results/dataset_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_dataset"]["size_bytes"] = len(altered)
    manifest["source_dataset"]["sha256"] = hashlib.sha256(altered).hexdigest()
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(DatasetValidationError, match="missing-value"):
        load_source_dataset(tmp_path)


def test_hosted_transport_fragments_are_not_present():
    assert not (ROOT / "data/source_parts").exists()
