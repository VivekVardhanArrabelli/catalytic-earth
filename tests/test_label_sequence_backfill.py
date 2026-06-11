"""Offline validation of the expansion-label sequence backfill.

No network: the UniProt sequence fetcher is injected with a dict of synthetic records
shaped like ``adapters.normalize_uniprot_tsv`` output, so the full chain (collect needed
accessions -> fetch -> add evidence.sequence_provenance -> write expansion registry) is
exercised and the guardrails (frozen never written, row count unchanged, leakage-safe,
length-conflict notes, idempotency, fetch-miss never fabricated) are asserted.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.external_annotation_anchored_import import _dump_registry
from catalytic_earth.label_sequence_backfill import (
    build_label_sequence_backfill,
    fetch_uniprot_sequences,
    summarize_backfill,
    write_label_sequence_backfill,
)
from catalytic_earth.labels import MechanismLabel


def _expansion_row(accession, *, label_type="seed_fingerprint", fingerprint="metallopeptidase",
                   sequence_length=120):
    fingerprint_id = fingerprint if label_type == "seed_fingerprint" else None
    evidence = {
        "sources": ["external_cofactor_ec_disambiguation"],
        "cofactor_evidence_level": "annotated",
        "conflicts": [],
        "evidence_basis": "reviewed_swissprot_ec_rhea_cofactor_annotation",
        "excluded_context": ["protein_name", "ec_label", "uniprot_prose", "target_family_lane"],
        "import_gate_evidence": [
            "reviewed_swissprot_entry",
            "annotation_anchored_scope_assignment",
        ],
        "migration": "label_factory_v1_default",
        "notes": ["annotation-anchored bronze"],
        "predictive_evidence": [],
        "review_only_context": ["accession_identity", "protein_name", "ec_label"],
        "source_provenance": {"accession": accession, "sequence_length": sequence_length},
    }
    return {
        "confidence": "high",
        "entry_id": f"uniprot:{accession}",
        "evidence": evidence,
        "evidence_score": 0.8,
        "fingerprint_id": fingerprint_id,
        "label_type": label_type,
        "ontology_version_at_decision": "label_factory_v1_8fp",
        "rationale": (
            f"{accession} imported as annotation-anchored bronze; EC/name/prose excluded "
            "from predictive features."
        ),
        "review_status": "automation_curated",
        "tier": "bronze",
    }


def _record(accession, sequence, *, reviewed="reviewed"):
    return {"accession": accession, "sequence": sequence, "length": len(sequence),
            "reviewed": reviewed}


class BuildBackfillTests(unittest.TestCase):
    def test_backfills_seed_and_oos_with_sequence_provenance(self) -> None:
        rows = [
            _expansion_row("P00001", sequence_length=4),
            _expansion_row("P00002", label_type="out_of_scope", fingerprint=None, sequence_length=3),
        ]
        sequences = {"P00001": _record("P00001", "MKLA"), "P00002": _record("P00002", "MAA")}
        audit = build_label_sequence_backfill(
            expansion_payload=rows, sequences=sequences, created_utc="2026-06-11T00:00:00Z"
        )
        self.assertEqual(audit["counts"]["backfilled_this_run"], 2)
        self.assertEqual(audit["counts"]["fetch_missing"], 0)
        self.assertEqual(audit["counts"]["rows_with_sequence_after"], 2)
        for original, new in zip(rows, audit["backfilled_registry"]):
            provenance = new["evidence"]["sequence_provenance"]
            accession = new["entry_id"].split(":", 1)[1]
            self.assertEqual(provenance["source_accession"], accession)
            self.assertEqual(provenance["source"], "reviewed_uniprot")
            self.assertEqual(provenance["sequence"], sequences[accession]["sequence"])
            self.assertEqual(
                provenance["sequence_sha256"],
                hashlib.sha256(sequences[accession]["sequence"].encode()).hexdigest(),
            )
            self.assertEqual(provenance["retrieved_utc"], "2026-06-11T00:00:00Z")
            # The leakage wall is unchanged: sequence is data, not a predictive feature.
            self.assertEqual(new["evidence"]["predictive_evidence"], [])
            self.assertNotIn("sequence_provenance", new["evidence"]["excluded_context"])
            # Round-trips through the canonical (leakage-aware) schema for both types.
            MechanismLabel.from_dict(new)

    def test_row_count_unchanged_and_frozen_untouched_flags(self) -> None:
        rows = [_expansion_row("P00001")]
        audit = build_label_sequence_backfill(
            expansion_payload=rows, sequences={"P00001": _record("P00001", "MK")},
        )
        self.assertEqual(len(audit["backfilled_registry"]), len(rows))
        self.assertTrue(audit["guardrails"]["row_count_unchanged"])
        self.assertTrue(audit["guardrails"]["frozen_current702_benchmark_preserved"])
        self.assertTrue(audit["guardrails"]["writes_expansion_registry_only"])

    def test_length_conflict_recorded_not_overwritten(self) -> None:
        # Stored sequence_length disagrees with the fetched sequence length.
        rows = [_expansion_row("P00001", sequence_length=999)]
        audit = build_label_sequence_backfill(
            expansion_payload=rows, sequences={"P00001": _record("P00001", "MKLA")},
        )
        self.assertEqual(audit["counts"]["length_conflicts"], 1)
        provenance = audit["backfilled_registry"][0]["evidence"]["sequence_provenance"]
        self.assertEqual(provenance["sequence_length"], 4)
        self.assertEqual(provenance["source_provenance_sequence_length"], 999)
        self.assertIn("length_conflict_note", provenance)
        # Stored provenance length is preserved (never overwritten).
        stored = audit["backfilled_registry"][0]["evidence"]["source_provenance"]
        self.assertEqual(stored["sequence_length"], 999)

    def test_fetch_miss_leaves_row_unchanged_and_is_recorded(self) -> None:
        rows = [_expansion_row("P00001"), _expansion_row("P00002")]
        audit = build_label_sequence_backfill(
            expansion_payload=rows, sequences={"P00001": _record("P00001", "MK")},
        )
        self.assertEqual(audit["counts"]["backfilled_this_run"], 1)
        self.assertEqual(audit["counts"]["fetch_missing"], 1)
        self.assertEqual(audit["fetch_failures"], ["P00002"])
        # The missing row is unchanged -- no sequence is ever fabricated.
        self.assertNotIn(
            "sequence_provenance", audit["backfilled_registry"][1]["evidence"]
        )

    def test_idempotent_skip_of_already_backfilled_rows(self) -> None:
        rows = [_expansion_row("P00001")]
        first = build_label_sequence_backfill(
            expansion_payload=rows, sequences={"P00001": _record("P00001", "MK")},
        )
        # Re-run over the already-backfilled output with NO fetch source available.
        second = build_label_sequence_backfill(
            expansion_payload=first["backfilled_registry"], sequences={},
        )
        self.assertEqual(second["counts"]["already_backfilled"], 1)
        self.assertEqual(second["counts"]["backfilled_this_run"], 0)
        self.assertEqual(second["counts"]["needed_fetch"], 0)


class FetchCacheTests(unittest.TestCase):
    def test_fetch_uses_cache_and_only_requests_missing(self) -> None:
        calls = []

        def fake_batch_fetcher(batch):
            calls.append(list(batch))
            return [_record(a, "M" * (len(a))) for a in batch]

        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            first = fetch_uniprot_sequences(
                ["P00001", "P00002"], batch_fetcher=fake_batch_fetcher, cache_path=cache_path
            )
            self.assertEqual(set(first), {"P00001", "P00002"})
            self.assertEqual(len(calls), 1)
            # Second call: cache satisfies P00001; only P00003 is fetched.
            calls.clear()
            second = fetch_uniprot_sequences(
                ["P00001", "P00003"], batch_fetcher=fake_batch_fetcher, cache_path=cache_path
            )
            self.assertEqual(set(second), {"P00001", "P00003"})
            self.assertEqual(calls, [["P00003"]])


class WriteApplyTests(unittest.TestCase):
    def _fetcher(self, mapping):
        def fetcher(accessions, *, batch_size, cache_path=None):
            return {a: _record(a, mapping[a]) for a in accessions if a in mapping}
        return fetcher

    def test_preview_is_non_destructive_apply_writes_expansion_only(self) -> None:
        rows = [_expansion_row("P00001", sequence_length=2)]
        mapping = {"P00001": "MK"}
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            expansion_path = tmp / "expansion.json"
            expansion_path.write_text(_dump_registry(rows), encoding="utf-8")
            frozen_path = tmp / "frozen.json"
            frozen_bytes = _dump_registry([])
            frozen_path.write_text(frozen_bytes, encoding="utf-8")
            out_path = tmp / "preview.json"
            report_path = tmp / "report.md"

            # Patch the live fetcher via the module-level default.
            import catalytic_earth.label_sequence_backfill as mod

            original = mod.fetch_uniprot_sequences
            mod.fetch_uniprot_sequences = self._fetcher(mapping)
            try:
                preview = write_label_sequence_backfill(
                    out_path=out_path,
                    report_path=report_path,
                    expansion_registry_path=expansion_path,
                    frozen_benchmark_path=frozen_path,
                    apply=False,
                    cache_path=None,
                )
                # Preview: expansion registry untouched (still no sequence_provenance).
                self.assertFalse(preview["expansion_registry_written"])
                before = json.loads(expansion_path.read_text(encoding="utf-8"))
                self.assertNotIn("sequence_provenance", before[0]["evidence"])
                self.assertTrue(out_path.exists())
                self.assertTrue(report_path.exists())
                # The summary artifact never embeds the full registry payload.
                summary = json.loads(out_path.read_text(encoding="utf-8"))
                self.assertNotIn("backfilled_registry", summary)

                applied = write_label_sequence_backfill(
                    out_path=out_path,
                    report_path=report_path,
                    expansion_registry_path=expansion_path,
                    frozen_benchmark_path=frozen_path,
                    apply=True,
                    cache_path=None,
                )
                self.assertTrue(applied["expansion_registry_written"])
                self.assertFalse(applied["frozen_benchmark_registry_written"])
                # Frozen benchmark byte-unchanged.
                self.assertEqual(frozen_path.read_text(encoding="utf-8"), frozen_bytes)
                # Expansion registry now carries the sequence, same row count.
                after = json.loads(expansion_path.read_text(encoding="utf-8"))
                self.assertEqual(len(after), len(rows))
                self.assertEqual(
                    after[0]["evidence"]["sequence_provenance"]["sequence"], "MK"
                )
                # Re-serialized with the canonical compact serializer.
                self.assertEqual(
                    expansion_path.read_text(encoding="utf-8"), _dump_registry(after)
                )
            finally:
                mod.fetch_uniprot_sequences = original

    def test_refuses_to_target_frozen_benchmark(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frozen_path = Path(tmp) / "frozen.json"
            frozen_path.write_text(_dump_registry([]), encoding="utf-8")
            with self.assertRaises(ValueError):
                write_label_sequence_backfill(
                    out_path=Path(tmp) / "preview.json",
                    report_path=None,
                    expansion_registry_path=frozen_path,
                    frozen_benchmark_path=frozen_path,
                    apply=True,
                    cache_path=None,
                )

    def test_summarize_drops_full_registry(self) -> None:
        rows = [_expansion_row("P00001")]
        audit = build_label_sequence_backfill(
            expansion_payload=rows, sequences={"P00001": _record("P00001", "MK")},
        )
        summary = summarize_backfill(audit)
        self.assertIn("counts", summary)
        self.assertNotIn("backfilled_registry", summary)


if __name__ == "__main__":
    unittest.main()
