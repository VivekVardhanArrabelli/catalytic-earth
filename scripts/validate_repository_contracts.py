"""Validate every machine-enforced P0 repository contract."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.core_cli import verified_golden_result  # noqa: E402
from catalytic_earth.truth_guard import validate_truth_governance  # noqa: E402


def _run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def _validate_legal_surfaces() -> None:
    for path in ("LICENSE", "NOTICE", "CITATION.cff", "docs/SOURCE_DATA_RIGHTS.md"):
        if not (ROOT / path).is_file():
            raise ValueError(f"missing legal/attribution surface: {path}")
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if "Apache License" not in license_text or "Version 2.0" not in license_text:
        raise ValueError("LICENSE is not Apache-2.0 text")
    rights = (ROOT / "docs/SOURCE_DATA_RIGHTS.md").read_text(encoding="utf-8")
    for source in (
        "UniProt",
        "Rhea",
        "M-CSA",
        "PDB",
        "AlphaFold",
        "BRENDA",
        "SABIO-RK",
        "ChEBI",
        "MGnify",
        "CAZy",
        "PAZy",
        "PlasticDB",
    ):
        if source not in rights:
            raise ValueError(f"source-rights matrix is missing {source}")


def _validate_active_paths() -> None:
    roots = [ROOT / "src", ROOT / "scripts"]
    docs = [
        ROOT / "README.md",
        ROOT / "docs/ARCHITECTURE.md",
        ROOT / "docs/CORE_REPRODUCTION.md",
        ROOT / "docs/EVALUATION_MEMORY.md",
        ROOT / "docs/LEAN_RELEASE.md",
        ROOT / "docs/P0_COMPLETION.md",
        ROOT / "docs/SOURCE_DATA_RIGHTS.md",
        ROOT / "docs/artifact_storage.md",
        ROOT / "docs/external_source_transfer.md",
    ]
    files = [
        path
        for root in roots
        for path in root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix.lower() in {".json", ".md", ".py", ".toml", ".yaml", ".yml"}
        and path.resolve() != Path(__file__).resolve()
    ] + docs
    forbidden = {
        "/private/tmp/catalytic-foldseek-env": "machine-specific Foldseek path",
        "git@github.com:": "private SSH clone example",
        "id_ed25519": "private SSH-key example",
    }
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker, description in forbidden.items():
            if marker in text:
                raise ValueError(f"{path.relative_to(ROOT)} contains {description}")


def _validate_markdown_links() -> None:
    documents = (
        "README.md",
        "CLAIMS.md",
        "ERRATA.md",
        "docs/ARCHITECTURE.md",
        "docs/ATLAS_TRUTH_POLICY.md",
        "docs/CORE_REPRODUCTION.md",
        "docs/EVALUATION_MEMORY.md",
        "docs/LEAN_RELEASE.md",
        "docs/P0_COMPLETION.md",
        "docs/SOURCE_DATA_RIGHTS.md",
    )
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for relative in documents:
        document = ROOT / relative
        for target in link_pattern.findall(document.read_text(encoding="utf-8")):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^(?:https?|mailto):", target):
                continue
            resolved = (document.parent / target).resolve()
            if ROOT.resolve() not in resolved.parents and resolved != ROOT.resolve():
                raise ValueError(f"{relative} link escapes repository: {target}")
            if not resolved.exists():
                raise ValueError(f"{relative} has broken relative link: {target}")


def _validate_json_surfaces(*, include_release_manifest: bool) -> None:
    paths = [
        "data/governance/claim_ledger.json",
        "data/governance/exposure_rows_manifest.json",
        "data/governance/preregistration-v1.schema.json",
        "data/governance/architecture_freeze.json",
        "data/governance/historical_lineage_quarantine.json",
        "data/governance/test_baseline.json",
        "environments/core.json",
        "environments/ml-test.json",
        "environments/scientific-tools.json",
        "release/live_artifact_manifest.json",
        "release/release-manifest-v1.schema.json",
        "release/report_archive_index.json",
        "tests/test_tiers.json",
    ]
    if include_release_manifest:
        paths.append("release/release_manifest.json")
    for path in paths:
        json.loads((ROOT / path).read_text(encoding="utf-8"))


def _validate_test_baseline() -> None:
    baseline = json.loads(
        (ROOT / "data/governance/test_baseline.json").read_text(encoding="utf-8")
    )
    if baseline.get("schema_version") != "catalytic-earth.test-baseline.v1":
        raise ValueError("unsupported test baseline schema")
    historical = baseline.get("historical_audit", {})
    if {
        key: historical.get(key)
        for key in ("tests", "failures", "errors", "skipped")
    } != {"tests": 2559, "failures": 74, "errors": 20, "skipped": 1}:
        raise ValueError("historical full-suite audit counts were altered")
    correction = baseline.get("root_cause_correction", {})
    if correction.get("test_failures_previously_attributed_to_stale_hashes") != 54:
        raise ValueError("test root-cause correction is incomplete")
    if correction.get("underlying_crlf_only_hash_comparisons") != 179:
        raise ValueError("CRLF-only hash audit count is wrong")
    if correction.get("genuine_current_content_lineage_drifts") != 1:
        raise ValueError("lineage quarantine count differs from the audit")
    current = baseline.get("current_validation", {})
    if current.get("status") != "green" or current.get("return_code") != 0:
        raise ValueError("current complete-suite baseline is not green")
    if current.get("failures") != 0 or current.get("errors") != 0:
        raise ValueError("current complete-suite baseline contains failures or errors")
    if not isinstance(current.get("tests"), int) or current["tests"] < 2559:
        raise ValueError("current complete-suite run is unexpectedly smaller")
    log = baseline.get("log", {})
    log_path = ROOT / str(log.get("path", ""))
    compressed = log_path.read_bytes()
    if hashlib.sha256(compressed).hexdigest() != log.get("compressed_sha256"):
        raise ValueError("compressed full-suite evidence hash differs")
    raw = gzip.decompress(compressed)
    if len(raw) != log.get("uncompressed_bytes"):
        raise ValueError("full-suite evidence size differs")
    if hashlib.sha256(raw).hexdigest() != log.get("uncompressed_sha256"):
        raise ValueError("full-suite evidence content hash differs")
    lock_path = ROOT / str(baseline.get("environment", {}).get("requirements_lock", ""))
    lock_digest = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    if lock_digest != baseline.get("environment", {}).get("requirements_lock_sha256"):
        raise ValueError("test baseline environment lock differs")


def _validate_p0_closure() -> None:
    completion = (ROOT / "docs/P0_COMPLETION.md").read_text(encoding="utf-8")
    for marker in (
        "P0A — correct the scientific record",
        "P0B — make evaluation memory mechanical",
        "P0C — make the repository legally and technically enterable",
        "P0D — shrink without destroying provenance",
        "P0E — freeze architectural entropy",
        "Guarded deferment",
        "software validation, not biological validation",
    ):
        if marker not in completion:
            raise ValueError(f"P0 completion record is missing: {marker}")
    freeze = json.loads(
        (ROOT / "data/governance/expansion_freeze.json").read_text(encoding="utf-8")
    )
    expected = {
        "claim_and_errata_ledgers": "met",
        "exposure_memory": "met",
        "locked_core_reproduction": "met",
        "live_artifact_manifest": "met",
        "explicit_reviewed_unfreeze_decision": "pending",
    }
    if freeze.get("requirement_status") != expected or freeze.get("frozen") is not True:
        raise ValueError("post-P0 expansion safety-latch state is inconsistent")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pre-release",
        action="store_true",
        help="validate the exact source commit before its asset manifest is generated",
    )
    args = parser.parse_args()
    result = validate_truth_governance(ROOT)
    _validate_legal_surfaces()
    _validate_active_paths()
    _validate_markdown_links()
    _validate_json_surfaces(include_release_manifest=not args.pre_release)
    _validate_test_baseline()
    _validate_p0_closure()
    verified_golden_result()
    _run("scripts/build_exposure_row_ledger.py", "--check")
    _run("scripts/build_historical_lineage_quarantine.py", "--check")
    if os.environ.get("CE_PARTIAL_CLONE") == "1":
        _run("scripts/build_live_artifact_manifest.py", "--check", "--index-only")
    else:
        _run("scripts/build_live_artifact_manifest.py", "--check")
    if os.environ.get("CE_PARTIAL_CLONE") == "1":
        _run("scripts/build_report_archive.py", "--check", "--index-only")
    else:
        _run("scripts/build_report_archive.py", "--check")
    if not args.pre_release:
        _run("scripts/build_release_manifest.py", "--check")
    _run("scripts/build_architecture_freeze.py", "--check")
    _run("scripts/run_test_tier.py", "--check")
    print(
        "Repository contracts valid: "
        f"claims={result['claims']}, exposure_rows={result['exposure_rows']}, "
        "golden_result=matched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
