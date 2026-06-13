from __future__ import annotations

import unittest

from catalytic_earth.external_cofactor_ec_disambiguation import (
    build_cofactor_ec_disambiguation,
    cofactor_evidence,
    disambiguate_row,
)
from catalytic_earth.external_scaleout_bronze_import import (
    build_current702_reference_index,
)
from catalytic_earth.labels import MechanismLabel

_NO_EXACT = "no_exact_current702_accession_or_sequence_sha_overlap"


def _row(*, accession="P00001", lane="redox oxygen/sulfur", cofactors=(), ec=(),
         flags=None, ligands=()):
    return {
        "accession": accession,
        "target_family_lane": lane,
        "cofactor_provenance": [{"name": n} for n in cofactors],
        "cofactor_family_flags": flags or {},
        "rhea_ec_provenance": {"ec_numbers": list(ec), "rhea_record_count": 1},
        "residue_locators": [{"ligand_name": n, "ligand_id": None} for n in ligands],
        "duplicate_status_summary": {"current702_status": _NO_EXACT},
        "afdb_or_pdb_identifier": "AF-%s-F1" % accession,
    }


def _empty_index():
    return build_current702_reference_index(
        current_manifest_payload={"rows": []},
        frozen_benchmark_payload=[],
        expansion_payload=[],
    )


class CofactorEvidenceTests(unittest.TestCase):
    def test_reads_names_flags_and_ligands(self) -> None:
        ev = cofactor_evidence(
            _row(cofactors=["heme b"], ligands=["S-adenosyl-L-methionine"],
                 flags={"sf4_or_fe_s_evidence_present": True})
        )
        self.assertTrue(ev["heme"])
        self.assertTrue(ev["sam"])
        self.assertTrue(ev["fe_s"])
        self.assertFalse(ev["flavin"])


