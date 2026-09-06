from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from catalytic_earth.atlas_candidate_extraction import extract_panel_candidate
from catalytic_earth.atlas_context_candidates import extract_context_panel_candidate


ROOT = Path(__file__).resolve().parents[2]
M0219_SOURCE = (
    ROOT
    / "data"
    / "atlas"
    / "source_drafts"
    / "batches"
    / "aldolase-transketolase"
    / "sources"
    / "M0219.json"
)
M0222_SOURCE = (
    ROOT
    / "data"
    / "atlas"
    / "source_drafts"
    / "batches"
    / "aldolase-transketolase"
    / "sources"
    / "M0222.json"
)
M0212_SOURCE = ROOT / "data" / "atlas" / "source_drafts" / "sources" / "M0212.json"
V1_SCAN = ROOT / "data" / "atlas" / "candidate_extraction" / "scan.json"


def _snapshot() -> dict:
    return json.loads(M0219_SOURCE.read_text(encoding="utf-8"))


def _snapshot_bytes(value: dict) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _scheme(value: dict, step_id: int) -> dict:
    return next(
        item
        for item in value["step_schemes"]
        if item["mechanism_id"] == 1 and item["step_id"] == step_id
    )


def _rewrite_scheme(value: dict, step_id: int, mutate) -> None:
    scheme = _scheme(value, step_id)
    root = ET.fromstring(scheme["content_utf8"])
    mutate(root)
    content = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    scheme["content_utf8"] = content
    scheme["content_sha256"] = hashlib.sha256(content.encode("utf-8")).hexdigest()


def _element(root: ET.Element, tag: str, element_id: str) -> ET.Element:
    return next(item for item in root.iter(tag) if item.get("id") == element_id)


def _stereo_text(root: ET.Element, bond_id: str) -> ET.Element:
    bond = _element(root, "bond", bond_id)
    return next(item for item in bond if item.tag.rsplit("}", 1)[-1] == "bondStereo")


def _semantic_edits(value: dict) -> set[tuple]:
    return {
        (
            item["operation"],
            tuple(sorted(item["atom_ids"])),
            item["before"],
            item["after"],
            item["source_flow_id"],
            item["support"],
        )
        for item in value["proposed_graph_edits"]
    }


class AtlasContextCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_bytes = M0219_SOURCE.read_bytes()

    def extract(self, source_bytes: bytes | None = None) -> dict:
        return extract_context_panel_candidate(
            self.source_bytes if source_bytes is None else source_bytes,
            mechanism_id=1,
            before_step_id=2,
        )

    def assert_needs_review(self, value: dict) -> None:
        self.assertEqual(value["status"], "unreviewed")
        self.assertEqual(value["extraction_status"], "needs_review")
        self.assertEqual(value["proposed_graph_edits"], [])
        self.assertEqual(value["source_flow_bindings"], [])
        self.assertIsNone(value["coverage"])
        self.assertTrue(value["diagnostics"])

    def test_real_context_candidate_preserves_source_rows_without_interpreting_them(self) -> None:
        value = self.extract()

        self.assertEqual(value["schema_version"], "catalytic-earth.context-panel-candidate.v1")
        self.assertEqual(value["status"], "unreviewed")
        self.assertEqual(value["extraction_status"], "candidate")
        self.assertEqual(value["diagnostics"], [])
        self.assertEqual(
            value["source_binding"],
            {
                "provider": "M-CSA",
                "record_id": "M0219",
                "snapshot_sha256": "054f1c3bee9ff38938b59e81b6b4065fe4d4204cb899171f4f68c284bad7d01c",
                "mechanism_id": 1,
                "before_step_id": 2,
                "after_step_id": 3,
                "before_scheme_sha256": "fa49fc016864c33d502ea1d74a07b19e5a3b65c0b858ca07c1092be73b30c135",
                "after_scheme_sha256": "346c93502f1fb77b354f8a9eeb42e9406b2f6d8166b8ce7bc7102f78b2b11e1a",
            },
        )

        expected_stereo = [
            ("b33", ("a30", "a34"), "1", "W"),
            ("b34", ("a33", "a35"), "1", "W"),
            ("b37", ("a36", "a38"), "1", "H"),
            ("b38", ("a37", "a39"), "1", "W"),
        ]
        expected_coord = [
            ("b69", ("a26", "a1"), None, "cxn:coord"),
            ("b70", ("a24", "a1"), None, "cxn:coord"),
        ]
        for panel in ("before", "after"):
            context = value["opaque_source_context"][panel]
            self.assertEqual(
                [
                    (
                        row["bond_id"],
                        tuple(row["ordered_atom_refs2"]),
                        row["order_token"],
                        row["raw_text"],
                    )
                    for row in context["bond_stereo"]
                ],
                expected_stereo,
            )
            self.assertTrue(all(row["raw_attributes"] == {} for row in context["bond_stereo"]))
            self.assertEqual(context["atom_parity"], [])
            self.assertEqual(
                [
                    (
                        row["bond_id"],
                        tuple(row["ordered_atom_refs2"]),
                        row["order_token"],
                        row["raw_convention"],
                    )
                    for row in context["bond_conventions"]
                ],
                expected_coord,
            )

        preservation = value["context_preservation"]
        self.assertEqual(
            preservation["status"],
            "preserved_opaque_context_disjoint_from_proposed_edits",
        )
        self.assertEqual(
            preservation["before_counts"],
            {"bond_stereo": 4, "atom_parity": 0, "bond_conventions": 2},
        )
        self.assertEqual(preservation["after_counts"], preservation["before_counts"])
        self.assertEqual(preservation["matched_counts"], preservation["before_counts"])
        self.assertTrue(preservation["all_references_mapped"])
        self.assertTrue(preservation["ordered_metadata_preserved"])
        self.assertTrue(preservation["proposed_edit_endpoints_disjoint"])

        self.assertEqual(len(value["correspondence"]["atom_map"]), 75)
        self.assertEqual(len(value["proposed_graph_edits"]), 12)
        self.assertTrue(
            all(
                item["support"] == "after_graph_confirmed"
                for item in value["proposed_graph_edits"]
            )
        )
        self.assertEqual(len(value["source_panels"]["before_graph"]["bonds"]), 73)
        self.assertEqual(len(value["source_panels"]["after_graph"]["bonds"]), 74)
        graph_pairs = {
            tuple(item["atom_ids"])
            for panel in ("before_graph", "after_graph")
            for item in value["source_panels"][panel]["bonds"]
        }
        self.assertNotIn(("a26", "a1"), graph_pairs)
        self.assertNotIn(("a24", "a1"), graph_pairs)
        self.assertTrue(value["coverage"]["full_covalent_graph_replay_asserted"])
        self.assertNotIn("full_panel_replay_asserted", value["coverage"])

        scope = value["scope_effect"]
        self.assertTrue(scope["opaque_annotations_preserved"])
        self.assertTrue(scope["covalent_graph_excludes_convention_bonds"])
        for key in (
            "reviewed_evidence",
            "physical_atom_map",
            "canonical_participant_correspondence",
            "stereochemistry_assignment",
            "stereochemistry_interpreted",
            "coordination_chemistry_interpreted",
            "full_source_electronic_state_replayed",
            "complete_mechanism_path",
            "experimentally_validated",
        ):
            self.assertFalse(scope[key])

    def test_semantic_edit_set_is_the_twelve_raw_arrow_confirmed_deltas(self) -> None:
        self.assertEqual(
            _semantic_edits(self.extract()),
            {
                ("set_bond_order", ("a28", "a29"), 2, 1, "o55", "after_graph_confirmed"),
                ("add_bond", ("a29", "a73"), 0, 1, "o55", "after_graph_confirmed"),
                ("remove_bond", ("a6", "a73"), 1, 0, "o56", "after_graph_confirmed"),
                ("set_bond_order", ("a3", "a6"), 1, 2, "o56", "after_graph_confirmed"),
                ("set_bond_order", ("a2", "a3"), 2, 1, "o57", "after_graph_confirmed"),
                ("set_bond_order", ("a2", "a4"), 1, 2, "o57", "after_graph_confirmed"),
                ("set_bond_order", ("a4", "a7"), 2, 1, "o58", "after_graph_confirmed"),
                ("add_bond", ("a7", "a72"), 0, 1, "o58", "after_graph_confirmed"),
                ("remove_bond", ("a63", "a72"), 1, 0, "o59", "after_graph_confirmed"),
                ("set_formal_charge", ("a63",), 0, -1, "o59", "after_graph_confirmed"),
                ("add_bond", ("a10", "a28"), 0, 1, "o60", "after_graph_confirmed"),
                ("set_formal_charge", ("a10",), -1, 0, "o60", "after_graph_confirmed"),
            },
        )

    def test_changed_reversed_or_dropped_context_does_not_yield_edits(self) -> None:
        changed = _snapshot()
        _rewrite_scheme(changed, 3, lambda root: setattr(_stereo_text(root, "b33"), "text", "H"))

        reversed_coord = _snapshot()
        _rewrite_scheme(
            reversed_coord,
            3,
            lambda root: _element(root, "bond", "b69").set("atomRefs2", "a1 a26"),
        )

        dropped = _snapshot()

        def drop_stereo(root: ET.Element) -> None:
            bond = _element(root, "bond", "b33")
            bond.remove(_stereo_text(root, "b33"))

        _rewrite_scheme(dropped, 3, drop_stereo)

        for label, source in (
            ("changed token", changed),
            ("reversed endpoints", reversed_coord),
            ("dropped row", dropped),
        ):
            with self.subTest(label=label):
                value = self.extract(_snapshot_bytes(source))
                self.assert_needs_review(value)
                self.assertEqual(
                    {item["code"] for item in value["diagnostics"]},
                    {"opaque_context_changed"},
                )
                self.assertIsNotNone(value["opaque_source_context"])
                self.assertFalse(value["context_preservation"]["ordered_metadata_preserved"])

    def test_unmatched_special_endpoint_does_not_yield_edits(self) -> None:
        source = _snapshot()

        def move_special_atom(root: ET.Element) -> None:
            atom = _element(root, "atom", "a30")
            atom.set("x2", str(float(atom.get("x2")) + 0.125))

        _rewrite_scheme(source, 3, move_special_atom)
        value = self.extract(_snapshot_bytes(source))

        self.assert_needs_review(value)
        self.assertEqual(
            {item["code"] for item in value["diagnostics"]},
            {"opaque_context_unmapped"},
        )
        self.assertFalse(value["context_preservation"]["all_references_mapped"])

    def test_context_on_any_edit_endpoint_blocks_the_candidate(self) -> None:
        source = _snapshot()

        def add_overlapping_coordination(root: ET.Element) -> None:
            bond_array = next(root.iter("bondArray"))
            ET.SubElement(
                bond_array,
                "bond",
                {
                    "id": "opaque_overlap",
                    "atomRefs2": "a28 a1",
                    "convention": "cxn:coord",
                },
            )

        _rewrite_scheme(source, 2, add_overlapping_coordination)
        _rewrite_scheme(source, 3, add_overlapping_coordination)
        value = self.extract(_snapshot_bytes(source))

        self.assert_needs_review(value)
        self.assertEqual(
            {item["code"] for item in value["diagnostics"]},
            {"opaque_context_overlaps_proposed_edit"},
        )
        self.assertTrue(value["context_preservation"]["ordered_metadata_preserved"])
        self.assertFalse(
            value["context_preservation"]["proposed_edit_endpoints_disjoint"]
        )

    def test_unmatched_covalent_neighbor_of_special_reference_blocks_candidate(self) -> None:
        source = _snapshot()

        def add_unmatched_neighbor(root: ET.Element) -> None:
            ET.SubElement(
                next(root.iter("atomArray")),
                "atom",
                {
                    "id": "a999",
                    "elementType": "H",
                    "x2": "99.0",
                    "y2": "99.0",
                },
            )
            ET.SubElement(
                next(root.iter("bondArray")),
                "bond",
                {
                    "id": "b999",
                    "atomRefs2": "a30 a999",
                    "order": "1",
                },
            )

        _rewrite_scheme(source, 2, add_unmatched_neighbor)
        value = self.extract(_snapshot_bytes(source))

        self.assert_needs_review(value)
        self.assertEqual(
            {item["code"] for item in value["diagnostics"]},
            {"opaque_context_unmapped_boundary"},
        )
        self.assertTrue(value["context_preservation"]["all_references_mapped"])
        self.assertTrue(value["context_preservation"]["ordered_metadata_preserved"])
        self.assertTrue(
            value["context_preservation"]["proposed_edit_endpoints_disjoint"]
        )

    def test_parity_and_decorated_or_unknown_special_metadata_fail_closed(self) -> None:
        parity = _snapshot()

        def add_parity(root: ET.Element) -> None:
            parity_row = ET.SubElement(
                _element(root, "atom", "a30"),
                "atomParity",
                {"atomRefs4": "a30 a34 a29 a31"},
            )
            parity_row.text = "1"

        _rewrite_scheme(parity, 2, add_parity)

        decorated_stereo = _snapshot()
        _rewrite_scheme(
            decorated_stereo,
            2,
            lambda root: _stereo_text(root, "b33").set("source", "unmodeled"),
        )

        unknown_convention = _snapshot()
        _rewrite_scheme(
            unknown_convention,
            2,
            lambda root: _element(root, "bond", "b69").set(
                "convention", "cxn:hydrogen"
            ),
        )

        overlapping_kinds = _snapshot()

        def decorate_coordination(root: ET.Element) -> None:
            child = ET.SubElement(_element(root, "bond", "b69"), "bondStereo")
            child.text = "W"

        _rewrite_scheme(overlapping_kinds, 2, decorate_coordination)

        for label, source in (
            ("atom parity", parity),
            ("decorated stereo", decorated_stereo),
            ("unknown convention", unknown_convention),
            ("overlapping kinds", overlapping_kinds),
        ):
            with self.subTest(label=label):
                value = self.extract(_snapshot_bytes(source))
                self.assert_needs_review(value)
                self.assertEqual(
                    {item["code"] for item in value["diagnostics"]},
                    {"unsupported_opaque_source_context"},
                )
                self.assertIsNone(value["opaque_source_context"])
                self.assertFalse(value["scope_effect"]["opaque_annotations_preserved"])

    def test_orphan_or_out_of_scope_stereo_metadata_is_not_silently_dropped(self) -> None:
        orphan_stereo = _snapshot()

        def add_orphan_stereo(root: ET.Element) -> None:
            child = ET.SubElement(next(root.iter("bondArray")), "bondStereo")
            child.text = "W"

        _rewrite_scheme(orphan_stereo, 2, add_orphan_stereo)

        root_attribute = _snapshot()
        _rewrite_scheme(
            root_attribute,
            2,
            lambda root: root.set("stereoModel", "opaque"),
        )

        for label, source in (
            ("orphan bondStereo", orphan_stereo),
            ("root stereo attribute", root_attribute),
        ):
            with self.subTest(label=label):
                value = self.extract(_snapshot_bytes(source))
                self.assert_needs_review(value)
                self.assertEqual(
                    {item["code"] for item in value["diagnostics"]},
                    {"unsupported_opaque_source_context"},
                )
                self.assertIsNone(value["opaque_source_context"])
                self.assertFalse(value["scope_effect"]["opaque_annotations_preserved"])

    def test_duplicate_or_covalent_overlapping_convention_edges_fail_closed(self) -> None:
        duplicate = _snapshot()

        def add_duplicate_coordination(root: ET.Element) -> None:
            ET.SubElement(
                next(root.iter("bondArray")),
                "bond",
                {
                    "id": "duplicate_coord",
                    "atomRefs2": "a1 a26",
                    "convention": "cxn:coord",
                },
            )

        _rewrite_scheme(duplicate, 2, add_duplicate_coordination)
        _rewrite_scheme(duplicate, 3, add_duplicate_coordination)

        covalent_overlap = _snapshot()

        def add_covalent_overlap(root: ET.Element) -> None:
            ET.SubElement(
                next(root.iter("bondArray")),
                "bond",
                {
                    "id": "covalent_overlap",
                    "atomRefs2": "a30 a34",
                    "convention": "cxn:coord",
                },
            )

        _rewrite_scheme(covalent_overlap, 2, add_covalent_overlap)
        _rewrite_scheme(covalent_overlap, 3, add_covalent_overlap)

        for label, source in (
            ("duplicate undirected coordinate edge", duplicate),
            ("coordinate and covalent edge overlap", covalent_overlap),
        ):
            with self.subTest(label=label):
                value = self.extract(_snapshot_bytes(source))
                self.assert_needs_review(value)
                self.assertEqual(
                    {item["code"] for item in value["diagnostics"]},
                    {"unsupported_opaque_source_context"},
                )
                self.assertIsNone(value["opaque_source_context"])
                self.assertFalse(value["scope_effect"]["opaque_annotations_preserved"])

        self_loop = _snapshot()
        _rewrite_scheme(
            self_loop,
            2,
            lambda root: _element(root, "bond", "b69").set("atomRefs2", "a1 a1"),
        )
        with self.assertRaisesRegex(ValueError, "bond identifiers or endpoints"):
            self.extract(_snapshot_bytes(self_loop))

    def test_after_ids_may_change_but_ordered_context_must_follow_the_map(self) -> None:
        source = _snapshot()

        def rename_after(root: ET.Element) -> None:
            atom_ids = {
                item.get("id"): f"z{item.get('id')[1:]}" for item in root.iter("atom")
            }
            bond_ids = {
                item.get("id"): f"q{index}"
                for index, item in enumerate(root.iter("bond"), start=1)
            }
            for item in root.iter():
                if item.tag == "atom" and item.get("id") in atom_ids:
                    item.set("id", atom_ids[item.get("id")])
                elif item.tag == "bond" and item.get("id") in bond_ids:
                    item.set("id", bond_ids[item.get("id")])
                for attribute in ("atomRef", "atomRefs", "atomRefs2"):
                    raw = item.get(attribute)
                    if raw is None:
                        continue
                    renamed = []
                    for token in raw.split():
                        prefix, separator, atom_id = token.rpartition(".")
                        replacement = atom_ids.get(atom_id, atom_id)
                        renamed.append(
                            f"{prefix}{separator}{replacement}"
                            if separator
                            else replacement
                        )
                    item.set(attribute, " ".join(renamed))

        _rewrite_scheme(source, 3, rename_after)
        value = self.extract(_snapshot_bytes(source))

        self.assertEqual(value["extraction_status"], "candidate")
        self.assertEqual(len(value["correspondence"]["atom_map"]), 75)
        self.assertEqual(
            value["opaque_source_context"]["after"]["bond_stereo"][0][
                "ordered_atom_refs2"
            ],
            ["z30", "z34"],
        )
        self.assertEqual(
            value["opaque_source_context"]["after"]["bond_conventions"][0][
                "ordered_atom_refs2"
            ],
            ["z26", "z1"],
        )
        self.assertTrue(value["context_preservation"]["ordered_metadata_preserved"])

    def test_frozen_v1_extractor_still_rejects_the_same_raw_context(self) -> None:
        value = extract_panel_candidate(
            self.source_bytes,
            mechanism_id=1,
            before_step_id=2,
        )
        self.assertEqual(value["schema_version"], "catalytic-earth.panel-candidate.v1")
        self.assertEqual(value["status"], "unreviewed")
        self.assertEqual(value["extraction_status"], "needs_review")
        self.assertEqual(
            {item["code"] for item in value["diagnostics"]},
            {"stereochemistry_requires_review"},
        )

    def test_m0222_global_absolute_stereo_withholds_two_legacy_candidates(self) -> None:
        source_bytes = M0222_SOURCE.read_bytes()
        self.assertEqual(
            hashlib.sha256(source_bytes).hexdigest(),
            "a798aef39309cdf3af82a003112b13949b160f9d305339c6ab9c08a3273908a7",
        )
        expected_v1 = {
            1: {
                "nodes": (57, 57, 30),
                "edit_support": {"after_graph_confirmed": 4},
            },
            3: {
                "nodes": (56, 56, 54),
                "edit_support": {
                    "after_graph_confirmed": 3,
                    "source_arrow_only": 3,
                },
            },
        }

        for before_step_id, expected in expected_v1.items():
            with self.subTest(before_step_id=before_step_id):
                context_value = extract_context_panel_candidate(
                    source_bytes,
                    mechanism_id=1,
                    before_step_id=before_step_id,
                )
                self.assert_needs_review(context_value)
                self.assertEqual(
                    {item["code"] for item in context_value["diagnostics"]},
                    {"unsupported_opaque_source_context"},
                )
                self.assertIn(
                    "unsupported stereo-related XML attribute",
                    context_value["diagnostics"][0]["detail"],
                )
                self.assertIsNone(context_value["opaque_source_context"])
                self.assertFalse(
                    context_value["scope_effect"]["opaque_annotations_preserved"]
                )

                legacy = extract_panel_candidate(
                    source_bytes,
                    mechanism_id=1,
                    before_step_id=before_step_id,
                )
                self.assertEqual(
                    legacy["schema_version"], "catalytic-earth.panel-candidate.v1"
                )
                self.assertEqual(legacy["extraction_status"], "candidate")
                coverage = legacy["coverage"]
                self.assertEqual(
                    (
                        coverage["before_node_count"],
                        coverage["after_node_count"],
                        coverage["mapped_node_count"],
                    ),
                    expected["nodes"],
                )
                support_counts: dict[str, int] = {}
                for edit in legacy["proposed_graph_edits"]:
                    support_counts[edit["support"]] = (
                        support_counts.get(edit["support"], 0) + 1
                    )
                self.assertEqual(support_counts, expected["edit_support"])

        self.assertEqual(
            hashlib.sha256(V1_SCAN.read_bytes()).hexdigest(),
            "ab1875bcf09b3984a66777f9c3a1022e9af1ad1318611e55f025a432b78e63ff",
        )

    def test_failed_graph_extraction_does_not_claim_edit_disjointness(self) -> None:
        value = extract_context_panel_candidate(
            M0212_SOURCE.read_bytes(),
            mechanism_id=1,
            before_step_id=7,
        )

        self.assert_needs_review(value)
        self.assertEqual(
            {item["code"] for item in value["diagnostics"]},
            {"contradictory_source_arrow"},
        )
        self.assertIsNotNone(value["opaque_source_context"])
        preservation = value["context_preservation"]
        self.assertEqual(preservation["status"], "needs_review")
        self.assertTrue(preservation["all_references_mapped"])
        self.assertTrue(preservation["ordered_metadata_preserved"])
        self.assertTrue(preservation["no_special_boundary_bonds"])
        self.assertIsNone(preservation["proposed_edit_endpoints_disjoint"])


if __name__ == "__main__":
    unittest.main()
