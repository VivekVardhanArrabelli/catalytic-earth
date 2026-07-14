"""Verify the packaged Atlas-3 kernel from an empty working directory."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import venv
from pathlib import Path
from tempfile import TemporaryDirectory


EXPECTED_RUNTIME_RESULT_SHA256 = (
    "1c21a74b09b5812f27c18d49e891cbe9cad6030364a4b6a41a895cdccb1f1921"
)


def _venv_python(root: Path) -> Path:
    return root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def verify_wheel(wheel: Path) -> dict[str, object]:
    wheel = wheel.resolve()
    # Python 3.13 on Windows rejects a venv invoked through an 8.3-short TEMP
    # alias when its recorded prefix uses the equivalent long user path.
    # Anchoring under Path.home() keeps the fresh environment path canonical.
    with TemporaryDirectory(dir=Path.home()) as tmp:
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
        completed = subprocess.run(
            [str(python), "-m", "catalytic_earth.core_cli", "atlas3"],
            cwd=empty_cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout)
    if payload.get("runtime_result_sha256") != EXPECTED_RUNTIME_RESULT_SHA256:
        raise ValueError("installed Atlas-3 runtime result hash differs")
    if payload.get("case_count") != 3 or payload.get("record_count") != 9:
        raise ValueError("installed Atlas-3 case/record counts differ")
    if payload.get("source_mechanism_abstention_count") != 1:
        raise ValueError("installed Atlas-3 lost the source-mechanism abstention")
    if not payload.get("matches_expected"):
        raise ValueError("installed Atlas-3 did not match its packaged expectation")
    if any(
        payload.get(field) is not False
        for field in ("network_used", "external_binary_used", "accelerator_used")
    ):
        raise ValueError("installed Atlas-3 used an undeclared runtime dependency")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    args = parser.parse_args()
    wheel = args.wheel
    if wheel.is_dir():
        wheels = sorted(wheel.glob("catalytic_earth-*.whl"))
        if len(wheels) != 1:
            raise SystemExit(f"expected one wheel in {wheel}, found {len(wheels)}")
        wheel = wheels[0]
    payload = verify_wheel(wheel)
    print(
        "Fresh-directory Atlas-3 wheel verification passed: "
        f"cases={payload['case_count']}, records={payload['record_count']}, "
        f"runtime_result_sha256={payload['runtime_result_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
