from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from catalytic_earth.atlas_transformation_query import query_transformation_sets
from catalytic_earth.atlas_transformation_sites import query_transformation_sites
from catalytic_earth.atlas_transformations import transformation_payload_sha256


ROOT = Path(__file__).resolve().parents[2]
ATLAS10 = ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json"
ATLAS10_EXPECTED = ROOT / "src/catalytic_earth/atlas_data/atlas10_runtime_expected.json"
TRANSFORMATIONS = {
    mcsa_id: ROOT / f"data/atlas/transformations/{mcsa_id.lower()}/transformations.json"
    for mcsa_id in ("M0173", "M0187")
}


class TransformationSiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.values = {
            mcsa_id: json.loads(path.read_text(encoding="utf-8"))
            for mcsa_id, path in TRANSFORMATIONS.items()
        }
        self.atlas10 = json.loads(ATLAS10.read_text(encoding="utf-8"))

    @staticmethod
    def records(bundle):
        rows = list(bundle.get("records", [])) + list(bundle.get("follow_on_records", []))
        if isinstance(bundle.get("inherited_kernel"), dict):
            rows.extend(TransformationSiteTests.records(bundle["inherited_kernel"]))
        return rows

    @classmethod
    def trypsin_records(cls, bundle):
        records = [
            row for row in cls.records(bundle)
            if row.get("case_id") == "atlas10.trypsin-fusarium.serine-protease"
        ]
        tier1 = next(row for row in records if row.get("evidence_tier") == 1)
        tier2 = next(row for row in records if row.get("evidence_tier") == 2)
        return tier1, tier2

    @staticmethod
    def proposal(record):
        return next(
            row for row in record["mechanism_proposals"]
            if row.get("source_record_id") == "M0173"
            and row.get("source_mechanism_id") == 1
        )

    @classmethod
    def before_step(cls, record):
        return next(
            row for row in cls.proposal(record)["mechanism_steps"]
            if row.get("source_step_id") == 1
        )

    @classmethod
    def descriptors(cls, record, atom_id):
        return [
            atom
            for flow in cls.before_step(record)["electron_flows"]
            for point in (flow["source_point"], flow["target_point"])
            for atom in point["atoms"]
            if atom["source_atom_ref"].rsplit(".", 1)[-1] == atom_id
        ]

    @staticmethod
    def repin(value):
        value["review"]["reviewed_payload_sha256"] = transformation_payload_sha256(value)

    @staticmethod
    def atoms(result):
        return {
            (match["transformation"]["record_binding"]["mcsa_id"], row["source_atom_id"]): row
            for match in result["matches"]
            for row in match["changed_source_atoms"]
        }

    def query(self, values=None, atlas10=None, **filters):
        return query_transformation_sites(
            self.values if values is None else values,
            atlas10_bundle=self.atlas10 if atlas10 is None else atlas10,
            **filters,
        )

    def test_exact_changed_atom_inventory_and_two_supported_links(self):
        result = self.query()
        self.assertEqual(
            (
                result["match_count"],
                result["changed_source_atom_count"],
                result["resolved_source_atom_count"],
                result["unresolved_source_atom_count"],
            ),
            (2, 12, 2, 10),
        )
        atoms = self.atoms(result)
        self.assertEqual(
            {atom_id for mcsa_id, atom_id in atoms if mcsa_id == "M0173"},
            {"a3", "a10", "a21", "a44", "a50"},
        )
        self.assertEqual(
            {atom_id for mcsa_id, atom_id in atoms if mcsa_id == "M0187"},
            {"a8", "a9", "a10", "a58", "a63", "a65", "a66"},
        )

        expected = {
            "a21": {
                "element": "N", "edit_ids": ["e5", "e6"], "flow_ids": ["o26"],
                "raw_label": "res:His56A", "site_id": "P35049:H65",
                "residue": "His", "sequence": 65, "author": 56, "label": 41,
            },
            "a44": {
                "element": "O", "edit_ids": ["e1", "e2"], "flow_ids": ["o24"],
                "raw_label": "res:Ser195A", "site_id": "P35049:S204",
                "residue": "Ser", "sequence": 204, "author": 195, "label": 180,
            },
        }
        for atom_id, wanted in expected.items():
            with self.subTest(atom_id=atom_id):
                row = atoms[("M0173", atom_id)]
                self.assertEqual(row["element"], wanted["element"])
                self.assertEqual(row["edit_ids"], wanted["edit_ids"])
                self.assertEqual(row["source_flow_ids"], wanted["flow_ids"])
                self.assertEqual(
                    row["source_residue_label"]["status"],
                    "explicit_bound_flow_mrv_extra_label",
                )
                self.assertEqual(
                    row["source_residue_label"]["residue_label"],
                    {
                        "raw_label": wanted["raw_label"],
                        "residue_name": wanted["residue"],
                        "author_position": wanted["author"],
                        "author_chain_id": "A",
                    },
                )
                mapping = row["source_record_residue_mapping"]
                self.assertEqual(mapping["status"], "unique_step_catalyst_site_match")
                self.assertEqual(mapping["site_id"], wanted["site_id"])
                self.assertEqual(mapping["source_assertion_row_selection"], "not_asserted")
                protein = row["protein_structure_context"]
                self.assertEqual(
                    (protein["uniprot_id"], protein["residue_name"], protein["sequence_position"]),
                    ("P35049", wanted["residue"], wanted["sequence"]),
                )
                [pdb_mapping] = protein["pdb_residue_mappings"]
                self.assertEqual(
                    (
                        pdb_mapping["pdb_id"], pdb_mapping["chain_id"],
                        pdb_mapping["author_position"], pdb_mapping["label_position"],
                    ),
                    ("1PQ5", "A", wanted["author"], wanted["label"]),
                )
                self.assertEqual(
                    row["deposited_atom_identity"],
                    {
                        "status": "not_asserted",
                        "atom_name": None,
                        "reason": "a source depiction node is not equated to a deposited atom by this query",
                    },
                )

    def test_unlabeled_nodes_and_nearby_aliases_do_not_inherit_sites(self):
        result = self.query()
        atoms = self.atoms(result)
        for key in [
            ("M0173", "a3"), ("M0173", "a10"), ("M0173", "a50"),
            ("M0187", "a8"), ("M0187", "a9"), ("M0187", "a10"),
            ("M0187", "a58"), ("M0187", "a63"), ("M0187", "a65"),
            ("M0187", "a66"),
        ]:
            with self.subTest(atom=key):
                row = atoms[key]
                self.assertEqual(row["source_residue_label"]["status"], "not_resolved")
                self.assertEqual(
                    row["source_residue_label"]["reason"],
                    "no_explicit_residue_label_on_bound_flow_atom",
                )
                self.assertIsNone(row["source_record_residue_mapping"]["site_id"])

        changed = copy.deepcopy(self.values)
        transformation = changed["M0173"]["transformations"][0]
        transformation["source_context"]["source_atom_annotations"]["rows"].append({
            "atom_id": "a50", "mrv_extra_label": None,
            "mrv_alias": "Ser195A", "rgroup_ref": None,
        })
        self.repin(changed["M0173"])
        result = self.query(values=changed, mcsa_id="M0173", source_atom_id="a50")
        [row] = result["matches"][0]["changed_source_atoms"]
        self.assertEqual(row["source_residue_label"]["status"], "not_resolved")
        self.assertIsNone(row["source_record_residue_mapping"]["site_id"])

    def test_filters_join_on_one_changed_atom_and_preserve_full_context(self):
        expected_source_query = query_transformation_sets(
            self.values, atlas10_bundle=self.atlas10, mcsa_id="M0173"
        )
        values_before = copy.deepcopy(self.values)
        atlas_before = copy.deepcopy(self.atlas10)
        result = self.query(source_atom_id="a44", mcsa_id="m0173", site_id="P35049:S204")
        self.assertEqual(result["source_transformation_query"], expected_source_query)
        self.assertEqual((result["match_count"], result["changed_source_atom_count"]), (1, 1))
        [match] = result["matches"]
        self.assertEqual(
            match["transformation"], self.values["M0173"]["transformations"][0]
        )
        self.assertEqual(match["bound_atlas10_record"]["evidence_tier"], 2)
        structure = match["changed_source_atoms"][0]["protein_structure_context"]["structures"][0]
        self.assertEqual(
            structure["context_flags"],
            ["static_structure", "condition_specific_pH_5", "physiological_protonation_unresolved"],
        )

        self.assertEqual(
            self.query(mcsa_id="M0173", source_atom_id="a44", site_id="P35049:H65")
            ["match_count"],
            0,
        )
        self.assertEqual(
            self.query(mcsa_id="M0187", site_id="P35049:S204")["match_count"], 0
        )
        self.assertEqual(self.query(mcsa_id="M0173", site_id="P35049:D108")["match_count"], 0)
        with self.assertRaisesRegex(ValueError, "source_atom_id requires mcsa_id"):
            self.query(source_atom_id="a44")

        result["matches"][0]["transformation"]["transformation_id"] = "changed"
        result["matches"][0]["bound_atlas10_record"]["sites"].clear()
        self.assertEqual(self.values, values_before)
        self.assertEqual(self.atlas10, atlas_before)

    def test_role_and_structure_limits_remain_residue_scoped(self):
        result = self.query(mcsa_id="M0173", source_atom_id="a44")
        [row] = result["matches"][0]["changed_source_atoms"]
        mapping = row["source_record_residue_mapping"]
        self.assertIn("nucleophile", mapping["site_record"]["roles"])
        self.assertEqual(mapping["source_assertion_row_selection"], "not_asserted")
        self.assertEqual(
            result["query_semantics"]["site_roles_apply_to"],
            "source_record_residue_not_source_depiction_atom",
        )
        self.assertFalse(result["query_semantics"]["source_assertion_row_selected"])
        for key in (
            "physical_cross_state_atom_correspondence", "deposited_atom_identity_asserted",
            "observed_intermediate_asserted", "transformation_trajectory_validated",
            "unlabeled_atom_adjacency_propagation",
        ):
            self.assertFalse(result["query_semantics"][key])
        expected = json.loads(ATLAS10_EXPECTED.read_text(encoding="utf-8"))
        self.assertEqual(
            result["query_semantics"]["atlas10_bundle_sha256"], expected["kernel_sha256"]
        )
        [structure] = row["protein_structure_context"]["structures"]
        self.assertIn("pH-5", structure["limitation"])
        self.assertIn("does not alone establish", structure["limitation"])

    def test_endpoint_label_loss_and_alias_origin_cannot_create_a_link(self):
        atlas = copy.deepcopy(self.atlas10)
        for record in self.trypsin_records(atlas):
            for descriptor in self.descriptors(record, "a44"):
                descriptor["semantic_labels"] = []
        result = self.query(atlas10=atlas, mcsa_id="M0173", source_atom_id="a44")
        [row] = result["matches"][0]["changed_source_atoms"]
        self.assertEqual(
            row["source_residue_label"]["reason"],
            "no_explicit_residue_label_on_bound_flow_atom",
        )
        self.assertIsNone(row["source_record_residue_mapping"]["site_id"])

        values = copy.deepcopy(self.values)
        annotations = values["M0173"]["transformations"][0]["source_context"][
            "source_atom_annotations"
        ]["rows"]
        next(item for item in annotations if item["atom_id"] == "a44")["mrv_alias"] = "Ser195A"
        self.repin(values["M0173"])
        result = self.query(values=values, mcsa_id="M0173", source_atom_id="a44")
        [row] = result["matches"][0]["changed_source_atoms"]
        self.assertEqual(
            row["source_residue_label"]["reason"],
            "residue_label_on_aliased_or_pseudoatom_not_resolved",
        )
        self.assertIsNone(row["source_record_residue_mapping"]["site_id"])

    def test_source_hash_review_and_tier_witness_mismatches_fail_closed(self):
        cases = {}

        wrong_hash_values = copy.deepcopy(self.values)
        transformation = wrong_hash_values["M0173"]["transformations"][0]
        transformation["record_binding"]["source_snapshot_sha256"] = "f" * 64
        binding = next(
            item for item in wrong_hash_values["M0173"]["source_bindings"]
            if item["binding_id"] == "source:M-CSA:M0173"
        )
        binding["sha256"] = "f" * 64
        self.repin(wrong_hash_values["M0173"])
        cases["wrong source snapshot"] = (wrong_hash_values, self.atlas10)

        stale_values = copy.deepcopy(self.values)
        stale_values["M0173"]["transformations"][0]["mandatory_abstentions"][0][
            "reason"
        ] += " altered"
        cases["stale transformation review"] = (stale_values, self.atlas10)

        proposal_atlas = copy.deepcopy(self.atlas10)
        _tier1, tier2 = self.trypsin_records(proposal_atlas)
        self.proposal(tier2)["annotation_texts"].append("injected mismatch")
        cases["Tier-2 proposal differs"] = (self.values, proposal_atlas)

        for name, (values, atlas) in cases.items():
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    self.query(values=values, atlas10=atlas, mcsa_id="M0173")

    def test_raw_molecule_namespace_is_preserved_without_mechanism_prefix_guess(self):
        renamed = copy.deepcopy(self.atlas10)
        for record in self.trypsin_records(renamed):
            for descriptor in self.descriptors(record, "a44"):
                descriptor["source_atom_ref"] = "opaquePanel.a44"
        result = self.query(atlas10=renamed, mcsa_id="M0173", source_atom_id="a44")
        [row] = result["matches"][0]["changed_source_atoms"]
        self.assertEqual(row["source_record_residue_mapping"]["site_id"], "P35049:S204")
        refs = {
            occurrence["atom"]["source_atom_ref"]
            for witness in row["source_flow_witnesses"]
            for occurrence in witness["source_atom_occurrences"]
        }
        self.assertEqual(refs, {"opaquePanel.a44"})

        ambiguous = copy.deepcopy(self.atlas10)
        for record in self.trypsin_records(ambiguous):
            self.descriptors(record, "a44")[0]["source_atom_ref"] = "otherPanel.a44"
        result = self.query(atlas10=ambiguous, mcsa_id="M0173", source_atom_id="a44")
        [row] = result["matches"][0]["changed_source_atoms"]
        self.assertEqual(
            row["source_residue_label"]["reason"],
            "ambiguous_molecule_qualified_source_atom_ref",
        )
        self.assertIsNone(row["source_record_residue_mapping"]["site_id"])

        bare = copy.deepcopy(self.atlas10)
        for record in self.trypsin_records(bare):
            for descriptor in self.descriptors(record, "a44"):
                descriptor["source_atom_ref"] = "a44"
        with self.assertRaisesRegex(ValueError, "not fully qualified"):
            self.query(atlas10=bare, mcsa_id="M0173")

    def test_cross_tier_element_flow_and_record_ambiguities_do_not_false_join(self):
        tier_mismatch = copy.deepcopy(self.atlas10)
        _tier1, tier2 = self.trypsin_records(tier_mismatch)
        self.descriptors(tier2, "a44")[0]["semantic_labels"] = []
        with self.assertRaisesRegex(ValueError, "before-step witness differs"):
            self.query(atlas10=tier_mismatch, mcsa_id="M0173")

        incompatible_element = copy.deepcopy(self.atlas10)
        for record in self.trypsin_records(incompatible_element):
            for descriptor in self.descriptors(record, "a44"):
                descriptor["element"] = "N"
        with self.assertRaisesRegex(ValueError, "element differs"):
            self.query(atlas10=incompatible_element, mcsa_id="M0173")

        duplicate_record = copy.deepcopy(self.atlas10)
        _tier1, tier2 = self.trypsin_records(duplicate_record)
        duplicate_record["follow_on_records"].append(copy.deepcopy(tier2))
        with self.assertRaisesRegex(ValueError, "one exact Tier-2"):
            self.query(atlas10=duplicate_record, mcsa_id="M0173")

    def test_ambiguous_site_or_coordinate_locator_is_never_selected(self):
        ambiguous_site = copy.deepcopy(self.atlas10)
        for record in self.trypsin_records(ambiguous_site):
            original = next(item for item in record["sites"] if item["site_id"] == "P35049:S204")
            added = copy.deepcopy(original)
            added["site_id"] = "P35049:S205"
            added["sequence_position"] = 205
            record["sites"].append(added)
            self.before_step(record)["catalyst_site_ids"].append("P35049:S205")
        result = self.query(
            atlas10=ambiguous_site, mcsa_id="M0173", source_atom_id="a44"
        )
        [row] = result["matches"][0]["changed_source_atoms"]
        self.assertEqual(
            row["source_record_residue_mapping"]["reason"],
            "multiple_step_catalyst_sites_match_explicit_residue_label",
        )
        self.assertIsNone(row["source_record_residue_mapping"]["site_id"])

        conflicting_locator = copy.deepcopy(self.atlas10)
        for record in self.trypsin_records(conflicting_locator):
            site = next(item for item in record["sites"] if item["site_id"] == "P35049:S204")
            added = copy.deepcopy(site["pdb_mappings"][0])
            added["label_position"] = 181
            added["numbering_note"] = "injected conflicting locator"
            site["pdb_mappings"].append(added)
        with self.assertRaisesRegex(ValueError, "mapping repeats an author locator"):
            self.query(atlas10=conflicting_locator, mcsa_id="M0173")


if __name__ == "__main__":
    unittest.main()
