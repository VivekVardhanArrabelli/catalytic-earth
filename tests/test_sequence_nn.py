import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.labels import MechanismLabel
from catalytic_earth.sequence_nn import (
    build_sequence_nn_label_manifest_and_compliance,
)


class SequenceNearestNeighborBaselineTests(unittest.TestCase):
    def test_incomplete_current_split_blocks_predictions_and_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = [
                MechanismLabel(
                    entry_id="m_csa:5",
                    fingerprint_id="ser_his_acid_hydrolase",
                    label_type="seed_fingerprint",
                    confidence="medium",
                    rationale="fixture",
                ),
                MechanismLabel(
                    entry_id="m_csa:204",
                    fingerprint_id=None,
                    label_type="out_of_scope",
                    confidence="medium",
                    rationale="fixture",
                ),
            ]
            paths = _fixture_paths(root)
            result = build_sequence_nn_label_manifest_and_compliance(
                labels=labels,
                fingerprints=[object()] * 8,
                coherence_audit={
                    "fingerprints_kept_for_primary_metric": [
                        "ser_his_acid_hydrolase"
                    ]
                },
                eval_contract=_eval_contract(),
                sequence_manifest={
                    "metadata": {
                        "current_label_count": 2,
                        "missing_sequence_entry_count": 0,
                        "sequence_covered_label_count": 2,
                    },
                    "rows": [
                        _sequence_row("m_csa:5", "P00005", "aaa"),
                        _sequence_row("m_csa:204", "P00104", "bbb"),
                    ],
                },
                split_artifact={
                    "metadata": {
                        "label_registry_count": 2,
                        "evaluated_count": 1,
                        "heldout_count": 1,
                        "in_distribution_count": 0,
                        "sequence_identity_target_achieved": True,
                    },
                    "rows": [
                        {
                            "entry_id": "m_csa:5",
                            "partition": "heldout",
                            "real_sequence_identity_cluster_id": "mmseqs30:m_csa:5",
                        }
                    ],
                },
                **paths,
            )

        manifest = result["label_manifest"]
        compliance = result["compliance"]
        self.assertEqual(manifest["metadata"]["status"], "blocked_split_incomplete")
        self.assertEqual(
            manifest["metadata"]["split_assignment_missing_entry_ids"],
            ["m_csa:204"],
        )
        blocker_reasons = {row["reason"] for row in compliance["blockers"]}
        self.assertIn("split_artifact_missing_current_label_rows", blocker_reasons)
        self.assertEqual(
            compliance["metadata"]["status"], "blocked_before_sequence_nn_metrics"
        )
        self.assertFalse(compliance["metadata"]["prediction_metrics_reported"])
        self.assertEqual(
            compliance["split_assignment_blocker"]["status"],
            "blocked_split_incomplete",
        )
        self.assertEqual(
            compliance["split_assignment_blocker"]["missing_current_label_rows"],
            [
                {
                    "accession": "P00104",
                    "benchmark_role": "oos_tier::unknown_oos",
                    "blocker": "missing_partition_in_split_artifact",
                    "entry_id": "m_csa:204",
                    "fingerprint_id": None,
                    "label_type": "out_of_scope",
                    "manifest_status": "blocked_missing_sequence_or_split",
                    "oos_tier": "unknown_oos",
                    "probe_role": "unknown_oos_abstention_diagnostic",
                    "sequence_coverage_status": "covered",
                    "sequence_id": "P00104",
                    "sequence_record_count": 1,
                    "sequence_sha256": "bbb",
                }
            ],
        )
        self.assertEqual(
            compliance["primary_seed_metrics"]["status"],
            "not_reported_split_blocked",
        )

    def test_secondary_probe_rows_get_contract_probe_role(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            labels = [
                MechanismLabel(
                    entry_id="m_csa:372",
                    fingerprint_id="radical_sam_enzyme",
                    label_type="seed_fingerprint",
                    confidence="medium",
                    rationale="fixture",
                )
            ]
            paths = _fixture_paths(root)
            result = build_sequence_nn_label_manifest_and_compliance(
                labels=labels,
                fingerprints=[object()] * 8,
                coherence_audit={
                    "fingerprints_kept_for_primary_metric": [
                        "ser_his_acid_hydrolase"
                    ]
                },
                eval_contract=_eval_contract(),
                sequence_manifest={
                    "metadata": {
                        "current_label_count": 1,
                        "missing_sequence_entry_count": 0,
                        "sequence_covered_label_count": 1,
                    },
                    "rows": [_sequence_row("m_csa:372", "P00372", "ccc")],
                },
                split_artifact={
                    "metadata": {
                        "label_registry_count": 1,
                        "evaluated_count": 1,
                        "heldout_count": 1,
                        "in_distribution_count": 0,
                        "sequence_identity_target_achieved": True,
                    },
                    "rows": [
                        {
                            "entry_id": "m_csa:372",
                            "partition": "heldout",
                            "real_sequence_identity_cluster_id": "mmseqs30:m_csa:372",
                        }
                    ],
                },
                **paths,
            )

        row = result["label_manifest"]["rows"][0]
        self.assertEqual(row["benchmark_role"], "secondary_ood_probe::radical_sam_enzyme")
        self.assertEqual(row["oos_tier"], "far_oos")
        self.assertEqual(row["probe_role"], "far_oos_tail_diagnostic")


def _fixture_paths(root: Path) -> dict[str, Path]:
    names = {
        "label_registry_path": "labels.json",
        "fingerprint_registry_path": "fingerprints.json",
        "coherence_audit_path": "coherence.json",
        "eval_contract_path": "contract.json",
        "sequence_manifest_path": "sequence_manifest.json",
        "split_artifact_path": "split.json",
        "label_manifest_out": "label_manifest.json",
        "predictions_out": "predictions.jsonl",
        "metrics_out": "metrics.json",
        "compliance_out": "compliance.json",
    }
    paths = {key: root / name for key, name in names.items()}
    for key, path in paths.items():
        if key.endswith("_out"):
            continue
        path.write_text(json.dumps({"fixture": key}), encoding="utf-8")
    return paths


def _sequence_row(entry_id: str, accession: str, sequence_hash: str) -> dict[str, object]:
    return {
        "entry_id": entry_id,
        "coverage_status": "covered",
        "sequence_record_count": 1,
        "sequence_records": [
            {
                "accession_or_structure_id": accession,
                "sequence_sha256": sequence_hash,
                "sequence_length": 100,
                "sequence_source_type": "fixture",
            }
        ],
    }


def _eval_contract() -> dict[str, object]:
    return {
        "mechanism_fingerprint_version": "label_factory_v1_8fp",
        "primary_fingerprints": ["ser_his_acid_hydrolase"],
        "secondary_ood_probe_fingerprints": [
            {
                "fingerprint_id": "radical_sam_enzyme",
                "oos_tier": "far_oos",
                "probe_role": "far_oos_tail_diagnostic",
            }
        ],
        "canary_examples": {
            "examples": [
                {
                    "entry_id": "m_csa:204",
                    "expected_eval_role": "oos_tier::unknown_oos",
                    "expected_behavior": "abstain",
                    "reason": "fixture",
                }
            ]
        },
        "diversity_stratified_accuracy_policy": {
            "primary_diversity_axis": {"name": "fixture_axis"}
        },
    }


if __name__ == "__main__":
    unittest.main()
