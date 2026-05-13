from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.transfer_scope import (
    audit_external_source_candidate_sample,
    build_external_ood_calibration_plan,
    build_external_source_candidate_sample,
    build_external_source_query_manifest,
    build_external_source_transfer_manifest,
)


ROOT = Path(__file__).resolve().parents[1]


class ExternalSourceTransferManifestTests(unittest.TestCase):
    def test_manifest_keeps_transfer_scope_non_countable(self) -> None:
        manifest = build_external_source_transfer_manifest(
            source_scale_audit={
                "metadata": {
                    "source_limit_reached": True,
                    "recommendation": "stop_m_csa_only_tranche_growth_and_scope_external_source_transfer",
                    "observed_source_entries": 1003,
                    "target_source_entries": 1025,
                    "public_target_countable_labels": 10000,
                }
            },
            learned_retrieval_manifest={"metadata": {"eligible_row_count": 617}},
            sequence_similarity_failure_sets={
                "metadata": {"duplicate_cluster_count": 6}
            },
            ontology_gap_audit={"metadata": {"row_count": 226}, "rows": []},
            active_learning_queue={
                "rows": [
                    {
                        "entry_id": "m_csa:1003",
                        "top1_ontology_family": "heme_redox",
                        "issue_classes": ["cofactor_family_ambiguity"],
                    }
                ]
            },
            labels=[
                {
                    "entry_id": "m_csa:1",
                    "label_type": "seed_fingerprint",
                    "review_status": "automation_curated",
                }
            ],
        )

        metadata = manifest["metadata"]
        self.assertFalse(metadata["ready_for_label_import"])
        self.assertEqual(metadata["countable_label_candidate_count"], 0)
        self.assertEqual(
            metadata["manifest_recommendation"],
            "prototype_external_source_transfer_before_next_count_growth",
        )
        self.assertIn("m_csa_source_limit_reached", manifest["blockers"])
        self.assertIn("heuristic geometry retrieval", manifest["required_guardrails"][0])

    def test_build_external_source_transfer_manifest_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_scale = root / "source_scale.json"
            learned = root / "learned.json"
            sequence = root / "sequence.json"
            ontology = root / "ontology.json"
            queue = root / "queue.json"
            labels = root / "labels.json"
            out = root / "transfer.json"
            source_scale.write_text(
                json.dumps({"metadata": {"source_limit_reached": True}}),
                encoding="utf-8",
            )
            learned.write_text(json.dumps({"metadata": {}}), encoding="utf-8")
            sequence.write_text(json.dumps({"metadata": {}}), encoding="utf-8")
            ontology.write_text(json.dumps({"metadata": {}, "rows": []}), encoding="utf-8")
            queue.write_text(json.dumps({"rows": []}), encoding="utf-8")
            labels.write_text(json.dumps([]), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-transfer-manifest",
                    "--source-scale-audit",
                    str(source_scale),
                    "--learned-retrieval-manifest",
                    str(learned),
                    "--sequence-similarity-failure-sets",
                    str(sequence),
                    "--ontology-gap-audit",
                    str(ontology),
                    "--active-learning-queue",
                    str(queue),
                    "--labels",
                    str(labels),
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["metadata"]["countable_label_candidate_count"], 0)

    def test_external_transfer_planning_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            transfer = root / "transfer.json"
            ontology = root / "ontology.json"
            sequence = root / "sequence.json"
            labels = root / "labels.json"
            queries = root / "queries.json"
            ood = root / "ood.json"
            sample = root / "sample.json"
            sample_audit = root / "sample_audit.json"
            transfer.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "manifest_recommendation": (
                                "prototype_external_source_transfer_before_next_count_growth"
                            ),
                            "m_csa_source_limit_reached": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            ontology.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "entry_id": "m_csa:1",
                                "scope_signals": ["transferase_phosphoryl"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            sequence.write_text(
                json.dumps({"metadata": {"duplicate_cluster_count": 1}}),
                encoding="utf-8",
            )
            labels.write_text(json.dumps([]), encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-source-query-manifest",
                    "--transfer-manifest",
                    str(transfer),
                    "--ontology-gap-audit",
                    str(ontology),
                    "--out",
                    str(queries),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "build-external-ood-calibration-plan",
                    "--query-manifest",
                    str(queries),
                    "--sequence-similarity-failure-sets",
                    str(sequence),
                    "--labels",
                    str(labels),
                    "--out",
                    str(ood),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )
            sample.write_text(
                json.dumps(
                    {
                        "rows": [
                            {
                                "accession": "P12345",
                                "reviewed": "reviewed",
                                "ec_numbers": ["2.7.1.1"],
                                "alphafold_ids": ["AF-P12345-F1"],
                                "countable_label_candidate": False,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "catalytic_earth.cli",
                    "audit-external-source-candidate-sample",
                    "--candidate-sample",
                    str(sample),
                    "--out",
                    str(sample_audit),
                ],
                cwd=ROOT,
                env={"PYTHONPATH": str(ROOT / "src")},
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                json.loads(queries.read_text(encoding="utf-8"))["metadata"][
                    "lane_count"
                ],
                1,
            )
            self.assertFalse(
                json.loads(ood.read_text(encoding="utf-8"))["metadata"][
                    "ready_for_label_import"
                ]
            )
            self.assertTrue(
                json.loads(sample_audit.read_text(encoding="utf-8"))["metadata"][
                    "guardrail_clean"
                ]
            )

    def test_query_manifest_uses_ontology_scope_signals(self) -> None:
        manifest = build_external_source_query_manifest(
            transfer_manifest={
                "metadata": {
                    "manifest_recommendation": (
                        "prototype_external_source_transfer_before_next_count_growth"
                    ),
                    "m_csa_source_limit_reached": True,
                }
            },
            ontology_gap_audit={
                "rows": [
                    {
                        "entry_id": "m_csa:603",
                        "scope_signals": ["transferase_phosphoryl"],
                    },
                    {
                        "entry_id": "m_csa:35",
                        "scope_signals": ["transferase_phosphoryl", "lyase"],
                    },
                ]
            },
            max_lanes=2,
        )

        self.assertEqual(manifest["metadata"]["lane_count"], 2)
        self.assertFalse(manifest["metadata"]["ready_for_label_import"])
        self.assertEqual(manifest["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(
            manifest["rows"][0]["lane_id"], "external_source:transferase_phosphoryl"
        )
        self.assertIn("kinase", manifest["rows"][0]["source_query_draft"])

    def test_ood_calibration_plan_keeps_external_lanes_review_only(self) -> None:
        plan = build_external_ood_calibration_plan(
            query_manifest={
                "rows": [
                    {
                        "lane_id": "external_source:lyase",
                        "scope_signal": "lyase",
                        "source_query_draft": "(reviewed:true) AND (ec:4.*)",
                    }
                ]
            },
            sequence_similarity_failure_sets={
                "metadata": {"duplicate_cluster_count": 2}
            },
            labels=[
                {
                    "entry_id": "m_csa:1",
                    "label_type": "out_of_scope",
                    "review_status": "automation_curated",
                }
            ],
        )

        self.assertFalse(plan["metadata"]["ready_for_label_import"])
        self.assertEqual(plan["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(plan["metadata"]["lane_count"], 1)
        self.assertEqual(plan["metadata"]["sequence_duplicate_cluster_count"], 2)
        self.assertIn(
            "exact_sequence_cluster_exclusion",
            plan["rows"][0]["calibration_controls"],
        )

    def test_candidate_sample_deduplicates_and_stays_non_countable(self) -> None:
        def fake_fetcher(query: str, size: int) -> dict:
            self.assertEqual(size, 2)
            return {
                "records": [
                    {
                        "accession": "P12345",
                        "entry_name": "KINASE_HUMAN",
                        "protein_name": "Example kinase",
                        "organism": "Homo sapiens",
                        "length": 300,
                        "reviewed": "reviewed",
                        "ec_numbers": ["2.7.1.1"],
                        "pdb_ids": ["1ABC"],
                        "alphafold_ids": ["AF-P12345-F1"],
                    },
                    {
                        "accession": "P12345",
                        "entry_name": "KINASE_HUMAN",
                        "protein_name": "Duplicate kinase",
                    },
                ]
            }

        sample = build_external_source_candidate_sample(
            query_manifest={
                "rows": [
                    {
                        "lane_id": "external_source:transferase_phosphoryl",
                        "scope_signal": "transferase_phosphoryl",
                        "source_query_draft": "reviewed:true",
                    }
                ]
            },
            max_records_per_lane=2,
            fetcher=fake_fetcher,
        )

        self.assertFalse(sample["metadata"]["ready_for_label_import"])
        self.assertEqual(sample["metadata"]["countable_label_candidate_count"], 0)
        self.assertEqual(sample["metadata"]["candidate_count"], 1)
        self.assertEqual(sample["rows"][0]["accession"], "P12345")
        self.assertFalse(sample["rows"][0]["countable_label_candidate"])

    def test_candidate_sample_audit_blocks_countable_external_rows(self) -> None:
        audit = audit_external_source_candidate_sample(
            {
                "rows": [
                    {
                        "accession": "P12345",
                        "reviewed": "reviewed",
                        "ec_numbers": ["2.7.1.1"],
                        "alphafold_ids": ["AF-P12345-F1"],
                        "countable_label_candidate": True,
                    }
                ]
            }
        )

        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertEqual(audit["metadata"]["countable_label_candidate_count"], 1)
        self.assertEqual(audit["metadata"]["reviewed_count"], 1)
        self.assertIn("external_rows_marked_countable", audit["blockers"])
