"""Offline validation of zinc hydro-lyase broadened-handle sourcing."""

from __future__ import annotations

import unittest

from catalytic_earth.zinc_lyase_hydratase_sourcing import (
    FAMILIES,
    build_zinc_lyase_hydratase_sourcing,
)

_ROWS = {
    "ZL0001": (
        ["4.2.1.1"],
        ["Lyase", "Zinc", "Metal-binding"],
        ["Zn(2+)"],
        "Carbonic anhydrase 2",
        "hydrogencarbonate + H(+) = CO2 + H2O",
        "Binding site",
        "Zn(2+) binding site",
    ),
    "ZL0002": (
        ["4.2.1.24"],
        ["Lyase", "Zinc"],
        ["Zn(2+)"],
        "Delta-aminolevulinic acid dehydratase",
        "2 5-aminolevulinate = porphobilinogen + 2 H2O + H(+)",
        "Active site",
        "proton donor/acceptor",
    ),
    "ZL0003": (
        ["4.2.1.109"],
        ["Lyase", "Zinc"],
        ["Zn(2+)"],
        "Methylthioribulose-1-phosphate dehydratase",
        "5-(methylsulfanyl)-D-ribulose 1-phosphate = 5-methylsulfanyl-2,3-dioxopentyl phosphate + H2O",
        "Binding site",
        "Zn(2+) binding site",
    ),
    # EC + lyase text only: hold because EC/name without zinc is insufficient.
    "NX0001": (
        ["4.2.1.1"],
        ["Lyase"],
        [],
        "Carbonic anhydrase-like protein",
        "hydrogencarbonate + H(+) = CO2 + H2O",
        "",
        "",
    ),
    # Boundary rows.
    "PL0001": (
        ["4.2.1.24"],
        ["Lyase", "Zinc"],
        ["Zn(2+)", "pyridoxal 5'-phosphate"],
        "PLP zinc dehydratase boundary",
        "substrate = product + H2O",
        "Binding site",
        "Zn(2+) binding site",
    ),
    "TD0001": (
        ["4.2.1.24"],
        ["Lyase", "Zinc"],
        ["Zn(2+)", "thiamine diphosphate"],
        "ThDP zinc dehydratase boundary",
        "substrate = product + H2O",
        "Binding site",
        "Zn(2+) binding site",
    ),
    "HD0001": (
        ["4.2.1.1", "3.1.1.1"],
        ["Lyase", "Zinc"],
        ["Zn(2+)"],
        "Hydrolase side-activity zinc dehydratase",
        "hydrogencarbonate + H(+) = CO2 + H2O",
        "Binding site",
        "Zn(2+) binding site",
    ),
    "TF0001": (
        ["4.2.1.109"],
        ["Lyase", "Zinc", "Transferase"],
        ["Zn(2+)"],
        "Transferase boundary dehydratase",
        "substrate = product + H2O",
        "Binding site",
        "Zn(2+) binding site",
    ),
    "IS0001": (
        ["4.2.1.109"],
        ["Lyase", "Zinc", "Isomerase"],
        ["Zn(2+)"],
        "Isomerase boundary dehydratase",
        "substrate = product + H2O",
        "Binding site",
        "Zn(2+) binding site",
    ),
}


def _search_record(accession):
    ec, _, _, protein_name, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": protein_name,
        "organism": f"Organism {accession}",
        "length": 310,
        "sequence": "M" + "A" * 309,
        "ec_numbers": ec,
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _feature(feature_type, description):
    if not feature_type:
        return []
    return [
        {
            "feature_type": feature_type,
            "begin": 91,
            "end": 91,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession):
    ec, keywords, cofactors, protein_name, reaction, feature_type, feature_description = _ROWS[
        accession
    ]
    active_features = (
        _feature(feature_type, feature_description) if feature_type == "Active site" else []
    )
    binding_features = (
        _feature(feature_type, feature_description) if feature_type == "Binding site" else []
    )
    catalytic = []
    if reaction:
        catalytic.append(
            {
                "reaction": reaction,
                "ec_number": ec[0],
                "cross_references": [{"database": "Rhea", "id": f"RHEA:{accession}"}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        )
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "protein_name": protein_name,
        "sequence_length": 310,
        "keywords": keywords,
        "active_site_features": active_features,
        "binding_site_features": binding_features,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": catalytic,
        "cofactor_comments": [
            {
                "cofactors": [
                    {
                        "name": name,
                        "cross_reference": {"id": None},
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                    }
                    for name in cofactors
                ]
            }
        ],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size):
    records = [_search_record(a) for a in sorted(_ROWS)]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class ZincLyaseHydrataseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_zinc_lyase_hydratase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T06:20:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            cap_ceiling=150,
            **kwargs,
        )

    def test_family_is_zinc_lyase_hydratase(self):
        self.assertEqual(FAMILIES, ("zinc_lyase_hydratase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 9)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 3)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 5)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 0)

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"zinc_lyase_hydratase": 3},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "zinc_lyase_hydratase")
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            for excluded in ("ec_label", "protein_name", "uniprot_prose", "target_family_lane"):
                self.assertIn(excluded, label["evidence"]["excluded_context"])
            tier = label["evidence"]["source_trust_tier"]
            self.assertEqual(tier["source_tier"], "source_tier_0")
            self.assertTrue(tier["meets_n_of_m"])
            self.assertNotIn("ec_scope_hint", tier["mechanism_corroborator_axes_present"])

    def test_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:ZL0001", "uniprot:ZL0002", "uniprot:ZL0003"})
        axes = labels["uniprot:ZL0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_boundary_controls_do_not_enter_family(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        for accession in ("NX0001", "PL0001", "TD0001", "HD0001", "TF0001", "IS0001"):
            self.assertNotIn(f"uniprot:{accession}", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["zinc_lyase_hydratase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "zinc_water_elimination_addition_context",
        )
        self.assertEqual(proj["cap_ceiling"], 150)
        self.assertTrue(proj["chemistry_confusable"])
        for label in audit["applied_labels"]:
            seq = label["evidence"]["sequence_provenance"]
            self.assertEqual(seq["sequence_length"], 310)
            self.assertEqual(seq["source"], "reviewed_uniprot")


if __name__ == "__main__":
    unittest.main()
