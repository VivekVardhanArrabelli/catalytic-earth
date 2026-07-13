#!/usr/bin/env python3
"""Build or verify the exact canonical 0.1.0 release manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "release" / "release_manifest.json"
EXPECTED_RESULT_SHA256 = "a2374c6530dfd3b4681db5c3db691fdcdedbf645604c6e7dfe0b95ab7e89ea98"
SOURCE_BINDINGS = (
    ".gitattributes",
    ".github/workflows/p0-contracts.yml",
    "CITATION.cff",
    "CLAIMS.md",
    "ERRATA.md",
    "LICENSE",
    "NOTICE",
    "docs/CORE_REPRODUCTION.md",
    "docs/P0_COMPLETION.md",
    "docs/SOURCE_DATA_RIGHTS.md",
    "data/governance/architecture_freeze.json",
    "data/governance/claim_ledger.json",
    "data/governance/exposure_rows_manifest.json",
    "data/governance/historical_lineage_quarantine.json",
    "data/governance/test_baseline.json",
    "environments/core.json",
    "environments/ml-test.json",
    "environments/scientific-tools.json",
    "requirements/build.lock",
    "requirements/core.lock",
    "requirements/ml.lock",
    "src/catalytic_earth/release_data/golden_input_v1.json",
    "src/catalytic_earth/release_data/golden_expected_v1.json",
    "src/catalytic_earth/schemas/mechanism-record-v1.schema.json",
    "release/live_artifact_manifest.json",
    "release/release-manifest-v1.schema.json",
    "release/report_archive_index.json",
    "release/validation/full-suite-python313-windows.log.gz",
    "scripts/build_canonical_release_assets.py",
    "scripts/verify_core_release.py",
)


def _git(*args: str, binary: bool = False) -> str | bytes:
    value = subprocess.check_output(["git", *args], cwd=ROOT)
    return value if binary else value.decode("utf-8").strip()


def _resolve_commit(commit: str) -> str:
    resolved = str(_git("rev-parse", f"{commit}^{{commit}}"))
    if not re.fullmatch(r"[0-9a-f]{40}", resolved):
        raise ValueError(f"invalid source commit: {resolved}")
    return resolved


def _blob(commit: str, path: str) -> bytes:
    return bytes(_git("show", f"{commit}:{path}", binary=True))


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _asset(path: Path, role: str) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "role": role,
        "filename": path.name,
        "bytes": len(raw),
        "sha256": _sha(raw),
    }


def _source_bindings(commit: str) -> list[dict[str, Any]]:
    return [
        {"path": path, "sha256": _sha(_blob(commit, path))}
        for path in SOURCE_BINDINGS
    ]


def build(
    *,
    source_commit: str,
    wheel: Path,
    source_archive: Path,
    report_bundle: Path,
    restore_duration_seconds: float,
) -> dict[str, Any]:
    commit = _resolve_commit(source_commit)
    live = json.loads(_blob(commit, "release/live_artifact_manifest.json"))
    exposure = json.loads(_blob(commit, "data/governance/exposure_rows_manifest.json"))
    scientific_tools = json.loads(_blob(commit, "environments/scientific-tools.json"))
    quarantine = json.loads(
        _blob(commit, "data/governance/historical_lineage_quarantine.json")
    )
    assets = [
        _asset(wheel, "installable_core_wheel"),
        _asset(source_archive, "deterministic_lean_source"),
        _asset(report_bundle, "indexed_historical_report_archive"),
    ]
    for asset in assets[:2]:
        if asset["bytes"] >= 100 * 1024 * 1024:
            raise ValueError(f"canonical release asset exceeds 100 MiB: {asset['filename']}")
    return {
        "schema_version": "catalytic-earth.release-manifest.v1",
        "release": "0.1.0",
        "release_tag": "v0.1.0-truth-reset",
        "source_commit": commit,
        "source_tree": str(_git("rev-parse", f"{commit}^{{tree}}")),
        "source_commit_epoch": int(str(_git("show", "-s", "--format=%ct", commit))),
        "canonical_surface": {
            "name": "typed project-authored core fixture",
            "command": "catalytic-earth reproduce",
            "expected_result_sha256": EXPECTED_RESULT_SHA256,
            "seed": 0,
            "network": False,
            "accelerator": False,
            "external_binary": False,
            "biological_claim_permitted": False,
            "claim_boundary": (
                "Packaging, schema, determinism, and negative-record retention only; "
                "not a biological benchmark or validation."
            ),
        },
        "dataset_and_split_hashes": {
            "core_fixture": {
                "dataset": "src/catalytic_earth/release_data/golden_input_v1.json",
                "dataset_sha256": _sha(
                    _blob(commit, "src/catalytic_earth/release_data/golden_input_v1.json")
                ),
                "split_id": "project_authored_fixture_v1_all_records",
                "split_row_count": 4,
                "expected": "src/catalytic_earth/release_data/golden_expected_v1.json",
                "expected_sha256": _sha(
                    _blob(commit, "src/catalytic_earth/release_data/golden_expected_v1.json")
                ),
            },
            "scientific_evaluation_memory": {
                "manifest": "data/governance/exposure_rows_manifest.json",
                "manifest_sha256": _sha(
                    _blob(commit, "data/governance/exposure_rows_manifest.json")
                ),
                "surface_row_set_sha256": {
                    key: value["row_id_set_sha256"]
                    for key, value in sorted(exposure["surfaces"].items())
                },
                "included_in_core_result": False,
            },
        },
        "build_and_reproduce_commands": [
            "python -m pip install -r requirements/build.lock",
            f"python scripts/build_canonical_release_assets.py --source-commit {commit}",
            "python scripts/verify_core_release.py --wheel dist --source-archive dist/catalytic-earth-0.1.0-lean-source.zip",
            "catalytic-earth reproduce",
        ],
        "restore_verification": {
            "command": (
                "python scripts/verify_core_release.py --wheel dist "
                "--source-archive dist/catalytic-earth-0.1.0-lean-source.zip"
            ),
            "empty_directory_wheel_install": True,
            "empty_directory_source_run": True,
            "passed": True,
            "duration_seconds": round(restore_duration_seconds, 3),
            "target_seconds": 600,
            "platform": platform.system(),
            "python": platform.python_version(),
            "cross_platform_contract": ".github/workflows/p0-contracts.yml",
        },
        "environment": {
            "python": ">=3.10 CPython; release CI targets 3.10 and 3.12",
            "runtime_lock": "requirements/core.lock",
            "build_lock": "requirements/build.lock",
            "model_revisions": [],
            "external_tool_versions": [],
            "known_unavailable_scientific_inputs": [
                {
                    "kind": "external_tool",
                    "id": row["id"],
                    "status": row["status"],
                }
                for row in scientific_tools.get("external_tools", [])
                if row.get("locked_version") is None
            ]
            + [
                {
                    "kind": "model",
                    "id": row["id"],
                    "status": row["status"],
                }
                for row in scientific_tools.get("models", [])
                if row.get("revision") is None
            ],
        },
        "assets": assets,
        "source_bindings": _source_bindings(commit),
        "historical_surface": {
            "tracked_artifact_files": live["tracked_artifact_files"],
            "tracked_artifact_logical_bytes": live["tracked_artifact_logical_bytes"],
            "artifact_index_sha256": live["artifact_index_sha256"],
            "included_in_lean_release": False,
            "restore_source": "Git history at source_commit",
            "history_rewritten": False,
            "quarantined_artifact_count": quarantine["metadata"][
                "quarantined_artifact_count"
            ],
            "quarantined_artifacts": [
                row["artifact_path"] for row in quarantine["quarantined_artifacts"]
            ],
            "quarantined_artifacts_in_canonical_release": False,
            "large_artifact_externalization_status": (
                "not_performed_no_deletion_authorized_pending_per-source_rights_and_destination"
            ),
        },
        "attribution_and_rights": {
            "code_license": "Apache-2.0",
            "notice": "NOTICE",
            "matrix": "docs/SOURCE_DATA_RIGHTS.md",
            "rule": "The canonical fixture is project-authored; restricted/ambiguous third-party data is excluded.",
        },
    }


def validate(manifest: dict[str, Any], *, asset_dir: Path | None = None) -> None:
    if manifest.get("schema_version") != "catalytic-earth.release-manifest.v1":
        raise ValueError("unsupported release manifest schema")
    commit = _resolve_commit(str(manifest.get("source_commit")))
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=ROOT,
        check=False,
    ).returncode:
        raise ValueError("release source commit is not an ancestor of the manifest commit")
    expected_tree = str(_git("rev-parse", f"{commit}^{{tree}}"))
    if manifest.get("source_tree") != expected_tree:
        raise ValueError("release source tree does not match source commit")
    bindings = manifest.get("source_bindings")
    expected_bindings = _source_bindings(commit)
    if bindings != expected_bindings:
        raise ValueError("release source bindings do not match exact commit blobs")
    canonical = manifest.get("canonical_surface", {})
    if canonical.get("expected_result_sha256") != EXPECTED_RESULT_SHA256:
        raise ValueError("release golden result hash is wrong")
    if canonical.get("biological_claim_permitted") is not False:
        raise ValueError("core fixture must not be presented as biological validation")
    verification = manifest.get("restore_verification", {})
    if verification.get("passed") is not True:
        raise ValueError("empty-directory restore is not recorded as passing")
    duration = verification.get("duration_seconds")
    if not isinstance(duration, (int, float)) or duration <= 0 or duration >= 600:
        raise ValueError("empty-directory restore did not meet the ten-minute target")
    assets = manifest.get("assets", [])
    if {row.get("role") for row in assets} != {
        "installable_core_wheel",
        "deterministic_lean_source",
        "indexed_historical_report_archive",
    }:
        raise ValueError("release asset roles are incomplete")
    if len({row.get("filename") for row in assets}) != len(assets):
        raise ValueError("release asset filenames must be unique")
    for row in assets:
        filename = str(row.get("filename", ""))
        if Path(filename).name != filename:
            raise ValueError(f"release asset filename is unsafe: {filename}")
        if not re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256", ""))):
            raise ValueError(f"invalid release asset SHA-256: {row}")
        if not isinstance(row.get("bytes"), int) or row["bytes"] <= 0:
            raise ValueError(f"invalid release asset size: {row}")
        if row["role"] != "indexed_historical_report_archive" and row["bytes"] >= 100 * 1024 * 1024:
            raise ValueError(f"lean release asset exceeds 100 MiB: {row['filename']}")
        if asset_dir is not None:
            path = asset_dir / row["filename"]
            observed = _asset(path, row["role"])
            if observed != row:
                raise ValueError(f"release asset differs from manifest: {path}")
    historical = manifest.get("historical_surface", {})
    if historical.get("history_rewritten") is not False:
        raise ValueError("release must preserve historical Git provenance")
    if historical.get("quarantined_artifacts_in_canonical_release") is not False:
        raise ValueError("quarantined artifacts cannot enter the canonical release")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit")
    parser.add_argument("--wheel", type=Path)
    parser.add_argument("--source-archive", type=Path)
    parser.add_argument("--report-bundle", type=Path)
    parser.add_argument("--restore-duration-seconds", type=float)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--asset-dir", type=Path)
    args = parser.parse_args()
    if args.check:
        manifest = json.loads(args.out.read_text(encoding="utf-8"))
        validate(manifest, asset_dir=args.asset_dir)
        print(
            f"Release manifest valid: source={manifest['source_commit']} "
            f"assets={len(manifest['assets'])}"
        )
        return 0
    required = (
        args.source_commit,
        args.wheel,
        args.source_archive,
        args.report_bundle,
        args.restore_duration_seconds,
    )
    if any(value is None for value in required):
        parser.error(
            "--source-commit, --wheel, --source-archive, --report-bundle, and "
            "--restore-duration-seconds are required"
        )
    manifest = build(
        source_commit=args.source_commit,
        wheel=args.wheel,
        source_archive=args.source_archive,
        report_bundle=args.report_bundle,
        restore_duration_seconds=args.restore_duration_seconds,
    )
    validate(manifest)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {args.out.relative_to(ROOT)} for {manifest['source_commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
