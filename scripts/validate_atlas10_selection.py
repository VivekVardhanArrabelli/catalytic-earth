"""Validate the Atlas-10 selection, Atlas-3 inheritance, and registry boundary."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS10_SELECTION = ROOT / "data/atlas/atlas10_selection.json"
ATLAS3_SELECTION = ROOT / "data/atlas/atlas3_selection.json"
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas10_selection import (  # noqa: E402
    load_atlas10_selection,
    validate_atlas10_selection,
)
from catalytic_earth.atlas_selection import validate_atlas3_selection  # noqa: E402


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    payload = load_atlas10_selection(ATLAS10_SELECTION)
    summary = validate_atlas10_selection(payload)
    inherited = payload["inherited_selection"]
    atlas3 = json.loads(ATLAS3_SELECTION.read_text(encoding="utf-8"))
    atlas3_summary = validate_atlas3_selection(atlas3)
    if atlas3_summary["selection_sha256"] != inherited["selection_sha256"]:
        raise ValueError("Atlas-10 inherited selection hash differs from current Atlas-3")

    baseline = payload["baseline_commit"]
    subprocess.run(
        ["git", "cat-file", "-e", f"{baseline}^{{commit}}"],
        cwd=ROOT,
        check=True,
    )
    changed_registry_paths = _git(
        "diff", "--name-only", baseline, "--", "data/registries"
    ).splitlines()
    untracked_registry_paths = _git(
        "ls-files", "--others", "--exclude-standard", "--", "data/registries"
    ).splitlines()
    changed = sorted(set(changed_registry_paths + untracked_registry_paths))
    if changed:
        raise ValueError(
            "Atlas-10 changed protected registry paths relative to its baseline: "
            + ", ".join(changed)
        )
    print(json.dumps(summary, sort_keys=True))
    print("Atlas-10 selection valid; Atlas-3 inherited; protected registries unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
