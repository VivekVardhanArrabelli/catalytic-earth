"""Build seven bounded Atlas-10 review packets and validate the attempt ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "data/atlas/atlas10_selection.json"
KERNEL_PATH = ROOT / "data/atlas/atlas10/kernel.json"
REVIEW_ROOT = ROOT / "data/atlas/atlas10/review"
PACKET_ROOT = REVIEW_ROOT / "packets"
MANIFEST_PATH = REVIEW_ROOT / "packet_manifest.json"
LEDGER_PATH = REVIEW_ROOT / "review_attempts.json"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )
    return hashlib.sha256(raw).hexdigest()


def _slug(case_id: str) -> str:
    return case_id.removeprefix("atlas10.").replace(".", "--")


def _packet(
    selected: dict[str, Any], hypothesis: dict[str, Any], micro_questions: list[str]
) -> dict[str, Any]:
    return {
        "schema_version": "catalytic-earth.atlas10-review-packet.v1",
        "packet_id": f"review-packet:{selected['case_id']}",
        "review_unit": "bounded_claim_packet",
        "case_id": selected["case_id"],
        "target_record_id": selected["target_record_id"],
        "compiled_hypothesis_sha256": _canonical_sha256(hypothesis),
        "provenance": hypothesis["provenance"],
        "protein_scope": hypothesis["biological_scope"],
        "reaction_or_source_gap": hypothesis["reaction"],
        "source_proposals": [
            {
                "proposal_id": proposal["proposal_id"],
                "source_record_id": proposal["source_record_id"],
                "source_mechanism_id": proposal["source_mechanism_id"],
                "rating": proposal["rating"],
                "is_detailed": proposal["is_detailed"],
                "preferred": proposal["preferred"],
                "components_summary": proposal["components_summary"],
                "mechanism_text": proposal["mechanism_text"],
                "annotation_texts": proposal["annotation_texts"],
                "steps": [
                    {
                        "order": step["order"],
                        "source_step_id": step["source_step_id"],
                        "summary": step["summary"],
                        "is_inferred": step["is_inferred"],
                        "catalyst_site_ids": step["catalyst_site_ids"],
                        "source_scheme_sha256": step["source_scheme_sha256"],
                        "source_electron_flow_count": len(step["electron_flows"]),
                        "atom_mapping_status": step["atom_mapping_status"],
                        "bond_edit_status": step["bond_edit_status"],
                    }
                    for step in proposal["mechanism_steps"]
                ],
                "terminal_state_source_step_ids": proposal[
                    "terminal_state_source_step_ids"
                ],
                "structured_detail_status": proposal["structured_detail_status"],
                "scheme_retrieval_issues": proposal["scheme_retrieval_issues"],
            }
            for proposal in hypothesis["mechanism_proposals"]
        ],
        "sites": hypothesis["sites"],
        "structures": hypothesis["structures"],
        "evidence": hypothesis["evidence"],
        "counterevidence": hypothesis["counterevidence"],
        "uncertainties": hypothesis["uncertainties"],
        "detail_abstention": hypothesis["detail_abstention"],
        "claim_boundary": hypothesis["claim_boundary"],
        "review_questions": micro_questions,
        "reviewer_instruction": (
            "Review only the bounded case and cited source scope. A correction, uncertainty, or rejection is useful. Do not infer independent validation from upstream curation, source rating, fold similarity, or another case."
        ),
    }


def _markdown(packet: dict[str, Any]) -> str:
    reaction = packet["reaction_or_source_gap"]
    lines = [
        f"# Review packet: {packet['case_id']}",
        "",
        f"- Packet ID: `{packet['packet_id']}`",
        f"- Compiled hypothesis SHA-256: `{packet['compiled_hypothesis_sha256']}`",
        f"- Source snapshot set SHA-256: `{packet['provenance']['source_snapshot_set_sha256']}`",
        "",
        "## Scope",
        "",
        f"- Protein: {packet['protein_scope']['case_label']} ({packet['protein_scope']['organism']})",
        f"- EC: {packet['protein_scope']['ec_number']}",
        f"- UniProt: {', '.join(packet['protein_scope']['uniprot_ids'])}",
        f"- Direct PDB: {', '.join(packet['protein_scope']['direct_pdb_ids'])}",
        f"- Reaction status: `{reaction['source_status']}`",
        f"- Reaction record: `{reaction['source_record_id']}`",
        f"- Equation: {reaction['equation'] or 'NULL — documented source gap'}",
        "",
        "## Source proposals",
        "",
    ]
    for proposal in packet["source_proposals"]:
        lines.extend(
            [
                f"### M-CSA {proposal['source_record_id']} mechanism {proposal['source_mechanism_id']}",
                "",
                f"Rating `{proposal['rating']}`; detailed `{str(proposal['is_detailed']).lower()}`; preferred `{str(proposal['preferred']).lower()}`.",
                "",
                proposal["mechanism_text"],
                "",
            ]
        )
        if proposal["steps"]:
            for step in proposal["steps"]:
                lines.append(
                    f"- Step {step['order']} (source {step['source_step_id']}): {step['summary']} "
                    f"Sites: `{', '.join(step['catalyst_site_ids']) or 'none source-resolved'}`; "
                    f"source flows: `{step['source_electron_flow_count']}`; inferred: `{str(step['is_inferred']).lower()}`; "
                    "atom map/bond edits: abstained."
                )
        else:
            lines.append("- No discrete steps compiled; see the mandatory detail abstention below.")
        lines.append("")
    lines.extend(["## Sites and structures", ""])
    for site in packet["sites"]:
        mappings = ", ".join(
            f"{mapping['pdb_id']}:{mapping['chain_id']} author {mapping['author_position']} label {mapping['label_position']} ({mapping['applicability']})"
            for mapping in site["pdb_mappings"]
        )
        role_text = ", ".join(site["roles"]) or "source listed no role string"
        lines.append(f"- `{site['site_id']}` — {role_text}. Mappings: {mappings}.")
    lines.append("")
    for structure in packet["structures"]:
        lines.append(
            f"- `{structure['pdb_id']}` ({structure['applicability']}): {structure['limitation']}"
        )
    lines.extend(["", "## Counterevidence, uncertainty, and abstention", ""])
    for item in packet["counterevidence"]:
        lines.append(f"- Counterevidence `{item['counterevidence_id']}`: {item['summary']}")
    for item in packet["uncertainties"]:
        lines.append(f"- Open uncertainty `{item['uncertainty_id']}`: {item['summary']}")
    lines.extend(
        [
            f"- Mandatory detail abstention: {packet['detail_abstention']['reason']}",
            "",
            "## Evidence handles",
            "",
        ]
    )
    for item in packet["evidence"]:
        lines.append(
            f"- [{item['evidence_id']}]({item['uri']}) — {item['evidence_role']}; "
            f"applicability `{item['applicability']}`; retrieval `{item['retrieval_status']}`; "
            f"snapshot `{item['snapshot_sha256']}`."
        )
    lines.extend(["", "## Five micro-questions", ""])
    for index, question in enumerate(packet["review_questions"], 1):
        lines.append(f"{index}. {question}")
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "Supports:",
            "",
            *[f"- {item}" for item in packet["claim_boundary"]["supports"]],
            "",
            "Does not support:",
            "",
            *[f"- {item}" for item in packet["claim_boundary"]["does_not_support"]],
            "",
            packet["reviewer_instruction"],
            "",
        ]
    )
    return "\n".join(lines)


def _outputs() -> tuple[dict[Path, bytes], dict[str, Any]]:
    selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
    kernel = json.loads(KERNEL_PATH.read_text(encoding="utf-8"))
    hypotheses = {
        record["case_id"]: record
        for record in kernel["follow_on_records"]
        if record["object_type"] == "mechanism_hypothesis"
    }
    outputs: dict[Path, bytes] = {}
    manifest_rows: list[dict[str, Any]] = []
    for selected in selection["follow_on_cases"]:
        packet = _packet(
            selected, hypotheses[selected["case_id"]], selection["review_contract"]["micro_questions"]
        )
        slug = _slug(selected["case_id"])
        json_path = PACKET_ROOT / f"{slug}.json"
        markdown_path = PACKET_ROOT / f"{slug}.md"
        json_raw = _json_bytes(packet)
        markdown_raw = _markdown(packet).encode("utf-8")
        outputs[json_path] = json_raw
        outputs[markdown_path] = markdown_raw
        manifest_rows.append(
            {
                "packet_id": packet["packet_id"],
                "case_id": selected["case_id"],
                "json_path": json_path.relative_to(ROOT).as_posix(),
                "json_sha256": hashlib.sha256(json_raw).hexdigest(),
                "markdown_path": markdown_path.relative_to(ROOT).as_posix(),
                "markdown_sha256": hashlib.sha256(markdown_raw).hexdigest(),
                "compiled_hypothesis_sha256": packet["compiled_hypothesis_sha256"],
            }
        )
    manifest = {
        "schema_version": "catalytic-earth.atlas10-review-packet-manifest.v1",
        "review_unit": "bounded_claim_packet",
        "packet_count": len(manifest_rows),
        "packet_count_contract": {
            "minimum": selection["review_contract"]["packet_count_min"],
            "maximum": selection["review_contract"]["packet_count_max"],
        },
        "packets": manifest_rows,
    }
    outputs[MANIFEST_PATH] = _json_bytes(manifest)
    return outputs, manifest


def _initial_ledger(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "catalytic-earth.atlas10-review-attempt-ledger.v1",
        "status": "external_review_attempt_gate_pending",
        "honesty_rule": "No request, response, or independent review may be recorded without a real dated event and resolvable channel/reference.",
        "attempts": [
            {
                "packet_id": row["packet_id"],
                "packet_json_sha256": row["json_sha256"],
                "status": "not_attempted_missing_reviewer_channel",
                "attempted_at": None,
                "channel": None,
                "recipient": None,
                "request_reference": None,
                "response_status": "not_requested",
                "independent_review_completed": False,
                "note": "Packet is ready; no external request is claimed.",
            }
            for row in manifest["packets"]
        ],
    }


def _validate_ledger(ledger: dict[str, Any], manifest: dict[str, Any]) -> None:
    if ledger.get("schema_version") != "catalytic-earth.atlas10-review-attempt-ledger.v1":
        raise ValueError("review attempt ledger schema differs")
    expected = {row["packet_id"]: row["json_sha256"] for row in manifest["packets"]}
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or {item.get("packet_id") for item in attempts} != set(
        expected
    ):
        raise ValueError("review attempt ledger packet set differs")
    for item in attempts:
        if item.get("packet_json_sha256") != expected[item["packet_id"]]:
            raise ValueError("review attempt ledger packet hash differs")
        status = item.get("status")
        if status == "not_attempted_missing_reviewer_channel":
            if any(
                item.get(field) is not None
                for field in ("attempted_at", "channel", "recipient", "request_reference")
            ) or item.get("response_status") != "not_requested":
                raise ValueError("unattempted review entry fabricates request metadata")
        elif status in {
            "attempted_awaiting_response",
            "attempted_no_response",
            "response_received",
        }:
            for field in ("attempted_at", "channel", "recipient", "request_reference"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    raise ValueError(f"attempted review entry lacks {field}")
        else:
            raise ValueError(f"unsupported review attempt status: {status}")
        if item.get("independent_review_completed") is True and status != "response_received":
            raise ValueError("independent review completion lacks a response")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs, manifest = _outputs()
    if not LEDGER_PATH.exists() and not args.check:
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_PATH.write_bytes(_json_bytes(_initial_ledger(manifest)))
    if not LEDGER_PATH.exists():
        raise SystemExit("Atlas-10 review attempt ledger is missing")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    _validate_ledger(ledger, manifest)
    if args.check:
        stale = [
            path.relative_to(ROOT).as_posix()
            for path, expected in outputs.items()
            if not path.is_file() or path.read_bytes() != expected
        ]
        if stale:
            raise SystemExit(f"Atlas-10 review packet outputs are stale: {stale}")
        print("Atlas-10 review packets and attempt ledger are current")
        return 0
    for path, raw in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    attempted = sum(item["status"] != "not_attempted_missing_reviewer_channel" for item in ledger["attempts"])
    print(
        json.dumps(
            {
                "packet_count": manifest["packet_count"],
                "external_attempt_count": attempted,
                "external_attempt_gate": "complete" if attempted >= 1 else "pending",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
