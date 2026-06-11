"""Offline validation of the AlphaFoldDB v6 coordinate staging backfill (Track 1 / 1b).

No network: the AFDB CIF fetcher is injected with synthetic CIF text (or None for a 404),
so the full chain (derive handle -> stage to temp -> hash -> record
structure_provenance.afdb_v6_coordinate -> write expansion registry) is exercised and the
guardrails (frozen never written, row count unchanged, large CIFs never committed,
additive to existing structure_provenance, resumable cache, idempotency) are asserted.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.external_annotation_anchored_import import _dump_registry
from catalytic_earth.label_structure_backfill import (
    STAGED_STATUS,
    UNAVAILABLE_STATUS,
    build_label_structure_backfill,
    stage_afdb_v6_coordinate,
    write_label_structure_backfill,
)
from catalytic_earth.labels import MechanismLabel

_CIF = "data_AF\nATOM 1 N . MET A 1\nATOM 2 CA . MET A 1\nHETATM 3 ZN . ZN B 1\n"


def _expansion_row(accession, *, label_type="seed_fingerprint", fingerprint="metallopeptidase",
                   existing_structure=None):
    structure = existing_structure or {
        "alphafold_ids": [accession],
        "structure_handle": f"AF-{accession}-F1",
        "coordinate_status": "afdb_predicted_coordinate_provenance_available",
        "coordinate_path": None,
        "pdb_ids": [],
    }
    evidence = {
        "sources": ["external_cofactor_ec_disambiguation"],
        "conflicts": [],
        "excluded_context": ["protein_name", "ec_label", "uniprot_prose", "target_family_lane"],
        "import_gate_evidence": ["reviewed_swissprot_entry", "annotation_anchored_scope_assignment"],
        "migration": "label_factory_v1_default",
        "notes": ["annotation-anchored bronze"],
        "predictive_evidence": [],
        "review_only_context": ["accession_identity", "protein_name", "ec_label"],
        "source_provenance": {"accession": accession, "sequence_length": 3},
        "structure_provenance": structure,
    }
    return {
        "confidence": "high",
        "entry_id": f"uniprot:{accession}",
        "evidence": evidence,
        "evidence_score": 0.8,
        "fingerprint_id": fingerprint if label_type == "seed_fingerprint" else None,
        "label_type": label_type,
        "ontology_version_at_decision": "label_factory_v1_8fp",
        "rationale": (
            f"{accession} imported as annotation-anchored bronze; EC/name/prose excluded "
            "from predictive features."
        ),
        "review_status": "automation_curated",
        "tier": "bronze",
    }


def _fetcher(mapping):
    return lambda accession: mapping.get(accession)


class StageCoordinateTests(unittest.TestCase):
    def test_stages_and_hashes_without_keeping_the_cif(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            staging = Path(tmp)
            provenance = stage_afdb_v6_coordinate(
                "P00001",
                cif_fetcher=_fetcher({"P00001": _CIF}),
                retrieved_utc="2026-06-11T00:00:00Z",
                staging_dir=staging,
            )
            self.assertEqual(provenance["status"], STAGED_STATUS)
            self.assertEqual(provenance["structure_handle"], "AF-P00001-F1")
            self.assertEqual(
                provenance["coordinate_sha256"],
                hashlib.sha256(_CIF.encode()).hexdigest(),
            )
            self.assertEqual(provenance["coordinate_bytes"], len(_CIF.encode()))
            self.assertEqual(provenance["atom_record_count"], 3)
            self.assertFalse(provenance["coordinate_committed"])
            # The staged CIF is discarded -- the staging dir holds no .cif.
            self.assertEqual(list(staging.glob("*.cif")), [])

    def test_unavailable_records_404_status(self) -> None:
        provenance = stage_afdb_v6_coordinate(
            "P00002", cif_fetcher=_fetcher({}), retrieved_utc="2026-06-11T00:00:00Z",
            staging_dir=None,
        )
        self.assertEqual(provenance["status"], UNAVAILABLE_STATUS)
        self.assertNotIn("coordinate_sha256", provenance)


class BuildBackfillTests(unittest.TestCase):
    def test_records_provenance_and_preserves_existing_structure(self) -> None:
        rows = [_expansion_row("P00001"), _expansion_row("P00002")]
        audit = build_label_structure_backfill(
            expansion_payload=rows,
            cif_fetcher=_fetcher({"P00001": _CIF}),  # P00002 -> 404
            created_utc="2026-06-11T00:00:00Z",
        )
        self.assertEqual(audit["counts"]["staged_this_run"], 1)
        self.assertEqual(audit["counts"]["unavailable"], 1)
        self.assertTrue(audit["guardrails"]["row_count_unchanged"])
        first = audit["backfilled_registry"][0]["evidence"]["structure_provenance"]
        # Existing fields preserved; new block additive.
        self.assertEqual(first["structure_handle"], "AF-P00001-F1")
        self.assertEqual(first["coordinate_status"],
                         "afdb_predicted_coordinate_provenance_available")
        self.assertEqual(first["afdb_v6_coordinate"]["status"], STAGED_STATUS)
        self.assertIn("coordinate_sha256", first["afdb_v6_coordinate"])
        second = audit["backfilled_registry"][1]["evidence"]["structure_provenance"]
        self.assertEqual(second["afdb_v6_coordinate"]["status"], UNAVAILABLE_STATUS)
        # Both rows still validate (structure is not a predictive feature).
        for row in audit["backfilled_registry"]:
            MechanismLabel.from_dict(row)
            self.assertEqual(row["evidence"]["predictive_evidence"], [])

    def test_limit_defers_extra_fetches(self) -> None:
        rows = [_expansion_row(f"P{i:05d}") for i in range(5)]
        mapping = {row["entry_id"].split(":")[1]: _CIF for row in rows}
        audit = build_label_structure_backfill(
            expansion_payload=rows, cif_fetcher=_fetcher(mapping), limit=2,
        )
        self.assertEqual(audit["counts"]["staged_this_run"], 2)
        self.assertEqual(audit["counts"]["deferred_over_limit"], 3)
        self.assertEqual(audit["counts"]["fetched_this_run"], 2)

    def test_idempotent_skip_of_already_staged(self) -> None:
        rows = [_expansion_row("P00001")]
        first = build_label_structure_backfill(
            expansion_payload=rows, cif_fetcher=_fetcher({"P00001": _CIF}),
        )

        def _boom(_accession):
            raise AssertionError("should not fetch already-staged rows")

        second = build_label_structure_backfill(
            expansion_payload=first["backfilled_registry"], cif_fetcher=_boom,
        )
        self.assertEqual(second["counts"]["already_staged"], 1)
        self.assertEqual(second["counts"]["staged_this_run"], 0)
        self.assertEqual(second["counts"]["fetched_this_run"], 0)


class CacheAndWriteTests(unittest.TestCase):
    def test_cache_makes_runs_resumable(self) -> None:
        calls = []

        def counting_fetcher(accession):
            calls.append(accession)
            return _CIF

        rows = [_expansion_row("P00001")]
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            build_label_structure_backfill(
                expansion_payload=rows, cif_fetcher=counting_fetcher, cache_path=cache_path,
            )
            self.assertEqual(calls, ["P00001"])
            # Second run over the ORIGINAL rows: cache satisfies P00001, no new fetch.
            calls.clear()
            audit = build_label_structure_backfill(
                expansion_payload=rows, cif_fetcher=counting_fetcher, cache_path=cache_path,
            )
            self.assertEqual(calls, [])
            self.assertEqual(audit["counts"]["fetched_this_run"], 0)
            self.assertEqual(
                audit["backfilled_registry"][0]["evidence"]["structure_provenance"][
                    "afdb_v6_coordinate"
                ]["status"],
                STAGED_STATUS,
            )

    def test_preview_non_destructive_apply_writes_expansion_only(self) -> None:
        rows = [_expansion_row("P00001")]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            expansion_path = tmp / "expansion.json"
            expansion_path.write_text(_dump_registry(rows), encoding="utf-8")
            frozen_path = tmp / "frozen.json"
            frozen_bytes = _dump_registry([])
            frozen_path.write_text(frozen_bytes, encoding="utf-8")

            import catalytic_earth.label_structure_backfill as mod

            original = mod.robust_afdb_v6_cif_fetcher
            mod.robust_afdb_v6_cif_fetcher = _fetcher({"P00001": _CIF})
            try:
                preview = write_label_structure_backfill(
                    out_path=tmp / "preview.json",
                    report_path=tmp / "report.md",
                    expansion_registry_path=expansion_path,
                    frozen_benchmark_path=frozen_path,
                    apply=False,
                    cache_path=None,
                )
                self.assertFalse(preview["expansion_registry_written"])
                before = json.loads(expansion_path.read_text(encoding="utf-8"))
                self.assertNotIn(
                    "afdb_v6_coordinate", before[0]["evidence"]["structure_provenance"]
                )
                summary = json.loads((tmp / "preview.json").read_text(encoding="utf-8"))
                self.assertNotIn("backfilled_registry", summary)

                applied = write_label_structure_backfill(
                    out_path=tmp / "preview.json",
                    report_path=tmp / "report.md",
                    expansion_registry_path=expansion_path,
                    frozen_benchmark_path=frozen_path,
                    apply=True,
                    cache_path=None,
                )
                self.assertTrue(applied["expansion_registry_written"])
                self.assertFalse(applied["frozen_benchmark_registry_written"])
                self.assertEqual(frozen_path.read_text(encoding="utf-8"), frozen_bytes)
                after = json.loads(expansion_path.read_text(encoding="utf-8"))
                self.assertEqual(len(after), len(rows))
                self.assertEqual(
                    after[0]["evidence"]["structure_provenance"]["afdb_v6_coordinate"]["status"],
                    STAGED_STATUS,
                )
                self.assertEqual(
                    expansion_path.read_text(encoding="utf-8"), _dump_registry(after)
                )
            finally:
                mod.robust_afdb_v6_cif_fetcher = original

    def test_refuses_to_target_frozen_benchmark(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frozen_path = Path(tmp) / "frozen.json"
            frozen_path.write_text(_dump_registry([]), encoding="utf-8")
            with self.assertRaises(ValueError):
                write_label_structure_backfill(
                    out_path=Path(tmp) / "preview.json",
                    report_path=None,
                    expansion_registry_path=frozen_path,
                    frozen_benchmark_path=frozen_path,
                    apply=True,
                    cache_path=None,
                )


if __name__ == "__main__":
    unittest.main()
