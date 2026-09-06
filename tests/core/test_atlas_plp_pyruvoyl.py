"""Inherited controls and source distinctions for the PLP/pyruvoyl batch."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas50_development_gate import (
    _validate_challenge_inheritance,
    build_development_status,
    require_operation,
)
from catalytic_earth.atlas50_state_probe import (
    declared_probe_case_ids,
    validate_probe_spec,
    validate_state_probe,
    validate_successor_probe_inheritance,
)
from catalytic_earth.atlas_draft_batch import (
    ALDOLASE_TRANSKETOLASE_BATCH,
    PLP_PYRUVOYL_BATCH,
)
from catalytic_earth.atlas_draft_query import query_source_drafts
from catalytic_earth.core_cli import verified_source_drafts


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE_SPEC = Path("data/atlas/atlas50/phase_a/candidate_spec.json")
PANEL_REVIEW = Path("data/atlas/atlas50/computational_review/panel_review.json")
MECHANISM_V3_SCHEMA = Path(
    "src/catalytic_earth/schemas/mechanism-record-v3.schema.json"
)
ATLAS3_KERNEL = Path("data/atlas/atlas3/kernel.json")
ATLAS10_KERNEL = Path("data/atlas/atlas10/kernel.json")
NEW_IDS = ("M0049", "M0066", "M0186", "M0213")


def _load(relative: Path) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class PlpPyruvoylControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.batch = PLP_PYRUVOYL_BATCH
        cls.spec = _load(cls.batch.probe_spec_path)
        cls.probe = _load(cls.batch.probe_report_path)
        cls.base_spec = _load(ALDOLASE_TRANSKETOLASE_BATCH.probe_spec_path)
        cls.base_probe = _load(ALDOLASE_TRANSKETOLASE_BATCH.probe_report_path)
        cls.challenge = _load(cls.batch.challenge_path)
        cls.candidate_spec = _load(CANDIDATE_SPEC)
        cls.panel_review = _load(PANEL_REVIEW)

    def test_thirteen_case_successor_preserves_all_nine_predecessor_decisions(self):
        declared = declared_probe_case_ids(self.spec, batch=self.batch)
        inherited = tuple(self.spec["inheritance"]["inherited_case_ids"])

        self.assertEqual(inherited, tuple(self.base_spec["declared_case_ids"]))
        self.assertEqual(declared, inherited + NEW_IDS)
        self.assertEqual(self.spec["cases"][:9], self.base_spec["cases"])
        self.assertEqual(self.probe["cases"][:9], self.base_probe["cases"])
        validate_successor_probe_inheritance(
            self.spec, self.probe, repo_root=ROOT, batch=self.batch,
        )

    def test_probe_rebuilds_with_source_bounded_new_identities(self):
        validate_state_probe(
            self.probe,
            spec=self.spec,
            candidate_spec=self.candidate_spec,
            panel_review=self.panel_review,
            mechanism_v3_schema=_load(MECHANISM_V3_SCHEMA),
            atlas3_kernel=_load(ATLAS3_KERNEL),
            atlas10_kernel=_load(ATLAS10_KERNEL),
            basis_inputs=self.probe["basis_inputs"],
            batch=self.batch,
            repo_root=ROOT,
        )
        self.assertIs(
            self.probe["external_source_checks"]["raw_source_bodies_committed"],
            False,
        )
        by_id = {case["mcsa_id"]: case for case in self.probe["cases"][-4:]}
        self.assertEqual(tuple(by_id), NEW_IDS)
        for case in by_id.values():
            self.assertEqual(case["contract_kind"], "component_state")
            self.assertEqual(
                case["allowed_operations"],
                ["source_annotation", "source_scoped_mechanism_draft"],
            )
            self.assertEqual(case["representation"]["state_transitions"], [])
            self.assertIsNone(case["representation"]["tethered_carrier"])
            self.assertIsNone(case["representation"]["polymer_topology"])
            self.assertEqual(case["missing_clauses"], ["complete_target_state"])

    def test_uncatalogued_successor_identity_is_checked_against_snapshot(self):
        changed = copy.deepcopy(self.spec)
        case = next(row for row in changed["cases"] if row["mcsa_id"] == "M0066")
        case["source_extract"]["uniprot_ids"] = ["P19939"]
        component = case["representation"]["components"][0]
        component["component_id"] = "protein:P19939"
        component["source_identifiers"][0]["accession"] = "P19939"
        case["representation"]["assembly"]["member_component_ids"] = [
            "protein:P19939"
        ]

        with self.assertRaisesRegex(ValueError, "invents or omits M-CSA protein"):
            validate_probe_spec(
                changed,
                candidate_spec=self.candidate_spec,
                panel_review=self.panel_review,
                batch=self.batch,
                repo_root=ROOT,
            )

        missing_evidence = copy.deepcopy(self.spec)
        missing_evidence["evidence"] = [
            item for item in missing_evidence["evidence"]
            if item["evidence_id"] != "source:M-CSA:M0066"
        ]
        with self.assertRaisesRegex(ValueError, "lacks exact official source evidence"):
            validate_probe_spec(
                missing_evidence,
                candidate_spec=self.candidate_spec,
                panel_review=self.panel_review,
                batch=self.batch,
                repo_root=ROOT,
            )

    def test_predecessor_substitution_and_inherited_case_edits_fail_closed(self):
        substituted = copy.deepcopy(self.spec)
        substituted["inheritance"]["base_batch_id"] = "default"
        with self.assertRaisesRegex(ValueError, "successor base batch differs"):
            declared_probe_case_ids(substituted, batch=self.batch)

        changed = copy.deepcopy(self.spec)
        changed["cases"][6]["label"] = "changed inherited decision"
        with self.assertRaisesRegex(ValueError, "changed an inherited probe-spec case"):
            validate_successor_probe_inheritance(
                changed, self.probe, repo_root=ROOT, batch=self.batch,
            )

        changed_challenge = copy.deepcopy(self.challenge)
        changed_challenge["claims"][0]["reasoning"] += " Changed downstream."
        with self.assertRaisesRegex(ValueError, "changed an inherited challenge claim"):
            _validate_challenge_inheritance(
                ROOT, changed_challenge, batch=self.batch,
            )

    def test_gate_keeps_case_specific_conflicts_and_blocks_exact_instances(self):
        status = build_development_status(ROOT, batch=self.batch)
        by_id = {case["mcsa_id"]: case for case in status["cases"][-4:]}
        expected = {
            "M0049": {
                "complete_target_state",
                "entry_scheme_substrate_identity",
                "pyruvoyl_maturation_mapping",
                "plp_equivalence",
            },
            "M0066": {
                "complete_target_state",
                "step_1_substrate_stereochemistry",
            },
            "M0186": {
                "complete_target_state",
                "plp_phosphate_base_assignment",
                "all_steps_enzyme_catalysed",
            },
            "M0213": {
                "complete_target_state",
                "direction_specific_role_assignment",
                "terminal_product_identity",
                "analogue_structure_context",
            },
        }
        for mcsa_id, clauses in expected.items():
            with self.subTest(mcsa_id=mcsa_id):
                case = by_id[mcsa_id]
                self.assertEqual(
                    case["allowed_operations"],
                    ["source_annotation", "source_scoped_mechanism_draft"],
                )
                self.assertTrue(
                    clauses
                    <= {item["clause_id"] for item in case["mandatory_abstentions"]}
                )
                require_operation(
                    ROOT, "source_scoped_mechanism_draft", mcsa_id,
                    batch=self.batch,
                )
                with self.assertRaisesRegex(ValueError, "operation not authorized"):
                    require_operation(
                        ROOT, "exact_reaction_instance", mcsa_id,
                        batch=self.batch,
                    )


class PlpPyruvoylSourceDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = verified_source_drafts("plp-pyruvoyl")

    def test_mechanism_components_retrieve_distinct_source_proposals(self):
        queries = (
            (("decarboxylation",), ["M0049"]),
            (("dehydration", "schiff base formed"), ["M0066"]),
            (("reaction occurs outside the enzyme",), ["M0186"]),
        )
        for components, expected in queries:
            with self.subTest(components=components):
                result = query_source_drafts(
                    self.bundle, mechanism_components=components,
                )
                self.assertEqual(
                    [record["mcsa_id"] for record in result["records"]],
                    expected,
                )
                self.assertEqual(
                    len(result["records"][0]["mechanism_component_matches"]), 1,
                )

    def test_directional_participants_isolate_alanine_racemase(self):
        result = query_source_drafts(
            self.bundle,
            reactants=("CHEBI:57972",),
            products=("CHEBI:57416",),
        )
        self.assertEqual([record["mcsa_id"] for record in result["records"]],
                         ["M0213"])
        self.assertEqual(
            [(row["normalized_chebi_id"], row["side"])
             for row in result["records"][0]["participant_matches"]],
            [("CHEBI:57972", "left"), ("CHEBI:57416", "right")],
        )
        self.assertEqual(
            result["query_semantics"]["side"],
            "left_or_right_in_the_source_drawing_not_physiological_direction",
        )

    def test_explicit_inference_and_assumption_tags_survive_compilation(self):
        record = query_source_drafts(
            self.bundle, mcsa_id="M0186", include_steps=True,
        )["records"][0]
        steps = {
            step["source_step_id"]: step
            for step in record["mechanism_proposals"][0]["mechanism_steps"]
        }
        self.assertIs(steps[4]["is_inferred"], True)
        self.assertIs(steps[5]["is_inferred"], True)
        self.assertIsNone(steps[6]["is_inferred"])
        self.assertIsNone(steps[7]["is_inferred"])
        self.assertIn("we infer", steps[4]["summary"].casefold())
        self.assertIn("we assume", steps[5]["summary"].casefold())
        self.assertTrue(
            all("outside the enzyme active site" in steps[index]["summary"]
                for index in (6, 7))
        )

    def test_source_scope_does_not_turn_pyruvoyl_into_plp(self):
        record = query_source_drafts(self.bundle, mcsa_id="M0049")["records"][0]
        self.assertIn("pyruvoyl", record["source_scope"].casefold())
        self.assertIn("do not relabel", record["source_scope"].casefold())
        self.assertTrue(
            {"plp_equivalence", "pyruvoyl_maturation_mapping"}
            <= {item["clause_id"] for item in record["mandatory_abstentions"]}
        )


if __name__ == "__main__":
    unittest.main()
