"""Focused tests for additive, reviewed source-draft batch configuration."""

from __future__ import annotations

import copy
import contextlib
import io
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
from catalytic_earth.atlas_draft_catalog import query_source_draft_batches
from catalytic_earth.atlas_draft_query import query_source_drafts
from catalytic_earth.core_cli import main, verified_primary_evidence, verified_source_drafts


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
        self.assertEqual(set(BATCHES), {"default", "aldolase-transketolase", "plp-pyruvoyl"})
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


class SourceDraftCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundles = {name: verified_source_drafts(name) for name in BATCHES}
        cls.evidence = {
            name: verified_primary_evidence(name, bundle=bundle)
            for name, bundle in cls.bundles.items()
        }

    def query(self, **filters):
        return query_source_draft_batches(
            self.bundles, primary_evidence_by_batch=self.evidence, **filters,
        )

    def test_catalog_retains_exact_per_batch_queries_and_source_boundaries(self):
        result = self.query()
        self.assertEqual(result["searched_batch_ids"], sorted(BATCHES))
        self.assertEqual(result["searched_record_count"], 11)
        self.assertEqual(result["record_count"], 11)
        self.assertNotIn("mechanism_proposal_match_count", result)
        for item in result["batches"]:
            name = item["batch_id"]
            self.assertEqual(item["result"], query_source_drafts(
                self.bundles[name], primary_evidence=self.evidence[name],
            ))
        self.assertFalse(result["query_semantics"]["cross_batch_evidence_join"])

    def test_schiff_base_query_spans_batches_and_preserves_source_conflicts(self):
        before = copy.deepcopy((self.bundles, self.evidence))
        compact = self.query(mechanism_components=(" Schiff Base Formed ",))
        full = self.query(mechanism_components=("schiff base formed",), include_steps=True)
        self.assertEqual(compact["record_count"], 5)
        self.assertEqual(compact["mechanism_proposal_match_count"], 5)
        records = [r for b in compact["batches"] for r in b["result"]["records"]]
        self.assertEqual({r["mcsa_id"] for r in records}, {"M0753", "M0222", "M0049", "M0066", "M0213"})
        self.assertTrue(all(r["evidence_tier"] == 1 for r in records))
        for item, full_item in zip(compact["batches"], full["batches"]):
            for record, whole in zip(item["result"]["records"], full_item["result"]["records"]):
                self.assertEqual(record["mechanism_component_matches"], whole["mechanism_component_matches"])
                self.assertEqual(record["mandatory_abstentions"], whole["mandatory_abstentions"])
                self.assertTrue(record["mandatory_abstentions"])
        aldolase = next(r for r in records if r["mcsa_id"] == "M0222")
        self.assertEqual(aldolase["primary_evidence_annotations"], [self.evidence["aldolase-transketolase"]["annotations"][1]])
        self.assertEqual((self.bundles, self.evidence), before)

    def test_component_conjunction_cannot_join_alternative_proposals(self):
        result = self.query(mechanism_components=(
            "decoordination from a metal ion", "decarboxylation",
        ))
        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["mechanism_proposal_match_count"], 0)
        self.assertEqual(len(result["batches"]), 3)
        for item in result["batches"]:
            self.assertEqual(item["result"]["selection"], self.bundles[item["batch_id"]]["selection"])
            self.assertEqual(item["result"]["records"], [])

    def test_record_chemical_filter_preserves_the_proposal_match_scope(self):
        result = self.query(
            mechanism_components=("schiff base formed",), reactants=("57642",),
        )
        records = [r for b in result["batches"] for r in b["result"]["records"]]
        self.assertEqual([r["mcsa_id"] for r in records], ["M0222"])
        self.assertTrue(records[0]["participant_matches"])
        self.assertTrue(records[0]["mechanism_component_matches"])
        self.assertTrue(records[0]["mandatory_abstentions"])

    def test_catalog_rejects_mislabeled_bundles_and_orphan_evidence(self):
        with self.assertRaisesRegex(ValueError, "bundle identity"):
            query_source_draft_batches({"aldolase-transketolase": self.bundles["default"]})
        with self.assertRaisesRegex(ValueError, "unselected"):
            query_source_draft_batches(self.bundles, primary_evidence_by_batch={"missing": {}})
        with self.assertRaisesRegex(ValueError, "at least one"):
            query_source_draft_batches({})

    def test_filter_cannot_hide_duplicate_records_in_separate_batches(self):
        duplicate = copy.deepcopy(self.bundles["default"])
        duplicate["bundle_id"] = "atlas50.source-scoped-mechanism-drafts.copy"
        with self.assertRaisesRegex(ValueError, "multiple selected batches"):
            query_source_draft_batches(
                {"default": self.bundles["default"], "copy": duplicate},
                mcsa_id="M9999",
            )

    def test_cli_searches_all_batches_and_rejects_multiple_labels_in_one_flag(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["atlas-drafts", "--batch", "all", "--mechanism-component", "schiff base formed"])
        self.assertEqual(code, 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["record_count"], 5)
        self.assertEqual(result["searched_batch_ids"], sorted(BATCHES))
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            main(["atlas-drafts", "--mechanism-component", "proton transfer, electron transfer"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