class DisambiguateRowTests(unittest.TestCase):
    def test_heme_peroxidase(self) -> None:
        d = disambiguate_row(_row(cofactors=["heme b"], ec=["1.11.1.7"]))
        self.assertEqual(d["fingerprint_id"], "heme_peroxidase_oxidase")

    def test_flavin_monooxygenase(self) -> None:
        d = disambiguate_row(_row(cofactors=["FAD"], ec=["1.14.14.1"]))
        self.assertEqual(d["fingerprint_id"], "flavin_monooxygenase")

    def test_flavin_dehydrogenase_reductase(self) -> None:
        d = disambiguate_row(_row(cofactors=["FAD"], ec=["1.8.1.7"]))
        self.assertEqual(d["fingerprint_id"], "flavin_dehydrogenase_reductase")

    def test_radical_sam_from_fes_and_sam(self) -> None:
        d = disambiguate_row(
            _row(flags={"sf4_or_fe_s_evidence_present": True,
                        "sam_or_adomet_evidence_present": True}, ec=["2.8.1.8"])
        )
        self.assertEqual(d["fingerprint_id"], "radical_sam_enzyme")

    def test_radical_sam_from_motif(self) -> None:
        d = disambiguate_row(_row(flags={"cx3cx2c_motif_evidence_present": True}))
        self.assertEqual(d["fingerprint_id"], "radical_sam_enzyme")

    def test_cobalamin_rearrangement(self) -> None:
        d = disambiguate_row(
            _row(flags={"cobalamin_or_b12_evidence_present": True}, ec=["5.4.99.2"])
        )
        self.assertEqual(d["fingerprint_id"], "cobalamin_radical_rearrangement")

    def test_cobalamin_rearrangement_from_oxidation_state_cofactor_name(self) -> None:
        # UniProt's canonical B12 cofactor names carry the cobalt oxidation state
        # inline (e.g. methylmalonyl-CoA mutase annotates "adenosylcob(III)alamin"),
        # which does not contain the bare substring "cobalamin".
        d = disambiguate_row(
            _row(cofactors=["adenosylcob(III)alamin"], ec=["5.4.99.2"])
        )
        self.assertEqual(d["fingerprint_id"], "cobalamin_radical_rearrangement")
        self.assertTrue(
            cofactor_evidence(_row(cofactors=["cob(II)alamin"]))["cobalamin"]
        )

    def test_no_corroboration_holds(self) -> None:
        # Copper oxidase outside the eight fingerprints -> no rule fires.
        d = disambiguate_row(_row(cofactors=["Cu cation"], ec=["1.10.3.2"]))
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(d["reason"], "no_mechanism_corroboration")

    def test_heme_without_peroxidase_ec_holds(self) -> None:
        d = disambiguate_row(_row(cofactors=["heme b"], ec=["1.14.99.1"]))
        self.assertEqual(d["decision"], "hold")

    def test_cytochrome_p450_requires_heme_and_non_peroxidase_oxygenase_handle(self) -> None:
        row = _row(
            cofactors=["heme b"],
            ec=["1.14.14.1"],
        )
        row["keywords"] = ["Cytochrome P450", "Monooxygenase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CP0001",
                "reaction": (
                    "RH + O2 + reduced [NADPH--hemoprotein reductase] = "
                    "ROH + H2O + oxidized [NADPH--hemoprotein reductase]"
                ),
                "ec_number": "1.14.14.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "cytochrome_p450_monooxygenase")
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_cytochrome_p450_peroxide_control_held(self) -> None:
        row = _row(cofactors=["heme b"], ec=["1.14.14.1"])
        row["keywords"] = ["Cytochrome P450", "Monooxygenase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PX0001",
                "reaction": "a donor + H2O2 = an oxidized donor + 2 H2O",
                "ec_number": "1.14.14.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_non_heme_iron_2og_requires_iron_and_2og_handle(self) -> None:
        row = _row(cofactors=["Fe(2+)"], ec=["1.14.11.2"])
        row["keywords"] = ["Dioxygenase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:OG0001",
                "reaction": "L-proline + 2-oxoglutarate + O2 = hydroxyproline + succinate + CO2",
                "ec_number": "1.14.11.2",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "non_heme_iron_2og_dioxygenase")
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_non_heme_iron_2og_heme_control_held(self) -> None:
        row = _row(cofactors=["heme b"], ec=["1.14.11.2"])
        row["keywords"] = ["Dioxygenase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:HX0001",
                "reaction": "substrate + 2-oxoglutarate + O2 = product + succinate + CO2",
                "ec_number": "1.14.11.2",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_coa_acyltransferase_requires_coa_or_active_site_handle(self) -> None:
        row = _row(ec=["2.3.1.48"])
        row["keywords"] = ["Acyltransferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CA0001",
                "reaction": "acetyl-CoA + L-carnitine = CoA + O-acetyl-L-carnitine",
                "ec_number": "2.3.1.48",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "coa_acyltransferase")
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_coa_acyltransferase_keyword_plus_active_site_fallback(self) -> None:
        row = _row(ec=["2.3.1.48"])
        row["keywords"] = ["Acyltransferase"]
        row["residue_locators"] = [
            {
                "position": 143,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "coa_acyltransferase")
        self.assertIn(
            "active_site_motif_or_residue_role",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "domain_or_family_profile",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_coa_acyltransferase_ec_keyword_only_control_held(self) -> None:
        row = _row(ec=["2.3.1.48"])
        row["keywords"] = ["Acyltransferase"]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_coa_acyltransferase_hydrolase_side_ec_control_held(self) -> None:
        row = _row(ec=["2.3.1.48", "3.1.1.4"])
        row["keywords"] = ["Acyltransferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:HY0001",
                "reaction": "acetyl-CoA + water = CoA + acetate",
                "ec_number": "2.3.1.48",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_cofactor_independent_isomerase_requires_reaction_or_active_site_handle(self) -> None:
        row = _row(ec=["5.3.1.1"])
        row["keywords"] = ["Isomerase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CI0001",
                "reaction": "D-glyceraldehyde 3-phosphate = glycerone phosphate",
                "ec_number": "5.3.1.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "cofactor_independent_isomerase")
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_cofactor_independent_isomerase_keyword_plus_active_site_fallback(self) -> None:
        row = _row(ec=["5.3.3.8"])
        row["keywords"] = ["Isomerase"]
        row["residue_locators"] = [
            {
                "position": 144,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "cofactor_independent_isomerase")
        self.assertIn(
            "active_site_motif_or_residue_role",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "domain_or_family_profile",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_cofactor_independent_isomerase_ec_keyword_only_control_held(self) -> None:
        row = _row(ec=["5.3.1.1"])
        row["keywords"] = ["Isomerase"]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_cofactor_independent_isomerase_non_5_3_side_ec_control_held(self) -> None:
        row = _row(ec=["5.3.3.8", "1.1.1.1"])
        row["keywords"] = ["Isomerase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CI0002",
                "reaction": "cholestenol = cholestenone",
                "ec_number": "5.3.3.8",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_molybdopterin_requires_moco_and_mechanism_handle(self) -> None:
        row = _row(
            cofactors=["Mo-bis(molybdopterin guanine dinucleotide)"],
            ec=["1.7.5.1"],
        )
        row["keywords"] = ["Molybdenum", "Oxidoreductase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:MO0001",
                "reaction": "nitrate + a quinol = a quinone + nitrite + H2O",
                "ec_number": "1.7.5.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "molybdopterin_oxidoreductase")
        self.assertIn(
            "cofactor_or_cosubstrate",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_molybdopterin_ec_only_control_held(self) -> None:
        row = _row(
            cofactors=["Mo-bis(molybdopterin guanine dinucleotide)"],
            ec=["1.7.5.1"],
        )
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_molybdopterin_side_ec_and_peroxide_controls_hold(self) -> None:
        row = _row(
            cofactors=["Mo-bis(molybdopterin guanine dinucleotide)"],
            ec=["1.7.5.1", "3.1.1.1"],
        )
        row["keywords"] = ["Molybdenum", "Oxidoreductase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:MO0002",
                "reaction": "nitrate + a quinol = a quinone + nitrite + H2O",
                "ec_number": "1.7.5.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

        peroxide = _row(
            cofactors=["Mo-bis(molybdopterin guanine dinucleotide)"],
            ec=["1.7.5.1"],
        )
        peroxide["keywords"] = ["Molybdenum", "Oxidoreductase"]
        peroxide["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:MO0003",
                "reaction": "a donor + H2O2 = an oxidized donor + 2 H2O",
                "ec_number": "1.7.5.1",
            }
        ]
        d2 = disambiguate_row(peroxide)
        self.assertEqual(d2["decision"], "hold")

    def test_copper_oxidoreductase_requires_copper_mechanism_handle(self) -> None:
        row = _row(cofactors=["Cu(2+)"], ec=["1.10.3.2"])
        row["keywords"] = ["Copper", "Oxidoreductase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CU0001",
                "reaction": "4 hydroquinone + O2 = 4 benzosemiquinone + 2 H2O",
                "ec_number": "1.10.3.2",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "copper_oxidoreductase")
        self.assertIn(
            "cofactor_or_cosubstrate",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_copper_ec_keyword_only_and_boundary_controls_hold(self) -> None:
        ec_only = _row(ec=["1.10.3.2"])
        ec_only["keywords"] = ["Copper"]
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        heme = _row(cofactors=["heme b"], ec=["1.10.3.2"])
        heme["keywords"] = ["Copper", "Oxidoreductase"]
        heme["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CU0002",
                "reaction": "a donor + O2 = product + H2O",
                "ec_number": "1.10.3.2",
            }
        ]
        self.assertEqual(disambiguate_row(heme)["decision"], "hold")

        side_ec = _row(cofactors=["Cu(2+)"], ec=["1.10.3.2", "2.4.1.1"])
        side_ec["keywords"] = ["Copper", "Oxidoreductase"]
        side_ec["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CU0003",
                "reaction": "a donor + O2 = product + H2O",
                "ec_number": "1.10.3.2",
            }
        ]
        self.assertEqual(disambiguate_row(side_ec)["decision"], "hold")

    def test_non_plp_racemase_epimerase_requires_mechanism_handle(self) -> None:
        row = _row(ec=["5.1.3.3"])
        row["protein_name"] = "Galactose mutarotase (Aldose 1-epimerase)"
        row["keywords"] = ["Isomerase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:MR0001",
                "reaction": "alpha-D-galactose = beta-D-galactose",
                "ec_number": "5.1.3.3",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "metal_racemase_epimerase_non_plp")
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "domain_or_family_profile",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_non_plp_racemase_epimerase_keyword_active_site_fallback(self) -> None:
        row = _row(ec=["5.1.99.4"])
        row["protein_name"] = "Alpha-methylacyl-CoA racemase"
        row["keywords"] = ["Isomerase"]
        row["residue_locators"] = [
            {
                "position": 101,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "metal_racemase_epimerase_non_plp")
        self.assertIn(
            "active_site_motif_or_residue_role",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_non_plp_racemase_epimerase_controls_hold(self) -> None:
        ec_only = _row(ec=["5.1.3.3"])
        ec_only["keywords"] = ["Isomerase"]
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        plp = _row(cofactors=["pyridoxal 5'-phosphate"], ec=["5.1.1.1"])
        plp["protein_name"] = "Alanine racemase"
        plp["keywords"] = ["Isomerase"]
        plp["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:MR0002",
                "reaction": "L-alanine = D-alanine",
                "ec_number": "5.1.1.1",
            }
        ]
        self.assertEqual(disambiguate_row(plp)["decision"], "hold")

        side_ec = _row(ec=["5.1.3.3", "2.5.1.18"])
        side_ec["protein_name"] = "Dual-function epimerase transferase"
        side_ec["keywords"] = ["Isomerase"]
        side_ec["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:MR0003",
                "reaction": "alpha-D-galactose = beta-D-galactose",
                "ec_number": "5.1.3.3",
            }
        ]
        self.assertEqual(disambiguate_row(side_ec)["decision"], "hold")

    def test_thiamine_diphosphate_requires_thdp_and_mechanism_handle(self) -> None:
        row = _row(cofactors=["thiamine diphosphate", "Mg(2+)"], ec=["2.2.1.1"])
        row["protein_name"] = "Transketolase"
        row["keywords"] = ["Thiamine pyrophosphate", "Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:TD0001",
                "reaction": "D-xylulose 5-phosphate + D-ribose 5-phosphate = D-glyceraldehyde 3-phosphate + D-sedoheptulose 7-phosphate",
                "ec_number": "2.2.1.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "thiamine_diphosphate_enzyme")
        self.assertIn(
            "cofactor_or_cosubstrate",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_thiamine_diphosphate_active_site_fallback(self) -> None:
        row = _row(cofactors=["thiamine pyrophosphate"], ec=["4.1.1.1"])
        row["protein_name"] = "Pyruvate decarboxylase"
        row["keywords"] = ["Thiamine pyrophosphate", "Lyase"]
        row["residue_locators"] = [
            {
                "position": 28,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "thiamine diphosphate",
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "thiamine_diphosphate_enzyme")
        self.assertIn(
            "active_site_motif_or_residue_role",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "domain_or_family_profile",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_thiamine_diphosphate_controls_hold(self) -> None:
        ec_only = _row(cofactors=["thiamine diphosphate"], ec=["2.2.1.1"])
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        plp = _row(
            cofactors=["thiamine diphosphate", "pyridoxal 5'-phosphate"],
            ec=["4.1.1.1"],
        )
        plp["keywords"] = ["Thiamine pyrophosphate", "Lyase"]
        plp["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:TD0002",
                "reaction": "2-oxo acid = aldehyde + CO2",
                "ec_number": "4.1.1.1",
            }
        ]
        self.assertEqual(disambiguate_row(plp)["decision"], "hold")

        side_ec = _row(cofactors=["thiamine diphosphate"], ec=["2.2.1.1", "3.1.1.1"])
        side_ec["protein_name"] = "Dual-function transketolase hydrolase"
        side_ec["keywords"] = ["Thiamine pyrophosphate"]
        side_ec["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:TD0003",
                "reaction": "D-xylulose 5-phosphate + aldehyde = product",
                "ec_number": "2.2.1.1",
            }
        ]
        self.assertEqual(disambiguate_row(side_ec)["decision"], "hold")

    def test_zinc_lyase_hydratase_requires_zinc_and_mechanism_handle(self) -> None:
        row = _row(cofactors=["Zn(2+)"], ec=["4.2.1.1"])
        row["protein_name"] = "Carbonic anhydrase 2"
        row["keywords"] = ["Lyase", "Zinc", "Metal-binding"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:ZL0001",
                "reaction": "hydrogencarbonate + H(+) = CO2 + H2O",
                "ec_number": "4.2.1.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "zinc_lyase_hydratase")
        self.assertIn(
            "cofactor_or_cosubstrate",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_zinc_lyase_hydratase_active_site_fallback(self) -> None:
        row = _row(cofactors=["Zn(2+)"], ec=["4.2.1.109"])
        row["protein_name"] = "Methylthioribulose-1-phosphate dehydratase"
        row["keywords"] = ["Lyase", "Zinc"]
        row["residue_locators"] = [
            {
                "position": 101,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "Zn(2+)",
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "zinc_lyase_hydratase")
        self.assertIn(
            "active_site_motif_or_residue_role",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_zinc_lyase_hydratase_controls_hold(self) -> None:
        no_zinc = _row(ec=["4.2.1.1"])
        no_zinc["protein_name"] = "Carbonic anhydrase"
        no_zinc["keywords"] = ["Lyase"]
        no_zinc["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:ZL0002",
                "reaction": "hydrogencarbonate + H(+) = CO2 + H2O",
                "ec_number": "4.2.1.1",
            }
        ]
        self.assertEqual(disambiguate_row(no_zinc)["decision"], "hold")

        plp = _row(cofactors=["Zn(2+)", "pyridoxal 5'-phosphate"], ec=["4.2.1.24"])
        plp["protein_name"] = "PLP zinc dehydratase boundary"
        plp["keywords"] = ["Lyase", "Zinc"]
        plp["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:ZL0003",
                "reaction": "substrate = product + H2O",
                "ec_number": "4.2.1.24",
            }
        ]
        self.assertEqual(disambiguate_row(plp)["decision"], "hold")

        side_ec = _row(cofactors=["Zn(2+)"], ec=["4.2.1.1", "3.1.1.1"])
        side_ec["protein_name"] = "Hydrolase side-activity zinc dehydratase"
        side_ec["keywords"] = ["Lyase", "Zinc"]
        side_ec["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:ZL0004",
                "reaction": "hydrogencarbonate + H(+) = CO2 + H2O",
                "ec_number": "4.2.1.1",
            }
        ]
        self.assertEqual(disambiguate_row(side_ec)["decision"], "hold")

    def test_biotin_dependent_carboxylase_requires_biotin_and_mechanism_handle(self) -> None:
        row = _row(cofactors=["Biotin", "Mg(2+)"], ec=["6.4.1.2"])
        row["protein_name"] = "Acetyl-CoA carboxylase"
        row["keywords"] = ["Biotin", "Ligase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:BC0001",
                "reaction": "acetyl-CoA + ATP + hydrogencarbonate = malonyl-CoA + ADP + phosphate",
                "ec_number": "6.4.1.2",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "biotin_dependent_carboxylase")
        self.assertIn(
            "cofactor_or_cosubstrate",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_biotin_dependent_carboxylase_biotinyl_lysine_fallback(self) -> None:
        row = _row(ec=["6.3.4.14"])
        row["protein_name"] = "Biotin carboxylase"
        row["keywords"] = ["Biotin", "Ligase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:BC0005",
                "reaction": "N(6)-biotinyl-L-lysyl-[protein] + hydrogencarbonate + ATP = N(6)-carboxybiotinyl-L-lysyl-[protein] + ADP + phosphate + H(+)",
                "ec_number": "6.3.4.14",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 32,
                "feature_code": "MOD_RES",
                "feature_type": "Modified residue",
                "ligand_name": "N6-biotinyl-L-lysine",
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            },
            {
                "position": 122,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            },
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "biotin_dependent_carboxylase")
        self.assertIn(
            "active_site_motif_or_residue_role",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "domain_or_family_profile",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_biotin_dependent_carboxylase_controls_hold(self) -> None:
        ec_only = _row(ec=["6.4.1.2"])
        ec_only["protein_name"] = "Acetyl-CoA carboxylase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        kinase = _row(cofactors=["Biotin"], ec=["6.4.1.2", "2.7.1.1"])
        kinase["protein_name"] = "Biotin carboxylase kinase boundary"
        kinase["keywords"] = ["Biotin", "Kinase"]
        kinase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:BC0002",
                "reaction": "ATP + hydrogencarbonate + biotin = ADP + carboxybiotin + phosphate",
                "ec_number": "6.4.1.2",
            }
        ]
        self.assertEqual(disambiguate_row(kinase)["decision"], "hold")

        side_ec = _row(cofactors=["Biotin"], ec=["6.4.1.2", "3.1.1.1"])
        side_ec["protein_name"] = "Biotin carboxylase hydrolase boundary"
        side_ec["keywords"] = ["Biotin", "Ligase"]
        side_ec["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:BC0003",
                "reaction": "ATP + hydrogencarbonate + biotin = ADP + carboxybiotin + phosphate",
                "ec_number": "6.4.1.2",
            }
        ]
        self.assertEqual(disambiguate_row(side_ec)["decision"], "hold")

        biotin_ligase = _row(cofactors=["Biotin"], ec=["6.3.4.15"])
        biotin_ligase["protein_name"] = "Biotin--[acetyl-CoA-carboxylase] ligase"
        biotin_ligase["keywords"] = ["Biotin", "Ligase"]
        biotin_ligase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:BC0004",
                "reaction": "biotin + L-lysyl-[protein] + ATP = N(6)-biotinyl-L-lysyl-[protein] + AMP + diphosphate + H(+)",
                "ec_number": "6.3.4.15",
            }
        ]
        self.assertEqual(disambiguate_row(biotin_ligase)["decision"], "hold")

    def test_nucleoside_diphosphate_kinase_requires_mechanism_handles(self) -> None:
        row = _row(ec=["2.7.4.6"])
        row["protein_name"] = "Nucleoside diphosphate kinase"
        row["keywords"] = ["Kinase", "Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:NK0001",
                "reaction": "ATP + nucleoside diphosphate = ADP + nucleoside triphosphate",
                "ec_number": "2.7.4.6",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 118,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Pros-phosphohistidine intermediate",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "nucleoside_diphosphate_kinase")
        axes = d["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_nucleoside_diphosphate_kinase_controls_hold(self) -> None:
        ec_only = _row(ec=["2.7.4.6"])
        ec_only["protein_name"] = "Nucleoside diphosphate kinase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        for ec_numbers, name in (
            (["2.7.4.6", "2.7.11.1"], "Nucleoside diphosphate protein kinase"),
            (["2.7.4.6", "2.7.13.3"], "Nucleoside diphosphate histidine kinase"),
            (["2.7.4.6", "3.1.11.1"], "Nucleoside diphosphate nuclease boundary"),
            (["2.7.4.6", "2.7.4.3"], "Nucleoside diphosphate adenylate kinase"),
        ):
            row = _row(ec=ec_numbers)
            row["protein_name"] = name
            row["rhea_ec_provenance"]["rhea_records"] = [
                {
                    "rhea_id": "RHEA:NK0002",
                    "reaction": "ATP + nucleoside diphosphate = ADP + nucleoside triphosphate",
                    "ec_number": "2.7.4.6",
                }
            ]
            row["residue_locators"] = [
                {
                    "position": 118,
                    "feature_code": "ACT_SITE",
                    "feature_type": "Active site",
                    "ligand_name": None,
                    "ligand_id": None,
                    "description": "Pros-phosphohistidine intermediate",
                    "evidence_codes": ["ECO:0000269"],
                }
            ]
            self.assertEqual(disambiguate_row(row)["decision"], "hold")

    def test_askha_sugar_acetate_kinase_requires_mechanism_handles(self) -> None:
        row = _row(ec=["2.7.1.1"])
        row["protein_name"] = "Hexokinase"
        row["keywords"] = ["Kinase", "Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AS0001",
                "reaction": "ATP + D-glucose = ADP + D-glucose 6-phosphate + H(+)",
                "ec_number": "2.7.1.1",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 210,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "askha_sugar_acetate_kinase")
        axes = d["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_askha_sugar_acetate_kinase_controls_hold(self) -> None:
        ec_only = _row(ec=["2.7.1.1"])
        ec_only["protein_name"] = "Hexokinase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        boundary_cases = (
            (["2.7.1.1", "2.7.11.1"], "Hexokinase protein kinase boundary"),
            (["2.7.1.1", "2.7.13.3"], "Hexokinase histidine kinase boundary"),
            (["2.7.1.1", "3.1.1.1"], "Hexokinase hydrolase boundary"),
            (["2.7.1.21"], "Thymidine kinase"),
            (["2.7.1.11"], "6-phosphofructokinase"),
        )
        for ec_numbers, name in boundary_cases:
            row = _row(ec=ec_numbers)
            row["protein_name"] = name
            row["keywords"] = ["Kinase", "Transferase"]
            row["rhea_ec_provenance"]["rhea_records"] = [
                {
                    "rhea_id": "RHEA:AS0002",
                    "reaction": "ATP + D-glucose = ADP + D-glucose 6-phosphate + H(+)",
                    "ec_number": ec_numbers[0],
                }
            ]
            row["residue_locators"] = [
                {
                    "position": 210,
                    "feature_code": "BINDING",
                    "feature_type": "Binding site",
                    "ligand_name": "ATP",
                    "ligand_id": None,
                    "description": "ATP",
                    "evidence_codes": ["ECO:0000269"],
                }
            ]
            self.assertEqual(disambiguate_row(row)["decision"], "hold")

        ndk_side = _row(ec=["2.7.1.1", "2.7.4.6"])
        ndk_side["protein_name"] = "Nucleoside diphosphate kinase"
        ndk_side["keywords"] = ["Kinase", "Transferase"]
        ndk_side["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AS0003",
                "reaction": "ATP + nucleoside diphosphate = ADP + nucleoside triphosphate",
                "ec_number": "2.7.4.6",
            }
        ]
        ndk_side["residue_locators"] = [
            {
                "position": 118,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        ndk_decision = disambiguate_row(ndk_side)
        self.assertEqual(ndk_decision["fingerprint_id"], "nucleoside_diphosphate_kinase")
        self.assertNotEqual(ndk_decision["fingerprint_id"], "askha_sugar_acetate_kinase")

        ghmp_side = _row(ec=["2.7.1.36"])
        ghmp_side["protein_name"] = "Mevalonate kinase"
        ghmp_side["keywords"] = ["Kinase", "Transferase"]
        ghmp_side["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AS0004",
                "reaction": "ATP + (R)-mevalonate = ADP + (R)-5-phosphomevalonate + H(+)",
                "ec_number": "2.7.1.36",
            }
        ]
        ghmp_side["residue_locators"] = [
            {
                "position": 105,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        ghmp_decision = disambiguate_row(ghmp_side)
        self.assertEqual(ghmp_decision["fingerprint_id"], "ghmp_small_molecule_kinase")
        self.assertNotEqual(ghmp_decision["fingerprint_id"], "askha_sugar_acetate_kinase")

    def test_ghmp_small_molecule_kinase_requires_mechanism_handles(self) -> None:
        row = _row(ec=["2.7.1.36"])
        row["protein_name"] = "Mevalonate kinase"
        row["keywords"] = ["Kinase", "Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GH0001",
                "reaction": "ATP + (R)-mevalonate = ADP + (R)-5-phosphomevalonate + H(+)",
                "ec_number": "2.7.1.36",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 105,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "ghmp_small_molecule_kinase")
        axes = d["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_ghmp_small_molecule_kinase_controls_hold(self) -> None:
        ec_only = _row(ec=["2.7.1.36"])
        ec_only["protein_name"] = "Mevalonate kinase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        boundary_cases = (
            (["2.7.1.36", "2.7.11.1"], "Mevalonate protein kinase boundary"),
            (["2.7.1.36", "2.7.13.3"], "Mevalonate histidine kinase boundary"),
            (["2.7.1.36", "3.1.1.1"], "Mevalonate hydrolase boundary"),
            (["2.7.1.21"], "Thymidine kinase"),
            (["2.7.1.11"], "6-phosphofructokinase"),
        )
        for ec_numbers, name in boundary_cases:
            row = _row(ec=ec_numbers)
            row["protein_name"] = name
            row["keywords"] = ["Kinase", "Transferase"]
            row["rhea_ec_provenance"]["rhea_records"] = [
                {
                    "rhea_id": "RHEA:GH0002",
                    "reaction": "ATP + (R)-mevalonate = ADP + (R)-5-phosphomevalonate + H(+)",
                    "ec_number": ec_numbers[0],
                }
            ]
            row["residue_locators"] = [
                {
                    "position": 105,
                    "feature_code": "BINDING",
                    "feature_type": "Binding site",
                    "ligand_name": "ATP",
                    "ligand_id": None,
                    "description": "ATP",
                    "evidence_codes": ["ECO:0000269"],
                }
            ]
            self.assertEqual(disambiguate_row(row)["decision"], "hold")

        askha_side = _row(ec=["2.7.1.1"])
        askha_side["protein_name"] = "Hexokinase"
        askha_side["keywords"] = ["Kinase", "Transferase"]
        askha_side["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GH0003",
                "reaction": "ATP + D-glucose = ADP + D-glucose 6-phosphate + H(+)",
                "ec_number": "2.7.1.1",
            }
        ]
        askha_side["residue_locators"] = [
            {
                "position": 210,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        askha_decision = disambiguate_row(askha_side)
        self.assertEqual(askha_decision["fingerprint_id"], "askha_sugar_acetate_kinase")
        self.assertNotEqual(askha_decision["fingerprint_id"], "ghmp_small_molecule_kinase")

    def test_deoxynucleoside_kinase_requires_mechanism_handles(self) -> None:
        row = _row(ec=["2.7.1.21"])
        row["protein_name"] = "Thymidine kinase"
        row["keywords"] = ["Kinase", "Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:DK0001",
                "reaction": "ATP + thymidine = ADP + dTMP + H(+)",
                "ec_number": "2.7.1.21",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 105,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "deoxynucleoside_kinase")
        axes = d["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_deoxynucleoside_kinase_controls_hold(self) -> None:
        ec_only = _row(ec=["2.7.1.21"])
        ec_only["protein_name"] = "Thymidine kinase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        boundary_cases = (
            (["2.7.1.21", "2.7.11.1"], "Thymidine protein kinase boundary"),
            (["2.7.1.21", "2.7.13.3"], "Thymidine histidine kinase boundary"),
            (["2.7.1.21", "3.1.1.1"], "Thymidine hydrolase boundary"),
            (["2.7.1.21", "2.7.4.6"], "Nucleoside diphosphate kinase boundary"),
            (["2.7.1.11"], "6-phosphofructokinase"),
        )
        for ec_numbers, name in boundary_cases:
            row = _row(ec=ec_numbers)
            row["protein_name"] = name
            row["keywords"] = ["Kinase", "Transferase"]
            row["rhea_ec_provenance"]["rhea_records"] = [
                {
                    "rhea_id": "RHEA:DK0002",
                    "reaction": "ATP + thymidine = ADP + dTMP + H(+)",
                    "ec_number": ec_numbers[0],
                }
            ]
            row["residue_locators"] = [
                {
                    "position": 105,
                    "feature_code": "BINDING",
                    "feature_type": "Binding site",
                    "ligand_name": "ATP",
                    "ligand_id": None,
                    "description": "ATP",
                    "evidence_codes": ["ECO:0000269"],
                }
            ]
            self.assertEqual(disambiguate_row(row)["decision"], "hold")

        askha_side = _row(ec=["2.7.1.1"])
        askha_side["protein_name"] = "Hexokinase"
        askha_side["keywords"] = ["Kinase", "Transferase"]
        askha_side["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:DK0003",
                "reaction": "ATP + D-glucose = ADP + D-glucose 6-phosphate + H(+)",
                "ec_number": "2.7.1.1",
            }
        ]
        askha_side["residue_locators"] = [
            {
                "position": 210,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        askha_decision = disambiguate_row(askha_side)
        self.assertEqual(askha_decision["fingerprint_id"], "askha_sugar_acetate_kinase")
        self.assertNotEqual(askha_decision["fingerprint_id"], "deoxynucleoside_kinase")

        ghmp_side = _row(ec=["2.7.1.36"])
        ghmp_side["protein_name"] = "Mevalonate kinase"
        ghmp_side["keywords"] = ["Kinase", "Transferase"]
        ghmp_side["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:DK0004",
                "reaction": "ATP + (R)-mevalonate = ADP + (R)-5-phosphomevalonate + H(+)",
                "ec_number": "2.7.1.36",
            }
        ]
        ghmp_side["residue_locators"] = [
            {
                "position": 105,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        ghmp_decision = disambiguate_row(ghmp_side)
        self.assertEqual(ghmp_decision["fingerprint_id"], "ghmp_small_molecule_kinase")
        self.assertNotEqual(ghmp_decision["fingerprint_id"], "deoxynucleoside_kinase")

    def test_multi_signal_conflict_holds(self) -> None:
        # Flavin + heme present, with a peroxidase EC and a flavin-monooxygenase
        # EC -> heme rule and (no, heme blocks flavin)... construct a true
        # conflict: radical-SAM cofactors AND a flavin monooxygenase signal.
        row = _row(
            cofactors=["FAD"],
            ligands=["S-adenosyl-L-methionine", "[4Fe-4S] cluster"],
            ec=["1.14.14.1"],
        )
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(d["reason"], "multi_fingerprint_signal_conflict")
        self.assertEqual(
            d["candidates"], ["flavin_monooxygenase", "radical_sam_enzyme"]
        )


class BuildDisambiguationTests(unittest.TestCase):
    def test_end_to_end_guardrails_dedup_and_leakage(self) -> None:
        index = build_current702_reference_index(
            current_manifest_payload={
                "rows": [{"entry_id": "m_csa:1", "accession": "P70000"}]
            },
            frozen_benchmark_payload=[{"entry_id": "m_csa:1"}],
            expansion_payload=[{"entry_id": "uniprot:P09999"}],
        )
        pools = [
            {
                "pool": "redox_cofactor_confounded",
                "path": "artifacts/redox.json",
                "rows": [
                    _row(accession="P00001", cofactors=["heme b"], ec=["1.11.1.7"]),
                    _row(accession="P00002", cofactors=["FAD"], ec=["1.14.14.1"]),
                    # no corroboration -> held
                    _row(accession="P00003", cofactors=["Cu cation"], ec=["1.10.3.2"]),
                    # already in current702 -> screened out
                    _row(accession="P70000", cofactors=["heme b"], ec=["1.11.1.7"]),
                    # already in expansion registry -> deduped
                    _row(accession="P09999", cofactors=["heme b"], ec=["1.11.1.7"]),
                ],
            },
        ]
        audit = build_cofactor_ec_disambiguation(
            pools=pools, registry=[{"entry_id": "uniprot:P09999"}], index=index
        )
        c = audit["counts"]
        self.assertEqual(c["importable_new_labels"], 2)
        self.assertEqual(c["fingerprint_counts"]["heme_peroxidase_oxidase"], 1)
        self.assertEqual(c["fingerprint_counts"]["flavin_monooxygenase"], 1)
        self.assertEqual(c["hold_count"], 1)
        self.assertEqual(c["skip_count"], 2)

        self.assertFalse(audit["guardrails"]["curated_registry_written"])
        self.assertFalse(
            audit["guardrails"]["predictive_features_use_ec_name_or_prose"]
        )
        self.assertTrue(
            audit["guardrails"]["ec_used_for_scope_assignment_only_never_predictive"]
        )

        imported_ids = {l["entry_id"] for l in audit["applied_labels"]}
        self.assertNotIn("uniprot:P70000", imported_ids)
        self.assertNotIn("uniprot:P09999", imported_ids)

        for label in audit["applied_labels"]:
            MechanismLabel.from_dict(label)
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["label_type"], "seed_fingerprint")
            self.assertTrue(label["fingerprint_id"])
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            self.assertIn("ec_label", label["evidence"]["excluded_context"])
            self.assertEqual(
                label["evidence"]["sources"], ["external_cofactor_ec_disambiguation"]
            )


if __name__ == "__main__":
    unittest.main()
