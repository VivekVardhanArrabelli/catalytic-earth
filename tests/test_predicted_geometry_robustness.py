from __future__ import annotations

import unittest

from catalytic_earth.predicted_geometry_robustness import (
    build_alphafold_predicted_geometry_features,
    build_predicted_geometry_in_distribution_atlas_retrieval,
    build_predicted_geometry_distillation_audit,
    build_predicted_geometry_robustness_audit,
)


MINI_CIF = """data_AF-TEST-F1
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_entity_id
_atom_site.label_seq_id
_atom_site.pdbx_PDB_ins_code
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.occupancy
_atom_site.B_iso_or_equiv
_atom_site.pdbx_formal_charge
_atom_site.auth_seq_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_atom_id
_atom_site.pdbx_PDB_model_num
ATOM 1 N N . ASP A 1 10 ? 0.0 0.0 0.0 1.00 90.0 ? 10 ASP A N 1
ATOM 2 C CA . ASP A 1 10 ? 1.0 0.0 0.0 1.00 90.0 ? 10 ASP A CA 1
ATOM 3 N N . HIS A 1 30 ? 4.0 0.0 0.0 1.00 90.0 ? 30 HIS A N 1
ATOM 4 C CA . HIS A 1 30 ? 5.0 0.0 0.0 1.00 90.0 ? 30 HIS A CA 1
ATOM 5 N N . GLY A 1 31 ? 5.0 2.0 0.0 1.00 90.0 ? 31 GLY A N 1
#
"""


