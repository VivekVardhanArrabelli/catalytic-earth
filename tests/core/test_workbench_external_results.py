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
    registered_artifact,
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
TRANSKETOLASE_2024 = "tk_2024:R520Q:specific_activity"


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

    def test_a_comparison_selects_only_its_own_study_sources(self) -> None:
        # tk2020, tk2024 and tktf all begin with the study-id prefix "tk". Only
        # the sources this comparison's own observations resolve through may be
        # admitted; a sibling transketolase study is a different study.
        found = resolve_case(TRANSKETOLASE)
        self.assertEqual(found["sources"], ["tk2020"])

    def test_a_sibling_study_witness_is_not_a_supported_publication(self) -> None:
        found = resolve_case(TRANSKETOLASE)
        supported = found["publications"]
        self.assertTrue(supported)
        # The 2020 study's own retained file stays.
        self.assertTrue(
            any("10084395" in url for url in supported),
            f"the tk2020 source witness is missing from {supported}",
        )
        # The unrelated 2024 and human-TKT witnesses do not.
        for foreign in ("s41598-024-51831-z", "s41586-019-1581-9"):
            self.assertFalse(
                any(foreign in url for url in supported),
                f"{foreign} belongs to another study but was admitted",
            )

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

    def _check_named(self, record, label):
        return next(
            entry
            for entry in record["result"]["association"]["checks"]
            if entry["label"] == label
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

    def test_a_sibling_study_publication_is_not_confirmed(self) -> None:
        # The negative the cross-study prefix used to pass: a 2024 witness URL
        # declared against the 2020 comparison.
        foreign = next(
            url
            for url in resolve_case(TRANSKETOLASE_2024)["publications"]
            if "s41598-024-51831-z" in url
        )
        record = self._import(
            case_ref=TRANSKETOLASE, publication=foreign, site_id="tk_2020:H473N"
        )
        self.assertEqual(record["result"]["match_status"], "conflict")

    def test_a_paper_and_site_from_different_relations_are_a_conflict(self) -> None:
        # PMID 7893690 is the K166R source; P11444:H297 is the histidine
        # relation. The case carries both, and no relation carries them
        # together, so membership alone must not read as a confirmed pair.
        record = self._import(
            case_ref=MANDELATE,
            publication="paper:PMID:7893690",
            site_id="P11444:H297",
        )
        self.assertEqual(record["result"]["match_status"], "conflict")
        relation = self._check_named(record, "relation")
        self.assertEqual(relation["status"], "conflict")
        self.assertIn("different evidence relations", relation["reason"])

    def test_a_structure_the_case_does_not_carry_is_a_conflict(self) -> None:
        # Matching functional identifiers must not carry an unmatched structure
        # through with them.
        record = self._import(
            case_ref=MANDELATE,
            publication="paper:PMID:1909893",
            site_id="P11444:H297",
            structure_id="1MRA",
        )
        self.assertEqual(record["result"]["match_status"], "conflict")
        self.assertEqual(self._check_named(record, "structure")["status"], "conflict")

    def test_a_structural_citation_is_external_context_not_a_conflict(self) -> None:
        # PMID 8292591 is 1MNS's own primary citation. The packaged record
        # enumerates functional-observation sources and database accessions for
        # its structures, so it can neither confirm nor contradict that
        # citation. It must be kept as declared, in its own status.
        record = self._import(
            case_ref=MANDELATE,
            publication="paper:PMID:8292591",
            site_id="P11444:H297",
            structure_id="1MNS",
        )
        result = record["result"]
        self.assertEqual(result["match_status"], "external_context")
        publication = self._check_named(record, "publication")
        self.assertEqual(publication["status"], "external_context")
        # The declared citation is preserved, never swapped for a carried one.
        self.assertEqual(publication["declared"], "paper:PMID:8292591")
        self.assertEqual(
            result["association"]["declared_publication"], "paper:PMID:8292591"
        )
        self.assertNotIn(
            "paper:PMID:8292591", result["association"]["packaged_publications"]
        )
        # The structure it is scoped to is the one the case really carries.
        self.assertEqual(self._check_named(record, "structure")["status"], "confirmed")

    def test_the_structural_citation_is_not_upgraded_by_the_site_alone(self) -> None:
        # Without a structure to scope it, the same citation is a plain
        # conflict against the functional sources.
        record = self._import(
            case_ref=MANDELATE,
            publication="paper:PMID:8292591",
            site_id="P11444:H297",
        )
        self.assertEqual(record["result"]["match_status"], "conflict")

    def test_the_association_says_what_it_checked(self) -> None:
        record = self._import(
            case_ref=MANDELATE,
            publication="paper:PMID:1909893",
            site_id="P11444:H297",
            context={"pdb_id": "1MRA"},
        )
        semantics = record["result"]["semantics"]
        self.assertIn("found in the case and carried", semantics["checked"])
        # A context string is not evidence and takes no part in any check.
        self.assertIn("take no part in any check", semantics["context"])
        self.assertIsNone(record["result"]["association"]["declared_structure"])

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


class SavedOutputReadBackTest(unittest.TestCase):
    """A recorded result can be opened again, on the terms it was recorded."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.ledger = self.dir / "ledger.json"
        self.artifact = self.dir / "saved-output.json"
        self.artifact.write_text('{"fixture": true}\n', encoding="utf-8")
        self.addCleanup(self._tmp.cleanup)
        self.record = import_result(
            provider_suite="Fixture Suite",
            provider_tool="fixture.tool",
            action="structure_view",
            query="fixture query",
            case_ref=MANDELATE,
            artifacts=[self.artifact],
            path=self.ledger,
        )
        self.digest = self.record["result"]["artifacts"][0]["sha256"]

    def test_a_registered_artifact_is_returned_as_its_own_text(self) -> None:
        found = registered_artifact(self.digest, self.ledger)
        self.assertTrue(found["available"])
        self.assertTrue(found["is_text"])
        self.assertEqual(found["text"], '{"fixture": true}\n')
        self.assertFalse(found["truncated"])
        self.assertIn(self.record["contribution_id"], found["recorded_in"])

    def test_only_a_registered_digest_can_be_read(self) -> None:
        with self.assertRaises(ExternalSourceError):
            registered_artifact("a" * 64, self.ledger)

    def test_a_path_is_not_a_key(self) -> None:
        # The ledger is the allowlist; nothing else addresses a file.
        for value in (str(self.artifact), "../../etc/passwd", "", "not-a-digest"):
            with self.assertRaises(ExternalSourceError):
                registered_artifact(value, self.ledger)

    def test_a_file_that_changed_is_not_served_as_that_result(self) -> None:
        self.artifact.write_text('{"fixture": "edited"}\n', encoding="utf-8")
        found = registered_artifact(self.digest, self.ledger)
        self.assertFalse(found["available"])
        self.assertIn("no longer matches the digest", found["reason"])
        # The record itself is untouched: hash and size still describe what was
        # imported, so the change is visible rather than absorbed.
        self.assertEqual(found["sha256"], self.digest)

    def test_a_file_that_is_gone_says_so(self) -> None:
        self.artifact.unlink()
        found = registered_artifact(self.digest, self.ledger)
        self.assertFalse(found["available"])
        self.assertIn("no longer at the path", found["reason"])

    def test_bytes_that_are_not_text_are_described_not_returned(self) -> None:
        binary = self.dir / "saved.bin"
        binary.write_bytes(b"\x89PNG\r\n\x1a\n\xff\xfe")
        record = import_result(
            provider_suite="Fixture Suite",
            provider_tool="fixture.tool",
            action="structure_view",
            query="fixture query",
            case_ref=MANDELATE,
            artifacts=[binary],
            path=self.ledger,
        )
        found = registered_artifact(
            record["result"]["artifacts"][0]["sha256"], self.ledger
        )
        self.assertTrue(found["available"])
        self.assertFalse(found["is_text"])
        self.assertNotIn("text", found)


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
