from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.active_site_encoder_cache import (
    build_active_site_encoder_cache,
    write_active_site_encoder_cache,
)


class ActiveSiteEncoderCacheTests(unittest.TestCase):
    def test_cache_keeps_ids_and_labels_out_of_predictive_features(self) -> None:
        cache = build_active_site_encoder_cache(
            readiness_matrix=_readiness_matrix(),
            geometry_features=_geometry_features(),
            include_rows=["m_csa:1"],
        )

        self.assertEqual(cache["summary"]["emitted_row_count"], 1)
        self.assertEqual(cache["summary"]["forbidden_inputs_used"], [])
        record = cache["records"][0]
        self.assertEqual(record["metadata"]["entry_id"], "m_csa:1")
        self.assertEqual(record["metadata"]["current_fingerprint_id"], "metal")
        self.assertNotIn("entry_id", record["predictive_features"])
        self.assertNotIn("current_fingerprint_id", record["predictive_features"])
        self.assertNotIn("mechanism_text_snippets", record["predictive_features"])
        self.assertEqual(record["predictive_features"]["pairwise_edge_count"], 1)
        self.assertEqual(record["predictive_features"]["residue_type_counts"]["HIS"], 1)

    def test_unknown_include_row_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "not label-blind smoke-ready"):
            build_active_site_encoder_cache(
                readiness_matrix=_readiness_matrix(),
                geometry_features=_geometry_features(),
                include_rows=["m_csa:missing"],
            )

    def test_writer_emits_jsonl_summary_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            readiness = root / "readiness.json"
            geometry = root / "geometry.json"
            out = root / "cache.jsonl"
            summary = root / "summary.json"
            report = root / "report.md"
            readiness.write_text(json.dumps(_readiness_matrix()), encoding="utf-8")
            geometry.write_text(json.dumps(_geometry_features()), encoding="utf-8")

            result = write_active_site_encoder_cache(
                readiness_matrix_path=readiness,
                geometry_features_path=geometry,
                out_path=out,
                summary_path=summary,
                report_path=report,
                include_rows=["m_csa:1"],
            )

            self.assertEqual(result["emitted_row_count"], 1)
            self.assertTrue(out.read_text(encoding="utf-8").startswith("{"))
            self.assertIn(
                "Active-site encoder cache smoke",
                report.read_text(encoding="utf-8"),
            )


def _readiness_matrix() -> dict:
    return {
        "rows": [
            {
                "allowed_use": "label_blind_feature_extraction_smoke_ready",
                "candidate_id": "m_csa:1",
                "coordinate_path": "coords/pdb_1ABC.cif",
                "coordinate_status": "already_materialized",
                "current_fingerprint_id": "metal",
                "local_cofactor_family_available": True,
                "pairwise_distance_count": 1,
                "pocket_descriptor_available": True,
                "quarantined_before_model_claims": False,
                "role_annotated_residue_count": 2,
                "selected_structure": "pdb:1ABC",
                "source_group": "clean_near_orphan_anchor",
                "split_assignment": "heldout",
                "structure_cofactor_family_available": True,
            }
        ]
    }


def _geometry_features() -> dict:
    return {
        "entries": [
            {
                "entry_id": "m_csa:1",
                "entry_name": "not predictive",
                "status": "ok",
                "residue_count": 2,
                "resolved_residue_count": 2,
                "missing_positions": 0,
                "mechanism_text_snippets": ["not predictive"],
                "ligand_context": {
                    "cofactor_families": ["metal_ion"],
                    "structure_cofactor_families": ["metal_ion"],
                    "proximal_ligands": [
                        {"code": "ZN", "min_distance_to_active_site": 3.2}
                    ],
                },
                "pocket_context": {
                    "descriptors": {
                        "hydrophobic_fraction": 0.2,
                        "polar_fraction": 0.3,
                        "positive_fraction": 0.1,
                        "negative_fraction": 0.0,
                        "charge_balance": 0.1,
                        "aromatic_fraction": 0.1,
                        "sulfur_fraction": 0.0,
                        "mean_min_distance_to_active_site": 4.2,
                    }
                },
                "residues": [
                    {
                        "atom_count": 10,
                        "ca": {"x": 1.0, "y": 0.0, "z": 0.0},
                        "centroid": {"x": 1.1, "y": 0.0, "z": 0.0},
                        "code": "His",
                        "residue_node_id": "m_csa:1:residue:1",
                        "roles": ["metal ligand"],
                    },
                    {
                        "atom_count": 8,
                        "ca": {"x": 4.0, "y": 0.0, "z": 0.0},
                        "centroid": {"x": 4.1, "y": 0.0, "z": 0.0},
                        "code": "Glu",
                        "residue_node_id": "m_csa:1:residue:2",
                        "roles": ["proton acceptor"],
                    },
                ],
                "pairwise_distances_angstrom": [
                    {
                        "coordinate_type": "ca_or_centroid",
                        "distance": 3.0,
                        "left": "m_csa:1:residue:1",
                        "right": "m_csa:1:residue:2",
                    }
                ],
            }
        ]
    }


if __name__ == "__main__":
    unittest.main()
