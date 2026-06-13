"""Offline validation of ThDP broadened-handle sourcing."""

from __future__ import annotations

import unittest

from catalytic_earth.thiamine_diphosphate_sourcing import (
    FAMILIES,
    build_thiamine_diphosphate_sourcing,
)

_ROWS = {
    "TD0001": (
        ["2.2.1.1"],
        ["Thiamine pyrophosphate", "Transferase"],
        ["thiamine diphosphate", "Mg(2+)"],
        "Transketolase",
        "D-xylulose 5-phosphate + D-ribose 5-phosphate = D-glyceraldehyde 3-phosphate + D-sedoheptulose 7-phosphate",
        "Binding site",
        "thiamine diphosphate and magnesium binding",
    ),
    "TD0002": (
        ["4.1.1.1"],
        ["Thiamine pyrophosphate", "Lyase"],
        ["thiamine pyrophosphate", "Mg(2+)"],
        "Pyruvate decarboxylase",
        "2-oxo acid = aldehyde + CO2",
        "Active site",
        "ThDP ylide activation residue",
    ),
    "TD0003": (
        ["1.2.4.1"],
        ["Thiamine pyrophosphate", "Oxidoreductase"],
        ["thiamine diphosphate", "Mg(2+)"],
        "Pyruvate dehydrogenase E1 component",
        "pyruvate + acceptor = acetyl group + CO2 + reduced acceptor",
        "Binding site",
        "thiamine diphosphate binding",
    ),
    # EC + ThDP only: hold because EC/cofactor with no mechanism handle is insufficient.
    "NX0001": (
        ["2.2.1.1"],
        [],
        ["thiamine diphosphate"],
        "Test enzyme",
        "",
        "",
        "",
    ),
    # Boundary rows.
    "PL0001": (
        ["4.1.1.1"],
        ["Thiamine pyrophosphate", "Lyase"],
        ["thiamine diphosphate", "pyridoxal 5'-phosphate"],
        "PLP/ThDP boundary decarboxylase",
        "2-oxo acid = aldehyde + CO2",
        "Binding site",
        "pyridoxal phosphate binding",
    ),
    "FL0001": (
        ["1.2.4.1"],
        ["Thiamine pyrophosphate", "Oxidoreductase"],
        ["thiamine diphosphate", "FAD"],
        "Flavin boundary dehydrogenase",
        "pyruvate + acceptor = acetyl group + CO2 + reduced acceptor",
        "Binding site",
        "thiamine diphosphate binding",
    ),
    "HD0001": (
        ["2.2.1.1", "3.1.1.1"],
        ["Thiamine pyrophosphate"],
        ["thiamine diphosphate"],
        "Dual-function transketolase hydrolase",
        "D-xylulose 5-phosphate + aldehyde = product",
        "Binding site",
        "thiamine diphosphate binding",
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
        "length": 510,
        "sequence": "M" + "A" * 509,
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
            "begin": 210,
            "end": 210,
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
        "sequence_length": 510,
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


class ThiamineDiphosphateSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_thiamine_diphosphate_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T05:20:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            cap_ceiling=150,
            **kwargs,
        )

    def test_family_is_thdp(self):
        self.assertEqual(FAMILIES, ("thiamine_diphosphate_enzyme",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 7)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 3)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 3)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 0)

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"thiamine_diphosphate_enzyme": 3},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "thiamine_diphosphate_enzyme")
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
        self.assertEqual(set(labels), {"uniprot:TD0001", "uniprot:TD0002", "uniprot:TD0003"})
        axes = labels["uniprot:TD0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_boundary_controls_do_not_enter_family(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        for accession in ("NX0001", "PL0001", "FL0001", "HD0001"):
            self.assertNotIn(f"uniprot:{accession}", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["thiamine_diphosphate_enzyme"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "thdp_mg_ylide_carbonyl_substrate_context",
        )
        self.assertEqual(proj["cap_ceiling"], 150)
        self.assertTrue(proj["chemistry_confusable"])
        for label in audit["applied_labels"]:
            seq = label["evidence"]["sequence_provenance"]
            self.assertEqual(seq["sequence_length"], 510)
            self.assertEqual(seq["source"], "reviewed_uniprot")


if __name__ == "__main__":
    unittest.main()