class PredictedGeometryRobustnessTests(unittest.TestCase):
    def test_builds_predicted_geometry_from_sequence_positions(self) -> None:
        graph = {
            "nodes": [
                {
                    "id": "m_csa:1:residue:1",
                    "type": "catalytic_residue",
                    "roles": ["proton acceptor"],
                    "sequence_positions": [
                        {
                            "code": "Asp",
                            "is_reference": True,
                            "resid": 10,
                            "uniprot_id": "TEST",
                        }
                    ],
                },
                {
                    "id": "m_csa:1:residue:2",
                    "type": "catalytic_residue",
                    "roles": ["proton donor"],
                    "sequence_positions": [
                        {
                            "code": "His",
                            "is_reference": True,
                            "resid": 30,
                            "uniprot_id": "TEST",
                        }
                    ],
                },
            ],
        }
        manifest_rows = [
            {
                "entry_id": "m_csa:1",
                "accession": "TEST",
                "sequence_id": "TEST",
                "benchmark_role": "primary_supervised_metric::metal_dependent_hydrolase",
                "split_assignment": "heldout",
            }
        ]
        experimental = {
            "entries": [
                {
                    "entry_id": "m_csa:1",
                    "status": "ok",
                    "pdb_id": "1ABC",
                }
            ]
        }

        def fake_fetcher(accession: str, version: str = "auto") -> tuple[str, dict]:
            return MINI_CIF, {
                "backend": "alphafold_db",
                "accession": accession,
                "alphafold_version": 6,
                "url": "memory://TEST",
            }

        features = build_alphafold_predicted_geometry_features(
            label_manifest_rows=manifest_rows,
            graph=graph,
            experimental_geometry_features=experimental,
            fetcher=fake_fetcher,
        )
        entry = features["entries"][0]
        self.assertEqual(entry["status"], "ok")
        self.assertEqual(entry["resolved_residue_count"], 2)
        self.assertEqual(entry["missing_positions"], 0)
        self.assertEqual(len(entry["pairwise_distances_angstrom"]), 1)
        self.assertEqual(entry["mechanism_text_snippets"], [])

    def test_esmfold_backend_is_precise_blocker(self) -> None:
        audit = build_predicted_geometry_robustness_audit(
            label_manifest={"rows": []},
            graph={"nodes": []},
            experimental_geometry_features={"entries": []},
            experimental_geometry_retrieval={"results": []},
            labels=[],
            wave1_audit={},
            backend="esmfold",
        )
        self.assertEqual(audit["status"], "blocked")
        self.assertEqual(audit["blocker"], "local_esmfold_runtime_or_weights_unavailable")
        self.assertFalse(audit["guardrails"]["large_model_downloads_performed"])

    def test_distillation_esmfold_backend_is_precise_blocker(self) -> None:
        audit = build_predicted_geometry_distillation_audit(
            label_manifest={"rows": []},
            graph={"nodes": []},
            experimental_geometry_features={"entries": []},
            wave1_audit={},
            backend="esmfold",
        )
        self.assertEqual(audit["status"], "blocked")
        self.assertEqual(
            audit["artifact_id"],
            "v3_predicted_geometry_distillation_audit_current702_20260529",
        )
        self.assertEqual(
            audit["blocker"], "local_esmfold_runtime_or_weights_unavailable"
        )
        self.assertFalse(audit["guardrails"]["large_model_downloads_performed"])

    def test_builds_in_distribution_atlas_retrieval_only_for_fingerprint_rows(self) -> None:
        graph = {
            "nodes": [
                {
                    "id": "m_csa:1:residue:1",
                    "type": "catalytic_residue",
                    "roles": ["proton acceptor"],
                    "sequence_positions": [
                        {
                            "code": "Asp",
                            "is_reference": True,
                            "resid": 10,
                            "uniprot_id": "TEST",
                        }
                    ],
                },
                {
                    "id": "m_csa:1:residue:2",
                    "type": "catalytic_residue",
                    "roles": ["proton donor"],
                    "sequence_positions": [
                        {
                            "code": "His",
                            "is_reference": True,
                            "resid": 30,
                            "uniprot_id": "TEST",
                        }
                    ],
                },
            ],
        }
        label_manifest = {
            "rows": [
                {
                    "entry_id": "m_csa:1",
                    "accession": "TEST",
                    "sequence_id": "TEST",
                    "fingerprint_id": "metal_dependent_hydrolase",
                    "benchmark_role": "primary_supervised_metric::metal_dependent_hydrolase",
                    "split_assignment": "in_distribution",
                },
                {
                    "entry_id": "m_csa:2",
                    "accession": "TEST2",
                    "sequence_id": "TEST2",
                    "fingerprint_id": None,
                    "benchmark_role": "oos_tier::unknown_oos",
                    "split_assignment": "in_distribution",
                },
            ]
        }
        experimental = {
            "entries": [
                {"entry_id": "m_csa:1", "status": "ok", "pdb_id": "1ABC"},
                {"entry_id": "m_csa:2", "status": "ok", "pdb_id": "2ABC"},
            ]
        }
        heldout = {
            "predicted_geometry_features": {
                "entries": [
                    {
                        "entry_id": "m_csa:3",
                        "accession": "HELD",
                        "sequence_id": "HELD",
                        "status": "ok",
                        "pdb_id": "AF-HELD-F1-model_v6",
                        "split_assignment": "heldout",
                    }
                ]
            },
            "predicted_geometry_retrieval": {
                "results": [
                    {
                        "entry_id": "m_csa:3",
                        "status": "ok",
                        "top_fingerprints": [
                            {
                                "fingerprint_id": "metal_dependent_hydrolase",
                                "score": 0.5,
                                "role_match_fraction": 0.25,
                            }
                        ],
                    }
                ]
            },
        }

        def fake_fetcher(accession: str, version: str = "auto") -> tuple[str, dict]:
            return MINI_CIF, {
                "backend": "alphafold_db",
                "accession": accession,
                "alphafold_version": 6,
                "url": "memory://TEST",
            }

        audit = build_predicted_geometry_in_distribution_atlas_retrieval(
            label_manifest=label_manifest,
            graph=graph,
            experimental_geometry_features=experimental,
            heldout_predicted_geometry_audit=heldout,
            fetcher=fake_fetcher,
        )

        self.assertEqual(audit["status"], "complete")
        self.assertEqual(audit["counts"]["atlas_rows_expected"], 1)
        self.assertEqual(audit["counts"]["atlas_rows_scored_ok"], 1)
        self.assertEqual(audit["counts"]["heldout_predicted_retrieval_rows_carried"], 1)
        self.assertEqual(audit["counts"]["combined_results_count"], 2)
        atlas_row = audit["atlas_predicted_geometry_retrieval"]["results"][0]
        self.assertEqual(atlas_row["entry_id"], "m_csa:1")
        self.assertEqual(atlas_row["split_assignment"], "in_distribution")
        self.assertIn("top1_score", atlas_row)
        self.assertIn("top1_role_match_fraction", atlas_row)
        self.assertNotIn("m_csa:2", audit["result_sets"]["atlas_entry_ids"])


if __name__ == "__main__":
    unittest.main()
