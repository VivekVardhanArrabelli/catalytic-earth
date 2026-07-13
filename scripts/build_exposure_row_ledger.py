"""Rebuild the row-level evaluation-memory ledger from first-exposure commits.

This script intentionally reads historical Git objects.  Current checkout
copies of the source artifacts have drifted since their first use, so deriving
row identity from HEAD would rewrite evaluation history.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.canonical_hash import canonical_file_sha256  # noqa: E402
LEDGER_PATH = ROOT / "data/governance/exposure_rows.jsonl"
MANIFEST_PATH = ROOT / "data/governance/exposure_rows_manifest.json"


def _git_bytes(commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{path}"],
            cwd=ROOT,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(
            f"cannot read historical source {commit}:{path}; use a full-history clone: {message}"
        ) from exc


def _historical_json(commit: str, path: str) -> tuple[Any, str]:
    raw = _git_bytes(commit, path)
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def _canonical_sha(value: Any) -> str:
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _rowset_sha(row_ids: list[str]) -> str:
    raw = "".join(f"{row_id}\n" for row_id in sorted(row_ids)).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _current_sha(path: str) -> str | None:
    full_path = ROOT / path
    if not full_path.is_file():
        return None
    return canonical_file_sha256(full_path)


def _heldout_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for row in payload["rows"] if row.get("split_assignment") == "heldout"]


def _registry_rows(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise ValueError("historical current702 registry was expected to be a JSON list")
    return payload


def _frozen_members(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload["frozen_heldout_set"]["members"]


def _rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload["rows"]


SURFACES: tuple[dict[str, Any], ...] = (
    {
        "surface_id": "mcsa.current702.heldout140",
        "release": "current702.sequence-split@2026-05-25",
        "source_path": "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json",
        "commit": "d102bc5a9806e31146b0d2f9c84b3c161805133d",
        "first_exposure_artifact": "artifacts/v3_sequence_nn_metrics_current702_20260525.json",
        "first_exposure_timestamp": "2026-05-25T15:11:34Z",
        "label_version": "current702@d102bc5a9806",
        "split_role": "heldout",
        "state": "exhausted",
        "what_was_exposed": ["input", "label", "score", "outcome"],
        "models_or_decisions_made_after_exposure": [
            "predicted-geometry/cofactor-fusion blind pass",
            "June 28 retrospective one-shot and its threshold/deployment interpretation",
            "heldout mechanism-feature diagnostics",
        ],
        "eligible_for_development": True,
        "eligible_for_independent_test": False,
        "extract": _heldout_rows,
        "expected_count": 140,
    },
    {
        "surface_id": "current702.chemistry_eval702",
        "release": "current702.registry@2026-06-28",
        "source_path": "data/registries/curated_mechanism_labels.json",
        "commit": "f2055b72fa51722cbcfb37cd6e020d4ff5cf2f39",
        "first_exposure_artifact": "artifacts/v3_mechanism_from_chemistry_gold702_eval.json",
        "first_exposure_timestamp": "2026-06-28T01:12:51Z",
        "label_version": "current702@f2055b72fa51",
        "split_role": "retrospective_evaluation",
        "state": "exhausted",
        "what_was_exposed": ["input", "label", "score", "outcome"],
        "models_or_decisions_made_after_exposure": [
            "cofactor-bucket interpretation",
            "chemistry-only mechanism-recovery headline and later correction",
        ],
        "eligible_for_development": True,
        "eligible_for_independent_test": False,
        "extract": _registry_rows,
        "expected_count": 702,
    },
    {
        "surface_id": "offmcsa.option_b.bronze22",
        "release": "option-b-bronze-proxy@2026-06-28",
        "source_path": "artifacts/v3_option_b_heldout_preregistration_current702_20260628.json",
        "commit": "e3a40a5c2a9fccb2734ec8ef20693cb1448c1247",
        "first_exposure_artifact": "artifacts/v3_option_b_heldout_preregistration_current702_20260628.json",
        "first_exposure_timestamp": "2026-06-28T23:18:15Z",
        "label_version": "external-bronze-proxy@e3a40a5c2a9f",
        "split_role": "frozen_independent_proxy_test",
        "state": "frozen_unscored",
        "what_was_exposed": ["input", "label"],
        "models_or_decisions_made_after_exposure": [],
        "eligible_for_development": False,
        "eligible_for_independent_test": True,
        "extract": _frozen_members,
        "expected_count": 22,
    },
    {
        "surface_id": "offmcsa.swissprot_pdbholo.ec_proxy136",
        "release": "swissprot-pdbholo-ec-proxy@2026-06-29",
        "source_path": "artifacts/v3_swissprot_pdbholo_gold_heldout_preregistration_current702_20260629.json",
        "commit": "55d31b72fd5da2ade6adeee06ba2b2ceb58d8aa9",
        "first_exposure_artifact": "artifacts/v3_swissprot_pdbholo_gold_heldout_preregistration_current702_20260629.json",
        "first_exposure_timestamp": "2026-06-29T20:37:45Z",
        "label_version": "swissprot-ec-proxy.v1@55d31b72fd5d",
        "split_role": "spent_proxy_evaluation",
        "state": "exhausted",
        "what_was_exposed": ["input", "label", "score", "outcome"],
        "models_or_decisions_made_after_exposure": [
            "fixed Foldseek score",
            "aggregate deployment interpretation",
            "post-hoc three-family interpretation",
            "GFAT2 mapping correction",
        ],
        "eligible_for_development": True,
        "eligible_for_independent_test": False,
        "extract": _rows,
        "expected_count": 136,
    },
)


def build() -> tuple[bytes, bytes]:
    ledger_rows: list[dict[str, Any]] = []
    surface_manifest: dict[str, Any] = {}

    for surface in SURFACES:
        payload, historical_sha = _historical_json(surface["commit"], surface["source_path"])
        extractor: Callable[[Any], list[dict[str, Any]]] = surface["extract"]
        source_rows = extractor(payload)
        if len(source_rows) != surface["expected_count"]:
            raise ValueError(
                f"{surface['surface_id']} expected {surface['expected_count']} rows, "
                f"found {len(source_rows)}"
            )
        row_ids = [row.get("entry_id") for row in source_rows]
        if any(not isinstance(row_id, str) or not row_id for row_id in row_ids):
            raise ValueError(f"{surface['surface_id']} contains a missing entry_id")
        if len(row_ids) != len(set(row_ids)):
            raise ValueError(f"{surface['surface_id']} contains duplicate entry_id values")

        current_sha = _current_sha(surface["source_path"])
        source_release = {
            "release": surface["release"],
            "path": surface["source_path"],
            "sha256_at_first_exposure": historical_sha,
        }
        for source_row in source_rows:
            row_id = source_row["entry_id"]
            ledger_rows.append(
                {
                    "surface_id": surface["surface_id"],
                    "row_id": row_id,
                    "source_release_and_hash": source_release,
                    "row_source_record_sha256": _canonical_sha(source_row),
                    "label_version": surface["label_version"],
                    "split_role": surface["split_role"],
                    "first_exposure_timestamp": surface["first_exposure_timestamp"],
                    "first_exposure_commit": surface["commit"],
                    "first_exposure_artifact": surface["first_exposure_artifact"],
                    "what_was_exposed": surface["what_was_exposed"],
                    "models_or_decisions_made_after_exposure": surface[
                        "models_or_decisions_made_after_exposure"
                    ],
                    "exposure_state": surface["state"],
                    "eligible_for_development": surface["eligible_for_development"],
                    "eligible_for_independent_test": surface[
                        "eligible_for_independent_test"
                    ],
                }
            )

        surface_manifest[surface["surface_id"]] = {
            "row_count": len(row_ids),
            "row_id_set_sha256": _rowset_sha(row_ids),
            "first_exposure_commit": surface["commit"],
            "source_path": surface["source_path"],
            "source_sha256_at_first_exposure": historical_sha,
            "source_sha256_in_current_checkout": current_sha,
            "source_bytes_drifted_since_first_exposure": historical_sha != current_sha,
            "exposure_state": surface["state"],
        }

    ledger_rows.sort(key=lambda row: (row["surface_id"], row["row_id"]))
    ledger_bytes = "".join(
        json.dumps(row, separators=(",", ":"), sort_keys=True) + "\n"
        for row in ledger_rows
    ).encode("utf-8")
    manifest = {
        "schema_version": "catalytic-earth.exposure-row-ledger.v1",
        "ledger_path": "data/governance/exposure_rows.jsonl",
        "ledger_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
        "row_count": len(ledger_rows),
        "surface_count": len(surface_manifest),
        "surfaces": surface_manifest,
        "generation_rule": (
            "Rows are reconstructed from the first-exposure Git commits; HEAD copies "
            "are recorded only as drift diagnostics and never replace historical identity. "
            "Current repository text is LF-normalized before hashing so Windows checkout "
            "line endings cannot create false drift."
        ),
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return ledger_bytes, manifest_bytes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if committed row-ledger outputs differ from a historical rebuild",
    )
    args = parser.parse_args()
    ledger_bytes, manifest_bytes = build()
    outputs = ((LEDGER_PATH, ledger_bytes), (MANIFEST_PATH, manifest_bytes))
    if args.check:
        mismatches = [str(path.relative_to(ROOT)) for path, expected in outputs if not path.is_file() or path.read_bytes() != expected]
        if mismatches:
            raise SystemExit(f"stale exposure-row outputs: {', '.join(mismatches)}")
        print(f"Exposure row ledger is current: {len(ledger_bytes):,} bytes")
        return 0
    for path, content in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    print(f"Wrote {LEDGER_PATH.relative_to(ROOT)} and {MANIFEST_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
