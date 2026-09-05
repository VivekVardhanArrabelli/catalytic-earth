"""Focused source-fidelity tests for the reusable Atlas draft compiler."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas50_development_gate import build_development_status
from catalytic_earth.atlas_draft_sources import load_draft_sources
from catalytic_earth.atlas_drafts import (
    SCHEMA_PATH,
    _build_source_drafts,
    _mechanism_proposals,
    build_source_drafts,
    validate_source_drafts,
)


ROOT = Path(__file__).resolve().parents[2]


def _record(bundle: dict, mcsa_id: str) -> dict:
    return next(item for item in bundle["records"] if item["mcsa_id"] == mcsa_id)


class AtlasDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = build_source_drafts(ROOT)
        cls.manifest, cls.entries = load_draft_sources(ROOT)
        cls.gate = build_development_status(ROOT)
        cls.probe = json.loads(
            (ROOT / "data/atlas/atlas50/state_probe/report.json").read_text(
                encoding="utf-8"
            )
        )

    def test_live_bundle_is_dynamic_tier_one_source_content(self) -> None:
        summary = validate_source_drafts(self.bundle)
        selected = self.manifest["selection"]["record_ids"]
        self.assertEqual([item["mcsa_id"] for item in self.bundle["records"]], selected)
        self.assertEqual(summary["record_count"], len(selected))
        self.assertEqual(summary["source_scoped_mechanism_draft_count"], len(selected))
        self.assertEqual(summary["evidence_tier_counts"], {"1": len(selected)})
        self.assertEqual(summary["canonical_reaction_count"], 0)
        self.assertEqual(summary["exact_reaction_instance_count"], 0)
        self.assertEqual(summary["tier_2_record_count"], 0)

    def test_schema_accepts_every_live_record(self) -> None:
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("jsonschema is not installed in this test environment")
        schema = json.loads((ROOT / SCHEMA_PATH).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        errors = [
            error
            for record in self.bundle["records"]
            for error in validator.iter_errors(record)
        ]
        self.assertEqual(errors, [])

    def test_source_alternatives_and_every_source_step_are_required(self) -> None:
        missing_alternative = copy.deepcopy(self.bundle)
        _record(missing_alternative, "M0107")["mechanism_proposals"].pop()
        with self.assertRaisesRegex(ValueError, "mechanism alternatives differ"):
            validate_source_drafts(missing_alternative)

        missing_step = copy.deepcopy(self.bundle)
        _record(missing_step, "M0106")["mechanism_proposals"][0][
            "mechanism_steps"
        ].pop()
        with self.assertRaisesRegex(ValueError, "omits or invents source steps"):
            validate_source_drafts(missing_step)

    def test_invented_electron_flow_and_source_residue_fail_closed(self) -> None:
        invented_flow = copy.deepcopy(self.bundle)
        step = _record(invented_flow, "M0106")["mechanism_proposals"][0][
            "mechanism_steps"
        ][0]
        step["electron_flows"].append(copy.deepcopy(step["electron_flows"][0]))
        with self.assertRaisesRegex(ValueError, "omits or invents source electron flows"):
            validate_source_drafts(invented_flow)

        invented_residue = copy.deepcopy(self.bundle)
        assertion = _record(invented_residue, "M0106")["source_residue_assertions"][0]
        assertion["source_role_labels"].append("invented catalytic role")
        with self.assertRaisesRegex(ValueError, "source projection binding differs"):
            validate_source_drafts(invented_residue)

    def test_scope_abstention_and_tier_cannot_be_promoted(self) -> None:
        broad_scope = copy.deepcopy(self.bundle)
        _record(broad_scope, "M0106")["source_scope"] = (
            "A complete exact carrier mechanism is established."
        )
        with self.assertRaisesRegex(ValueError, "scope or abstention binding differs"):
            validate_source_drafts(broad_scope)

        dropped_abstention = copy.deepcopy(self.bundle)
        _record(dropped_abstention, "M0106")["mandatory_abstentions"].pop()
        with self.assertRaisesRegex(ValueError, "scope or abstention binding differs"):
            validate_source_drafts(dropped_abstention)

        promoted_tier = copy.deepcopy(self.bundle)
        _record(promoted_tier, "M0107")["evidence_tier"] = 2
        with self.assertRaisesRegex(ValueError, "must remain Tier 1"):
            validate_source_drafts(promoted_tier)

    def test_manifest_operation_must_be_allowed_by_the_gate(self) -> None:
        denied_gate = copy.deepcopy(self.gate)
        selected_id = self.manifest["selection"]["record_ids"][0]
        gate_case = next(
            item for item in denied_gate["cases"] if item["mcsa_id"] == selected_id
        )
        gate_case["allowed_operations"].remove("source_scoped_mechanism_draft")
        with self.assertRaisesRegex(ValueError, "development gate denies"):
            _build_source_drafts(
                source_manifest=self.manifest,
                entries=self.entries,
                development_gate=denied_gate,
                state_probe=self.probe,
                input_bindings=self.bundle["input_bindings"],
            )

    def test_missing_scheme_retains_step_text_and_explicitly_abstains(self) -> None:
        entry = copy.deepcopy(self.entries["M0106"])
        mechanism = entry["mechanisms"][0]
        source_step = next(step for step in mechanism["steps"] if not step["is_product"])
        key = mechanism["mechanism_id"], source_step["step_id"]
        wrapper = entry["scheme_index"][key]
        wrapper.update(
            {
                "content_sha256": None,
                "content_utf8": None,
                "electron_flow_count": None,
                "flow_parse_error": None,
                "flow_parse_status": "source_scheme_unavailable",
                "http_status": 404,
                "retrieval_status": "source_link_missing_http_404",
            }
        )
        proposal = _mechanism_proposals(
            entry,
            "M0106",
            requested_operation="source_scoped_mechanism_draft",
        )[0]
        step = next(
            item
            for item in proposal["mechanism_steps"]
            if item["source_step_id"] == source_step["step_id"]
        )
        self.assertEqual(step["summary"], source_step["description"])
        self.assertEqual(step["electron_flows"], [])
        self.assertIn("unavailable", step["electron_flow_abstention"])
        self.assertEqual(
            proposal["structured_detail_status"],
            "source_steps_preserved_with_flow_abstentions",
        )

    def test_hisf_source_role_conflict_remains_unresolved(self) -> None:
        hisf = _record(self.bundle, "M0753")
        self.assertIn(
            "resolved_aspartate_roles",
            {item["clause_id"] for item in hisf["mandatory_abstentions"]},
        )
        self.assertEqual(
            hisf["residue_role_resolution"],
            {
                "status": "source_conflict_unresolved",
                "abstention_clause_ids": ["resolved_aspartate_roles"],
            },
        )
        falsely_resolved = copy.deepcopy(self.bundle)
        _record(falsely_resolved, "M0753")["residue_role_resolution"] = {
            "status": "source_transcription_only_not_independently_adjudicated",
            "abstention_clause_ids": [],
        }
        with self.assertRaisesRegex(ValueError, "residue-role conflict binding differs"):
            validate_source_drafts(falsely_resolved)

    def test_inference_flag_requires_an_explicit_source_tag(self) -> None:
        nitrogenase = _record(self.bundle, "M0212")
        hedged_step = next(
            step
            for proposal in nitrogenase["mechanism_proposals"]
            for step in proposal["mechanism_steps"]
            if "is thought to" in step["summary"]
        )
        self.assertIsNone(hedged_step["is_inferred"])

        explicitly_inferred = next(
            step
            for record in self.bundle["records"]
            for proposal in record["mechanism_proposals"]
            for step in proposal["mechanism_steps"]
            if "inferred return step" in step["summary"]
        )
        self.assertIs(explicitly_inferred["is_inferred"], True)

        guessed_not_inferred = copy.deepcopy(self.bundle)
        guessed_step = next(
            step
            for proposal in _record(guessed_not_inferred, "M0212")[
                "mechanism_proposals"
            ]
            for step in proposal["mechanism_steps"]
            if "is thought to" in step["summary"]
        )
        guessed_step["is_inferred"] = False
        with self.assertRaisesRegex(ValueError, "explicit source tag"):
            validate_source_drafts(guessed_not_inferred)


if __name__ == "__main__":
    unittest.main()
