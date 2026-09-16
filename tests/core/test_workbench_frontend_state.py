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

    def test_the_pattern_generation_advances_before_validation(self) -> None:
        # A refused attempt must still retire any request in flight. If the
        # counter advanced only after validation, the refusal would return
        # early and an older response would land on top of its message.
        body = self.js[self.js.index("function runPattern") :][:3000]
        self.assertLess(
            body.index("++state.patternRequest"),
            body.index("invalid.length"),
        )
        self.assertEqual(body.count("++state.patternRequest"), 1)

    def test_obsolete_errors_cannot_replace_current_state(self) -> None:
        for loader in ("loadMechanism", "loadEvidence", "runPattern"):
            body = self.js[self.js.index(f"function {loader}") :][:2600]
            catch = body[body.index("catch") :]
            self.assertIn("if (stale()) return;", catch[:160], loader)

    def test_the_selected_mechanism_commits_with_its_results(self) -> None:
        body = self.js[self.js.index("function loadMechanism") :][:2600]
        guard = body.index("if (stale()) return;")
        self.assertLess(guard, body.index("state.mcsaId = mcsaId;"))


class FailureRecoveryTest(unittest.TestCase):
    """A failed request must not leave controls describing something else."""

    def setUp(self) -> None:
        self.js = APP.read_text(encoding="utf-8")
        self.html = Path(
            "src/catalytic_earth/workbench/static/index.html"
        ).read_text(encoding="utf-8")

    def test_failure_notices_have_somewhere_to_go(self) -> None:
        for node in ("mechanism-notice", "evidence-notice"):
            self.assertIn(f'id="{node}"', self.html)
            self.assertIn(node, self.js)

    def test_a_failed_mechanism_load_restores_its_control(self) -> None:
        body = self.js[self.js.index("function loadMechanism") :][:3200]
        catch = body[body.index("} catch") :]
        self.assertIn('el("mechanism-select").value = state.mcsaId', catch)

    def test_a_failed_evidence_load_restores_its_controls(self) -> None:
        body = self.js[self.js.index("function loadEvidence") :][:3600]
        catch = body[body.index("} catch") :]
        self.assertIn("state.loadedFilters.variant", catch)
        self.assertIn("state.loadedFilters.endpoint", catch)

    def test_the_last_loaded_filters_are_tracked(self) -> None:
        self.assertIn("loadedFilters", self.js)
        body = self.js[self.js.index("function loadEvidence") :][:3600]
        self.assertIn("state.loadedFilters = { variant, endpoint };", body)


class GuidedBindingTest(unittest.TestCase):
    """The guide must stay on one case, and only claim steps that worked."""

    def setUp(self) -> None:
        self.js = APP.read_text(encoding="utf-8")

    def test_the_guided_mechanism_comes_from_the_record(self) -> None:
        # A written-in mechanism id would silently diverge from the case.
        self.assertIn("function guidedMechanismId", self.js)
        self.assertIn("transformation_binding", self.js)
        body = self.js[self.js.index("function guidedMechanismId") :][:600]
        self.assertNotIn('"M0187"', body)

    def test_case_dependent_steps_load_the_case_first(self) -> None:
        for step in ("guidedReplay", "guidedResidue", "guidedEndpoints"):
            body = self.js[self.js.index(f"function {step}") :][:900]
            self.assertIn("guidedEnsureMechanism", body, step)
            self.assertIn("return false", body, step)

    def test_the_focal_variant_is_derived_after_the_filters_settle(self) -> None:
        body = self.js[self.js.index("function guidedEndpoints") :][:1600]
        self.assertLess(body.index("await loadEvidence()"), body.index("focalVariant()"))

    def test_the_endpoint_comparison_clears_both_filters(self) -> None:
        body = self.js[self.js.index("function guidedEndpoints") :][:1600]
        self.assertIn('el("variant-select").value = ""', body)
        self.assertIn('el("endpoint-select").value = ""', body)

    def test_a_step_is_marked_done_only_on_success(self) -> None:
        body = self.js[self.js.index("GUIDED_STEPS[Number(btn.dataset.gs)]") :][:600]
        self.assertIn("=== true", body)
        self.assertNotIn("state.guidedDone[step.id] = true;", body)


