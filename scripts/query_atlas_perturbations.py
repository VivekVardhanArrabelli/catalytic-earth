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
    parser.add_argument("--state-link", help="Exact construct-to-state link; retains its functional observations")
    parser.add_argument("--model-link", help="Exact source-model transition link; retains its existing endpoint observations")
    parser.add_argument("--control-relation", help="Exact two-system source contrast; retains original arm rows, systems and normalization")
    parser.add_argument("--with-comparisons", action="store_true", help="With --state-link, include ratio and multiplicative comparisons using its observations as controls, including abstentions; states remain parent-only")
    parser.add_argument("--output", type=Path, help="Write JSON here instead of stdout")
    parser.add_argument("--verify-witnesses", action="store_true", help="Also hash-check retained primary files in the Git common directory; never fetch")
    parser.add_argument("--check", action="store_true", help="Resolve the relation and report compact integrity/coverage counts")
    args = parser.parse_args()
    if sum(bool(value) for value in (args.state_link, args.comparison, args.model_link, args.control_relation)) > 1:
        parser.error("--state-link, --model-link, --comparison and --control-relation select different relations")
    if args.with_comparisons and not args.state_link:
        parser.error("--with-comparisons requires --state-link")
    result = project(ROOT)
    if args.verify_witnesses:
        common = subprocess.check_output(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, text=True).strip()
        result["source_witness_cache_status"] = verify_witnesses(ROOT / common, result)
    if args.study:
        studies = {row["study_id"] for row in result["observations"] + result["control_relations"]}
        if args.study not in studies:
            parser.error("unknown study ID")
        result["observations"] = [row for row in result["observations"] if row["study_id"] == args.study]
        result["comparisons"] = [row for row in result["comparisons"] if row["study_id"] == args.study]
        result["state_links"] = [row for row in result["state_links"] if row["study_id"] == args.study]
        result["model_links"] = [row for row in result["model_links"] if row["study_id"] == args.study]
        result["control_relations"] = [row for row in result["control_relations"] if row["study_id"] == args.study]
    if args.control_relation:
        result["control_relations"] = [row for row in result["control_relations"] if row["id"] == args.control_relation]
        if not result["control_relations"]:
            parser.error("unknown control relation within selected scope")
        result["observations"] = []
        result["comparisons"] = []
        result["state_links"] = []
        result["model_links"] = []
    elif args.comparison or args.state_link or args.model_link:
        result["control_relations"] = []
    if args.comparison:
        result["comparisons"] = [row for row in result["comparisons"] if row["id"] == args.comparison]
        if not result["comparisons"]:
            parser.error("unknown comparison ID within selected scope")
        ids = {ref for row in result["comparisons"] for ref in row["roles"].values()}
        ids.update(ref for row in result["comparisons"] for ref in row.get("context_observations", []))
        result["observations"] = [row for row in result["observations"] if row["id"] in ids]
    if args.state_link:
        result["state_links"] = [row for row in result["state_links"] if row["id"] == args.state_link]
        if not result["state_links"]:
            parser.error("unknown state link within selected scope")
        ids = {ref for link in result["state_links"] for ref in link["observation_ids"]}
        result["comparisons"] = [
            row for row in result["comparisons"]
            if args.with_comparisons
            and row["operation"] in {"ratio", "multiplicative"}
            and row["roles"].get("denominator", row["roles"].get("parent")) in ids
        ]
        ids.update(ref for row in result["comparisons"] for ref in row["roles"].values())
        ids.update(ref for row in result["comparisons"] for ref in row.get("context_observations", []))
        result["observations"] = [row for row in result["observations"] if row["id"] in ids]
    if args.model_link:
        result["model_links"] = [row for row in result["model_links"] if row["id"] == args.model_link]
        if not result["model_links"]:
            parser.error("unknown model link within selected scope")
        ids = {ref for link in result["model_links"] for ref in link["observation_ids"]}
        result["observations"] = [row for row in result["observations"] if row["id"] in ids]
        result["comparisons"] = []
    selected_ids = {row["id"] for row in result["observations"]}
    result["state_links"] = [link for link in result["state_links"]
                             if set(link["observation_ids"]) <= selected_ids]
    result["model_links"] = [link for link in result["model_links"]
                             if set(link["observation_ids"]) <= selected_ids]
    comparison_ids = {item["id"] for item in result["comparisons"]}
    for row in result["observations"]:
        row["comparison_memberships"] = [item for item in row["comparison_memberships"]
                                         if item["comparison_id"] in comparison_ids]
    if args.check:
        print(json.dumps({"status": "source_projection_verified", "parameter_records": len(result["observations"]),
                          "comparison_requests": len(result["comparisons"]),
                          "state_links": len(result["state_links"]),
                          "model_links": len(result["model_links"]),
                          "system_control_relations": len(result["control_relations"]),
                          "eligible_system_ratios": sum(item["eligible"] for item in result["control_relations"]),
                          "eligible_descriptive_comparisons": sum(item["eligible"] for item in result["comparisons"]),
                          "primary_witness_cache": result["source_witness_cache_status"]}))
        return 0
    text = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        # JSON transport must preserve source symbols across platform locales.
        sys.stdout.reconfigure(encoding="utf-8")
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
