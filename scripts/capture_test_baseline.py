#!/usr/bin/env python3
"""Run the complete local suite and preserve a machine-verifiable baseline."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "data" / "governance" / "test_baseline.json"
COMPRESSED_LOG = ROOT / "release" / "validation" / "full-suite-python313-windows.log.gz"
LOCKFILE = ROOT / "requirements" / "ml.lock"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _parse_summary(raw: bytes, returncode: int) -> dict[str, int | float]:
    text = raw.decode("utf-8", errors="replace")
    ran = re.search(r"Ran ([0-9,]+) tests? in ([0-9.]+)s", text)
    if ran is None:
        raise ValueError("could not parse unittest run count and duration")
    failures = errors = skipped = 0
    failed = re.search(r"FAILED \(([^)]*)\)", text)
    ok = re.search(r"^OK(?: \(([^)]*)\))?\s*$", text, flags=re.MULTILINE)
    details = failed.group(1) if failed else (ok.group(1) if ok and ok.group(1) else "")
    for key, value in re.findall(r"(failures|errors|skipped)=([0-9]+)", details):
        if key == "failures":
            failures = int(value)
        elif key == "errors":
            errors = int(value)
        else:
            skipped = int(value)
    if returncode == 0 and failed is not None:
        raise ValueError("unittest returned zero but printed FAILED")
    if returncode != 0 and failed is None:
        raise ValueError("unittest failed without a parseable FAILED summary")
    return {
        "tests": int(ran.group(1).replace(",", "")),
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "duration_seconds": float(ran.group(2)),
    }


def _run_suite(*, stream: bool) -> tuple[bytes, int]:
    environment = dict(os.environ)
    existing = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = str(ROOT / "src") + (
        os.pathsep + existing if existing else ""
    )
    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    with tempfile.TemporaryFile() as log:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        assert process.stdout is not None
        for line in iter(process.stdout.readline, b""):
            if stream:
                sys.stdout.buffer.write(line)
                sys.stdout.buffer.flush()
            log.write(line)
        returncode = process.wait()
        log.seek(0)
        return log.read(), returncode


def _payload(raw_log: bytes, returncode: int) -> dict[str, object]:
    summary = _parse_summary(raw_log, returncode)
    compressed = gzip.compress(raw_log, compresslevel=9, mtime=0)
    COMPRESSED_LOG.parent.mkdir(parents=True, exist_ok=True)
    COMPRESSED_LOG.write_bytes(compressed)
    lock_raw = LOCKFILE.read_bytes()
    return {
        "schema_version": "catalytic-earth.test-baseline.v1",
        "recorded_date": date.today().isoformat(),
        "historical_audit": {
            "python": "3.13.2",
            "os": "Windows",
            "tests": 2559,
            "failures": 74,
            "errors": 20,
            "skipped": 1,
            "status": "preserved_not_green",
        },
        "root_cause_correction": {
            "test_failures_previously_attributed_to_stale_hashes": 54,
            "underlying_crlf_only_hash_comparisons": 179,
            "genuine_current_content_lineage_drifts": 1,
            "genuine_drift_disposition": (
                "historical artifact quarantined; embedded hash not refreshed"
            ),
            "other_remediated_classes": [
                "undeclared ML test dependencies",
                "Windows long paths and POSIX path assumptions",
                "scikit-learn sparse index-width compatibility",
                "test subprocess environment replacement",
                "newline-sensitive test fixtures",
            ],
        },
        "current_validation": {
            "command": "python -m unittest discover -s tests -v",
            "return_code": returncode,
            **summary,
            "status": "green" if returncode == 0 else "failed",
        },
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "os": platform.system(),
            "os_release": platform.release(),
            "requirements_lock": "requirements/ml.lock",
            "requirements_lock_sha256": _sha(lock_raw),
        },
        "log": {
            "path": COMPRESSED_LOG.relative_to(ROOT).as_posix(),
            "compression": "gzip",
            "uncompressed_bytes": len(raw_log),
            "uncompressed_sha256": _sha(raw_log),
            "compressed_bytes": len(compressed),
            "compressed_sha256": _sha(compressed),
        },
        "source_binding": (
            "This baseline and its log are hashed by release/release_manifest.json "
            "against the exact source commit."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-failed",
        action="store_true",
        help="write a failed baseline instead of returning immediately after capture",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="preserve the complete log without echoing every test name",
    )
    args = parser.parse_args()
    raw_log, returncode = _run_suite(stream=not args.quiet)
    payload = _payload(raw_log, returncode)
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {BASELINE.relative_to(ROOT)} and {COMPRESSED_LOG.relative_to(ROOT)}")
    if returncode and not args.allow_failed:
        return returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