class AcceptedQueryTest(unittest.TestCase):
    """Chemistry is inspected through the query its result came from."""

    def setUp(self) -> None:
        self.js = APP.read_text(encoding="utf-8")

    def test_the_accepted_query_is_captured_whole(self) -> None:
        self.assertIn("acceptedQuery", self.js)
        self.assertNotIn("lastClauses", self.js)
        body = self.js[self.js.index("state.acceptedQuery = {") :][:260]
        for field in ("clauses", "mcsa_id", "support", "generation"):
            self.assertIn(field, body)

    def test_chemistry_never_reads_live_controls(self) -> None:
        body = self.js[self.js.index("function viewMatchedChemistry") :][:1700]
        self.assertNotIn('el("pattern-mcsa")', body)
        self.assertNotIn('el("support-select")', body)
        self.assertIn("query.clauses", body)
        self.assertIn("query.mcsa_id", body)
        self.assertIn("query.support", body)

    def test_every_search_attempt_retires_open_chemistry(self) -> None:
        body = self.js[self.js.index("function runPattern") :][:2200]
        self.assertIn("state.acceptedQuery = null", body)
        self.assertIn("state.chemRequest += 1", body)
        # Before validation, so a refused attempt also retires it.
        self.assertLess(body.index("state.acceptedQuery = null"), body.index("invalid.length"))

    def test_chemistry_checks_its_parent_result_too(self) -> None:
        body = self.js[self.js.index("function viewMatchedChemistry") :][:1700]
        self.assertIn("state.acceptedQuery !== query", body)
        self.assertIn("query.generation !== state.patternRequest", body)


class PanelAnnotationTest(unittest.TestCase):
    """Highlights must follow the record, not inferred edges or matching ids."""

    def setUp(self) -> None:
        self.js = APP.read_text(encoding="utf-8")

    def test_witness_bonds_come_only_from_bond_edits(self) -> None:
        self.assertIn("witnessBonds", self.js)
        self.assertIn('String(e.operation || "").includes("bond")', self.js)
        # The old test inferred an edge from two witness endpoints.
        self.assertNotIn("witnessAtoms.has(a1) && witnessAtoms.has(a2)", self.js)

    def test_the_after_panel_is_annotated_through_the_correspondence(self) -> None:
        body = self.js[self.js.index("function renderMatchedChemistry") :][:3000]
        self.assertIn("atom_map", body)
        self.assertIn("afterBound", body)
        self.assertIn("afterWitnessBonds", body)
        self.assertIn("unmappedBound", body)

    def test_an_unmapped_bound_atom_is_disclosed(self) -> None:
        self.assertIn("no retained\n         correspondence to the after panel", self.js)

    def test_source_confirmation_is_not_styled_as_a_measurement(self) -> None:
        # chip-measured is reserved for a reported experimental value.
        self.assertIn("chip chip-confirmed", self.js)
        body = self.js[self.js.index("function renderMatchedChemistry") :]
        self.assertNotIn("chip-measured", body)


class AssociationDisplayTest(unittest.TestCase):
    """An association status is metadata, and must not be dressed as a result."""

    def setUp(self) -> None:
        self.js = APP.read_text(encoding="utf-8")
        start = self.js.index("function matchChip")
        self.chip = self.js[start : self.js.index("\n}", start)]

    def test_association_chips_do_not_borrow_the_measurement_styles(self) -> None:
        # An identifier match is not a published measurement and an identifier
        # conflict is not an experimental nondetection.
        self.assertNotIn("chip-measured", self.chip)
        self.assertNotIn("chip-nondetect", self.chip)
        for status in ("confirmed", "conflict", "external", "unresolved"):
            self.assertIn(f"chip-assoc-{status}", self.chip)

    def test_separately_sourced_context_has_its_own_label(self) -> None:
        self.assertIn("external_context", self.chip)
        self.assertIn("separately sourced context", self.chip)


class SavedResultDisplayTest(unittest.TestCase):
    """The saved output is openable, and is shown as text rather than run."""

    def setUp(self) -> None:
        self.js = APP.read_text(encoding="utf-8")

    def test_a_saved_artifact_has_an_open_control(self) -> None:
        self.assertIn("data-artifact=", self.js)
        self.assertIn("data-preview-host", self.js)
        self.assertIn("previewArtifact", self.js)

    def test_the_control_is_keyed_by_digest_not_by_path(self) -> None:
        self.assertIn("/api/result-artifact/${encodeURIComponent(sha256)}", self.js)
        self.assertNotRegex(self.js, r"result-artifact/\$\{[^}]*\.path")

    def test_imported_content_is_written_as_text_never_as_markup(self) -> None:
        body = self.js[self.js.index("async function previewArtifact") :]
        body = body[: body.index("\n}\n")]
        self.assertIn("pre.textContent = file.text", body)
        self.assertNotIn("innerHTML = file.text", body)
        self.assertNotIn("insertAdjacentHTML", body)

    def test_context_fields_are_shown_as_unverified(self) -> None:
        self.assertIn("(result.semantics || {}).context", self.js)
        self.assertIn("(result.semantics || {}).checked", self.js)


class ClauseValueTest(unittest.TestCase):
    def test_clause_values_are_parsed_exactly_not_coerced(self) -> None:
        js = APP.read_text(encoding="utf-8")
        # A bare Number() on user text turns "" into 0 and keeps fractions.
        self.assertNotIn("before: Number(c.before)", js)
        self.assertIn("clauseInteger", js)
        self.assertIn(r"^-?(0|[1-9][0-9]*)$", js)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
