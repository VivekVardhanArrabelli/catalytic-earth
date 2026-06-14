from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.label_pdb_id_backfill import (
    BACKFILLED_STATUS,
    build_label_pdb_id_backfill,
    write_label_pdb_id_backfill,
)
from catalytic_earth.registry_io import dump_registry, load_registry


def _row(accession: str, *, pdb_ids: list[str] | None = None) -> dict:
    return {
        "entry_id": f"uniprot:{accession}",
        "fingerprint_id": "metallopeptidase",
        "label_type": "seed_fingerprint",
        "tier": "bronze",
        "review_status": "automation_curated",
        "confidence": "high",
        "evidence_score": 0.8,
        "ontology_version_at_decision": "label_factory_v1_8fp",
        "rationale": (
            "Synthetic annotation-anchored bronze test row with structure provenance "
            "for PDB backfill validation."
        ),
        "evidence": {
            "sources": ["test"],
            "excluded_context": ["protein_name"],
            "predictive_evidence": [],
            "source_provenance": {"accession": accession, "sequence_length": 3},
            "structure_provenance": {
                "alphafold_ids": [accession],
                "pdb_ids": pdb_ids or [],
            },
        },
    }


def _payload(records: list[dict]) -> dict:
    return {
        "metadata": {"source": "uniprot", "record_count": len(records)},
        "records": records,
    }


class LabelPdbIdBackfillTests(unittest.TestCase):
    def test_backfills_missing_pdb_ids_as_provenance_only(self) -> None:
        audit = build_label_pdb_id_backfill(
            expansion_payload=[_row("P00001")],
            created_utc="2026-06-14T00:00:00Z",
            uniprot_payload=_payload(
                [{"accession": "P00001", "pdb_ids": ["1abc", "2DEF"], "reviewed": "reviewed"}]
            ),
        )
        self.assertEqual(audit["counts"]["backfilled_pdb_rows_this_run"], 1)
        row = audit["backfilled_registry"][0]
        structure = row["evidence"]["structure_provenance"]
        self.assertEqual(structure["pdb_ids"], ["1ABC", "2DEF"])
        self.assertEqual(
            structure["pdb_id_backfill_provenance"]["status"], BACKFILLED_STATUS
        )
        self.assertEqual(row["evidence"]["predictive_evidence"], [])

    def test_preserves_existing_pdb_ids_and_defers_over_limit(self) -> None:
        seen = []

        def fetcher(accessions):
            seen.extend(accessions)
            return _payload([{"accession": "P00002", "pdb_ids": ["3GHI"]}])

        audit = build_label_pdb_id_backfill(
            expansion_payload=[_row("P00001", pdb_ids=["1ABC"]), _row("P00002"), _row("P00003")],
            accessions_fetcher=fetcher,
            limit=1,
        )
        self.assertEqual(seen, ["P00002"])
        self.assertEqual(audit["counts"]["already_had_pdb_ids"], 1)
        self.assertEqual(audit["counts"]["backfilled_pdb_rows_this_run"], 1)
        self.assertEqual(audit["counts"]["deferred_over_limit"], 1)
        self.assertEqual(
            audit["backfilled_registry"][0]["evidence"]["structure_provenance"]["pdb_ids"],
            ["1ABC"],
        )

    def test_preview_apply_writes_expansion_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            expansion = tmp / "expansion.json"
            frozen = tmp / "frozen.json"
            expansion.write_text(dump_registry([_row("P00001")]), encoding="utf-8")
            frozen_bytes = dump_registry([])
            frozen.write_text(frozen_bytes, encoding="utf-8")

            import catalytic_earth.label_pdb_id_backfill as mod

            original = mod.fetch_uniprot_accessions
            mod.fetch_uniprot_accessions = lambda accessions: _payload(
                [{"accession": "P00001", "pdb_ids": ["4JKL"], "reviewed": "reviewed"}]
            )
            try:
                preview = write_label_pdb_id_backfill(
                    out_path=tmp / "preview.json",
                    report_path=tmp / "report.md",
                    expansion_registry_path=expansion,
                    frozen_benchmark_path=frozen,
                    apply=False,
                )
                self.assertFalse(preview["expansion_registry_written"])
                self.assertEqual(load_registry(expansion)[0]["evidence"]["structure_provenance"]["pdb_ids"], [])

                applied = write_label_pdb_id_backfill(
                    out_path=tmp / "preview.json",
                    report_path=tmp / "report.md",
                    expansion_registry_path=expansion,
                    frozen_benchmark_path=frozen,
                    apply=True,
                )
                self.assertTrue(applied["expansion_registry_written"])
                self.assertFalse(applied["frozen_benchmark_registry_written"])
                self.assertEqual(frozen.read_text(encoding="utf-8"), frozen_bytes)
                self.assertEqual(
                    load_registry(expansion)[0]["evidence"]["structure_provenance"]["pdb_ids"],
                    ["4JKL"],
                )
            finally:
                mod.fetch_uniprot_accessions = original

    def test_refuses_to_target_frozen_benchmark(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            frozen = Path(tmpdir) / "frozen.json"
            frozen.write_text(json.dumps([]), encoding="utf-8")
            with self.assertRaises(ValueError):
                write_label_pdb_id_backfill(
                    out_path=Path(tmpdir) / "preview.json",
                    report_path=None,
                    expansion_registry_path=frozen,
                    frozen_benchmark_path=frozen,
                    apply=True,
                )


if __name__ == "__main__":
    unittest.main()
