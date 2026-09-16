"""Guards on the Workbench's claim labels.

A claim label is a scientific statement about what kind of thing the viewer is
looking at. A label used without a legend entry, or a legend entry reused for a
different kind of claim, misreports the packaged data just as surely as a wrong
number would. These checks keep the label vocabulary closed and honest.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

STATIC = Path("src/catalytic_earth/workbench/static")
CHIP = re.compile(r"chip chip-([a-z]+)")


def _read(name: str) -> str:
    return (STATIC / name).read_text(encoding="utf-8")


class ChipLegendTest(unittest.TestCase):
    def setUp(self) -> None:
        self.html = _read("index.html")
        self.js = _read("app.js")
        self.css = _read("style.css")
        start = self.html.index("<footer")
        self.footer = self.html[start : self.html.index("</footer>")]

    def test_every_label_used_has_a_legend_entry(self) -> None:
        legend = set(CHIP.findall(self.footer))
        used = set(CHIP.findall(self.js)) | set(CHIP.findall(self.html))
        self.assertEqual(
            used - legend, set(), "these labels appear with no legend entry"
        )

    def test_every_legend_entry_is_actually_used(self) -> None:
        legend = set(CHIP.findall(self.footer))
        body = self.html[: self.html.index("<footer")]
        used = set(CHIP.findall(self.js)) | set(CHIP.findall(body))
        self.assertEqual(
            legend - used, set(), "these legend entries label nothing"
        )

    def test_every_label_has_a_distinct_style(self) -> None:
        for name in set(CHIP.findall(self.footer)):
            self.assertIn(f".chip-{name}", self.css, f"chip-{name} has no style")

    def test_source_proposal_labels_only_the_replay(self) -> None:
        # "source proposal" means a published depiction replayed symbolically.
        # A site mapping, an external lookup or a reported outcome is not that,
        # so the label must not appear in the dynamically rendered views.
        self.assertNotIn("chip chip-proposal", self.js)

    def test_site_mappings_are_not_labelled_as_depictions(self) -> None:
        self.assertIn("chip chip-site", self.js)

    def test_external_contributions_carry_their_own_label(self) -> None:
        self.assertIn("chip chip-external", self.js)

    def test_a_reported_outcome_is_not_labelled_a_deposited_structure(self) -> None:
        # "no detectable difference" is how a source reported an outcome. It is
        # not a deposited structure, which is what chip-structure denotes.
        self.assertIn('chip chip-nodiff">no detectable difference', self.js)
        self.assertNotIn('chip chip-structure">no detectable difference', self.js)


class ConflationGuardTest(unittest.TestCase):
    """The interface shows more than one resolution. Keep them apart."""

    def test_structure_observations_disclaim_a_deposited_structure(self) -> None:
        js = _read("app.js")
        self.assertIn("names no deposited structure", js)

    def test_distinct_resolutions_come_from_distinct_records(self) -> None:
        from catalytic_earth.workbench.adapter import evidence_view

        view = evidence_view("H297N")
        reference = {
            structure["resolution_angstrom"]
            for relation in view["relations"]
            for structure in (relation["protein_structure_context"] or {}).get(
                "structures", []
            )
        }
        reported = {
            condition["value"]
            for observation in view["observations"]
            for condition in observation.get("conditions", [])
            if "resolution" in condition["name"]
        }
        # Both are present and they are not the same number, so the interface
        # must never let one stand in for the other.
        self.assertTrue(reference)
        self.assertTrue(reported)
        self.assertFalse(reference & reported)

    def test_structure_observation_carries_no_deposited_accession(self) -> None:
        from catalytic_earth.workbench.adapter import evidence_view

        for observation in evidence_view("H297N")["observations"]:
            if observation["endpoint"]["kind"] != "structure":
                continue
            joined = " ".join(str(key) for key in observation)
            self.assertNotIn("pdb", joined.lower())


class AbstentionVisibilityTest(unittest.TestCase):
    def test_mandatory_abstentions_reach_the_interface(self) -> None:
        from catalytic_earth.workbench.adapter import evidence_view

        abstentions = evidence_view("H297N")["abstentions"]
        self.assertTrue(abstentions)
        ids = {entry.get("abstention_id") for entry in abstentions}
        # The structure-applicability abstention is the one that keeps the
        # reference structure from being read as the variant's structure.
        self.assertIn("structure-applicability", ids)

    def test_abstentions_are_not_hidden_behind_a_closed_disclosure(self) -> None:
        html = _read("index.html")
        js = _read("app.js")
        self.assertIn('id="abstention-strip"', html)
        self.assertIn("abstention-strip", js)
        # The strip sits outside the collapsed details element.
        strip = html.index('id="abstention-strip"')
        detail = html.index('id="evidence-detail"')
        self.assertLess(strip, detail)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
