from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from catalytic_earth.predicted_geometry_robustness import (
    ESMFOLD2_BLOCKER,
    _target_manifest_row_selection,
    build_alphafold_predicted_geometry_features,
    build_esmfold2_robustness_experiment_contract,
    build_predicted_geometry_in_distribution_atlas_retrieval,
    build_predicted_geometry_distillation_audit,
    build_predicted_geometry_robustness_audit,
    make_esmfold2_staged_supplier,
    resolve_esmfold2_staged_dir,
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

    def test_target_selection_can_opt_into_predicted_only_sequence_positions(
        self,
    ) -> None:
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
                    "benchmark_role": "oos_tier::unknown_oos",
                    "split_assignment": "in_distribution",
                }
            ]
        }
        experimental = {
            "entries": [
                {
                    "entry_id": "m_csa:1",
                    "status": "no_structure_positions",
                    "pdb_id": None,
                }
            ]
        }

        strict_rows, strict_excluded = _target_manifest_row_selection(
            label_manifest=label_manifest,
            graph=graph,
            experimental_geometry_features=experimental,
            split_assignment=None,
            max_rows=0,
        )
        self.assertEqual(strict_rows, [])
        self.assertEqual(
            strict_excluded[0]["reason"],
            "experimental_geometry_not_ok:no_structure_positions",
        )

        repaired_rows, repaired_excluded = _target_manifest_row_selection(
            label_manifest=label_manifest,
            graph=graph,
            experimental_geometry_features=experimental,
            split_assignment=None,
            max_rows=0,
            allow_missing_experimental_geometry_if_sequence_positions=True,
        )
        self.assertEqual(repaired_excluded, [])
        self.assertEqual(repaired_rows[0]["entry_id"], "m_csa:1")
        self.assertEqual(
            repaired_rows[0]["predicted_geometry_accession_repair"]["policy"],
            "reference_sequence_positions_without_experimental_structure_positions",
        )
        self.assertEqual(
            repaired_rows[0]["predicted_geometry_accession_repair"][
                "selected_residue_count"
            ],
            2,
        )

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


