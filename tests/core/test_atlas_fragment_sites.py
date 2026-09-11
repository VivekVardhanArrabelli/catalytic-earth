"""Adversarial checks for source-fragment to reference-site relations."""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from catalytic_earth import core_cli
from catalytic_earth.atlas10_source_adapters import parse_mcsa_scheme_flows
from catalytic_earth.atlas_fragment_sites import derive_fragment_site, query_fragment_sites
from catalytic_earth.atlas_mechanism_evidence import query_mechanism_evidence


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/atlas/atlas10/sources/mcsa/M0187.json"
ATLAS10 = ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json"
EVIDENCE = ROOT / "data/atlas/mechanism_evidence/m0187/evidence.json"
FRAGMENT_REVIEW = ROOT / "data/atlas/mechanism_evidence/source_fragment_review.json"
FRAGMENT_SPEC = ROOT / "data/atlas/mechanism_evidence/source_fragment_spec.json"
TRANSFORMATIONS = ROOT / "data/atlas/transformations/m0187/transformations.json"


def _records(bundle: dict) -> list[dict]:
    rows = list(bundle.get("records", [])) + list(bundle.get("follow_on_records", []))
    inherited = bundle.get("inherited_kernel")
    if isinstance(inherited, dict):
        rows.extend(_records(inherited))
    return rows


class FragmentSiteDerivationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = json.loads(SOURCE.read_text(encoding="utf-8"))
        atlas10 = json.loads(ATLAS10.read_text(encoding="utf-8"))
        [self.record] = [
            row for row in _records(atlas10)
            if row.get("record_id") == "mechanism:mandelate-racemase-pputida-enolate-v1"
            and row.get("evidence_tier") == 2
        ]
        [self.proposal] = [
            row for row in self.record["mechanism_proposals"]
            if row.get("source_record_id") == "M0187"
            and row.get("source_mechanism_id") == 1
        ]

    def step(self, source_step_id: int) -> dict:
        return next(
            row for row in self.proposal["mechanism_steps"]
            if row["source_step_id"] == source_step_id
        )

    def altered_scheme(self, source_step_id: int, change) -> tuple[dict, dict]:
        """Return coherent direct-function inputs after an XML-only graph change."""
        source = copy.deepcopy(self.source)
        step = copy.deepcopy(self.step(source_step_id))
        scheme = next(
            row for row in source["step_schemes"]
            if row["mechanism_id"] == 1 and row["step_id"] == source_step_id
        )
        root = ET.fromstring(scheme["content_utf8"])
        change(root)
        scheme["content_utf8"] = ET.tostring(root, encoding="unicode")
        digest = hashlib.sha256(scheme["content_utf8"].encode("utf-8")).hexdigest()
        scheme["content_sha256"] = digest
        step["source_scheme_sha256"] = digest
        step["electron_flows"] = parse_mcsa_scheme_flows(scheme)["electron_flows"]
        return source, step

    @staticmethod
    def atom(root: ET.Element, atom_id: str) -> ET.Element:
        return next(row for row in root.iter("atom") if row.get("id") == atom_id)

    @staticmethod
    def add_bond(
        root: ET.Element, left: str, right: str, *, order: str | None = None,
        convention: str | None = None,
    ) -> None:
        bond_array = next(root.iter("bondArray"))
        attributes = {"id": "adversarial", "atomRefs2": f"{left} {right}"}
        if order is not None:
            attributes["order"] = order
        if convention is not None:
            attributes["convention"] = convention
        ET.SubElement(bond_array, "bond", attributes)

    def test_his_endpoint_resolves_as_one_source_fragment_reference_site(self):
        row = derive_fragment_site(self.source, self.record, self.step(1), "a58")

        self.assertEqual((row["source_step_id"], row["source_atom_id"], row["source_atom_ref"]),
                         (1, "a58", "m1.a58"))
        self.assertEqual(row["fragment"]["basis"], "heavy_atom_covalent_connected_component")
        self.assertEqual(row["fragment"]["atom_ids"], [
            "a52", "a53", "a54", "a55", "a56", "a57", "a58",
        ])
        [anchor] = row["fragment"]["alias_anchors"]
        self.assertEqual((anchor["atom_id"], anchor["mrv_alias"]), ("a52", "His297A"))
        self.assertEqual(
            row["source_residue_label"],
            {
                "status": "unique_source_fragment_alias",
                "raw_semantic_labels": [],
                "residue_label": {
                    "raw_label": "His297A", "residue_name": "His",
                    "author_position": 297, "author_chain_id": "A",
                },
                "reason": None,
            },
        )
        mapping = row["source_record_residue_mapping"]
        self.assertEqual((mapping["status"], mapping["site_id"]),
                         ("unique_step_catalyst_site_match", "P11444:H297"))
        self.assertIn("fragment", mapping["match_basis"])
        protein = row["protein_structure_context"]
        self.assertEqual(
            (protein["uniprot_id"], protein["residue_name"], protein["sequence_position"]),
            ("P11444", "His", 297),
        )
        [pdb_mapping] = protein["pdb_residue_mappings"]
        self.assertEqual(
            (pdb_mapping["pdb_id"], pdb_mapping["chain_id"],
             pdb_mapping["author_position"], pdb_mapping["label_position"]),
            ("1MNS", "A", 297, 295),
        )
        [structure] = protein["structures"]
        self.assertIn("inhibitor_bound_context", structure["context_flags"])
        self.assertIn("chemical_modification_context", structure["context_flags"])
        self.assertIn("do not interpret", structure["limitation"])
        self.assertEqual(row["deposited_atom_identity"],
                         {"status": "not_asserted", "atom_name": None})
        rendered = json.dumps(row)
        self.assertNotIn("NE2", rendered)
        self.assertNotIn("ND1", rendered)

    def test_glu_endpoint_and_nearby_proton_do_not_inherit_the_only_step_site(self):
        glu = derive_fragment_site(self.source, self.record, self.step(1), "a63")
        self.assertEqual(glu["fragment"]["atom_ids"],
                         ["a59", "a60", "a61", "a62", "a63", "a64"])
        self.assertEqual(glu["source_residue_label"]["residue_label"]["raw_label"],
                         "Glu317A")
        self.assertEqual(glu["source_record_residue_mapping"]["site_id"], None)
        self.assertIn(
            "no_step_catalyst_site_matches",
            glu["source_record_residue_mapping"]["reason"],
        )

        proton = derive_fragment_site(self.source, self.record, self.step(1), "a66")
        self.assertEqual(proton["source_record_residue_mapping"]["site_id"], None)
        self.assertEqual(
            proton["source_residue_label"]["reason"],
            "hydrogen_alias_or_pseudoatom_is_not_a_residue_atom_anchor",
        )
        self.assertNotEqual(proton["source_record_residue_mapping"]["site_id"],
                            "P11444:H297")

    def test_second_step_lys_endpoint_generalizes_but_wrong_step_does_not(self):
        lys = derive_fragment_site(self.source, self.record, self.step(2), "a19")
        self.assertEqual(lys["source_residue_label"]["residue_label"], {
            "raw_label": "Lys166A", "residue_name": "Lys",
            "author_position": 166, "author_chain_id": "A",
        })
        self.assertEqual(lys["source_record_residue_mapping"]["site_id"], "P11444:K166")

        with self.assertRaisesRegex(ValueError, "lacks one molecule-qualified flow reference"):
            derive_fragment_site(self.source, self.record, self.step(2), "a58")

    def test_hydrogen_on_a_residue_fragment_is_still_not_a_site_atom(self):
        row = derive_fragment_site(self.source, self.record, self.step(3), "a56")
        self.assertEqual(row["source_record_residue_mapping"]["site_id"], None)
        self.assertEqual(
            row["source_residue_label"]["reason"],
            "hydrogen_alias_or_pseudoatom_is_not_a_residue_atom_anchor",
        )

    def test_alias_on_the_endpoint_and_duplicate_panel_aliases_fail_closed(self):
        def move_alias(root: ET.Element) -> None:
            self.atom(root, "a52").attrib.pop("mrvAlias")
            self.atom(root, "a58").set("mrvAlias", "His297A")

        source, step = self.altered_scheme(1, move_alias)
        aliased_endpoint = derive_fragment_site(source, self.record, step, "a58")
        self.assertEqual(aliased_endpoint["source_record_residue_mapping"]["site_id"], None)
        self.assertEqual(
            aliased_endpoint["source_residue_label"]["reason"],
            "hydrogen_alias_or_pseudoatom_is_not_a_residue_atom_anchor",
        )

        def duplicate_alias(root: ET.Element) -> None:
            self.atom(root, "a59").set("mrvAlias", "His297A")

        source, step = self.altered_scheme(1, duplicate_alias)
        duplicate = derive_fragment_site(source, self.record, step, "a58")
        self.assertEqual(duplicate["source_record_residue_mapping"]["site_id"], None)
        self.assertEqual(
            duplicate["source_residue_label"]["reason"],
            "source_residue_alias_is_not_unique_in_panel",
        )

    def test_conflicting_component_aliases_and_ligand_merge_fail_closed(self):
        def add_conflict(root: ET.Element) -> None:
            self.atom(root, "a53").set("mrvAlias", "Glu317A")

        source, step = self.altered_scheme(1, add_conflict)
        conflict = derive_fragment_site(source, self.record, step, "a58")
        self.assertEqual(conflict["source_record_residue_mapping"]["site_id"], None)
        self.assertEqual(
            conflict["source_residue_label"]["reason"],
            "source_fragment_does_not_have_one_alias_anchor",
        )

        def merge_ligand(root: ET.Element) -> None:
            self.add_bond(root, "a58", "a9", order="1")

        source, step = self.altered_scheme(1, merge_ligand)
        merged = derive_fragment_site(source, self.record, step, "a58")
        self.assertEqual(merged["source_record_residue_mapping"]["site_id"], None)
        self.assertEqual(
            merged["source_residue_label"]["reason"],
            "source_fragment_has_other_identity_labels_or_pseudoatoms",
        )

    def test_coordinate_proximity_does_not_merge_residue_fragments(self):
        def add_coordination(root: ET.Element) -> None:
            self.add_bond(root, "a58", "a63", convention="cxn:coord")

        source, step = self.altered_scheme(1, add_coordination)
        row = derive_fragment_site(source, self.record, step, "a58")
        self.assertEqual(row["fragment"]["atom_ids"],
                         ["a52", "a53", "a54", "a55", "a56", "a57", "a58"])
        self.assertEqual(row["source_record_residue_mapping"]["site_id"], "P11444:H297")
        self.assertTrue(any(
            item["raw_convention"] == "cxn:coord"
            for item in row["fragment"]["opaque_panel_context"]["bond_conventions"]
        ))


