"""Validate the frozen Atlas-3 selection and its protected-registry boundary."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "data/atlas/atlas3_selection.json"
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_selection import (  # noqa: E402
    load_atlas3_selection,
    validate_atlas3_selection,
)


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    payload = load_atlas3_selection(SELECTION)
    summary = validate_atlas3_selection(payload)
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
            "Atlas-3 changed protected registry paths relative to its baseline: "
            + ", ".join(changed)
        )
    print(json.dumps(summary, sort_keys=True))
    print("Atlas-3 selection valid; protected registries unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
