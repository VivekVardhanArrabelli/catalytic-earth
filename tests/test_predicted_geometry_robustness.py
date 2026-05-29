from __future__ import annotations

import unittest

from catalytic_earth.predicted_geometry_robustness import (
    build_alphafold_predicted_geometry_features,
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


if __name__ == "__main__":
    unittest.main()