class ESMFold2BackendTests(unittest.TestCase):
    GRAPH = {
        "nodes": [
            {
                "id": "m_csa:1:residue:1",
                "type": "catalytic_residue",
                "roles": ["proton acceptor"],
                "sequence_positions": [
                    {"code": "Asp", "is_reference": True, "resid": 10, "uniprot_id": "TEST"}
                ],
            },
            {
                "id": "m_csa:1:residue:2",
                "type": "catalytic_residue",
                "roles": ["proton donor"],
                "sequence_positions": [
                    {"code": "His", "is_reference": True, "resid": 30, "uniprot_id": "TEST"}
                ],
            },
        ]
    }
    MANIFEST_ROWS = [
        {
            "entry_id": "m_csa:1",
            "accession": "TEST",
            "sequence_id": "TEST",
            "benchmark_role": "primary_supervised_metric::metal_dependent_hydrolase",
            "split_assignment": "heldout",
        }
    ]
    EXPERIMENTAL = {"entries": [{"entry_id": "m_csa:1", "status": "ok", "pdb_id": "1ABC"}]}

    def test_staged_supplier_feeds_frozen_geometry_features(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "ESMFOLD2-TEST.cif").write_text(MINI_CIF, encoding="utf-8")
            supplier = make_esmfold2_staged_supplier(tmp)
            text, meta = supplier("TEST")
            self.assertEqual(meta["backend"], "esmfold2")
            self.assertIn("data_AF-TEST", text)
            features = build_alphafold_predicted_geometry_features(
                label_manifest_rows=self.MANIFEST_ROWS,
                graph=self.GRAPH,
                experimental_geometry_features=self.EXPERIMENTAL,
                fetcher=supplier,
            )
            entry = features["entries"][0]
            self.assertEqual(entry["status"], "ok")
            self.assertEqual(entry["resolved_residue_count"], 2)

    def test_staged_supplier_raises_on_missing_accession(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "ESMFOLD2-TEST.cif").write_text(MINI_CIF, encoding="utf-8")
            supplier = make_esmfold2_staged_supplier(tmp)
            with self.assertRaises(RuntimeError):
                supplier("NOPE")

    def test_resolve_staged_dir_requires_cif(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(resolve_esmfold2_staged_dir(tmp))
            Path(tmp, "ESMFOLD2-TEST.cif").write_text(MINI_CIF, encoding="utf-8")
            self.assertEqual(resolve_esmfold2_staged_dir(tmp), Path(tmp))
        self.assertIsNone(resolve_esmfold2_staged_dir(None))

    def test_robustness_backend_blocked_without_staged_coordinates(self) -> None:
        audit = build_predicted_geometry_robustness_audit(
            label_manifest={"rows": []},
            graph={"nodes": []},
            experimental_geometry_features={"entries": []},
            experimental_geometry_retrieval={"results": []},
            labels=[],
            wave1_audit={},
            backend="esmfold2",
        )
        self.assertEqual(audit["status"], "blocked")
        self.assertEqual(audit["blocker"], ESMFOLD2_BLOCKER)
        self.assertFalse(audit["guardrails"]["large_model_downloads_performed"])

    def test_distillation_backend_blocked_without_staged_coordinates(self) -> None:
        audit = build_predicted_geometry_distillation_audit(
            label_manifest={"rows": []},
            graph={"nodes": []},
            experimental_geometry_features={"entries": []},
            wave1_audit={},
            backend="esmfold2",
        )
        self.assertEqual(audit["status"], "blocked")
        self.assertEqual(audit["blocker"], ESMFOLD2_BLOCKER)


class ESMFold2ExperimentContractTests(unittest.TestCase):
    MANIFEST = {
        "rows": [
            {
                "entry_id": "m_csa:1",
                "accession": "A1",
                "sequence_id": "A1",
                "fingerprint_id": "metal_dependent_hydrolase",
                "benchmark_role": "primary_supervised_metric::metal_dependent_hydrolase",
                "split_assignment": "in_distribution",
            },
            {
                "entry_id": "m_csa:2",
                "accession": "A2",
                "sequence_id": "A2",
                "fingerprint_id": None,
                "benchmark_role": "oos_tier::unknown_oos",
                "split_assignment": "heldout",
            },
            {
                "entry_id": "m_csa:3",
                "accession": "A3",
                "sequence_id": "A3",
                "fingerprint_id": None,
                "benchmark_role": "oos_tier::unknown_oos",
                "split_assignment": "in_distribution",
            },
        ]
    }

    def test_contract_blocked_and_counts_without_staged_coordinates(self) -> None:
        contract = build_esmfold2_robustness_experiment_contract(
            label_manifest=self.MANIFEST,
        )
        self.assertEqual(contract["status"], "blocked_on_staged_coordinates")
        inventory = contract["accession_inventory"]
        self.assertEqual(inventory["atlas_row_count"], 1)
        self.assertEqual(inventory["heldout_row_count"], 1)
        self.assertEqual(inventory["unique_accessions_to_predict"], 2)
        guardrails = contract["guardrails"]
        self.assertFalse(guardrails["heldout_labels_used_for_fit_or_threshold"])
        self.assertFalse(guardrails["esmfold2_inference_run"])
        self.assertFalse(guardrails["large_model_downloads_performed"])
        self.assertFalse(
            contract["model_under_test"]["predicts_cofactor_or_substrate_geometry"]
        )

    def test_contract_ready_when_all_accessions_staged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for accession in ("A1", "A2"):
                Path(tmp, f"ESMFOLD2-{accession}.cif").write_text(
                    MINI_CIF, encoding="utf-8"
                )
            contract = build_esmfold2_robustness_experiment_contract(
                label_manifest=self.MANIFEST,
                esmfold2_staged_dir=tmp,
            )
            self.assertEqual(contract["status"], "ready_to_run")
            self.assertEqual(
                contract["staging_status"]["accessions_with_staged_cif"], 2
            )
            self.assertIsNone(contract["staging_status"]["blocker"])


if __name__ == "__main__":
    unittest.main()
