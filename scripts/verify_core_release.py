"""Verify a wheel and optional lean source archive from empty directories."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import venv
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory


EXPECTED_RESULT_SHA256 = "a2374c6530dfd3b4681db5c3db691fdcdedbf645604c6e7dfe0b95ab7e89ea98"


def _venv_python(root: Path) -> Path:
    return root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def _run_golden(python: Path, *, cwd: Path, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(
        [str(python), "-m", "catalytic_earth.core_cli", "reproduce"],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    if payload.get("result_sha256") != EXPECTED_RESULT_SHA256 or not payload.get(
        "matches_expected"
    ):
        raise ValueError("installed core produced the wrong golden result")


def verify_wheel(wheel: Path) -> None:
    wheel = wheel.resolve()
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        environment = root / "venv"
        empty_cwd = root / "empty"
        empty_cwd.mkdir()
        venv.EnvBuilder(with_pip=True, clear=True).create(environment)
        python = _venv_python(environment)
        subprocess.run(
            [str(python), "-m", "pip", "install", "--no-deps", str(wheel)],
            cwd=empty_cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        _run_golden(python, cwd=empty_cwd)


def verify_source_archive(archive: Path) -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        with zipfile.ZipFile(archive) as bundle:
            for member in bundle.infolist():
                target = (root / member.filename).resolve()
                if root.resolve() not in target.parents:
                    raise ValueError(f"unsafe archive member: {member.filename}")
            bundle.extractall(root)
        source_roots = list(root.glob("*/src"))
        if len(source_roots) != 1:
            raise ValueError("lean source archive must contain one src directory")
        empty_cwd = root / "empty"
        empty_cwd.mkdir()
        env = dict(os.environ)
        env["PYTHONPATH"] = str(source_roots[0])
        _run_golden(Path(sys.executable), cwd=empty_cwd, env=env)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--source-archive", type=Path)
    args = parser.parse_args()
    wheel = args.wheel
    if wheel.is_dir():
        wheels = sorted(wheel.glob("catalytic_earth-0.1.0-*.whl"))
        if len(wheels) != 1:
            raise SystemExit(f"expected one 0.1.0 wheel in {wheel}, found {len(wheels)}")
        wheel = wheels[0]
    verify_wheel(wheel)
    if args.source_archive:
        verify_source_archive(args.source_archive)
    print("Fresh-directory core release verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
