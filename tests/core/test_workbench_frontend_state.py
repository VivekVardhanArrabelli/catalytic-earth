"""Guards on the Workbench frontend's state handling.

Two defect classes are cheap to reintroduce and expensive to notice: pinning a
response object so a later filter leaves stale data on screen, and installing
a slow earlier response over a later selection. The browser harness covers the
behaviour; these keep the structural invariants in the fast tier.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

APP = Path("src/catalytic_earth/workbench/static/app.js")


class SelectionStateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.js = APP.read_text(encoding="utf-8")

    def test_selection_is_held_as_an_identifier_not_a_response_object(self) -> None:
        # Holding a relation object pins the observations of the response it
        # came from, so a later filter leaves stale evidence in the inspector.
        self.assertIn("selectedFragmentId", self.js)
        self.assertNotIn("state.selectedFragment =", self.js)

    def test_the_selection_is_re_resolved_against_the_current_result(self) -> None:
        self.assertRegex(
            self.js,
            r"function selectedFragment\(\)[\s\S]{0,240}state\.evidence[\s\S]{0,160}relation_id",
        )

    def test_a_selection_without_a_relation_is_dropped(self) -> None:
        self.assertRegex(
            self.js, r"state\.selectedFragmentId\s*=\s*null;[\s\S]{0,80}\}"
        )
        self.assertIn("relations || []).some", self.js)


class RequestOrderingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.js = APP.read_text(encoding="utf-8")

    def test_each_async_loader_carries_a_generation_guard(self) -> None:
        for loader in ("loadMechanism", "loadEvidence", "runPattern"):
            body = self.js[self.js.index(f"function {loader}") :][:2600]
            self.assertIn("++state.", body, loader)
            self.assertIn("stale()", body, loader)

    def test_obsolete_errors_cannot_replace_current_state(self) -> None:
        for loader in ("loadMechanism", "loadEvidence", "runPattern"):
            body = self.js[self.js.index(f"function {loader}") :][:2600]
            catch = body[body.index("catch") :]
            self.assertIn("if (stale()) return;", catch[:160], loader)

    def test_the_selected_mechanism_commits_with_its_results(self) -> None:
        body = self.js[self.js.index("function loadMechanism") :][:2600]
        guard = body.index("if (stale()) return;")
        self.assertLess(guard, body.index("state.mcsaId = mcsaId;"))


class ClauseValueTest(unittest.TestCase):
    def test_clause_values_are_parsed_exactly_not_coerced(self) -> None:
        js = APP.read_text(encoding="utf-8")
        # A bare Number() on user text turns "" into 0 and keeps fractions.
        self.assertNotIn("before: Number(c.before)", js)
        self.assertIn("clauseInteger", js)
        self.assertIn(r"^-?(0|[1-9][0-9]*)$", js)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
