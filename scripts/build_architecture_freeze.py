"""Freeze legacy entropy and validate the bounded replacement architecture."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/governance/architecture_freeze.json"
GIANT_MODULES = (
    "src/catalytic_earth/northstar_next_levers.py",
    "src/catalytic_earth/labels.py",
    "src/catalytic_earth/cli.py",
    "src/catalytic_earth/lever2_mechanism_incremental_readout.py",
    "src/catalytic_earth/transfer_scope.py",
)
DETERMINISTIC_MODULES = (
    "src/catalytic_earth/atlas_selection.py",
    "src/catalytic_earth/canonical_hash.py",
    "src/catalytic_earth/core_cli.py",
    "src/catalytic_earth/schema.py",
    "src/catalytic_earth/execution_context.py",
    "src/catalytic_earth/family_onboarding.py",
    "src/catalytic_earth/lineage_quarantine.py",
    "src/catalytic_earth/path_compat.py",
)
PATH_CEILING = 180
POST_SOURCE_RELEASE_METADATA = {"release/release_manifest.json"}


def _canonical_text_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _sha(path: Path) -> str:
    return hashlib.sha256(_canonical_text_bytes(path)).hexdigest()


def _family_modules() -> list[str]:
    paths = sorted(path.relative_to(ROOT).as_posix() for path in (ROOT / "scripts").glob("source_*.py"))
    stage1 = "scripts/stage1_source_holes.py"
    if not (ROOT / stage1).is_file():
        raise ValueError(f"missing grandfathered family source module: {stage1}")
    return sorted([*paths, stage1])


def _all_repository_paths() -> list[str]:
    raw = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    )
    return sorted(
        path.decode("utf-8")
        for path in raw.split(b"\0")
        if path and path.decode("utf-8") not in POST_SOURCE_RELEASE_METADATA
    )


def _set_sha(paths: list[str]) -> str:
    return hashlib.sha256("".join(f"{path}\n" for path in paths).encode("utf-8")).hexdigest()


def build() -> bytes:
    family_modules = _family_modules()
    if len(family_modules) != 47:
        raise ValueError(
            f"family-specific source-module baseline changed: expected 47, found {len(family_modules)}"
        )
    giant = {
        path: {
            "bytes": len(_canonical_text_bytes(ROOT / path)),
            "sha256": _sha(ROOT / path),
        }
        for path in GIANT_MODULES
    }
    deterministic = {}
    forbidden_runtime_calls = re.compile(
        r"(?:datetime\.(?:now|utcnow)|time\.time|random\.(?:random|randint|choice))\s*\("
    )
    for path in DETERMINISTIC_MODULES:
        text = (ROOT / path).read_text(encoding="utf-8")
        matches = forbidden_runtime_calls.findall(text)
        if matches:
            raise ValueError(f"{path} bypasses injected time/seed policy: {matches}")
        deterministic[path] = {"bytes": len(text.encode("utf-8")), "sha256": _sha(ROOT / path)}
    paths = _all_repository_paths()
    over_ceiling = [path for path in paths if len(path) > PATH_CEILING]
    if over_ceiling:
        raise ValueError(f"repository paths exceed {PATH_CEILING}: {over_ceiling[:5]}")
    manifest: dict[str, Any] = {
        "schema_version": "catalytic-earth.architecture-freeze.v1",
        "frozen": True,
        "giant_modules_no_new_code": giant,
        "grandfathered_family_source_modules": family_modules,
        "grandfathered_family_source_module_count": len(family_modules),
        "grandfathered_family_source_module_set_sha256": _set_sha(family_modules),
        "replacement_family_path": {
            "engine": "src/catalytic_earth/family_onboarding.py",
            "schema": "src/catalytic_earth/schemas/family-onboarding-v1.schema.json",
            "example": "config/family_onboarding.example.json",
            "rule": "No new family-specific Python module; use declarative proposal-only configuration and the shared engine."
        },
        "typed_schema": {
            "python": "src/catalytic_earth/schema.py",
            "json_schema": "src/catalytic_earth/schemas/mechanism-record-v1.schema.json",
            "atlas3_selection_python": "src/catalytic_earth/atlas_selection.py",
            "atlas3_selection_schema": (
                "src/catalytic_earth/schemas/atlas3-selection-v1.schema.json"
            ),
            "atlas3_selection_contract": "data/atlas/atlas3_selection.json"
        },
        "deterministic_modules": deterministic,
        "test_tiers": {
            "manifest": "tests/test_tiers.json",
            "sha256": _sha(ROOT / "tests/test_tiers.json"),
            "runner": "scripts/run_test_tier.py"
        },
        "installed_commands": {
            "canonical": "catalytic-earth reproduce",
            "legacy": "catalytic-earth-legacy",
            "legacy_status": "deprecated_frozen_outside_core_guarantee"
        },
        "path_policy": {
            "maximum_relative_path_characters": PATH_CEILING,
            "observed_maximum": max(map(len, paths)),
            "paths_checked": len(paths),
            "excluded_post_source_release_metadata": sorted(POST_SOURCE_RELEASE_METADATA),
        }
    }
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != expected:
            raise SystemExit("data/governance/architecture_freeze.json is stale")
        print("Architecture freeze is current")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(expected)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
