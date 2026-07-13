#!/usr/bin/env python3
"""Build the lean source and wheel from the release manifest's exact commit."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "release" / "release_manifest.json"
DEFAULT_DIST = ROOT / "dist"


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def _resolve_source_commit(manifest: Path, override: str | None) -> str:
    candidate = override
    if candidate is None:
        candidate = str(json.loads(manifest.read_text(encoding="utf-8"))["source_commit"])
    return _git("rev-parse", f"{candidate}^{{commit}}")


def _clear_previous_outputs(dist: Path) -> None:
    dist.mkdir(parents=True, exist_ok=True)
    for pattern in (
        "catalytic_earth-0.1.0-*.whl",
        "catalytic-earth-0.1.0-lean-source.zip",
    ):
        for path in dist.glob(pattern):
            if path.is_file():
                path.unlink()


def build_assets(*, source_commit: str, dist: Path) -> tuple[Path, Path]:
    _clear_previous_outputs(dist)
    source_archive = dist / "catalytic-earth-0.1.0-lean-source.zip"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_lean_source_archive.py"),
            "--source-commit",
            source_commit,
            "--output",
            str(source_archive),
        ],
        cwd=ROOT,
        check=True,
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        extraction_root = Path(tmpdir)
        with zipfile.ZipFile(source_archive) as archive:
            archive.extractall(extraction_root)
        source_roots = [path for path in extraction_root.iterdir() if path.is_dir()]
        if len(source_roots) != 1:
            raise ValueError("lean source archive must contain exactly one source root")
        environment = dict(os.environ)
        environment["SOURCE_DATE_EPOCH"] = _git(
            "show", "-s", "--format=%ct", source_commit
        )
        subprocess.run(
            [
                sys.executable,
                "-m",
                "build",
                "--wheel",
                "--no-isolation",
                "--outdir",
                str(dist.resolve()),
            ],
            cwd=source_roots[0],
            env=environment,
            check=True,
        )
    wheels = sorted(dist.glob("catalytic_earth-0.1.0-*.whl"))
    if len(wheels) != 1:
        raise ValueError(f"expected exactly one wheel, found {wheels}")
    if source_archive.stat().st_size >= 100 * 1024 * 1024:
        raise ValueError("lean source archive exceeds 100 MiB")
    if wheels[0].stat().st_size >= 100 * 1024 * 1024:
        raise ValueError("core wheel exceeds 100 MiB")
    return wheels[0], source_archive


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--source-commit")
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    args = parser.parse_args()
    commit = _resolve_source_commit(args.manifest, args.source_commit)
    wheel, archive = build_assets(source_commit=commit, dist=args.dist)
    print(
        f"Canonical release assets built from {commit}: "
        f"{wheel.name} ({wheel.stat().st_size} bytes), "
        f"{archive.name} ({archive.stat().st_size} bytes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
