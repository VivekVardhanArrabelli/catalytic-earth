from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.bronze_silver_promotion_preview import (
    assess_promotion,
    build_bronze_silver_promotion_preview,
    expected_cofactor_comp_ids,
    structure_confirmability,
    write_bronze_silver_promotion_preview,
)
from catalytic_earth.mechanism_representation_loop import fingerprint_centroids
from catalytic_earth.registry_io import load_json

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPANSION_PATH = REPO_ROOT / "data/registries/external_bronze_labels.json"


def _cif(*, protein_comp="SER", het_comps=()):
    """Minimal mmCIF atom_site loop: one protein residue + given HETATM comp ids."""
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
    rows = [f"ATOM 1 {protein_comp} A 1 CA 0.0 0.0 0.0"]
    for i, comp in enumerate(het_comps, start=2):
        rows.append(f"HETATM {i} {comp} B {i} {comp} 1.0 1.0 1.0")
    return "\n".join(cols + rows) + "\n"


def _row(*, entry_id, fp, cofactors=(), coordinate_path=None, active=8, catalytic=2,
         binding=6):
    return {
        "entry_id": entry_id,
        "label_type": "seed_fingerprint" if fp else "out_of_scope",
        "fingerprint_id": fp,
        "tier": "bronze",
        "evidence": {
            "mechanism_evidence": {
                "cofactors": [{"name": c} for c in cofactors],
                "active_site_residues": [
                    {"feature_code": "BINDING", "ligand_name": c} for c in cofactors
                ],
                "active_site_residue_count": active,
                "catalytic_residue_count": catalytic,
                "binding_residue_count": binding,
            },
            "structure_provenance": {"coordinate_path": coordinate_path},
            "pending_promotion_audits": [
                "geometry_inverse_gate_confirmation_on_holo_or_cofactor_fused_structure",
            ],
        },
    }


def _seed_population():
    rows = []
    for i in range(8):
        rows.append(_row(entry_id=f"zn{i}", fp="metal_dependent_hydrolase",
                         cofactors=["Zn(2+)"]))
    for i in range(8):
        rows.append(_row(entry_id=f"plp{i}", fp="plp_dependent_enzyme",
                         cofactors=["pyridoxal 5'-phosphate"]))
    return rows


class ExpectedCofactorTests(unittest.TestCase):
    def test_zinc_maps_to_zn(self) -> None:
        self.assertIn("ZN", expected_cofactor_comp_ids(
            _row(entry_id="a", fp="metal_dependent_hydrolase", cofactors=["Zn(2+)"])))

    def test_plp_maps_to_plp(self) -> None:
        self.assertIn("PLP", expected_cofactor_comp_ids(
            _row(entry_id="a", fp="plp_dependent_enzyme",
                 cofactors=["pyridoxal 5'-phosphate"])))


class StructureConfirmabilityTests(unittest.TestCase):
    def test_holo_when_cofactor_present_in_coords(self) -> None:
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "holo.cif"
            cif.write_text(_cif(het_comps=["ZN"]))
            row = _row(entry_id="a", fp="metal_dependent_hydrolase",
                       cofactors=["Zn(2+)"], coordinate_path=str(cif))
            self.assertEqual(structure_confirmability(row), "holo")

    def test_apo_when_experimental_but_cofactor_absent(self) -> None:
        # the crux of the degradation: coords exist (even experimental) but the
        # cofactor is not in them -> apo, gate abstains
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "apo.cif"
            cif.write_text(_cif(het_comps=[]))  # no cofactor
            row = _row(entry_id="a", fp="metal_dependent_hydrolase",
                       cofactors=["Zn(2+)"], coordinate_path=str(cif))
            self.assertEqual(structure_confirmability(row), "apo")

    def test_apo_when_wrong_het_present(self) -> None:
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "apo.cif"
            cif.write_text(_cif(het_comps=["SO4", "GOL"]))  # additives, not the cofactor
            row = _row(entry_id="a", fp="metal_dependent_hydrolase",
                       cofactors=["Zn(2+)"], coordinate_path=str(cif))
            self.assertEqual(structure_confirmability(row), "apo")

    def test_none_when_no_coordinates(self) -> None:
        self.assertEqual(
            structure_confirmability(_row(entry_id="a", fp="x", cofactors=["Zn(2+)"])),
            "none",
        )


class AssessPromotionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.centroids = fingerprint_centroids(_seed_population())

    def test_silver_ready_only_when_cofactor_present(self) -> None:
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "holo.cif"
            cif.write_text(_cif(het_comps=["ZN"]))
            row = _row(entry_id="t", fp="metal_dependent_hydrolase",
                       cofactors=["Zn(2+)"], coordinate_path=str(cif))
            d = assess_promotion(row, self.centroids, cohesion_threshold=0.5)
            self.assertEqual(d["decision"], "silver_ready_pending_geometry_run")

    def test_blocked_apo_when_cofactor_absent_even_with_coords(self) -> None:
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "apo.cif"
            cif.write_text(_cif(het_comps=[]))
            row = _row(entry_id="t", fp="metal_dependent_hydrolase",
                       cofactors=["Zn(2+)"], coordinate_path=str(cif))
            d = assess_promotion(row, self.centroids, cohesion_threshold=0.5)
            self.assertEqual(d["decision"], "blocked_apo_needs_cofactor_fusion")

    def test_blocked_pending_structure_when_no_coordinates(self) -> None:
        row = _row(entry_id="t", fp="metal_dependent_hydrolase", cofactors=["Zn(2+)"])
        d = assess_promotion(row, self.centroids, cohesion_threshold=0.5)
        self.assertEqual(d["decision"], "blocked_pending_structure")

    def test_review_when_chemistry_disagrees(self) -> None:
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "holo.cif"
            cif.write_text(_cif(het_comps=["PLP"]))
            # labeled metal but carries PLP chemistry -> nearest is plp -> review,
            # regardless of structure
            row = _row(entry_id="bad", fp="metal_dependent_hydrolase",
                       cofactors=["pyridoxal 5'-phosphate"], coordinate_path=str(cif))
            d = assess_promotion(row, self.centroids, cohesion_threshold=0.5)
            self.assertEqual(d["decision"], "review_chemistry_disagrees")


class BuildPreviewTests(unittest.TestCase):
    def test_decisions_partition_and_holo_promotes(self) -> None:
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "holo.cif"
            cif.write_text(_cif(het_comps=["ZN"]))
            seed = _seed_population()
            seed.append(_row(entry_id="holo", fp="metal_dependent_hydrolase",
                             cofactors=["Zn(2+)"], coordinate_path=str(cif)))
            audit = build_bronze_silver_promotion_preview(seed, cohesion_threshold=0.5)
            self.assertEqual(audit["seed_labels"], len(seed))
            self.assertEqual(audit["bronze_seed_labels"], len(seed))
            self.assertEqual(audit["already_silver_confirmed_count"], 0)
            self.assertEqual(sum(audit["decision_counts"].values()), len(seed))
            self.assertEqual(audit["silver_ready_count"], 1)
            g = audit["guardrails"]
            self.assertFalse(g["registry_written"])
            self.assertFalse(g["geometry_confirmation_run_or_faked"])

    def test_already_silver_rows_are_not_requeued_for_promotion(self) -> None:
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "holo.cif"
            cif.write_text(_cif(het_comps=["ZN"]))
            seed = _seed_population()
            silver = _row(
                entry_id="already_silver",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_path=str(cif),
            )
            silver["tier"] = "silver"
            seed.append(silver)
            audit = build_bronze_silver_promotion_preview(seed, cohesion_threshold=0.5)
            self.assertEqual(audit["seed_labels"], len(seed))
            self.assertEqual(audit["bronze_seed_labels"], len(seed) - 1)
            self.assertEqual(audit["already_silver_confirmed_count"], 1)
            self.assertEqual(audit["already_silver_confirmed_entry_ids"], ["already_silver"])
            self.assertEqual(audit["silver_ready_count"], 0)
            self.assertEqual(sum(audit["decision_counts"].values()), len(seed) - 1)


class RealRegistryTests(unittest.TestCase):
    def test_write_non_destructive_and_honest_about_apo(self) -> None:
        before = EXPANSION_PATH.read_bytes()
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "prom.json"
            report = Path(tmp) / "prom.md"
            audit = write_bronze_silver_promotion_preview(
                out_path=out,
                report_path=report,
                expansion_registry_path=EXPANSION_PATH,
            )
            # 5638 prior seed labels + 146 HAD-like phosphatase bronze rows
            # applied on 2026-06-14; the 30 promoted rows remain seed labels
            # while moving from bronze to silver.
            self.assertEqual(audit["seed_labels"], 5784)
            # HONEST about structure (2026-06-14, after holo_structure_promotion):
            # silver_ready is now > 0 because experimental-PDB holo_pdb_confirmation rows
            # exist (the annotated cofactor was found as a HETATM in a sha-pinned PDB) --
            # this is REAL corroboration, not inflation. It must NOT be faked, and the
            # gate must still ABSTAIN honestly on the overwhelming majority that lack holo
            # coordinates: blocked_pending_structure stays by far the largest blocked
            # bucket. The AFDB-staged coordinates remain apo (AlphaFold has no cofactor).
            dc = audit["decision_counts"]
            self.assertGreater(audit["silver_ready_count"], 0)
            self.assertGreater(dc.get("blocked_pending_structure", 0), audit["silver_ready_count"])
            # every silver_ready row must rest on a recorded holo confirmation, never a fake
            for d in audit["silver_ready_preview"]:
                self.assertEqual(d["structure_confirmability"], "holo")
            self.assertFalse(audit["guardrails"]["geometry_confirmation_run_or_faked"])
            self.assertEqual(EXPANSION_PATH.read_bytes(), before)

    def test_deterministic(self) -> None:
        expansion = load_json(EXPANSION_PATH)
        a = build_bronze_silver_promotion_preview(expansion)
        b = build_bronze_silver_promotion_preview(expansion)
        a.pop("created_utc")
        b.pop("created_utc")
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
