"""Offline validation of the ser_his hole-sourcing runner.

No network: the UniProt query/entry fetchers and the AlphaFoldDB CIF fetcher are
injected with synthetic payloads, so the full chain (fetch -> stage coordinate ->
triad confirmation -> novelty gate -> preview) is exercised and the routing and
guardrails are asserted.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from catalytic_earth.labels import MechanismLabel
from catalytic_earth.ser_his_hole_sourcing import build_ser_his_hole_sourcing


def _search_record(accession, ec_numbers):
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": "Serine hydrolase test",
        "organism": f"Organism {accession}",
        "length": 300,
        "sequence": "M" + "A" * 299,
        "ec_numbers": ec_numbers,
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _entry_record(accession, *, act_sites, cofactor_names, ec):
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "sequence_length": 300,
        "active_site_features": [
            {
                "feature_type": "Active site",
                "begin": pos,
                "end": pos,
                "description": "",
                "ligand_name": None,
                "ligand_id": None,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
            for pos in act_sites
        ],
        "binding_site_features": [],
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": [
            {
                "reaction": f"reaction for {accession}",
                "ec_number": ec,
                "cross_references": [],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        ],
        "cofactor_comments": [
            {
                "cofactors": [
                    {"name": name, "cross_reference": {"database": "ChEBI", "id": "CHEBI:0"},
                     "evidence": []}
                    for name in cofactor_names
                ]
            }
        ]
        if cofactor_names
        else [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


# A ``coord`` of "triad" stages a CIF whose Ser/His/Asp geometry resolves at the
# residue ids 50/57/99; "scatter" stages one where the residues are far apart;
# "missing" stages no coordinate (the fetcher returns None).
_ACT_SITES = (50, 57, 99)


def _triad_cif() -> str:
    return (
        "data_test\n"
        "loop_\n"
        "_atom_site.group_PDB\n"
        "_atom_site.id\n"
        "_atom_site.auth_comp_id\n"
        "_atom_site.auth_asym_id\n"
        "_atom_site.auth_seq_id\n"
        "_atom_site.auth_atom_id\n"
        "_atom_site.Cartn_x\n"
        "_atom_site.Cartn_y\n"
        "_atom_site.Cartn_z\n"
        "ATOM 1 SER A 50 OG 0.000 0.000 0.000\n"
        "ATOM 2 HIS A 57 NE2 3.000 0.000 0.000\n"
        "ATOM 3 HIS A 57 ND1 3.000 2.000 0.000\n"
        "ATOM 4 ASP A 99 OD2 3.000 5.000 0.000\n"
        "ATOM 5 ASP A 99 OD1 4.000 5.000 0.000\n"
        "#\n"
    )


def _scatter_cif() -> str:
    return (
        "data_test\n"
        "loop_\n"
        "_atom_site.group_PDB\n"
        "_atom_site.id\n"
        "_atom_site.auth_comp_id\n"
        "_atom_site.auth_asym_id\n"
        "_atom_site.auth_seq_id\n"
        "_atom_site.auth_atom_id\n"
        "_atom_site.Cartn_x\n"
        "_atom_site.Cartn_y\n"
        "_atom_site.Cartn_z\n"
        "ATOM 1 SER A 50 OG 0.000 0.000 0.000\n"
        "ATOM 2 HIS A 57 NE2 40.000 0.000 0.000\n"
        "ATOM 3 ASP A 99 OD2 80.000 0.000 0.000\n"
        "#\n"
    )


# accession -> (ec, cofactor_names, coordinate kind)
_FIXTURES = {
    "SH0001": ("3.4.21.1", [], "triad"),     # assigns
    "SH0002": ("3.4.21.4", ["Ca(2+)"], "triad"),  # held: cofactor annotated
    "SH0003": ("3.4.16.1", [], "scatter"),   # held: no coordinate triad
    "SH0004": ("3.1.1.3", [], "missing"),    # held: no AFDB coordinate
    "NM0001": ("2.7.11.1", [], "triad"),     # skipped: not a serine-hydrolase EC
}


def _query_fetcher(query, size):
    records = [_search_record(acc, [fx[0]]) for acc, fx in _FIXTURES.items()]
    # the pilot fetches every lane; return all rows on the 3.4.21 lane only so
    # cross-lane dedup keeps each accession once.
    if "3.4.21" in query:
        return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": []}


def _entry_fetcher(accession):
    ec, cofactors, _ = _FIXTURES[accession]
    return {
        "metadata": {"url": f"test://{accession}"},
        "record": _entry_record(accession, act_sites=_ACT_SITES, cofactor_names=cofactors, ec=ec),
    }


def _cif_fetcher(accession):
    _, _, kind = _FIXTURES[accession]
    if kind == "missing":
        return None
    return _triad_cif() if kind == "triad" else _scatter_cif()


class SerHisHoleSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        kwargs.setdefault("frozen_benchmark_payload", [])
        kwargs.setdefault("expansion_payload", [])
        with tempfile.TemporaryDirectory() as tmp:
            return build_ser_his_hole_sourcing(
                max_records_per_lane=10,
                current_manifest_payload={"rows": []},
                staging_dir=Path(tmp),
                created_utc="2026-06-11T00:00:00Z",
                query_fetcher=_query_fetcher,
                entry_fetcher=_entry_fetcher,
                cif_fetcher=_cif_fetcher,
                **kwargs,
            )

    def test_only_the_confirmed_cofactorless_triad_is_admitted(self):
        audit = self._run()
        c = audit["counts"]
        self.assertEqual(c["triad_confirmed_labels"], 1)
        self.assertEqual(c["novelty_admitted_labels"], 1)
        label = audit["applied_labels"][0]
        self.assertEqual(label["entry_id"], "uniprot:SH0001")
        self.assertEqual(label["fingerprint_id"], "ser_his_acid_hydrolase")

    def test_hold_and_skip_reasons(self):
        audit = self._run()
        reasons = audit["counts"]["hold_reason_counts"]
        # cofactor-annotated, no-triad, no-coordinate, and non-serine-EC are each held/skipped
        self.assertEqual(reasons.get("catalytic_cofactor_annotated"), 1)
        self.assertEqual(reasons.get("no_afdb_predicted_coordinate"), 1)
        self.assertEqual(reasons.get("not_a_serine_hydrolase_ec_family"), 1)
        self.assertTrue(any(k.startswith("triad:") for k in reasons))

    def test_admitted_label_is_bronze_cofactorless_and_leakage_safe(self):
        audit = self._run()
        label = audit["applied_labels"][0]
        MechanismLabel.from_dict(label)
        self.assertEqual(label["tier"], "bronze")
        self.assertEqual(label["review_status"], "automation_curated")
        self.assertEqual(label["label_type"], "seed_fingerprint")
        ev = label["evidence"]
        self.assertEqual(ev["predictive_evidence"], [])
        for excluded in ("ec_label", "protein_name", "uniprot_prose"):
            self.assertIn(excluded, ev["excluded_context"])
        # the corroboration is the coordinate triad, recorded on structure_provenance
        triad = ev["structure_provenance"]["ser_his_triad_confirmation"]
        self.assertEqual(triad["status"], "ser_his_triad_annotation_corroborated")
        self.assertGreaterEqual(triad["annotated_act_site_overlap_count"], 2)
        # no cofactor was used; the committed label carries no transient staged path
        self.assertIsNone(ev["structure_provenance"]["coordinate_path"])
        self.assertEqual(ev["structure_provenance"]["structure_handle"], "AF-SH0001-F1")

    def test_guardrails_non_destructive(self):
        audit = self._run()
        g = audit["guardrails"]
        self.assertFalse(g["curated_registry_written"])
        self.assertTrue(g["frozen_current702_benchmark_preserved"])
        self.assertFalse(g["predictive_features_use_ec_name_or_prose"])
        self.assertTrue(g["ec_used_for_scope_assignment_only_never_predictive"])
        self.assertTrue(g["cofactorless_corroboration_is_coordinate_triad_not_cofactor"])
        self.assertTrue(g["novelty_gated_against_both_registries"])
        self.assertEqual(
            audit["status"],
            "non_destructive_preview_pending_explicit_registry_merge_authorization",
        )

    def test_existing_accession_is_deduped(self):
        existing = [
            {
                "entry_id": "uniprot:SH0001",
                "fingerprint_id": "ser_his_acid_hydrolase",
                "label_type": "seed_fingerprint",
                "tier": "bronze",
                "evidence": {},
            }
        ]
        audit = self._run(expansion_payload=existing)
        admitted_ids = [l["entry_id"] for l in audit["applied_labels"]]
        self.assertNotIn("uniprot:SH0001", admitted_ids)


if __name__ == "__main__":
    unittest.main()
