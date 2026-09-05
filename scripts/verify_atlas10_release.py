"""Verify the packaged Atlas-10 query surface from an empty working directory."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import venv
from pathlib import Path
from tempfile import TemporaryDirectory


EXPECTED_RUNTIME_RESULT_SHA256 = (
    "57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb"
)


def _venv_python(root: Path) -> Path:
    return root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def verify_wheel(wheel: Path, *, include_source_drafts: bool = False) -> dict[str, object]:
    wheel = wheel.resolve()
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
            [str(python), "-m", "catalytic_earth.core_cli", "atlas10"],
            cwd=empty_cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout)
        if include_source_drafts:
            # A packaged query must work without the checkout, raw snapshots,
            # inherited PYTHONPATH, or a network connection.
            isolated_env = dict(os.environ)
            isolated_env.pop("PYTHONPATH", None)
            query = (
                "import sys\n"
                "def block_network(event, args):\n"
                "    if event == 'socket.connect':\n"
                "        raise RuntimeError('network is forbidden during offline query')\n"
                "sys.addaudithook(block_network)\n"
                "from catalytic_earth.core_cli import main\n"
                "raise SystemExit(main(['atlas-drafts', '--steps']))\n"
            )
            draft_run = subprocess.run(
                [str(python), "-c", query], cwd=empty_cwd, env=isolated_env,
                check=True, capture_output=True, text=True,
            )
            drafts = json.loads(draft_run.stdout)
            records = drafts["records"]
            if {record["mcsa_id"] for record in records} != {"M0106", "M0107", "M0212", "M0753"}:
                raise ValueError("installed source draft batch differs")
            if len(records) != 4 or any(record["evidence_tier"] != 1 for record in records):
                raise ValueError("installed source drafts overstate their record count or tier")
            hisf = next(record for record in records if record["mcsa_id"] == "M0753")
            if not any(item["clause_id"] == "resolved_aspartate_roles"
                       for item in hisf["mandatory_abstentions"]):
                raise ValueError("installed source draft lost HisF source conflict")
            if not any(proposal["mechanism_steps"] for record in records
                       for proposal in record["mechanism_proposals"]):
                raise ValueError("installed source draft package lacks source steps")
            print("Fresh-directory source draft query passed with network connections blocked")
    expected_counts = {
        "case_count": 10,
        "record_count": 30,
        "follow_on_case_count": 7,
        "follow_on_record_count": 21,
        "documented_rhea_gap_count": 3,
        "non_detailed_abstention_count": 1,
        "source_mechanism_step_count": 21,
        "source_electron_flow_count": 61,
    }
    if any(payload.get(field) != value for field, value in expected_counts.items()):
        raise ValueError("installed Atlas-10 case/truth counts differ")
    if payload.get("runtime_result_sha256") != EXPECTED_RUNTIME_RESULT_SHA256:
        raise ValueError("installed Atlas-10 runtime result hash differs")
    query_results = payload.get("relationship_query_results", {})
    if {query_id: len(rows) for query_id, rows in query_results.items()} != {
        "atlas10.query.convergent-strategy": 2,
        "atlas10.query.shared-fold-divergent-chemistry": 2,
    }:
        raise ValueError("installed Atlas-10 relationship query rows differ")
    if not payload.get("matches_expected"):
        raise ValueError("installed Atlas-10 did not match its packaged expectation")
    if any(
        payload.get(field) is not False
        for field in ("network_used", "external_binary_used", "accelerator_used")
    ):
        raise ValueError("installed Atlas-10 used an undeclared runtime dependency")
    rendered = json.dumps(payload)
    for required in (
        "engineered_source_reference",
        "documented_query_gap",
        "historical_fingerprint_bridge",
        "inferred=1",
    ):
        if required not in rendered:
            raise ValueError(f"installed Atlas-10 lost required boundary: {required}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--include-source-drafts", action="store_true")
    args = parser.parse_args()
    wheel = args.wheel
    if wheel.is_dir():
        wheels = sorted(wheel.glob("catalytic_earth-*.whl"))
        if len(wheels) != 1:
            raise SystemExit(f"expected one wheel in {wheel}, found {len(wheels)}")
        wheel = wheels[0]
    payload = verify_wheel(wheel, include_source_drafts=args.include_source_drafts)
    print(
        "Fresh-directory Atlas-10 wheel verification passed: "
        f"cases={payload['case_count']}, records={payload['record_count']}, "
        f"runtime_result_sha256={payload['runtime_result_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
