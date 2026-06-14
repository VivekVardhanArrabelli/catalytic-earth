from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.bronze_silver_promotion_preview import (
    build_bronze_silver_promotion_preview,
    structure_confirmability,
)
from catalytic_earth.holo_structure_promotion import (
    CONFIRMED_STATUS,
    NO_HOLO_STATUS,
    build_holo_structure_promotion,
    hetatm_comp_ids_from_cif,
    write_holo_structure_promotion,
)


def _cif(*, het_comps=()):
    cols = [
        "data_test",
        "loop_",
        "_atom_site.group_PDB",
        "_atom_site.id",
        "_atom_site.label_comp_id",
        "_atom_site.label_asym_id",
        "_atom_site.label_seq_id",
        "_atom_site.label_atom_id",
        "_atom_site.Cartn_x",
        "_atom_site.Cartn_y",
        "_atom_site.Cartn_z",
    ]
    rows = ["ATOM 1 SER A 1 CA 0.0 0.0 0.0"]
    for i, comp in enumerate(het_comps, start=2):
        rows.append(f"HETATM {i} {comp} B {i} {comp} 1.0 1.0 1.0")
    return "\n".join(cols + rows) + "\n"


def _row(*, entry_id, fp, cofactors=(), pdb_ids=(), label_type="seed_fingerprint"):
    return {
        "entry_id": entry_id,
        "label_type": label_type,
        "fingerprint_id": fp,
        "tier": "bronze",
        "evidence": {
            "mechanism_evidence": {
                "cofactors": [{"name": c} for c in cofactors],
                "active_site_residues": [
                    {"feature_code": "BINDING", "ligand_name": c} for c in cofactors
                ],
                "active_site_residue_count": 8,
                "catalytic_residue_count": 2,
                "binding_residue_count": 6,
            },
            "structure_provenance": {"pdb_ids": list(pdb_ids), "coordinate_path": None},
        },
    }


def _flavin_population(n=6, pdb_ids=("5X68",)):
    # a coherent single-fingerprint cluster so chemistry corroborates each member
    return [
        _row(entry_id=f"fmo{i}", fp="flavin_monooxygenase", cofactors=["FAD"],
             pdb_ids=pdb_ids)
        for i in range(n)
    ]


class _FakeFetcher:
    """Deterministic offline mmCIF fetcher: HOLO pdbs carry the cofactor HETATM."""

    def __init__(self, holo_map):
        self.holo_map = holo_map  # pdb_id(upper) -> list of HETATM comp ids
        self.calls = []

    def __call__(self, pdb_id):
        self.calls.append(pdb_id.upper())
        comps = self.holo_map.get(pdb_id.upper())
        if comps is None:
            return None  # genuine 404
        return _cif(het_comps=comps)


class HetatmParsingTests(unittest.TestCase):
    def test_hetatm_excludes_water(self) -> None:
        comps = hetatm_comp_ids_from_cif(_cif(het_comps=["FAD", "HOH"]))
        self.assertEqual(comps, {"FAD"})


