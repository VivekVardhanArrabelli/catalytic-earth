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

    def test_short_chain_dehydrogenase_reductase_requires_sdr_wall(self) -> None:
        row = _row(ec=["1.1.1.100"])
        row["protein_name"] = "Short-chain dehydrogenase/reductase SDR"
        row["keywords"] = ["NAD", "NADP"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:SDR001",
                "reaction": "secondary alcohol + NAD(+) = ketone + NADH + H(+)",
                "ec_number": "1.1.1.100",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 153,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "description": "Ser-Tyr-Lys catalytic tetrad",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]

        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "short_chain_dehydrogenase_reductase")
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

    def test_short_chain_dehydrogenase_reductase_ec_name_only_control_held(self) -> None:
        row = _row(ec=["1.1.1.100"])
        row["protein_name"] = "Short-chain dehydrogenase/reductase-like protein"
        row["keywords"] = ["NAD"]

        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_aldo_keto_reductase_gets_its_own_fingerprint_not_sdr_or_generic_nad_p(self) -> None:
        row = _row(ec=["1.1.1.21"])
        row["protein_name"] = "Aldo-keto reductase"
        row["keywords"] = ["NADP"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AKR001",
                "reaction": "aldehyde + NADPH + H(+) = alcohol + NADP(+)",
                "ec_number": "1.1.1.21",
            }
        ]

        d = disambiguate_row(row)
        # AKR family text + NADP cosubstrate + carbonyl-reduction reaction now
        # route to the dedicated aldo_keto_reductase fingerprint, not the SDR
        # family or the generic NAD(P) dehydrogenase bucket.
        self.assertEqual(d.get("fingerprint_id"), "aldo_keto_reductase")
        self.assertNotEqual(d.get("fingerprint_id"), "short_chain_dehydrogenase_reductase")
        self.assertNotEqual(d.get("fingerprint_id"), "nad_p_dehydrogenase")

    def test_aldo_keto_reductase_ec_name_only_control_held(self) -> None:
        # Name only, no NADP cosubstrate / reaction corroboration -> held.
        row = _row(ec=["1.1.1.21"])
        row["protein_name"] = "Aldo-keto reductase-like protein"
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_aldo_keto_reductase_sdr_boundary_not_forced(self) -> None:
        # An SDR-named row must not be pulled into the AKR fingerprint.
        row = _row(ec=["1.1.1.100"])
        row["protein_name"] = "Short-chain dehydrogenase/reductase SDR"
        row["keywords"] = ["NADP"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:SDR009",
                "reaction": "secondary alcohol + NADP(+) = ketone + NADPH + H(+)",
                "ec_number": "1.1.1.100",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "aldo_keto_reductase")

    def test_aminoglycoside_acetyltransferase_gets_its_own_fingerprint_not_coa(self) -> None:
        row = _row(ec=["2.3.1.82"])
        row["protein_name"] = "Aminoglycoside N(6')-acetyltransferase"
        row["keywords"] = ["Antibiotic resistance", "Acetyltransferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AAC001",
                "reaction": "acetyl-CoA + kanamycin = CoA + N(6')-acetylkanamycin",
                "ec_number": "2.3.1.82",
            }
        ]
        d = disambiguate_row(row)
        # AAC family text + acetyl-CoA + acetyl-transfer reaction route to the dedicated
        # aminoglycoside_acetyltransferase fingerprint, not the generic CoA acyltransferase.
        self.assertEqual(d.get("fingerprint_id"), "aminoglycoside_acetyltransferase")
        self.assertNotEqual(d.get("fingerprint_id"), "coa_acyltransferase")

    def test_generic_coa_acyltransferase_not_pulled_into_aac(self) -> None:
        row = _row(ec=["2.3.1.16"])
        row["protein_name"] = "Acetyl-CoA C-acyltransferase"
        row["keywords"] = ["Acyltransferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:COA001",
                "reaction": "acetyl-CoA + an acyl-CoA = CoA + a 3-oxoacyl-CoA",
                "ec_number": "2.3.1.16",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "aminoglycoside_acetyltransferase")

    def test_aminoglycoside_acetyltransferase_name_only_control_held(self) -> None:
        row = _row(ec=["2.3.1.81"])
        row["protein_name"] = "Aminoglycoside acetyltransferase"
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_bifunctional_aac_aph_is_held(self) -> None:
        # A bifunctional acetyltransferase-phosphotransferase trips both family
        # boundaries and is held rather than forced into either fingerprint.
        row = _row(ec=["2.3.1.81"])
        row["protein_name"] = "Bifunctional aminoglycoside acetyltransferase-phosphotransferase"
        row["keywords"] = ["Antibiotic resistance"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:BIF001",
                "reaction": "acetyl-CoA + gentamicin = CoA + N-acetylgentamicin",
                "ec_number": "2.3.1.81",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_metallo_beta_lactamase_gets_its_own_fingerprint_not_serine_or_amidohydrolase(self) -> None:
        row = _row(ec=["3.5.2.6"], cofactors=["Zn(2+)"])
        row["protein_name"] = "Beta-lactamase NDM-1"
        row["keywords"] = ["Antibiotic resistance", "Zinc"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:MBL001",
                "reaction": "a beta-lactam + H2O = a substituted beta-amino acid",
                "ec_number": "3.5.2.6",
            }
        ]
        d = disambiguate_row(row)
        # Zn context + beta-lactam hydrolysis at EC 3.5.2.6 routes to the dedicated
        # metallo_beta_lactamase fingerprint, not serine_beta_lactamase (zinc-excluded)
        # and not the generic metallo_amidohydrolase_deaminase (beta-lactam excluded).
        self.assertEqual(d.get("fingerprint_id"), "metallo_beta_lactamase")
        self.assertNotEqual(d.get("fingerprint_id"), "serine_beta_lactamase")
        self.assertNotEqual(d.get("fingerprint_id"), "metallo_amidohydrolase_deaminase")

    def test_serine_beta_lactamase_not_pulled_into_mbl(self) -> None:
        row = _row(ec=["3.5.2.6"])
        row["protein_name"] = "Beta-lactamase TEM-1"
        row["keywords"] = ["Antibiotic resistance"]
        row["residue_locators"] = [
            {
                "position": 70,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "description": "Acyl-ester intermediate; nucleophile serine",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:SBL001",
                "reaction": "a beta-lactam + H2O = a substituted beta-amino acid",
                "ec_number": "3.5.2.6",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "metallo_beta_lactamase")

    def test_metallo_amidohydrolase_non_betalactam_still_routes_to_amidohydrolase(self) -> None:
        # A zinc deaminase (EC 3.5.4) must stay metallo_amidohydrolase_deaminase --
        # the MBL exclusion only diverts beta-lactam-hydrolyzing rows.
        row = _row(ec=["3.5.4.4"], cofactors=["Zn(2+)"])
        row["protein_name"] = "Adenosine deaminase"
        row["keywords"] = ["Hydrolase", "Zinc"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:ADA001",
                "reaction": "adenosine + H2O = inosine + NH3",
                "ec_number": "3.5.4.4",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d.get("fingerprint_id"), "metallo_amidohydrolase_deaminase")

    def test_peroxiredoxin_gets_its_own_fingerprint_not_heme_peroxidase(self) -> None:
        row = _row(ec=["1.11.1.24"])
        row["protein_name"] = "Peroxiredoxin-2"
        row["keywords"] = ["Antioxidant", "Redox-active center"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PRX001",
                "reaction": (
                    "[thioredoxin]-dithiol + a hydroperoxide = "
                    "[thioredoxin]-disulfide + an alcohol + H2O"
                ),
                "ec_number": "1.11.1.24",
            }
        ]
        d = disambiguate_row(row)
        # A peroxidatic-thiol family name + peroxide-reduction reaction at EC 1.11.1
        # (no heme) routes to the dedicated peroxiredoxin_thiol_peroxidase fingerprint,
        # not heme_peroxidase_oxidase (which requires heme).
        self.assertEqual(d.get("fingerprint_id"), "peroxiredoxin_thiol_peroxidase")

    def test_selenocysteine_glutathione_peroxidase_routes_to_peroxiredoxin(self) -> None:
        row = _row(ec=["1.11.1.9"])
        row["protein_name"] = "Glutathione peroxidase 1"
        row["keywords"] = ["Selenocysteine", "Antioxidant"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GPX001",
                "reaction": "2 glutathione + H2O2 = glutathione disulfide + 2 H2O",
                "ec_number": "1.11.1.9",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d.get("fingerprint_id"), "peroxiredoxin_thiol_peroxidase")

    def test_heme_peroxidase_not_pulled_into_peroxiredoxin(self) -> None:
        # A heme peroxidase / catalase must stay heme_peroxidase_oxidase -- it has heme
        # and no peroxidatic-thiol family text, so the peroxiredoxin rule cannot fire.
        row = _row(ec=["1.11.1.6"], cofactors=["heme b"])
        row["protein_name"] = "Catalase"
        row["keywords"] = ["Heme", "Hydrogen peroxide"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CAT001",
                "reaction": "2 H2O2 = O2 + 2 H2O",
                "ec_number": "1.11.1.6",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d.get("fingerprint_id"), "heme_peroxidase_oxidase")
        self.assertNotEqual(d.get("fingerprint_id"), "peroxiredoxin_thiol_peroxidase")

    def test_flavin_nadh_peroxidase_not_pulled_into_peroxiredoxin(self) -> None:
        # FAD-dependent NADH peroxidase (EC 1.11.1.1) is a flavoprotein, not a
        # peroxidatic-thiol peroxidase: flavin-excluded, so it is held.
        row = _row(ec=["1.11.1.1"], cofactors=["FAD"])
        row["protein_name"] = "NADH peroxidase"
        row["keywords"] = ["FAD", "Flavoprotein"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:NPX001",
                "reaction": "NADH + H+ + H2O2 = NAD+ + 2 H2O",
                "ec_number": "1.11.1.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "peroxiredoxin_thiol_peroxidase")

    def test_multi_ec_glutathione_peroxidase_moonlighter_is_held(self) -> None:
        # A moonlighting multi-EC entry (e.g. glutathione-peroxidase-active ceruloplasmin
        # carrying a copper-oxidase EC) trips the side-EC guard and is held, not labelled.
        row = _row(ec=["1.11.1.9", "1.16.3.1"], cofactors=["copper"])
        row["protein_name"] = "Glutathione peroxidase ceruloplasmin"
        row["keywords"] = ["Copper", "Antioxidant"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:CERU001",
                "reaction": "2 glutathione + H2O2 = glutathione disulfide + 2 H2O",
                "ec_number": "1.11.1.9",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "peroxiredoxin_thiol_peroxidase")

    def test_paps_sulfotransferase_routes_on_family_and_paps_reaction(self) -> None:
        row = _row(ec=["2.8.2.1"])
        row["protein_name"] = "Sulfotransferase 1A1"
        row["keywords"] = ["Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:SUL001",
                "reaction": (
                    "a phenol + 3'-phosphoadenylyl sulfate = an aryl sulfate + "
                    "adenosine 3',5'-bisphosphate + H(+)"
                ),
                "ec_number": "2.8.2.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d.get("fingerprint_id"), "paps_sulfotransferase")

    def test_sulfurtransferase_rhodanese_not_pulled_into_sulfotransferase(self) -> None:
        # A sulfur-relay sulfurtransferase (EC 2.8.1, rhodanese) is boundary-guarded and
        # off-scope (not 2.8.2); it must not route to paps_sulfotransferase.
        row = _row(ec=["2.8.1.1"])
        row["protein_name"] = "Thiosulfate sulfurtransferase"
        row["keywords"] = ["Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:RHD001",
                "reaction": "thiosulfate + hydrogen cyanide = sulfite + thiocyanate + 2 H(+)",
                "ec_number": "2.8.1.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "paps_sulfotransferase")

    def test_sulfotransferase_name_without_paps_reaction_is_held(self) -> None:
        row = _row(ec=["2.8.2.1"])
        row["protein_name"] = "Sulfotransferase-like protein"
        row["keywords"] = ["Transferase"]
        d = disambiguate_row(row)
        self.assertEqual(d.get("decision"), "hold")

    def test_glutathione_s_transferase_routes_on_family_and_conjugation(self) -> None:
        row = _row(ec=["2.5.1.18"])
        row["protein_name"] = "Glutathione S-transferase P"
        row["keywords"] = ["Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GST001",
                "reaction": "RX + glutathione = an S-substituted glutathione + a halide anion + H(+)",
                "ec_number": "2.5.1.18",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d.get("fingerprint_id"), "glutathione_s_transferase")

    def test_glutathione_reductase_not_pulled_into_gst(self) -> None:
        # Glutathione reductase (EC 1.8.1.7) is a flavin disulfide reductase, off-scope for
        # the GST EC 2.5.1.18 and boundary-guarded; it must not route to glutathione_s_transferase.
        row = _row(ec=["1.8.1.7"])
        row["protein_name"] = "Glutathione reductase"
        row["keywords"] = ["Oxidoreductase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GR001",
                "reaction": "2 glutathione + NADP(+) = glutathione disulfide + NADPH + H(+)",
                "ec_number": "1.8.1.7",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "glutathione_s_transferase")

    def test_glutathione_peroxidase_routes_to_peroxiredoxin_not_gst(self) -> None:
        # A glutathione peroxidase (EC 1.11.1) is a thiol/selenol peroxidase, not a GST; its EC
        # scope keeps it out of the GST rule and routes it to peroxiredoxin_thiol_peroxidase.
        row = _row(ec=["1.11.1.9"])
        row["protein_name"] = "Glutathione peroxidase 1"
        row["keywords"] = ["Selenocysteine"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GPX001",
                "reaction": "2 glutathione + H2O2 = glutathione disulfide + 2 H2O",
                "ec_number": "1.11.1.9",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "glutathione_s_transferase")

    def test_aminoacyl_trna_synthetase_routes_on_family_and_aminoacylation(self) -> None:
        row = _row(ec=["6.1.1.3"])
        row["protein_name"] = "Threonine--tRNA ligase"
        row["keywords"] = ["Ligase", "Aminoacyl-tRNA synthetase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AARS001",
                "reaction": (
                    "tRNA(Thr) + L-threonine + ATP = L-threonyl-tRNA(Thr) + AMP + "
                    "diphosphate + H(+)"
                ),
                "ec_number": "6.1.1.3",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d.get("fingerprint_id"), "aminoacyl_trna_synthetase")

    def test_atp_amide_ligase_not_pulled_into_aars(self) -> None:
        # Glutamine synthetase (EC 6.3.1.2) shares the ATP-adenylation step but is off-scope
        # for the aaRS EC 6.1.1; it must route to the generic atp_amide_ligase, not aaRS.
        row = _row(ec=["6.3.1.2"])
        row["protein_name"] = "Glutamine synthetase"
        row["keywords"] = ["Ligase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GLN001",
                "reaction": "L-glutamate + NH4(+) + ATP = L-glutamine + ADP + phosphate + H(+)",
                "ec_number": "6.3.1.2",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "aminoacyl_trna_synthetase")

    def test_trna_methyltransferase_not_pulled_into_aars(self) -> None:
        row = _row(ec=["2.1.1.31"])
        row["protein_name"] = "tRNA (guanine-N(7))-methyltransferase"
        row["keywords"] = ["Methyltransferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:TRM001",
                "reaction": (
                    "guanosine in tRNA + S-adenosyl-L-methionine = N(7)-methylguanosine in "
                    "tRNA + S-adenosyl-L-homocysteine"
                ),
                "ec_number": "2.1.1.31",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "aminoacyl_trna_synthetase")

    def test_acid_coa_ligase_routes_on_family_and_acyl_adenylate(self) -> None:
        row = _row(ec=["6.2.1.3"])
        row["protein_name"] = "Long-chain-fatty-acid--CoA ligase 1"
        row["keywords"] = ["Ligase", "Fatty acid metabolism"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:ACS001",
                "reaction": (
                    "a long-chain fatty acid + ATP + CoA = a long-chain acyl-CoA + AMP + "
                    "diphosphate"
                ),
                "ec_number": "6.2.1.3",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d.get("fingerprint_id"), "acid_coa_ligase")

    def test_adp_forming_succinyl_coa_ligase_not_pulled_into_acid_coa_ligase(self) -> None:
        # An ADP-forming succinate--CoA ligase (EC 6.2.1.5) has a CoA-ligase name and EC scope,
        # but its reaction releases ADP + phosphate (substrate-level phosphorylation), NOT AMP, so
        # the acyl-adenylate reaction anchor is absent: it must NOT route to acid_coa_ligase.
        row = _row(ec=["6.2.1.5"])
        row["protein_name"] = "Succinate--CoA ligase [ADP-forming] subunit beta"
        row["keywords"] = ["Ligase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:SUCC001",
                "reaction": "ATP + succinate + CoA = ADP + phosphate + succinyl-CoA",
                "ec_number": "6.2.1.5",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "acid_coa_ligase")

    def test_coa_transferase_not_pulled_into_acid_coa_ligase(self) -> None:
        # A CoA acyltransferase (EC 2.3.1) forms a CoA thioester but releases no AMP and is
        # off-scope for EC 6.2.1; it must route to coa_acyltransferase, not acid_coa_ligase.
        row = _row(ec=["2.3.1.7"])
        row["protein_name"] = "Carnitine O-acetyltransferase"
        row["keywords"] = ["Transferase", "Acyltransferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:COAT001",
                "reaction": "acetyl-CoA + carnitine = CoA + O-acetylcarnitine",
                "ec_number": "2.3.1.7",
            }
        ]
        d = disambiguate_row(row)
        self.assertNotEqual(d.get("fingerprint_id"), "acid_coa_ligase")

    def test_glycoside_hydrolase_requires_hydrolysis_and_active_site_handle(self) -> None:
        row = _row(ec=["3.2.1.4"])
        row["protein_name"] = "Endoglucanase"
        row["keywords"] = ["Glycosidase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GH0001",
                "reaction": "cellulose + H2O = cellooligosaccharides",
                "ec_number": "3.2.1.4",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 200,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "glycoside_hydrolase")
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "domain_or_family_profile",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "active_site_motif_or_residue_role",
            d["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            d["corroboration"]["distinct_corroborator_axes"],
        )

    def test_tier2_requires_three_independent_mechanism_axes(self) -> None:
        row = _row(cofactors=["heme b"], ec=["1.11.1.7"])
        d = disambiguate_row(row, source_tier="source_tier_2")
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(d["reason"], "trust_tier_corroboration_insufficient")
        self.assertEqual(d["corroboration"]["required_independent_corroborators"], 3)
        self.assertEqual(
            d["corroboration"]["distinct_corroborator_axes"],
            ["cofactor_or_cosubstrate"],
        )

    def test_tier2_admits_only_when_three_mechanism_axes_present(self) -> None:
        row = _row(ec=["3.2.1.4"])
        row["protein_name"] = "Endoglucanase"
        row["keywords"] = ["Glycosidase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GH0001",
                "reaction": "cellulose + H2O = cellooligosaccharides",
                "ec_number": "3.2.1.4",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 200,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row, source_tier="source_tier_2")
        self.assertEqual(d["fingerprint_id"], "glycoside_hydrolase")
        self.assertEqual(d["corroboration"]["source_tier"], "source_tier_2")
        self.assertEqual(d["corroboration"]["distinct_corroborator_count"], 3)

    def test_glycoside_hydrolase_ec_keyword_only_control_held(self) -> None:
        row = _row(ec=["3.2.1.4"])
        row["protein_name"] = "Endoglucanase"
        row["keywords"] = ["Glycosidase"]
        d = disambiguate_row(row)
        self.assertEqual(d["decision"], "hold")

    def test_glycoside_hydrolase_boundary_controls_held(self) -> None:
        transferase = _row(ec=["3.2.1.4", "2.4.1.1"])
        transferase["protein_name"] = "Transglycosylase boundary enzyme"
        transferase["keywords"] = ["Glycosidase"]
        transferase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GH0002",
                "reaction": "cellulose + H2O = cellooligosaccharides",
                "ec_number": "3.2.1.4",
            }
        ]
        transferase["residue_locators"] = [
            {
                "position": 201,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        self.assertEqual(disambiguate_row(transferase)["decision"], "hold")

        phosphorylase = _row(ec=["3.2.1.4"])
        phosphorylase["protein_name"] = "Cellobiose phosphorylase"
        phosphorylase["keywords"] = ["Glycosidase"]
        phosphorylase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GH0003",
                "reaction": "cellobiose + phosphate = alpha-D-glucose 1-phosphate + D-glucose",
                "ec_number": "3.2.1.4",
            }
        ]
        phosphorylase["residue_locators"] = transferase["residue_locators"]
        self.assertEqual(disambiguate_row(phosphorylase)["decision"], "hold")

        non_scope = _row(ec=["3.1.1.1"])
        non_scope["protein_name"] = "Glycosidase-like esterase"
        non_scope["keywords"] = ["Glycosidase"]
        non_scope["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GH0004",
                "reaction": "glycoside + H2O = sugar + alcohol",
                "ec_number": "3.1.1.1",
            }
        ]
        non_scope["residue_locators"] = transferase["residue_locators"]
        self.assertEqual(disambiguate_row(non_scope)["decision"], "hold")

    def test_n_ribosyl_hydrolase_requires_non_ec_mechanism_handles(self) -> None:
        row = _row(ec=["3.2.2.2"])
        row["protein_name"] = "Nucleoside hydrolase"
        row["keywords"] = ["Hydrolase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:NRH0001",
                "reaction": "inosine + H2O = D-ribose + hypoxanthine",
                "ec_number": "3.2.2.2",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 14,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic aspartate acid/base",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        decision = disambiguate_row(row)
        self.assertEqual(decision["fingerprint_id"], "n_ribosyl_hydrolase")
        axes = decision["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("domain_or_family_profile", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_n_ribosyl_hydrolase_boundary_controls_hold(self) -> None:
        ec_only = _row(ec=["3.2.2.2"])
        ec_only["protein_name"] = "Nucleoside hydrolase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        phosphorylase_side = _row(ec=["3.2.2.2", "2.4.2.1"])
        phosphorylase_side["protein_name"] = "Nucleoside phosphorylase"
        phosphorylase_side["keywords"] = ["Transferase"]
        phosphorylase_side["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:NRH0002",
                "reaction": "inosine + phosphate = alpha-D-ribose 1-phosphate + hypoxanthine",
                "ec_number": "2.4.2.1",
            }
        ]
        self.assertEqual(disambiguate_row(phosphorylase_side)["decision"], "hold")

        phosphorylase_family_boundary = _row(ec=["3.2.2.2"])
        phosphorylase_family_boundary["protein_name"] = (
            "Nucleoside hydrolase phosphorylase boundary"
        )
        phosphorylase_family_boundary["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:NRH0005",
                "reaction": "inosine + H2O = D-ribose + hypoxanthine",
                "ec_number": "3.2.2.2",
            }
        ]
        self.assertEqual(
            disambiguate_row(phosphorylase_family_boundary)["decision"], "hold"
        )

        o_glycoside_boundary = _row(ec=["3.2.2.2"])
        o_glycoside_boundary["protein_name"] = "Nucleoside hydrolase glycosidase boundary"
        o_glycoside_boundary["keywords"] = ["Glycosidase"]
        o_glycoside_boundary["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:NRH0003",
                "reaction": "uridine + H2O = D-ribose + uracil",
                "ec_number": "3.2.2.2",
            }
        ]
        self.assertEqual(disambiguate_row(o_glycoside_boundary)["decision"], "hold")

        kinase_boundary = _row(ec=["3.2.2.2", "2.7.1.1"])
        kinase_boundary["protein_name"] = "Nucleoside hydrolase kinase boundary"
        kinase_boundary["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:NRH0004",
                "reaction": "adenosine + H2O = D-ribose + adenine",
                "ec_number": "3.2.2.2",
            }
        ]
        self.assertEqual(disambiguate_row(kinase_boundary)["decision"], "hold")

    def test_metal_independent_phosphodiesterase_requires_non_ec_mechanism_handles(self) -> None:
        row = _row(ec=["3.1.4.17"])
        row["protein_name"] = "Cyclic nucleotide phosphodiesterase"
        row["keywords"] = ["Hydrolase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PDE0001",
                "reaction": "3',5'-cyclic AMP + H2O = AMP + H(+)",
                "ec_number": "3.1.4.17",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 77,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic histidine general acid/base",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        decision = disambiguate_row(row)
        self.assertEqual(
            decision["fingerprint_id"],
            "metal_independent_phosphodiesterase",
        )
        axes = decision["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("domain_or_family_profile", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertNotIn("cofactor_or_cosubstrate", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_metal_independent_phosphodiesterase_accepts_phospholipase_d_split(self) -> None:
        row = _row(ec=["3.1.4.4"])
        row["protein_name"] = "Phospholipase D"
        row["keywords"] = ["Hydrolase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PDEPLD1",
                "reaction": (
                    "a 1,2-diacyl-sn-glycero-3-phosphocholine + H2O = "
                    "a 1,2-diacyl-sn-glycero-3-phosphate + choline + H(+)"
                ),
                "ec_number": "3.1.4.4",
            }
        ]
        decision = disambiguate_row(row)
        self.assertEqual(
            decision["fingerprint_id"],
            "metal_independent_phosphodiesterase",
        )
        axes = decision["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("domain_or_family_profile", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_metal_independent_phosphodiesterase_boundary_controls_hold(self) -> None:
        ec_only = _row(ec=["3.1.4.17"])
        ec_only["protein_name"] = "Cyclic nucleotide phosphodiesterase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        metal_dependent = _row(cofactors=["Mg(2+)"], ec=["3.1.4.17"])
        metal_dependent["protein_name"] = "Cyclic nucleotide phosphodiesterase"
        metal_dependent["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PDE0002",
                "reaction": "3',5'-cyclic GMP + H2O = GMP + H(+)",
                "ec_number": "3.1.4.17",
            }
        ]
        metal_decision = disambiguate_row(metal_dependent)
        self.assertNotEqual(
            metal_decision.get("fingerprint_id"),
            "metal_independent_phosphodiesterase",
        )

        phosphomonoesterase = _row(ec=["3.1.3.1"])
        phosphomonoesterase["protein_name"] = "Cyclic nucleotide phosphatase"
        phosphomonoesterase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PDE0003",
                "reaction": "phosphomonoester + H2O = alcohol + phosphate",
                "ec_number": "3.1.3.1",
            }
        ]
        self.assertEqual(disambiguate_row(phosphomonoesterase)["decision"], "hold")

        phosphatase_family_boundary = _row(ec=["3.1.4.17"])
        phosphatase_family_boundary["protein_name"] = (
            "Cyclic nucleotide phosphodiesterase phosphatase boundary"
        )
        phosphatase_family_boundary["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PDE0005",
                "reaction": "3',5'-cyclic AMP + H2O = AMP + H(+)",
                "ec_number": "3.1.4.17",
            }
        ]
        self.assertEqual(
            disambiguate_row(phosphatase_family_boundary)["decision"], "hold"
        )

        lyase = _row(ec=["4.6.1.1"])
        lyase["protein_name"] = "Adenylate cyclase"
        lyase["keywords"] = ["Lyase"]
        lyase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PDE0004",
                "reaction": "ATP = 3',5'-cyclic AMP + diphosphate",
                "ec_number": "4.6.1.1",
            }
        ]
        self.assertEqual(disambiguate_row(lyase)["decision"], "hold")

        phospholipase_c_boundary = _row(ec=["3.1.4.11"])
        phospholipase_c_boundary["protein_name"] = "Phospholipase C"
        phospholipase_c_boundary["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PDEPLC1",
                "reaction": "phosphatidylcholine + H2O = choline + phosphatidate + H(+)",
                "ec_number": "3.1.4.11",
            }
        ]
        self.assertEqual(
            disambiguate_row(phospholipase_c_boundary)["decision"], "hold"
        )

    def test_glycosyltransferase_not_collapsed_to_glycoside_hydrolase(self) -> None:
        row = _row(ec=["2.4.1.1"])
        row["protein_name"] = "Glycosyltransferase"
        row["keywords"] = ["Glycosyltransferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GT0001",
                "reaction": "UDP-glucose + acceptor = UDP + glycosylated acceptor",
                "ec_number": "2.4.1.1",
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "glycosyltransferase")

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

    def test_mn_fe_superoxide_dismutase_requires_mechanism_handles(self) -> None:
        row = _row(cofactors=["Manganese"], ec=["1.15.1.1"])
        row["protein_name"] = "Superoxide dismutase [Mn]"
        row["keywords"] = ["Superoxide dismutase", "Metal-binding"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:20696",
                "reaction": "2 superoxide + 2 H(+) = H2O2 + O2",
                "ec_number": "1.15.1.1",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 27,
                "feature_code": "METAL",
                "feature_type": "Metal binding",
                "ligand_name": "Manganese",
                "ligand_id": None,
                "description": "Manganese",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "manganese_iron_superoxide_dismutase")
        axes = d["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_mn_fe_superoxide_dismutase_controls_hold(self) -> None:
        ec_only = _row(ec=["1.15.1.1"])
        ec_only["protein_name"] = "Superoxide dismutase [Mn]"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        base_reaction = {
            "rhea_id": "RHEA:20696",
            "reaction": "2 superoxide + 2 H(+) = H2O2 + O2",
            "ec_number": "1.15.1.1",
        }
        hold_cases = (
            (["Copper", "Zinc"], ["Superoxide dismutase"], "Superoxide dismutase [Cu-Zn]", ["1.15.1.1"]),
            (["heme b"], ["Superoxide dismutase"], "Peroxidase-like superoxide dismutase", ["1.15.1.1"]),
            (["Iron"], ["Superoxide dismutase"], "Superoxide reductase", ["1.15.1.1"]),
            (["Iron"], ["Superoxide dismutase"], "Superoxide dismutase [Fe]", ["1.15.1.1", "1.11.1.7"]),
        )
        for cofactors, keywords, name, ec_numbers in hold_cases:
            row = _row(cofactors=cofactors, ec=ec_numbers)
            row["protein_name"] = name
            row["keywords"] = keywords
            row["rhea_ec_provenance"]["rhea_records"] = [base_reaction]
            row["residue_locators"] = [
                {
                    "position": 27,
                    "feature_code": "METAL",
                    "feature_type": "Metal binding",
                    "ligand_name": cofactors[0],
                    "ligand_id": None,
                    "description": cofactors[0],
                    "evidence_codes": ["ECO:0000269"],
                }
            ]
            self.assertEqual(disambiguate_row(row)["decision"], "hold")

        missing_site = _row(cofactors=["Iron"], ec=["1.15.1.1"])
        missing_site["protein_name"] = "Superoxide dismutase [Fe]"
        missing_site["keywords"] = ["Superoxide dismutase"]
        missing_site["rhea_ec_provenance"]["rhea_records"] = [base_reaction]
        self.assertEqual(disambiguate_row(missing_site)["decision"], "hold")

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

    def test_pfka_phosphofructokinase_requires_mechanism_handles(self) -> None:
        row = _row(ec=["2.7.1.11"])
        row["protein_name"] = "ATP-dependent 6-phosphofructokinase (Phosphohexokinase)"
        row["keywords"] = ["Kinase", "Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PF0001",
                "reaction": "beta-D-fructose 6-phosphate + ATP = beta-D-fructose 1,6-bisphosphate + ADP + H(+)",
                "ec_number": "2.7.1.11",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 145,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "ATP",
                "ligand_id": None,
                "description": "ATP",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        d = disambiguate_row(row)
        self.assertEqual(d["fingerprint_id"], "pfka_phosphofructokinase")
        axes = d["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_pfka_phosphofructokinase_controls_hold(self) -> None:
        ec_only = _row(ec=["2.7.1.11"])
        ec_only["protein_name"] = "ATP-dependent 6-phosphofructokinase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        hold_cases = (
            (["2.7.1.11", "2.7.11.1"], "6-phosphofructokinase protein kinase boundary"),
            (["2.7.1.11", "2.7.13.3"], "6-phosphofructokinase histidine kinase boundary"),
            (["2.7.1.11", "3.1.1.1"], "6-phosphofructokinase hydrolase boundary"),
            (["2.7.1.21"], "Thymidine kinase"),
        )
        for ec_numbers, name in hold_cases:
            row = _row(ec=ec_numbers)
            row["protein_name"] = name
            row["keywords"] = ["Kinase", "Transferase"]
            row["rhea_ec_provenance"]["rhea_records"] = [
                {
                    "rhea_id": "RHEA:PF0002",
                    "reaction": "beta-D-fructose 6-phosphate + ATP = beta-D-fructose 1,6-bisphosphate + ADP + H(+)",
                    "ec_number": ec_numbers[0],
                }
            ]
            row["residue_locators"] = [
                {
                    "position": 145,
                    "feature_code": "BINDING",
                    "feature_type": "Binding site",
                    "ligand_name": "ATP",
                    "ligand_id": None,
                    "description": "ATP",
                    "evidence_codes": ["ECO:0000269"],
                }
            ]
            self.assertEqual(disambiguate_row(row)["decision"], "hold")

        off_target_cases = (
            (["2.7.1.1"], "Hexokinase", "askha_sugar_acetate_kinase"),
            (["2.7.1.36"], "Mevalonate kinase", "ghmp_small_molecule_kinase"),
            (["2.7.1.56"], "1-phosphofructokinase ribokinase-family boundary", "pfkb_ribokinase_family"),
        )
        for ec_numbers, name, expected_fp in off_target_cases:
            row = _row(ec=ec_numbers)
            row["protein_name"] = name
            row["keywords"] = ["Kinase", "Transferase"]
            reaction = (
                "ATP + D-fructose 1-phosphate = ADP + D-fructose 1,6-bisphosphate + H(+)"
                if expected_fp == "pfkb_ribokinase_family"
                else "beta-D-fructose 6-phosphate + ATP = beta-D-fructose 1,6-bisphosphate + ADP + H(+)"
            )
            row["rhea_ec_provenance"]["rhea_records"] = [
                {
                    "rhea_id": "RHEA:PF0002",
                    "reaction": reaction,
                    "ec_number": ec_numbers[0],
                }
            ]
            row["residue_locators"] = [
                {
                    "position": 145,
                    "feature_code": "BINDING",
                    "feature_type": "Binding site",
                    "ligand_name": "ATP",
                    "ligand_id": None,
                    "description": "ATP",
                    "evidence_codes": ["ECO:0000269"],
                }
            ]
            decision = disambiguate_row(row)
            self.assertEqual(decision["fingerprint_id"], expected_fp)
            self.assertNotEqual(decision["fingerprint_id"], "pfka_phosphofructokinase")

        ndk_side = _row(ec=["2.7.1.11", "2.7.4.6"])
        ndk_side["protein_name"] = "Nucleoside diphosphate kinase"
        ndk_side["keywords"] = ["Kinase", "Transferase"]
        ndk_side["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PF0003",
                "reaction": "ATP + nucleoside diphosphate = ADP + nucleoside triphosphate",
                "ec_number": "2.7.4.6",
            }
        ]
        ndk_side["residue_locators"] = [
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
        ndk_decision = disambiguate_row(ndk_side)
        self.assertEqual(ndk_decision["fingerprint_id"], "nucleoside_diphosphate_kinase")
        self.assertNotEqual(ndk_decision["fingerprint_id"], "pfka_phosphofructokinase")

    def test_pfkb_ribokinase_family_requires_mechanism_handles(self) -> None:
        row = _row(ec=["2.7.1.15"])
        row["protein_name"] = "Ribokinase"
        row["keywords"] = ["Kinase", "Transferase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:RB0001",
                "reaction": "ATP + D-ribose = ADP + D-ribose 5-phosphate + H(+)",
                "ec_number": "2.7.1.15",
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
        self.assertEqual(d["fingerprint_id"], "pfkb_ribokinase_family")
        axes = d["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_pfkb_ribokinase_family_controls_hold(self) -> None:
        ec_only = _row(ec=["2.7.1.15"])
        ec_only["protein_name"] = "Ribokinase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        hold_cases = (
            (["2.7.1.15", "2.7.11.1"], "Ribokinase protein kinase boundary"),
            (["2.7.1.15", "2.7.13.3"], "Ribokinase histidine kinase boundary"),
            (["2.7.1.15", "3.1.1.1"], "Ribokinase hydrolase boundary"),
            (["2.7.1.11"], "ATP-dependent 6-phosphofructokinase"),
            (["2.7.1.21"], "Thymidine kinase"),
        )
        for ec_numbers, name in hold_cases:
            row = _row(ec=ec_numbers)
            row["protein_name"] = name
            row["keywords"] = ["Kinase", "Transferase"]
            row["rhea_ec_provenance"]["rhea_records"] = [
                {
                    "rhea_id": "RHEA:RB0002",
                    "reaction": "ATP + D-ribose = ADP + D-ribose 5-phosphate + H(+)",
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

        off_target_cases = (
            (["2.7.1.1"], "Hexokinase", "ATP + D-glucose = ADP + D-glucose 6-phosphate + H(+)", "askha_sugar_acetate_kinase"),
            (["2.7.1.36"], "Mevalonate kinase", "ATP + (R)-mevalonate = ADP + (R)-5-phosphomevalonate + H(+)", "ghmp_small_molecule_kinase"),
            (["2.7.1.11"], "ATP-dependent 6-phosphofructokinase", "ATP + D-fructose 6-phosphate = ADP + D-fructose 1,6-bisphosphate + H(+)", "pfka_phosphofructokinase"),
        )
        for ec_numbers, name, reaction, expected_fp in off_target_cases:
            row = _row(ec=ec_numbers)
            row["protein_name"] = name
            row["keywords"] = ["Kinase", "Transferase"]
            row["rhea_ec_provenance"]["rhea_records"] = [
                {"rhea_id": "RHEA:RB0003", "reaction": reaction, "ec_number": ec_numbers[0]}
            ]
            row["residue_locators"] = [
                {
                    "position": 145,
                    "feature_code": "BINDING",
                    "feature_type": "Binding site",
                    "ligand_name": "ATP",
                    "ligand_id": None,
                    "description": "ATP",
                    "evidence_codes": ["ECO:0000269"],
                }
            ]
            decision = disambiguate_row(row)
            self.assertEqual(decision["fingerprint_id"], expected_fp)
            self.assertNotEqual(decision["fingerprint_id"], "pfkb_ribokinase_family")

    def test_terpene_cyclase_requires_non_ec_mechanism_handles(self) -> None:
        row = _row(ec=["4.2.3.10"])
        row["protein_name"] = "Germacrene synthase"
        row["keywords"] = ["Terpene biosynthesis"]
        row["cofactor_provenance"] = [{"name": "magnesium"}]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:TP0001",
                "reaction": "farnesyl diphosphate = germacrene A + diphosphate",
                "ec_number": "4.2.3.10",
            }
        ]
        decision = disambiguate_row(row)
        self.assertEqual(decision["fingerprint_id"], "terpene_cyclase_synthase")
        self.assertIn(
            "cofactor_or_cosubstrate",
            decision["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertIn(
            "rhea_reaction_or_participant_pattern",
            decision["corroboration"]["distinct_corroborator_axes"],
        )
        self.assertNotIn(
            "ec_scope_hint",
            decision["corroboration"]["distinct_corroborator_axes"],
        )

    def test_terpene_cyclase_active_site_fallback_remains_mechanism_only(self) -> None:
        row = _row(ec=["4.2.3.20"])
        row["protein_name"] = "Copalyl diphosphate synthase"
        row["keywords"] = ["Terpene biosynthesis"]
        row["residue_locators"] = [
            {
                "position": 312,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "magnesium",
                "ligand_id": "ChEBI:CHEBI:18420",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        decision = disambiguate_row(row)
        self.assertEqual(decision["fingerprint_id"], "terpene_cyclase_synthase")
        self.assertIn(
            "active_site_motif_or_residue_role",
            decision["corroboration"]["distinct_corroborator_axes"],
        )

    def test_terpene_ec_only_and_boundary_controls_hold(self) -> None:
        ec_only = _row(ec=["4.2.3.10"])
        ec_only["protein_name"] = "Uncharacterized EC 4.2.3 enzyme"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        prenyltransferase = _row(ec=["4.2.3.10", "2.5.1.1"])
        prenyltransferase["protein_name"] = "Prenyltransferase-like terpene enzyme"
        prenyltransferase["keywords"] = ["Terpene biosynthesis"]
        prenyltransferase["cofactor_provenance"] = [{"name": "magnesium"}]
        prenyltransferase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:PT0001",
                "reaction": "geranyl diphosphate + isopentenyl diphosphate = farnesyl diphosphate + diphosphate",
                "ec_number": "2.5.1.1",
            }
        ]
        self.assertEqual(disambiguate_row(prenyltransferase)["decision"], "hold")

        hydratase = _row(ec=["4.2.3.10"])
        hydratase["protein_name"] = "Generic hydratase"
        hydratase["keywords"] = ["Hydratase"]
        hydratase["cofactor_provenance"] = [{"name": "magnesium"}]
        hydratase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:HY0001",
                "reaction": "substrate + H2O = product",
                "ec_number": "4.2.3.10",
            }
        ]
        self.assertEqual(disambiguate_row(hydratase)["decision"], "hold")

    def test_had_like_phosphatase_requires_non_ec_mechanism_handles(self) -> None:
        row = _row(cofactors=["Mg(2+)"], ec=["3.1.3.3"])
        row["protein_name"] = "HAD-like phosphoserine phosphatase"
        row["keywords"] = ["Phosphatase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:HP0001",
                "reaction": "O-phospho-L-serine + H2O = L-serine + phosphate",
                "ec_number": "3.1.3.3",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 11,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic Asp nucleophile",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        decision = disambiguate_row(row)
        self.assertEqual(decision["fingerprint_id"], "had_like_phosphatase")
        axes = decision["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_had_like_phosphatase_controls_do_not_force_had_label(self) -> None:
        ec_only = _row(ec=["3.1.3.3"])
        ec_only["protein_name"] = "HAD-like phosphatase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        metal_without_had = _row(cofactors=["Zn(2+)"], ec=["3.1.3.1"])
        metal_without_had["protein_name"] = "Alkaline phosphatase"
        self.assertEqual(
            disambiguate_row(metal_without_had)["fingerprint_id"],
            "metallophosphomonoesterase",
        )

        phosphodiesterase = _row(cofactors=["Mg(2+)"], ec=["3.1.3.1", "3.1.4.1"])
        phosphodiesterase["protein_name"] = "HAD-like phosphodiesterase boundary"
        phosphodiesterase["keywords"] = ["Phosphatase"]
        phosphodiesterase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:HP0003",
                "reaction": "phosphomonoester + H2O = alcohol + phosphate",
                "ec_number": "3.1.3.1",
            }
        ]
        phosphodiesterase["residue_locators"] = [
            {
                "position": 11,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "Mg(2+)",
                "ligand_id": None,
                "description": "Mg(2+) binding",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        self.assertEqual(
            disambiguate_row(phosphodiesterase)["fingerprint_id"],
            "metallophosphoesterase_nuclease",
        )

    def test_ser_thr_protein_phosphatase_requires_protein_substrate_and_metal(self) -> None:
        row = _row(cofactors=["Mn(2+)"], ec=["3.1.3.16"])
        row["protein_name"] = "Serine/threonine-protein phosphatase"
        row["keywords"] = ["Phosphoprotein", "Phosphatase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:STP0001",
                "reaction": "phosphoprotein + H2O = protein + phosphate",
                "ec_number": "3.1.3.16",
            }
        ]
        decision = disambiguate_row(row)
        self.assertEqual(decision["fingerprint_id"], "ser_thr_protein_phosphatase")
        axes = decision["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_ser_thr_protein_phosphatase_accepts_seryl_protein_rhea_form(self) -> None:
        row = _row(cofactors=["Mn(2+)"], ec=["3.1.3.16"])
        row["protein_name"] = "Serine/threonine-protein phosphatase PP1-alpha catalytic subunit"
        row["keywords"] = ["Protein phosphatase", "Phosphoprotein"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:STP0002",
                "equation": "O-phospho-L-seryl-[protein] + H2O = L-seryl-[protein] + phosphate",
                "ec_number": "3.1.3.16",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 64,
                "feature_code": "BINDING",
                "feature_type": "Binding site",
                "ligand_name": "Mn(2+)",
                "ligand_id": None,
                "description": "Mn(2+) binding",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        decision = disambiguate_row(row)
        self.assertEqual(decision["fingerprint_id"], "ser_thr_protein_phosphatase")
        axes = decision["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_ser_thr_protein_phosphatase_controls_hold(self) -> None:
        ec_only = _row(ec=["3.1.3.16"])
        ec_only["protein_name"] = "Serine/threonine-protein phosphatase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        no_metal = _row(ec=["3.1.3.16"])
        no_metal["protein_name"] = "Serine/threonine-protein phosphatase"
        no_metal["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:STP0002",
                "reaction": "phosphoprotein + H2O = protein + phosphate",
                "ec_number": "3.1.3.16",
            }
        ]
        self.assertEqual(disambiguate_row(no_metal)["decision"], "hold")

        cys_ptp = _row(ec=["3.1.3.48"])
        cys_ptp["protein_name"] = "Protein-tyrosine phosphatase PTP1B"
        cys_ptp["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:STP0003",
                "reaction": "phosphoprotein + H2O = protein + phosphate",
                "ec_number": "3.1.3.48",
            }
        ]
        cys_ptp["residue_locators"] = [
            {
                "position": 215,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic Cys nucleophile",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        self.assertEqual(disambiguate_row(cys_ptp)["decision"], "hold")

        alkaline = _row(cofactors=["Zn(2+)"], ec=["3.1.3.1"])
        alkaline["protein_name"] = "Alkaline phosphatase"
        self.assertEqual(
            disambiguate_row(alkaline)["fingerprint_id"],
            "metallophosphomonoesterase",
        )

    def test_aldehyde_dehydrogenase_requires_non_ec_mechanism_handles(self) -> None:
        row = _row(ec=["1.2.1.3"])
        row["protein_name"] = "Aldehyde dehydrogenase"
        row["keywords"] = ["NAD"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AD0001",
                "reaction": "an aldehyde + NAD(+) + H2O = a carboxylate + NADH + H(+)",
                "ec_number": "1.2.1.3",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 302,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic cysteine nucleophile",
                "evidence_codes": ["ECO:0000269"],
            },
            {
                "position": 268,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic glutamate base",
                "evidence_codes": ["ECO:0000269"],
            },
        ]
        decision = disambiguate_row(row)
        self.assertEqual(decision["fingerprint_id"], "aldehyde_dehydrogenase")
        axes = decision["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_aldehyde_dehydrogenase_boundary_controls_hold(self) -> None:
        ec_only = _row(ec=["1.2.1.3"])
        ec_only["protein_name"] = "Aldehyde dehydrogenase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        no_site = _row(ec=["1.2.1.3"])
        no_site["protein_name"] = "Aldehyde dehydrogenase"
        no_site["keywords"] = ["NAD"]
        no_site["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AD0004",
                "reaction": "an aldehyde + NAD(+) + H2O = a carboxylate + NADH + H(+)",
                "ec_number": "1.2.1.3",
            }
        ]
        no_site_decision = disambiguate_row(no_site)
        self.assertEqual(no_site_decision["fingerprint_id"], "aldehyde_dehydrogenase")
        self.assertNotIn(
            "active_site_motif_or_residue_role",
            no_site_decision["corroboration"]["distinct_corroborator_axes"],
        )

        generic_nad = _row(ec=["1.2.1.3"])
        generic_nad["keywords"] = ["NAD"]
        generic_nad["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AD0002",
                "reaction": "an aldehyde + NAD(+) + H2O = a carboxylate + NADH + H(+)",
                "ec_number": "1.2.1.3",
            }
        ]
        self.assertEqual(disambiguate_row(generic_nad)["decision"], "hold")

        flavin_oxidase = _row(cofactors=["FAD"], ec=["1.2.3.1"])
        flavin_oxidase["protein_name"] = "Aldehyde oxidase"
        flavin_oxidase["keywords"] = ["Flavoprotein"]
        flavin_oxidase["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:AD0003",
                "reaction": "an aldehyde + O2 + H2O = a carboxylate + H2O2",
                "ec_number": "1.2.3.1",
            }
        ]
        self.assertEqual(disambiguate_row(flavin_oxidase)["decision"], "hold")

    def test_alpha_beta_hydrolase_requires_non_ec_mechanism_handles(self) -> None:
        row = _row(ec=["3.1.1.1"])
        row["protein_name"] = "Alpha/beta hydrolase esterase"
        row["keywords"] = ["Esterase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:ABH0001",
                "reaction": "a carboxylic ester + H2O = an alcohol + a carboxylate",
                "ec_number": "3.1.1.1",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 105,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic serine nucleophile",
                "evidence_codes": ["ECO:0000269"],
            },
            {
                "position": 230,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic histidine base",
                "evidence_codes": ["ECO:0000269"],
            },
            {
                "position": 255,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic aspartate acid",
                "evidence_codes": ["ECO:0000269"],
            },
        ]
        decision = disambiguate_row(row)
        self.assertEqual(
            decision["fingerprint_id"],
            "alpha_beta_hydrolase_esterase_lipase",
        )
        axes = decision["corroboration"]["distinct_corroborator_axes"]
        self.assertIn("domain_or_family_profile", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_alpha_beta_hydrolase_boundary_controls_hold(self) -> None:
        ec_only = _row(ec=["3.1.1.1"])
        ec_only["protein_name"] = "Alpha/beta hydrolase esterase"
        self.assertEqual(disambiguate_row(ec_only)["decision"], "hold")

        protease_side_ec = _row(ec=["3.1.1.1", "3.4.21.1"])
        protease_side_ec["protein_name"] = "Serine protease esterase boundary"
        protease_side_ec["keywords"] = ["Esterase"]
        protease_side_ec["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:ABH0002",
                "reaction": "a carboxylic ester + H2O = an alcohol + a carboxylate",
                "ec_number": "3.1.1.1",
            }
        ]
        protease_side_ec["residue_locators"] = [
            {
                "position": 105,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "description": "Catalytic Ser-His-Asp triad",
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        self.assertEqual(disambiguate_row(protease_side_ec)["decision"], "hold")

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

    def test_requested_source_tier_is_recorded_on_imported_label(self) -> None:
        row = _row(accession="G20001", ec=["3.2.1.4"])
        row["protein_name"] = "Endoglucanase"
        row["keywords"] = ["Glycosidase"]
        row["rhea_ec_provenance"]["rhea_records"] = [
            {
                "rhea_id": "RHEA:GH0001",
                "reaction": "cellulose + H2O = cellooligosaccharides",
                "ec_number": "3.2.1.4",
            }
        ]
        row["residue_locators"] = [
            {
                "position": 200,
                "feature_code": "ACT_SITE",
                "feature_type": "Active site",
                "ligand_name": None,
                "ligand_id": None,
                "evidence_codes": ["ECO:0000269"],
            }
        ]
        audit = build_cofactor_ec_disambiguation(
            pools=[{"pool": "tier2_test", "path": "artifacts/tier2.json", "rows": [row]}],
            registry=[],
            index=_empty_index(),
            source_tier="source_tier_2",
        )
        self.assertEqual(audit["counts"]["importable_new_labels"], 1)
        label = audit["applied_labels"][0]
        self.assertEqual(label["evidence"]["source_trust_tier"]["source_tier"], "source_tier_2")
        self.assertEqual(
            len(label["evidence"]["source_trust_tier"]["mechanism_corroborator_axes_present"]),
            3,
        )
        self.assertEqual(label["evidence"]["predictive_evidence"], [])


if __name__ == "__main__":
    unittest.main()
