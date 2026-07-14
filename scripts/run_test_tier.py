"""Classify, list, validate, or run one explicit unittest tier."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests/test_tiers.json"


def load_manifest() -> dict[str, Any]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "catalytic-earth.test-tiers.v1":
        raise ValueError("unsupported test tier schema")
    if set(payload.get("precedence", [])) != set(payload.get("tiers", {})):
        raise ValueError("test tier precedence must cover every tier exactly")
    return payload


def classify_tests() -> dict[str, list[str]]:
    manifest = load_manifest()
    grouped = {tier: [] for tier in manifest["precedence"]}
    files = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("test_*.py")
        if path.is_file()
    )
    for path in files:
        match = next(
            (
                tier
                for tier in manifest["precedence"]
                if any(re.search(pattern, path) for pattern in manifest["tiers"][tier]["patterns"])
            ),
            None,
        )
        if match is None:
            raise ValueError(f"unclassified test file: {path}")
        grouped[match].append(path)
    empty = [tier for tier, paths in grouped.items() if not paths]
    if empty:
        raise ValueError(f"test tiers must not be empty: {empty}")
    return grouped


def _module_name(path: str) -> str:
    if not path.endswith(".py"):
        raise ValueError(path)
    return path[:-3].replace("/", ".")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tier", nargs="?", choices=list(load_manifest()["tiers"]))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    grouped = classify_tests()
    if args.check:
        print(
            "Test tiers valid: "
            + ", ".join(f"{tier}={len(paths)}" for tier, paths in grouped.items())
        )
        return 0
    if args.tier is None:
        parser.error("tier is required unless --check is used")
    if args.list:
        print("\n".join(grouped[args.tier]))
        return 0
    if args.tier == "external/integration" and os.environ.get("CE_RUN_EXTERNAL_INTEGRATION") != "1":
        raise SystemExit(
            "external/integration is opt-in; set CE_RUN_EXTERNAL_INTEGRATION=1 after "
            "provisioning declared sources and tools"
        )
    env = dict(os.environ)
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(ROOT / "src") + (os.pathsep + existing if existing else "")
    command = [
        sys.executable,
        "-m",
        "unittest",
        "-v",
        *(_module_name(path) for path in grouped[args.tier]),
    ]
    return subprocess.run(command, cwd=ROOT, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
