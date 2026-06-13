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