class FragmentSiteCliTests(unittest.TestCase):
    def command(self, *args: str) -> dict:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(["atlas-mechanism-evidence", *args]), 0)
        return json.loads(output.getvalue())

    @staticmethod
    def relation(result: dict, source_step_id: int, source_atom_id: str) -> dict:
        return next(
            row for row in result["source_fragment_query"]["relations"]
            if row["source_step_id"] == source_step_id
            and row["source_atom_id"] == source_atom_id
        )

    def test_opt_in_composes_two_sites_without_changing_default_query(self):
        baseline = self.command()
        included = self.command("--include-source-fragments")
        fragment_query = included.pop("source_fragment_query")
        self.assertEqual(included, baseline)
        self.assertNotIn("source_fragment_query", baseline)
        self.assertEqual(
            (fragment_query["relation_count"], fragment_query["resolved_relation_count"]),
            (3, 2),
        )

        his = next(row for row in fragment_query["relations"]
                   if row["source_step_id"] == 1 and row["source_atom_id"] == "a58")
        self.assertEqual(his["source_record_residue_mapping"]["site_id"], "P11444:H297")
        self.assertEqual(
            his["functional_evidence"]["relationship"],
            "reference_site_context_not_exact_assayed_construct",
        )
        self.assertEqual(
            {row["observation_id"] for row in his["functional_evidence"]["matched_observations"]},
            {"H297N-racemization", "H297N-S-exchange", "H297N-R-exchange", "H297N-structure"},
        )
        self.assertFalse(his["functional_evidence"]["source_arrow_experimentally_validated"])

        glu = next(row for row in fragment_query["relations"]
                   if row["source_step_id"] == 1 and row["source_atom_id"] == "a63")
        self.assertIsNone(glu["source_record_residue_mapping"]["site_id"])
        self.assertEqual(glu["functional_evidence"]["matched_observations"], [])

        lys = next(row for row in fragment_query["relations"]
                   if row["source_step_id"] == 2 and row["source_atom_id"] == "a19")
        self.assertEqual(lys["source_record_residue_mapping"]["site_id"], "P11444:K166")
        # K166R is only contextual inside the focal H297N case, not a standalone
        # K166 adjudication that this generic reference-site join may promote.
        self.assertEqual(lys["functional_evidence"]["matched_observations"], [])

        semantics = fragment_query["query_semantics"]
        self.assertFalse(semantics["source_residue_role_is_atom_role"])
        self.assertFalse(semantics["exact_assayed_construct_identity"])
        self.assertFalse(semantics["deposited_atom_identity"])
        self.assertFalse(semantics["source_arrow_experimentally_validated"])

    def test_filters_only_copied_observations_and_preserve_endpoint_types(self):
        result = self.command(
            "--variant", "H297N", "--endpoint", "isotope_exchange",
            "--include-source-fragments",
        )
        query = result["source_fragment_query"]
        self.assertEqual((query["relation_count"], query["resolved_relation_count"]), (3, 2))
        self.assertEqual(
            query["query_semantics"]["observation_filters_apply_to"],
            "copied_observations_not_source_relations",
        )

        his = self.relation(result, 1, "a58")
        observations = his["functional_evidence"]["matched_observations"]
        self.assertEqual(
            {row["observation_id"] for row in observations},
            {"H297N-S-exchange", "H297N-R-exchange"},
        )
        self.assertTrue(all(row["endpoint"] == {
            "kind": "isotope_exchange",
            "name": "alpha-proton exchange with solvent deuterium",
            "net_direction": None,
        } for row in observations))
        not_detected = next(row for row in observations
                            if row["result"]["result_class"] == "not_detected")
        self.assertIsNone(not_detected["result"]["value"])
        self.assertIsNone(not_detected["result"]["unit"])
        self.assertFalse(query["query_semantics"]["nondetection_is_numeric_zero"])
        self.assertFalse(query["query_semantics"]["exchange_is_racemization"])
        self.assertEqual(self.relation(result, 2, "a19")["functional_evidence"]
                         ["matched_observations"], [])


class FragmentSiteBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bundle = {
            "spec": json.loads(FRAGMENT_SPEC.read_text(encoding="utf-8")),
            "review": json.loads(FRAGMENT_REVIEW.read_text(encoding="utf-8")),
            "source_snapshots_utf8": {"M0187": SOURCE.read_text(encoding="utf-8")},
            "reference_snapshots_utf8": {
                "UniProtKB:P11444": (ROOT / "data/atlas/atlas10/sources/uniprot/P11444.json").read_text(encoding="utf-8"),
            },
        }
        self.repin_review(self.bundle)
        self.atlas10 = json.loads(ATLAS10.read_text(encoding="utf-8"))
        self.transformations = {
            "M0187": json.loads(TRANSFORMATIONS.read_text(encoding="utf-8")),
        }
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.evidence_query = query_mechanism_evidence(
            evidence,
            atlas10_bundle=self.atlas10,
            transformation_values=self.transformations,
        )

    @staticmethod
    def canonical_sha256(value: dict) -> str:
        encoded = json.dumps(
            value, ensure_ascii=True, allow_nan=False,
            separators=(",", ":"), sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def repin_review(cls, bundle: dict) -> None:
        bundle["review"]["spec_sha256"] = cls.canonical_sha256(bundle["spec"])

    @classmethod
    def repin_evidence_case(cls, bundle: dict, evidence_query: dict) -> None:
        bundle["spec"]["evidence_case_sha256"] = cls.canonical_sha256(
            evidence_query["matches"][0]["case"]
        )
        cls.repin_review(bundle)

    def query(self, bundle: dict | None = None, evidence_query: dict | None = None) -> dict:
        return query_fragment_sites(
            self.bundle if bundle is None else bundle,
            atlas10_bundle=self.atlas10,
            evidence_query=self.evidence_query if evidence_query is None else evidence_query,
            transformation_values=self.transformations,
        )

    def test_high_level_source_scheme_and_qualified_atom_bindings_fail_closed(self):
        stale_source = copy.deepcopy(self.bundle)
        stale_source["source_snapshots_utf8"]["M0187"] += "\n"
        with self.assertRaisesRegex(ValueError, "source fragment source hash differs"):
            self.query(stale_source)

        repinned_scheme = copy.deepcopy(self.bundle)
        source = json.loads(repinned_scheme["source_snapshots_utf8"]["M0187"])
        source["step_schemes"][0]["content_utf8"] += " "
        encoded_source = json.dumps(source, sort_keys=True).encode("utf-8")
        repinned_scheme["source_snapshots_utf8"]["M0187"] = encoded_source.decode("utf-8")
        repinned_scheme["spec"]["source_bindings"][0]["sha256"] = (
            hashlib.sha256(encoded_source).hexdigest()
        )
        self.repin_review(repinned_scheme)
        with self.assertRaisesRegex(ValueError, "source fragment record binding differs"):
            self.query(repinned_scheme)

        wrong_atom_ref = copy.deepcopy(self.bundle)
        wrong_atom_ref["spec"]["requests"][0]["source_atom_ref"] = "m2.a58"
        self.repin_review(wrong_atom_ref)
        with self.assertRaisesRegex(
            ValueError, "source fragment request molecule-qualified atom differs",
        ):
            self.query(wrong_atom_ref)

    def test_transformation_and_evidence_context_cannot_cross_link(self):
        for field, replacement in (
            ("transformation_id", "transformation:M0187:wrong"),
            ("transformation_payload_sha256", "0" * 64),
        ):
            with self.subTest(field=field):
                bundle = copy.deepcopy(self.bundle)
                evidence_query = copy.deepcopy(self.evidence_query)
                bundle["spec"]["transformation_binding"][field] = replacement
                for match in evidence_query["matches"]:
                    match["case"]["transformation_binding"] = copy.deepcopy(
                        bundle["spec"]["transformation_binding"]
                    )
                self.repin_evidence_case(bundle, evidence_query)
                with self.assertRaisesRegex(
                    ValueError, "source fragment reviewed transformation binding differs",
                ):
                    self.query(bundle, evidence_query)

        wrong_case = copy.deepcopy(self.evidence_query)
        wrong_case["matches"][0]["case"]["case_id"] = "another-case"
        with self.assertRaisesRegex(
            ValueError, "source fragment evidence case or transformation binding differs",
        ):
            self.query(evidence_query=wrong_case)

        wrong_site = copy.deepcopy(self.evidence_query)
        wrong_site["matches"][0]["case"]["site_context_binding"]["site_id"] = "P11444:K166"
        with self.assertRaisesRegex(ValueError, "source fragment evidence case content differs"):
            self.query(evidence_query=wrong_site)

    def test_cached_evidence_rows_are_rederived_and_contextual_rows_do_not_promote(self):
        duplicate_match = copy.deepcopy(self.evidence_query)
        duplicate_match["matches"].append(copy.deepcopy(duplicate_match["matches"][0]))
        with self.assertRaisesRegex(ValueError, "count"):
            self.query(evidence_query=duplicate_match)
        duplicate_match["case_count"] = len(duplicate_match["matches"])
        duplicate_match["matched_observation_count"] = sum(
            len(match["matched_observations"])
            for match in duplicate_match["matches"]
        )
        with self.assertRaisesRegex(ValueError, "repeat"):
            self.query(evidence_query=duplicate_match)

        altered_observation = copy.deepcopy(self.evidence_query)
        altered_observation["matches"][0]["matched_observations"][0]["result"]["value"] = 999
        with self.assertRaisesRegex(ValueError, "source fragment filtered observations differ"):
            self.query(evidence_query=altered_observation)

        altered_ids = copy.deepcopy(self.evidence_query)
        altered_ids["matches"][0]["matched_observation_ids"].pop()
        with self.assertRaisesRegex(ValueError, "source fragment filtered observations differ"):
            self.query(evidence_query=altered_ids)

        altered_case = copy.deepcopy(self.evidence_query)
        altered_case["matches"][0]["case"]["observations"][0]["result"]["value"] = 999
        with self.assertRaisesRegex(ValueError, "source fragment evidence case content differs"):
            self.query(evidence_query=altered_case)

        contextual_k166 = copy.deepcopy(self.evidence_query)
        case = contextual_k166["matches"][0]["case"]
        case["site_context_binding"]["site_id"] = "P11444:K166"
        case["focal_variant_id"] = "K166R"
        bundle = copy.deepcopy(self.bundle)
        self.repin_evidence_case(bundle, contextual_k166)
        result = self.query(bundle, contextual_k166)
        lys = next(
            row for row in result["relations"]
            if row["source_step_id"] == 2 and row["source_atom_id"] == "a19"
        )
        self.assertEqual(
            {row["observation_id"] for row in contextual_k166["matches"][0]
             ["matched_observations"] if row["variant"]["variant_id"] == "K166R"},
            {"K166R-R-to-S-turnover", "K166R-S-to-R-turnover"},
        )
        self.assertTrue(all(
            row["functional_evidence"]["matched_observations"] == []
            for row in result["relations"]
        ))


if __name__ == "__main__":
    unittest.main()
