"""Focused tests for additive, reviewed source-draft batch configuration."""

from __future__ import annotations

import copy
import json
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from catalytic_earth.atlas50_state_probe import (
    declared_probe_case_ids,
    validate_probe_spec,
    validate_state_probe,
    validate_successor_probe_inheritance,
)
from catalytic_earth.atlas50_development_gate import (
    build_development_status,
    require_operation,
    validate_adjudications,
)
from catalytic_earth.atlas_draft_batch import (
    ALDOLASE_TRANSKETOLASE_BATCH,
    BATCHES,
    DEFAULT_BATCH,
    DraftBatchPaths,
    resolve_batch,
)


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE_SPEC = Path("data/atlas/atlas50/phase_a/candidate_spec.json")
PANEL_REVIEW = Path("data/atlas/atlas50/computational_review/panel_review.json")
MECHANISM_V3_SCHEMA = Path(
    "src/catalytic_earth/schemas/mechanism-record-v3.schema.json"
)
ATLAS3_KERNEL = Path("data/atlas/atlas3/kernel.json")
ATLAS10_KERNEL = Path("data/atlas/atlas10/kernel.json")


def _load(relative: Path) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class AtlasDraftBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.batch = ALDOLASE_TRANSKETOLASE_BATCH
        cls.spec = _load(cls.batch.probe_spec_path)
        cls.probe = _load(cls.batch.probe_report_path)
        cls.candidate_spec = _load(CANDIDATE_SPEC)
        cls.panel_review = _load(PANEL_REVIEW)
        cls.basis_inputs = cls.probe["basis_inputs"]

    def test_declarative_paths_are_immutable_and_resolve_by_name(self) -> None:
        self.assertIs(resolve_batch(None), DEFAULT_BATCH)
        self.assertIs(resolve_batch("default"), DEFAULT_BATCH)
        self.assertIs(
            resolve_batch("aldolase-transketolase"),
            ALDOLASE_TRANSKETOLASE_BATCH,
        )
        self.assertEqual(set(BATCHES), {"default", "aldolase-transketolase"})
        self.assertEqual(
            self.batch.manifest_path,
            self.batch.source_directory / "source_manifest.json",
        )
        self.assertEqual(
            self.batch.sources_directory, self.batch.source_directory / "sources"
        )
        self.assertEqual(
            self.batch.status_path, self.batch.gate_directory / "status.json"
        )
        with self.assertRaises(FrozenInstanceError):
            self.batch.batch_id = "changed"  # type: ignore[misc]
        with self.assertRaises(ValueError):
            resolve_batch("unknown")
        with self.assertRaises(ValueError):
            DraftBatchPaths(
                batch_id="unsafe",
                source_directory=Path("../outside"),
                probe_spec_path=Path("spec.json"),
                probe_report_path=Path("probe.json"),
                gate_directory=Path("review"),
                challenge_path=Path("challenge.json"),
            )

    def test_successor_declares_nine_cases_and_preserves_legacy_cases(self) -> None:
        declared = declared_probe_case_ids(self.spec, batch=self.batch)
        inherited = tuple(self.spec["inheritance"]["inherited_case_ids"])
        self.assertEqual(declared[: len(inherited)], inherited)
        self.assertEqual(len(declared), 9)
        validate_successor_probe_inheritance(
            self.spec, self.probe, repo_root=ROOT, batch=self.batch
        )
        base_spec = _load(DEFAULT_BATCH.probe_spec_path)
        base_probe = _load(DEFAULT_BATCH.probe_report_path)
        self.assertEqual(self.spec["cases"][:6], base_spec["cases"])
        self.assertEqual(self.probe["cases"][:6], base_probe["cases"])

    def test_successor_probe_is_deterministic_and_source_bounded(self) -> None:
        validate_state_probe(
            self.probe,
            spec=self.spec,
            candidate_spec=self.candidate_spec,
            panel_review=self.panel_review,
            mechanism_v3_schema=_load(MECHANISM_V3_SCHEMA),
            atlas3_kernel=_load(ATLAS3_KERNEL),
            atlas10_kernel=_load(ATLAS10_KERNEL),
            basis_inputs=self.basis_inputs,
            batch=self.batch,
            repo_root=ROOT,
        )
        self.assertIs(
            self.probe["external_source_checks"]["raw_source_bodies_committed"],
            False,
        )
        for case in self.probe["cases"][-3:]:
            self.assertEqual(case["contract_kind"], "component_state")
            self.assertEqual(
                case["allowed_operations"],
                ["source_annotation", "source_scoped_mechanism_draft"],
            )
            self.assertEqual(case["representation"]["state_transitions"], [])
            self.assertIsNone(case["representation"]["tethered_carrier"])
            self.assertIsNone(case["representation"]["polymer_topology"])
            self.assertIn(
                "complete_target_state",
                {
                    item["clause_id"]
                    for item in case["mandatory_abstentions"]
                },
            )

    def test_declared_ids_cannot_be_spoofed_past_frozen_candidate_identity(self) -> None:
        spoofed = copy.deepcopy(self.spec)
        spoofed["declared_case_ids"][-1] = "M9999"
        spoofed["cases"][-1]["mcsa_id"] = "M9999"
        spoofed["cases"][-1]["candidate_id"] = "atlas50.candidate.m9999"
        with self.assertRaisesRegex(ValueError, "frozen source/review identity"):
            validate_probe_spec(
                spoofed,
                candidate_spec=self.candidate_spec,
                panel_review=self.panel_review,
                batch=self.batch,
            )

    def test_inherited_case_and_exact_scope_changes_fail_closed(self) -> None:
        changed_inheritance = copy.deepcopy(self.spec)
        changed_inheritance["cases"][0]["label"] = "changed"
        with self.assertRaisesRegex(ValueError, "changed an inherited probe-spec case"):
            validate_successor_probe_inheritance(
                changed_inheritance,
                self.probe,
                repo_root=ROOT,
                batch=self.batch,
            )

        broadened = copy.deepcopy(self.spec)
        broadened["cases"][-1]["target_operation"] = "exact_reaction_instance"
        with self.assertRaisesRegex(ValueError, "target operation is invalid"):
            validate_probe_spec(
                broadened,
                candidate_spec=self.candidate_spec,
                panel_review=self.panel_review,
                batch=self.batch,
            )

    def test_successor_gate_preserves_inheritance_and_blocks_exact_instances(
        self,
    ) -> None:
        status = build_development_status(ROOT, batch=self.batch)
        self.assertEqual(
            [case["mcsa_id"] for case in status["cases"]],
            list(declared_probe_case_ids(self.spec, batch=self.batch)),
        )

        expected_new_abstentions = {
            "M0052": {"all_steps_enzyme_catalysed", "native_metal_identity"},
            "M0219": {
                "proposal_specific_reaction_context",
                "proposal_protein_applicability",
                "native_divalent_metal_identity",
                "typed_cofactor_redox_state",
            },
            "M0222": {
                "step_1_substrate_identity",
                "protein_specific_mechanism_applicability",
            },
        }
        for case in status["cases"][-3:]:
            case_id = case["mcsa_id"]
            self.assertEqual(
                case["allowed_operations"],
                ["source_annotation", "source_scoped_mechanism_draft"],
            )
            abstentions = {
                item["clause_id"] for item in case["mandatory_abstentions"]
            }
            self.assertIn("complete_target_state", abstentions)
            self.assertTrue(expected_new_abstentions[case_id] <= abstentions)
            require_operation(
                ROOT,
                "source_scoped_mechanism_draft",
                case_id,
                batch=self.batch,
            )
            with self.assertRaisesRegex(ValueError, "operation not authorized"):
                require_operation(
                    ROOT,
                    "exact_reaction_instance",
                    case_id,
                    batch=self.batch,
                )

        adjudications = _load(self.batch.adjudications_path)
        challenge = _load(self.batch.challenge_path)
        changed = copy.deepcopy(adjudications)
        changed["cases"][0]["resolution"] += " Mutated after inheritance."
        with self.assertRaisesRegex(
            ValueError, "changed an inherited adjudication case"
        ):
            validate_adjudications(
                changed,
                self.probe,
                challenge,
                case_id_order=declared_probe_case_ids(
                    self.spec, batch=self.batch
                ),
                batch=self.batch,
                repo_root=ROOT,
            )


if __name__ == "__main__":
    unittest.main()
