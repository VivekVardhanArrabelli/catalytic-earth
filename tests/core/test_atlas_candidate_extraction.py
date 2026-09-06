from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from catalytic_earth.atlas_candidate_extraction import extract_panel_candidate


ROOT = Path(__file__).resolve().parents[2]
M0173_SOURCE = ROOT / "data/atlas/atlas10/sources/mcsa/M0173.json"


def _snapshot() -> dict:
    return json.loads(M0173_SOURCE.read_text(encoding="utf-8"))


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


def _semantic_edits(value: dict, atom_normalizer=lambda atom_id: atom_id) -> set[tuple]:
    return {
        (
            item["operation"],
            tuple(sorted(atom_normalizer(atom_id) for atom_id in item["atom_ids"])),
            item["before"],
            item["after"],
            item["source_flow_id"],
            item["support"],
        )
        for item in value["proposed_graph_edits"]
    }


def _all_keys(value) -> set[str]:
    if isinstance(value, dict):
        return set(value) | set().union(*(_all_keys(item) for item in value.values()), set())
    if isinstance(value, list):
        return set().union(*(_all_keys(item) for item in value), set())
    return set()


def _rename_panel_ids(
    root: ET.Element,
    *,
    atom_prefix: str,
    bond_prefix: str,
    flow_prefix: str | None = None,
) -> None:
    atom_ids = {
        item.get("id"): f"{atom_prefix}{item.get('id')[1:]}"
        for item in root.iter("atom")
    }
    bond_ids = {
        item.get("id"): f"{bond_prefix}{index}"
        for index, item in enumerate(root.iter("bond"), start=1)
    }
    flow_ids = (
        {
            item.get("id"): f"{flow_prefix}{index}"
            for index, item in enumerate(root.iter("MEFlow"), start=1)
        }
        if flow_prefix is not None
        else {}
    )

    for item in root.iter():
        if item.tag == "atom" and item.get("id") in atom_ids:
            item.set("id", atom_ids[item.get("id")])
        elif item.tag == "bond" and item.get("id") in bond_ids:
            item.set("id", bond_ids[item.get("id")])
        elif item.tag == "MEFlow" and item.get("id") in flow_ids:
            item.set("id", flow_ids[item.get("id")])

        for attribute in ("atomRefs", "atomRefs2", "atomRef"):
            raw = item.get(attribute)
            if raw is None:
                continue
            renamed = []
            for token in raw.split():
                prefix, separator, atom_id = token.rpartition(".")
                replacement = atom_ids.get(atom_id, atom_id)
                renamed.append(f"{prefix}{separator}{replacement}" if separator else replacement)
            item.set(attribute, " ".join(renamed))


class AtlasCandidateExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_bytes = M0173_SOURCE.read_bytes()

    def extract(self, before_step_id: int, source_bytes: bytes | None = None) -> dict:
        return extract_panel_candidate(
            self.source_bytes if source_bytes is None else source_bytes,
            mechanism_id=1,
            before_step_id=before_step_id,
        )

    def assert_needs_review(self, value: dict) -> None:
        self.assertEqual(value["status"], "unreviewed")
        self.assertEqual(value["extraction_status"], "needs_review")
        self.assertEqual(value["proposed_graph_edits"], [])
        self.assertEqual(value["source_flow_bindings"], [])
        self.assertIsNone(value["coverage"])
        self.assertTrue(value["diagnostics"])

    def test_complete_transition_is_derived_from_raw_panels_and_arrows(self) -> None:
        value = self.extract(1)
        self.assertEqual(value["status"], "unreviewed")
        self.assertEqual(value["extraction_status"], "candidate")
        self.assertEqual(value["diagnostics"], [])
        self.assertEqual(
            _semantic_edits(value),
            {
                ("remove_bond", ("a44", "a50"), 1, 0, "o24", "after_graph_confirmed"),
                ("add_bond", ("a3", "a44"), 0, 1, "o24", "after_graph_confirmed"),
                ("set_bond_order", ("a10", "a3"), 2, 1, "o25", "after_graph_confirmed"),
                ("set_formal_charge", ("a10",), 0, -1, "o25", "after_graph_confirmed"),
                ("add_bond", ("a21", "a50"), 0, 1, "o26", "after_graph_confirmed"),
                ("set_formal_charge", ("a21",), 0, 1, "o26", "after_graph_confirmed"),
            },
        )
        coverage = value["coverage"]
        self.assertEqual(
            (
                coverage["before_node_count"],
                coverage["after_node_count"],
                coverage["mapped_node_count"],
            ),
            (50, 50, 50),
        )
        self.assertEqual(coverage["unmatched_before_atom_ids"], [])
        self.assertEqual(coverage["unmatched_after_atom_ids"], [])
        self.assertEqual(coverage["after_graph_unverified_edit_ids"], [])
        self.assertEqual(
            set(coverage["replayed_edit_ids"]),
            {item["edit_id"] for item in value["proposed_graph_edits"]},
        )
        self.assertTrue(coverage["projection_replays_exactly"])
        self.assertTrue(coverage["full_panel_replay_asserted"])

    def test_partial_transition_separates_confirmed_from_arrow_only_edits(self) -> None:
        value = self.extract(2)
        self.assertEqual(value["extraction_status"], "candidate")
        self.assertEqual(
            _semantic_edits(value),
            {
                ("remove_bond", ("a3", "a4"), 1, 0, "o24", "source_arrow_only"),
                ("add_bond", ("a4", "a50"), 0, 1, "o24", "source_arrow_only"),
                ("remove_bond", ("a21", "a50"), 1, 0, "o25", "source_arrow_only"),
                ("set_formal_charge", ("a21",), 1, 0, "o25", "after_graph_confirmed"),
                ("set_bond_order", ("a10", "a3"), 1, 2, "o26", "after_graph_confirmed"),
                ("set_formal_charge", ("a10",), -1, 0, "o26", "after_graph_confirmed"),
            },
        )
        coverage = value["coverage"]
        self.assertEqual(
            (
                coverage["before_node_count"],
                coverage["after_node_count"],
                coverage["mapped_node_count"],
            ),
            (50, 42, 40),
        )
        self.assertEqual(
            set(coverage["unmatched_before_atom_ids"]),
            {"a4", "a5", "a6", "a7", "a8", "a9", "a12", "a13", "a14", "a50"},
        )
        self.assertEqual(set(coverage["unmatched_after_atom_ids"]), {"a6", "a7"})
        self.assertEqual(
            (
                coverage["full_before_formal_charge"],
                coverage["full_after_formal_charge"],
                coverage["projected_before_formal_charge"],
                coverage["projected_after_formal_charge"],
            ),
            (-1, 0, 0, 0),
        )
        self.assertFalse(coverage["full_panel_replay_asserted"])
        self.assertNotIn(
            ("set_formal_charge", ("a7",), -1, 0, "o24", "source_arrow_only"),
            _semantic_edits(value),
        )
        water_pairs = {frozenset(("a12", "a13")), frozenset(("a13", "a14"))}
        self.assertFalse(
            any(
                item["operation"] == "remove_bond"
                and frozenset(item["atom_ids"]) in water_pairs
                for item in value["proposed_graph_edits"]
            )
        )

    def test_candidate_never_self_promotes_to_reviewed_evidence(self) -> None:
        value = self.extract(1)
        self.assertEqual(value["status"], "unreviewed")
        self.assertTrue(value["scope_effect"]["unreviewed_candidate"])
        self.assertTrue(
            all(
                not enabled
                for key, enabled in value["scope_effect"].items()
                if key != "unreviewed_candidate"
            )
        )
        self.assertTrue(
            {"review", "reviewed_payload_sha256", "evidence_tier", "registry_id"}.isdisjoint(
                _all_keys(value)
            )
        )

    def test_duplicate_locator_identity_is_reported_as_ambiguous(self) -> None:
        source = _snapshot()

        def duplicate(root: ET.Element) -> None:
            original = _element(root, "atom", "a48")
            duplicate_atom = _element(root, "atom", "a49")
            for name in (
                "elementType",
                "x2",
                "y2",
                "isotope",
                "mrvExtraLabel",
                "mrvAlias",
                "rgroupRef",
            ):
                if original.get(name) is None:
                    duplicate_atom.attrib.pop(name, None)
                else:
                    duplicate_atom.set(name, original.get(name))

        _rewrite_scheme(source, 1, duplicate)
        _rewrite_scheme(source, 2, duplicate)
        value = self.extract(1, _snapshot_bytes(source))
        self.assert_needs_review(value)
        self.assertIn("ambiguous_locator_key", {item["code"] for item in value["diagnostics"]})
        self.assertTrue(value["correspondence"]["ambiguous_matches"])

    def test_stereochemistry_and_unsupported_flow_fail_closed(self) -> None:
        stereo = _snapshot()

        def add_stereo(root: ET.Element) -> None:
            bond = _element(root, "bond", "b1")
            ET.SubElement(bond, "bondStereo").text = "W"

        _rewrite_scheme(stereo, 1, add_stereo)

        after_stereo = _snapshot()
        _rewrite_scheme(after_stereo, 2, add_stereo)

        unsupported_flow = _snapshot()

        def add_third_endpoint(root: ET.Element) -> None:
            flow = _element(root, "MEFlow", "o24")
            point = next(item for item in flow if item.tag == "MAtomSetPoint")
            point.set("atomRefs", f"{point.get('atomRefs')} m1.a3")

        _rewrite_scheme(unsupported_flow, 1, add_third_endpoint)

        head_flags = _snapshot()
        _rewrite_scheme(
            head_flags,
            1,
            lambda root: _element(root, "MEFlow", "o24").set("headFlags", "1"),
        )

        missing_flow_id = _snapshot()
        _rewrite_scheme(
            missing_flow_id,
            1,
            lambda root: _element(root, "MEFlow", "o24").attrib.pop("id"),
        )

        for label, source in (
            ("stereo", stereo),
            ("after_stereo", after_stereo),
            ("flow", unsupported_flow),
            ("head_flags", head_flags),
            ("missing_flow_id", missing_flow_id),
        ):
            with self.subTest(label=label):
                self.assert_needs_review(self.extract(1, _snapshot_bytes(source)))

    def test_after_panel_arrow_metadata_does_not_gate_current_transition(self) -> None:
        source = _snapshot()
        _rewrite_scheme(
            source,
            2,
            lambda root: _element(root, "MEFlow", "o24").set("headFlags", "1"),
        )
        changed = self.extract(1, _snapshot_bytes(source))
        baseline = self.extract(1)

        self.assertEqual(changed["extraction_status"], "candidate")
        self.assertEqual(_semantic_edits(changed), _semantic_edits(baseline))
        self.assertEqual(changed["source_panels"], baseline["source_panels"])
        self.assertEqual(changed["correspondence"], baseline["correspondence"])
        self.assertEqual(changed["coverage"], baseline["coverage"])
        self.assertNotEqual(
            changed["source_binding"]["snapshot_sha256"],
            baseline["source_binding"]["snapshot_sha256"],
        )
        self.assertNotEqual(
            changed["source_binding"]["after_scheme_sha256"],
            baseline["source_binding"]["after_scheme_sha256"],
        )

    def test_reversed_or_graph_contradictory_arrow_is_not_arrow_only(self) -> None:
        reversed_arrow = _snapshot()

        def reverse_flow(root: ET.Element) -> None:
            flow = _element(root, "MEFlow", "o24")
            children = list(flow)
            flow.remove(children[0])
            flow.remove(children[1])
            flow.extend(reversed(children))

        _rewrite_scheme(reversed_arrow, 1, reverse_flow)

        unchanged_source_bond = _snapshot()

        def retain_removed_bond(root: ET.Element) -> None:
            bond_array = next(root.iter("bondArray"))
            ET.SubElement(
                bond_array,
                "bond",
                {"id": "retained", "atomRefs2": "a44 a50", "order": "1"},
            )

        _rewrite_scheme(unchanged_source_bond, 2, retain_removed_bond)

        for label, source in (
            ("reversed", reversed_arrow),
            ("contradictory", unchanged_source_bond),
        ):
            with self.subTest(label=label):
                value = self.extract(1, _snapshot_bytes(source))
                self.assert_needs_review(value)
                self.assertIn(
                    "contradictory_source_arrow",
                    {item["code"] for item in value["diagnostics"]},
                )

    def test_reversed_charge_only_arrow_cannot_use_opposite_singleton_sides(self) -> None:
        source = _snapshot()

        def leave_only_oppositely_directed_charge_deltas(root: ET.Element) -> None:
            bond_array = next(root.iter("bondArray"))
            for bond in list(bond_array):
                refs = set((bond.get("atomRefs2") or "").split())
                if refs in ({"a3", "a44"}, {"a21", "a50"}):
                    bond_array.remove(bond)
                elif refs == {"a3", "a10"}:
                    bond.set("order", "2")
            ET.SubElement(
                bond_array,
                "bond",
                {"id": "restored", "atomRefs2": "a44 a50", "order": "1"},
            )

        def replace_with_reversed_charge_flow(root: ET.Element) -> None:
            document = next(root.iter("MDocument"))
            for child in list(document):
                if child.tag == "MEFlow":
                    document.remove(child)
            flow = ET.SubElement(
                document,
                "MEFlow",
                {
                    "id": "charge-flow",
                    "arcAngle": "270",
                    "baseElectronContainerIndex": "0",
                    "baseElectronIndexInContainer": "-1",
                },
            )
            ET.SubElement(flow, "MEFlowBasePoint", {"atomRef": "m1.a10"})
            ET.SubElement(flow, "MAtomSetPoint", {"atomRefs": "m1.a21"})

        _rewrite_scheme(source, 2, leave_only_oppositely_directed_charge_deltas)
        _rewrite_scheme(source, 1, replace_with_reversed_charge_flow)
        value = self.extract(1, _snapshot_bytes(source))
        self.assert_needs_review(value)
        self.assertIn(
            "contradictory_source_arrow",
            {item["code"] for item in value["diagnostics"]},
        )

    def test_missing_charged_endpoint_cannot_invent_an_after_charge(self) -> None:
        source = _snapshot()

        def break_oxygen_locator(root: ET.Element) -> None:
            oxygen = _element(root, "atom", "a4")
            oxygen.set("x2", "999.0")

        _rewrite_scheme(source, 3, break_oxygen_locator)
        value = self.extract(2, _snapshot_bytes(source))
        self.assert_needs_review(value)
        self.assertFalse(value["proposed_graph_edits"])

    def test_atom_bond_and_flow_ids_are_not_chemical_correspondence(self) -> None:
        source = _snapshot()
        _rewrite_scheme(
            source,
            1,
            lambda root: _rename_panel_ids(
                root, atom_prefix="b", bond_prefix="u", flow_prefix="f"
            ),
        )
        _rewrite_scheme(
            source,
            2,
            lambda root: _rename_panel_ids(
                root, atom_prefix="c", bond_prefix="v"
            ),
        )
        value = self.extract(1, _snapshot_bytes(source))
        self.assertEqual(value["extraction_status"], "candidate")
        self.assertEqual(
            _semantic_edits(value, lambda atom_id: f"a{atom_id[1:]}"),
            {
                ("remove_bond", ("a44", "a50"), 1, 0, "f1", "after_graph_confirmed"),
                ("add_bond", ("a3", "a44"), 0, 1, "f1", "after_graph_confirmed"),
                ("set_bond_order", ("a10", "a3"), 2, 1, "f2", "after_graph_confirmed"),
                ("set_formal_charge", ("a10",), 0, -1, "f2", "after_graph_confirmed"),
                ("add_bond", ("a21", "a50"), 0, 1, "f3", "after_graph_confirmed"),
                ("set_formal_charge", ("a21",), 0, 1, "f3", "after_graph_confirmed"),
            },
        )
        self.assertTrue(
            all(item["before_atom_id"].startswith("b") for item in value["correspondence"]["atom_map"])
        )
        self.assertTrue(
            all(item["after_atom_id"].startswith("c") for item in value["correspondence"]["atom_map"])
        )

    def test_corrupt_content_hash_and_invalid_transition_raise(self) -> None:
        source = _snapshot()
        _scheme(source, 1)["content_utf8"] += " "
        with self.assertRaises(ValueError):
            self.extract(1, _snapshot_bytes(source))

        for mechanism_id, before_step_id in ((99, 1), (1, 99)):
            with self.subTest(mechanism_id=mechanism_id, before_step_id=before_step_id):
                with self.assertRaises(ValueError):
                    extract_panel_candidate(
                        self.source_bytes,
                        mechanism_id=mechanism_id,
                        before_step_id=before_step_id,
                    )


if __name__ == "__main__":
    unittest.main()
