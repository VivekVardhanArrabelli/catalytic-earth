from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.mechanism_representation_loop import (
    build_mechanism_representation_loop,
    classify_reaction_bond_change,
    featurize,
    fingerprint_centroids,
    promotion_triage,
    propose_for_fingerprint,
    write_mechanism_representation_loop,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPANSION_PATH = REPO_ROOT / "data/registries/external_bronze_labels.json"


def _row(*, entry_id, fp, cofactors=(), binding_ligands=(), active=8, catalytic=2, binding=6,
         reactions=()):
    residues = [
        {"feature_code": "ACT_SITE", "position": i} for i in range(catalytic)
    ] + [
        {"feature_code": "BINDING", "position": 100 + i, "ligand_name": lig}
        for i, lig in enumerate(binding_ligands)
    ]
    return {
        "entry_id": entry_id,
        "label_type": "seed_fingerprint" if fp else "out_of_scope",
        "fingerprint_id": fp,
        "evidence": {
            "mechanism_evidence": {
                "cofactors": [{"name": c} for c in cofactors],
                "active_site_residues": residues,
                "active_site_residue_count": active,
                "catalytic_residue_count": catalytic,
                "binding_residue_count": binding,
                "ec_numbers": ["9.9.9.9"],  # must be ignored by featurize
                "reaction_equations": [
                    # ec_number co-stored but must be ignored; only `reaction` is read.
                    {"reaction": r, "ec_number": "9.9.9.9"} for r in reactions
                ],
            },
            "source_provenance": {
                "protein_name": "SHOULD NOT BE READ",
                "target_family_lane": "SHOULD NOT BE READ",
            },
        },
    }


class BondChangeFeatureTests(unittest.TestCase):
    def test_hydrolysis_classes_from_reaction_string(self) -> None:
        self.assertEqual(
            classify_reaction_bond_change("a phosphate monoester + H2O = an alcohol + phosphate"),
            {"bc_phosphomonoester"},
        )
        self.assertEqual(
            classify_reaction_bond_change("3',5'-cyclic GMP + H2O = GMP + H(+)"),
            {"bc_phosphodiester"},
        )
        self.assertEqual(
            classify_reaction_bond_change(
                "substance P + H2O = substance P(1-9) + L-Leu-L-Met-NH2"
            ),
            {"bc_peptide_cn"},
        )
        self.assertEqual(
            classify_reaction_bond_change("cytosine + H2O = uracil + NH3"),
            {"bc_amide_cn"},
        )

    def test_lyase_without_water_yields_no_bond_change(self) -> None:
        # Cobalamin ammonia-lyase: releases ammonia but no water -> not a hydrolysis bond
        # change, so it stays out of the bond space (keeps non-metal families separable).
        self.assertEqual(
            classify_reaction_bond_change("ethanolamine = acetaldehyde + NH4(+)"), set()
        )

    def test_featurize_sets_bond_change_and_ignores_reaction_ec(self) -> None:
        f = featurize(
            _row(
                entry_id="pm",
                fp="metallophosphomonoesterase",
                cofactors=["Zn(2+)"],
                reactions=["a phosphate monoester + H2O = an alcohol + phosphate"],
            )
        )
        self.assertEqual(f["bc_phosphomonoester"], 1.0)
        self.assertEqual(f["bc_peptide_cn"], 0.0)
        self.assertEqual(f["zinc"], 1.0)
        # Two metal rows with the SAME cofactor but DIFFERENT bond change separate.
        peptidase = featurize(
            _row(entry_id="pep", fp="metallopeptidase", cofactors=["Zn(2+)"],
                 reactions=["a peptide + H2O = a shorter peptide"])
        )
        self.assertEqual(peptidase["bc_peptide_cn"], 1.0)
        self.assertEqual(peptidase["bc_phosphomonoester"], 0.0)


class FeaturizeLeakageTests(unittest.TestCase):
    def test_metal_chemistry_features(self) -> None:
        f = featurize(_row(entry_id="m", fp="metal_dependent_hydrolase",
                            cofactors=["Zn(2+)"]))
        self.assertEqual(f["zinc"], 1.0)
        self.assertEqual(f["flavin"], 0.0)

    def test_flavin_from_binding_ligand(self) -> None:
        f = featurize(_row(entry_id="x", fp=None, binding_ligands=["FAD"]))
        self.assertEqual(f["flavin"], 1.0)

    def test_featurize_ignores_ec_name_lane_fingerprint(self) -> None:
        base = _row(entry_id="r", fp="plp_dependent_enzyme",
                    cofactors=["pyridoxal 5'-phosphate"])
        f1 = featurize(base)
        # mutate every excluded field; representation must be byte-identical
        mutated = json.loads(json.dumps(base))
        mutated["fingerprint_id"] = "heme_peroxidase_oxidase"
        mutated["label_type"] = "out_of_scope"
        mutated["evidence"]["mechanism_evidence"]["ec_numbers"] = ["1.11.1.7"]
        mutated["evidence"]["source_provenance"]["protein_name"] = "totally different"
        mutated["evidence"]["source_provenance"]["target_family_lane"] = "heme lane"
        f2 = featurize(mutated)
        self.assertEqual(f1, f2)


class CentroidAndTriageTests(unittest.TestCase):
    def _seed(self):
        rows = []
        for i in range(6):
            rows.append(_row(entry_id=f"zn{i}", fp="metal_dependent_hydrolase",
                             cofactors=["Zn(2+)"], binding_ligands=["Zn(2+)"]))
        for i in range(6):
            rows.append(_row(entry_id=f"plp{i}", fp="plp_dependent_enzyme",
                             cofactors=["pyridoxal 5'-phosphate"]))
        for i in range(6):
            rows.append(_row(entry_id=f"fad{i}", fp="flavin_monooxygenase",
                             cofactors=["FAD"]))
        return rows

    def test_centroids_per_fingerprint(self) -> None:
        c = fingerprint_centroids(self._seed())
        self.assertEqual(
            sorted(c.keys()),
            ["flavin_monooxygenase", "metal_dependent_hydrolase", "plp_dependent_enzyme"],
        )

    def test_triage_promotes_coherent_and_flags_outlier(self) -> None:
        seed = self._seed()
        # inject a mislabeled row: PLP chemistry but labeled metal -> outlier
        seed.append(_row(entry_id="bad", fp="metal_dependent_hydrolase",
                         cofactors=["pyridoxal 5'-phosphate"]))
        tri = promotion_triage(seed, cohesion_threshold=0.9)
        self.assertGreater(tri["leave_one_out_self_consistency"], 0.8)
        outlier_ids = {o["entry_id"] for o in tri["review_outlier_samples"]}
        self.assertIn("bad", outlier_ids)

    def test_propose_requires_real_cofactor_overlap(self) -> None:
        seed = self._seed()
        centroids = fingerprint_centroids(seed)
        pool = [
            _row(entry_id="cand_zn", fp=None, cofactors=["Zn(2+)"],
                 binding_ligands=["Zn(2+)"]),
            _row(entry_id="cand_empty", fp=None),  # no cofactor -> must NOT propose
        ]
        proposals = propose_for_fingerprint(
            "metal_dependent_hydrolase", pool, centroids, min_similarity=0.3
        )
        ids = {p["entry_id"] for p in proposals}
        self.assertIn("cand_zn", ids)
        self.assertNotIn("cand_empty", ids)


class BuildWriteRealRegistryTests(unittest.TestCase):
    def test_build_on_real_registry_is_leakage_safe(self) -> None:
        expansion = json.loads(EXPANSION_PATH.read_text())
        audit = build_mechanism_representation_loop(expansion)
        self.assertEqual(audit["seed_labels"], 1716)
        g = audit["leakage_guardrails"]
        self.assertFalse(g["frozen_benchmark_read"])
        self.assertFalse(g["ec_name_prose_lane_used"])
        self.assertFalse(g["fingerprint_label_used_as_feature"])
        triage = audit["promotion_triage"]
        conf = triage["confusion_by_fingerprint"]
        sc = triage["self_consistency_by_fingerprint"]
        # FINDING (Track 1 / 1c, 2026-06-11): adding the leakage-safe row-specific
        # reaction-center BOND-CHANGE feature (derived from Rhea substrate->product
        # chemistry -- NOT the fingerprint's declared bond_change, NOT EC) makes the four
        # metal v2 SUB-FAMILIES predictively separable. Before the feature they collapsed
        # (metal-only self-consistency ~0.49, overall ~0.68) because they share the
        # divalent-metal cofactor + water-activator residue roles and differ only by the
        # bond hydrolysed. After: overall rises to ~0.75 and each v2 sub-family separates
        # strongly. The coarse v1 umbrella `metal_dependent_hydrolase` now (correctly)
        # scatters to its sub-families -- it has no single bond-change signature -- so its
        # own self-consistency drops to ~0; that is the split working, not a regression.
        metal_family = {
            "metal_dependent_hydrolase",
            "metallopeptidase",
            "metallophosphoesterase_nuclease",
            "metallophosphomonoesterase",
            "metallo_amidohydrolase_deaminase",
        }
        # Overall rises with the bond-change feature (was ~0.68; well above 1/12 ~= 0.08).
        self.assertGreater(triage["leave_one_out_self_consistency"], 0.70)
        # The four v2 metal sub-families are now strongly separable (each was ~indistinct
        # before the bond-change feature). amidohydrolase/deaminase is the lowest (it
        # shares deamination chemistry with some rows) but still clearly separable.
        self.assertGreater(sc["metallopeptidase"], 0.8)
        self.assertGreater(sc["metallophosphoesterase_nuclease"], 0.8)
        self.assertGreater(sc["metallophosphomonoesterase"], 0.8)
        self.assertGreater(sc["metallo_amidohydrolase_deaminase"], 0.7)
        # The NON-metal fingerprints remain strongly chemistry-separable: requiring water
        # for a bond-change class keeps non-hydrolase (lyase/transferase) chemistries out
        # of the bond space, so the cofactor-based separation is preserved unchanged.
        nonmetal_correct = nonmetal_total = 0
        for fp, row in conf.items():
            if fp in metal_family:
                continue
            nonmetal_total += sum(row.values())
            nonmetal_correct += row.get(fp, 0)
        self.assertGreater(nonmetal_correct / nonmetal_total, 0.8)

    def test_write_non_destructive(self) -> None:
        expansion_before = EXPANSION_PATH.read_bytes()
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "loop.json"
            report = Path(tmp) / "loop.md"
            write_mechanism_representation_loop(
                out_path=out,
                report_path=report,
                expansion_registry_path=EXPANSION_PATH,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(EXPANSION_PATH.read_bytes(), expansion_before)

    def test_deterministic(self) -> None:
        expansion = json.loads(EXPANSION_PATH.read_text())
        a = build_mechanism_representation_loop(expansion)
        b = build_mechanism_representation_loop(expansion)
        a.pop("created_utc")
        b.pop("created_utc")
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