class HoloConfirmationTests(unittest.TestCase):
    def test_confirms_holo_for_corroborated_row(self) -> None:
        seed = _flavin_population()
        fetch = _FakeFetcher({"5X68": ["FAD"]})
        audit = build_holo_structure_promotion(
            expansion_payload=seed, cif_fetcher=fetch, cohesion_threshold=0.5
        )
        self.assertEqual(audit["counts"]["holo_confirmed_this_run"], len(seed))
        # the cif is fetched once and cached across rows sharing the pdb
        self.assertEqual(len(set(fetch.calls)), 1)
        row0 = audit["promoted_registry"][0]
        conf = row0["evidence"]["structure_provenance"]["holo_pdb_confirmation"]
        self.assertEqual(conf["status"], CONFIRMED_STATUS)
        self.assertEqual(conf["cofactor_comp_ids_present"], ["FAD"])
        self.assertFalse(conf["coordinate_committed"])
        # the gate now reads the recorded confirmation as holo, no file needed
        self.assertEqual(structure_confirmability(row0), "holo")

    def test_no_holo_when_pdb_is_apo(self) -> None:
        seed = _flavin_population(pdb_ids=("9APO",))
        fetch = _FakeFetcher({"9APO": ["SO4"]})  # crystallographic additive, not the cofactor
        audit = build_holo_structure_promotion(
            expansion_payload=seed, cif_fetcher=fetch, cohesion_threshold=0.5
        )
        self.assertEqual(audit["counts"]["holo_confirmed_this_run"], 0)
        self.assertEqual(audit["counts"]["no_holo_pdb_found"], len(seed))
        conf = audit["promoted_registry"][0]["evidence"]["structure_provenance"][
            "holo_pdb_confirmation"
        ]
        self.assertEqual(conf["status"], NO_HOLO_STATUS)

    def test_tries_pdbs_in_order_until_holo(self) -> None:
        seed = [_row(entry_id="fmo0", fp="flavin_monooxygenase", cofactors=["FAD"],
                     pdb_ids=("9APO", "5X68"))]
        seed += _flavin_population()  # give the centroid coherent support
        fetch = _FakeFetcher({"9APO": ["SO4"], "5X68": ["FAD"]})
        audit = build_holo_structure_promotion(
            expansion_payload=seed, cif_fetcher=fetch, cohesion_threshold=0.5
        )
        conf = audit["promoted_registry"][0]["evidence"]["structure_provenance"][
            "holo_pdb_confirmation"
        ]
        self.assertEqual(conf["status"], CONFIRMED_STATUS)
        self.assertEqual(conf["pdb_id"], "5X68")
        self.assertEqual(conf["pdb_ids_checked"], ["9APO", "5X68"])

    def test_skips_rows_without_pdb_or_cofactor(self) -> None:
        seed = [_row(entry_id="x", fp="flavin_monooxygenase", cofactors=["FAD"], pdb_ids=())]
        seed += _flavin_population()
        fetch = _FakeFetcher({"5X68": ["FAD"]})
        audit = build_holo_structure_promotion(
            expansion_payload=seed, cif_fetcher=fetch, cohesion_threshold=0.5
        )
        self.assertGreaterEqual(audit["counts"]["no_pdb_or_cofactor"], 1)

    def test_per_fingerprint_cap_and_limit(self) -> None:
        seed = _flavin_population(n=10)
        fetch = _FakeFetcher({"5X68": ["FAD"]})
        audit = build_holo_structure_promotion(
            expansion_payload=seed, cif_fetcher=fetch, cohesion_threshold=0.5,
            per_fingerprint_cap=3,
        )
        self.assertEqual(audit["counts"]["holo_confirmed_this_run"], 3)
        self.assertGreaterEqual(audit["counts"]["deferred_over_fingerprint_cap"], 1)


class WriteTests(unittest.TestCase):
    def test_preview_is_non_destructive_and_frozen_untouched(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            exp = tmp / "expansion.json"
            frozen = tmp / "frozen.json"
            # no pdb_ids -> no network fetch is attempted (offline-safe write-path test)
            seed = _flavin_population(pdb_ids=())
            exp.write_text(json.dumps(seed))
            frozen.write_text(json.dumps([{"entry_id": "frozen0"}]))
            frozen_before = frozen.read_bytes()
            exp_before = exp.read_bytes()
            summary = write_holo_structure_promotion(
                out_path=tmp / "out.json",
                report_path=tmp / "out.md",
                expansion_registry_path=exp,
                frozen_benchmark_path=frozen,
                cache_path=None,
                cohesion_threshold=0.5,
                # offline: stub the fetcher via monkeypatching the module default
            )
            # preview did not write either registry
            self.assertFalse(summary["expansion_registry_written"])
            self.assertEqual(exp.read_bytes(), exp_before)
            self.assertEqual(frozen.read_bytes(), frozen_before)
            self.assertTrue(summary["frozen_benchmark_byte_unchanged"])

    def test_refuses_to_target_frozen(self) -> None:
        with self.assertRaises(ValueError):
            write_holo_structure_promotion(
                expansion_registry_path=Path("data/registries/curated_mechanism_labels.json"),
                frozen_benchmark_path=Path("data/registries/curated_mechanism_labels.json"),
            )


if __name__ == "__main__":
    unittest.main()
