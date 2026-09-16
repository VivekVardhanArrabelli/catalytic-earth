"""Checks for the Workbench external tool contribution ledger.

The ledger exists so an external research suite can be credited for the work
it actually did, separately from local Python calculations, and so the suite
behind a contribution can be swapped without touching the interface.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.workbench.external_sources import (
    ACTIONS,
    DEFAULT_LEDGER_PATH,
    ExternalSourceError,
    ledger_view,
    load_ledger,
    record_contribution,
)

VALID = {
    "provider_suite": "Example Suite",
    "provider_tool": "example.search",
    "action": "literature_lookup",
    "query": "mandelate racemase H297N",
}


class EmptyLedgerTest(unittest.TestCase):
    def test_missing_ledger_reads_as_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            view = ledger_view(Path(tmp) / "absent.json")
        self.assertEqual(view["contribution_count"], 0)
        self.assertEqual(view["contributions"], [])
        self.assertIsNone(view["active_provider"])
        self.assertEqual(view["providers_used"], [])

    def test_empty_is_not_described_as_a_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            semantics = ledger_view(Path(tmp) / "absent.json")["semantics"]
        self.assertIn("not a receipt", semantics["empty_means"])

    def test_repository_ledger_holds_no_unearned_contribution(self) -> None:
        # Any row here must come from a call that actually happened. A
        # placeholder or example row committed to the repository would be a
        # fabricated plugin receipt.
        if not DEFAULT_LEDGER_PATH.is_file():
            self.skipTest("no repository ledger file yet")
        for record in load_ledger(DEFAULT_LEDGER_PATH)["contributions"]:
            self.assertTrue(record["provider_suite"].strip())
            self.assertTrue(record["provider_tool"].strip())
            self.assertEqual(record["origin"], "external_tool_call")
            self.assertFalse(record["changes_packaged_claim"])


class RecordingTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "ledger.json"
        self.addCleanup(self._tmp.cleanup)

    def test_contribution_round_trips(self) -> None:
        record = record_contribution(
            **VALID, retrieved=["PMID:1909893"], subject="paper:PMID:1909893",
            path=self.path,
        )
        self.assertEqual(record["origin"], "external_tool_call")
        self.assertFalse(record["changes_packaged_claim"])
        self.assertEqual(record["result_count"], 1)

        view = ledger_view(self.path)
        self.assertEqual(view["contribution_count"], 1)
        self.assertEqual(view["active_provider"], "Example Suite")
        self.assertEqual(
            view["contributions_by_subject"]["paper:PMID:1909893"],
            [record["contribution_id"]],
        )

    def test_a_call_that_returned_nothing_is_recorded_as_nothing(self) -> None:
        record = record_contribution(**VALID, retrieved=[], path=self.path)
        self.assertEqual(record["result_count"], 0)
        self.assertEqual(record["retrieved"], [])

    def test_unattributed_contributions_are_refused(self) -> None:
        for field in ("provider_suite", "provider_tool", "query"):
            for blank in ("", "   "):
                payload = dict(VALID, **{field: blank})
                with self.assertRaises(ExternalSourceError):
                    record_contribution(**payload, path=self.path)

    def test_unknown_actions_are_refused(self) -> None:
        with self.assertRaises(ExternalSourceError):
            record_contribution(**dict(VALID, action="wet_lab_experiment"), path=self.path)
        with self.assertRaises(ExternalSourceError):
            record_contribution(**dict(VALID, action="local_calculation"), path=self.path)

    def test_actions_stay_limited_to_workflow_lookups(self) -> None:
        self.assertEqual(
            set(ACTIONS), {"literature_lookup", "database_lookup", "structure_view"}
        )

    def test_retrieved_entries_must_be_real_strings(self) -> None:
        for bad in ([""], ["  "], [None], [3]):
            with self.assertRaises(ExternalSourceError):
                record_contribution(**VALID, retrieved=bad, path=self.path)

    def test_appending_preserves_earlier_contributions(self) -> None:
        first = record_contribution(**VALID, path=self.path)
        second = record_contribution(
            **dict(VALID, provider_suite="Other Suite"), path=self.path
        )
        view = ledger_view(self.path)
        self.assertEqual(view["contribution_count"], 2)
        self.assertEqual(view["providers_used"], ["Example Suite", "Other Suite"])
        ids = [entry["contribution_id"] for entry in view["contributions"]]
        self.assertEqual(ids, [first["contribution_id"], second["contribution_id"]])

    def test_provider_can_be_swapped_without_losing_prior_credit(self) -> None:
        # Swapping the suite must not rewrite who did the earlier work.
        record_contribution(**VALID, path=self.path)
        record_contribution(**dict(VALID, provider_suite="Rosalind"), path=self.path)
        view = ledger_view(self.path)
        self.assertEqual(view["active_provider"], "Rosalind")
        self.assertEqual(view["contributions"][0]["provider_suite"], "Example Suite")

    def test_a_corrupt_ledger_is_reported_not_silently_reset(self) -> None:
        self.path.write_text("{not json", encoding="utf-8")
        with self.assertRaises(ExternalSourceError):
            load_ledger(self.path)

    def test_an_unsupported_schema_is_refused(self) -> None:
        self.path.write_text(json.dumps({"schema_version": "other"}), encoding="utf-8")
        with self.assertRaises(ExternalSourceError):
            load_ledger(self.path)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
