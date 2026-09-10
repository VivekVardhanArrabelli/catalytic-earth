"""Export source-bound perturbation observations and eligible comparisons offline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_perturbations import project, verify_witnesses  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", help="Source study ID; retains evidence and comparison exclusions")
    parser.add_argument("--comparison", help="Exact comparison ID; retains all its control observations")
    parser.add_argument("--output", type=Path, help="Write JSON here instead of stdout")
    parser.add_argument("--verify-witnesses", action="store_true", help="Also hash-check retained primary files in the Git common directory; never fetch")
    parser.add_argument("--check", action="store_true", help="Resolve the relation and report compact integrity/coverage counts")
    args = parser.parse_args()
    result = project(ROOT)
    if args.verify_witnesses:
        common = subprocess.check_output(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, text=True).strip()
        result["source_witness_cache_status"] = verify_witnesses(ROOT / common, result)
    if args.study:
        if args.study not in {row["study_id"] for row in result["observations"]}:
            parser.error("unknown study ID")
        result["observations"] = [row for row in result["observations"] if row["study_id"] == args.study]
        result["comparisons"] = [row for row in result["comparisons"] if row["study_id"] == args.study]
    if args.comparison:
        result["comparisons"] = [row for row in result["comparisons"] if row["id"] == args.comparison]
        if not result["comparisons"]:
            parser.error("unknown comparison ID within selected scope")
        ids = {ref for row in result["comparisons"] for ref in row["roles"].values()}
        ids.update(ref for row in result["comparisons"] for ref in row.get("context_observations", []))
        result["observations"] = [row for row in result["observations"] if row["id"] in ids]
    comparison_ids = {item["id"] for item in result["comparisons"]}
    for row in result["observations"]:
        row["comparison_memberships"] = [item for item in row["comparison_memberships"]
                                         if item["comparison_id"] in comparison_ids]
    if args.check:
        print(json.dumps({"status": "source_projection_verified", "parameter_records": len(result["observations"]),
                          "comparison_requests": len(result["comparisons"]),
                          "eligible_descriptive_comparisons": sum(item["eligible"] for item in result["comparisons"]),
                          "primary_witness_cache": result["source_witness_cache_status"]}))
        return 0
    text = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
