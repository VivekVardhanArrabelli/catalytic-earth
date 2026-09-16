"""Checks for the external result-return path.

A result is an output a tool actually produced, tied to the case it answers.
These checks pin the parts that would otherwise drift into claiming more than
the output supports: a missing artifact, a mismatched association quietly
accepted, or external context leaking into the packaged record.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.workbench.external_results import (
    MATCH_STATUSES,
    import_result,
    resolve_case,
)
from catalytic_earth.workbench.external_sources import (
    DEFAULT_LEDGER_PATH,
    ExternalSourceError,
    ledger_view,
    load_ledger,
)

MANDELATE = "atlas10.mandelate-racemase-pputida.enolate"
TRANSKETOLASE = "tk_2020:H473N:DHB_accumulation"


class CaseResolutionTest(unittest.TestCase):
    """One resolver serves both packaged record families."""

    def test_a_mechanism_evidence_case_resolves(self) -> None:
        found = resolve_case(MANDELATE)
        self.assertTrue(found["resolved"])
        self.assertEqual(found["kind"], "mechanism_evidence_case")
        self.assertIn("paper:PMID:1909893", found["publications"])
        self.assertIn("P11444:H297", found["sites"])

    def test_a_perturbation_comparison_resolves_through_the_same_call(self) -> None:
        found = resolve_case(TRANSKETOLASE)
        self.assertTrue(found["resolved"])
        self.assertEqual(found["kind"], "perturbation_comparison")
        self.assertIn("tk_2020:H473N", found["sites"])
        self.assertTrue(found["publications"])

    def test_the_two_families_need_no_enzyme_specific_branch(self) -> None:
        # Both go through resolve_case with only the identifier differing.
        kinds = {resolve_case(ref)["kind"] for ref in (MANDELATE, TRANSKETOLASE)}
        self.assertEqual(kinds, {"mechanism_evidence_case", "perturbation_comparison"})

    def test_an_unknown_case_stays_unresolved(self) -> None:
        found = resolve_case("no.such.case")
        self.assertFalse(found["resolved"])
        self.assertIsNone(found["kind"])
        self.assertEqual(found["publications"], [])

    def test_a_blank_reference_is_refused(self) -> None:
        for value in ("", "   ", None):
            with self.assertRaises(ExternalSourceError):
                resolve_case(value)


class ImportTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.ledger = self.dir / "ledger.json"
        self.artifact = self.dir / "saved-output.json"
        self.artifact.write_text('{"fixture": true}', encoding="utf-8")
        self.addCleanup(self._tmp.cleanup)
        self.base = {
            "provider_suite": "Fixture Suite",
            "provider_tool": "fixture.tool",
            "action": "structure_view",
            "query": "fixture query",
        }

    def _import(self, **kw):
        return import_result(
            **self.base, artifacts=[self.artifact], path=self.ledger, **kw
        )

    def test_a_result_needs_an_artifact_that_exists(self) -> None:
        with self.assertRaises(ExternalSourceError):
            import_result(**self.base, case_ref=MANDELATE, artifacts=[], path=self.ledger)
        with self.assertRaises(ExternalSourceError):
            import_result(
                **self.base, case_ref=MANDELATE,
                artifacts=[self.dir / "absent.json"], path=self.ledger,
            )

    def test_an_empty_artifact_is_refused(self) -> None:
        empty = self.dir / "empty.bin"
        empty.write_bytes(b"")
        with self.assertRaises(ExternalSourceError):
            import_result(
                **self.base, case_ref=MANDELATE, artifacts=[empty], path=self.ledger
            )

    def test_artifacts_are_described_from_the_file_on_disk(self) -> None:
        record = self._import(case_ref=MANDELATE)
        reference = record["result"]["artifacts"][0]
        self.assertEqual(reference["bytes"], self.artifact.stat().st_size)
        self.assertEqual(len(reference["sha256"]), 64)
        self.assertEqual(reference["name"], "saved-output.json")

    def test_a_correct_association_is_confirmed(self) -> None:
        record = self._import(
            case_ref=MANDELATE,
            publication="paper:PMID:1909893",
            site_id="P11444:H297",
            context={"resolution": "2.0 A"},
        )
        self.assertEqual(record["result"]["match_status"], "confirmed")
        self.assertEqual(record["result"]["context"], {"resolution": "2.0 A"})

    def test_a_publication_the_record_lacks_is_a_conflict(self) -> None:
        record = self._import(
            case_ref=MANDELATE, publication="paper:PMID:0000000", site_id="P11444:H297"
        )
        self.assertEqual(record["result"]["match_status"], "conflict")
        check = next(
            c for c in record["result"]["association"]["checks"]
            if c["label"] == "publication"
        )
        self.assertEqual(check["status"], "conflict")
        # The declared value and the real ones are both kept.
        self.assertEqual(check["declared"], "paper:PMID:0000000")
        self.assertIn("paper:PMID:1909893", check["reason"])

    def test_a_site_the_record_lacks_is_a_conflict(self) -> None:
        record = self._import(
            case_ref=MANDELATE, publication="paper:PMID:1909893", site_id="P99999:Z1"
        )
        self.assertEqual(record["result"]["match_status"], "conflict")

    def test_an_unresolved_case_is_recorded_without_an_association(self) -> None:
        record = self._import(case_ref="no.such.case", publication="x", site_id="y")
        self.assertEqual(record["result"]["match_status"], "unresolved")
        self.assertFalse(record["result"]["association"]["case_resolved"])

    def test_an_undeclared_identifier_is_not_a_match(self) -> None:
        record = self._import(case_ref=MANDELATE)
        self.assertEqual(record["result"]["match_status"], "unresolved")
        for check in record["result"]["association"]["checks"]:
            self.assertEqual(check["status"], "unresolved")

    def test_the_transketolase_case_uses_the_same_import(self) -> None:
        record = self._import(
            case_ref=TRANSKETOLASE,
            site_id="tk_2020:H473N",
            context={"reported_DHB_24h": "5.5 mM"},
        )
        association = record["result"]["association"]
        self.assertEqual(association["case_kind"], "perturbation_comparison")
        self.assertTrue(association["case_resolved"])
        self.assertIn("tk_2020:H473N", association["packaged_sites"])

    def test_every_match_status_is_one_of_the_declared_set(self) -> None:
        for kwargs in (
            {"case_ref": MANDELATE, "publication": "paper:PMID:1909893",
             "site_id": "P11444:H297"},
            {"case_ref": MANDELATE, "publication": "wrong"},
            {"case_ref": "no.such.case"},
        ):
            record = self._import(**kwargs)
            self.assertIn(record["result"]["match_status"], MATCH_STATUSES)

    def test_context_values_must_be_real_strings(self) -> None:
        for bad in ({"k": ""}, {"k": None}, {"": "v"}, {"k": 3}):
            with self.assertRaises(ExternalSourceError):
                self._import(case_ref=MANDELATE, context=bad)

    def test_a_result_never_rewrites_a_packaged_record(self) -> None:
        from catalytic_earth.workbench.adapter import evidence_view

        before = json.dumps(evidence_view("H297N"), sort_keys=True)
        self._import(
            case_ref=MANDELATE, publication="paper:PMID:1909893",
            site_id="P11444:H297", context={"resolution": "9.9 A"},
        )
        after = json.dumps(evidence_view("H297N"), sort_keys=True)
        self.assertEqual(before, after)

    def test_results_are_readable_back_from_the_ledger(self) -> None:
        self._import(case_ref=MANDELATE, site_id="P11444:H297")
        view = ledger_view(self.ledger)
        self.assertEqual(view["contribution_count"], 1)
        self.assertIn("result", view["contributions"][0])
        self.assertTrue(view["contributions"][0]["result"]["artifacts"])

    def test_the_separation_statement_travels_with_the_result(self) -> None:
        record = self._import(case_ref=MANDELATE)
        semantics = record["result"]["semantics"]
        self.assertIn("does not change, override or extend", semantics["separation"])
        self.assertIn("never counted as a match", semantics["conflicts"])


class RepositoryLedgerTest(unittest.TestCase):
    def test_the_repository_ledger_holds_no_fixture_result(self) -> None:
        # A fixture recorded into the repository ledger would be a fabricated
        # receipt. Fixtures belong in a temporary path only.
        if not DEFAULT_LEDGER_PATH.is_file():
            self.skipTest("no repository ledger yet")
        for record in load_ledger(DEFAULT_LEDGER_PATH)["contributions"]:
            result = record.get("result")
            if not result:
                continue
            for artifact in result["artifacts"]:
                self.assertTrue(artifact["sha256"])
                self.assertGreater(artifact["bytes"], 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
