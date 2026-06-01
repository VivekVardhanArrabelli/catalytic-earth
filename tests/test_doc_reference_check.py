from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from catalytic_earth.doc_reference_check import (
    build_current_docs_artifact_reference_check,
    write_current_docs_artifact_reference_check,
)


class CurrentDocsArtifactReferenceCheckTests(unittest.TestCase):
    def test_ignores_templates_and_reports_missing_concrete_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            doc = root / "doc.md"
            doc.write_text(
                "\n".join(
                    [
                        "`docs/agent_runbook.md`",
                        "`artifacts/missing.json`",
                        "`artifacts/v3_<topic>_<date>.json`",
                        "`artifacts/*.json`",
                    ]
                ),
                encoding="utf-8",
            )

            audit = build_current_docs_artifact_reference_check(doc_paths=[doc])

        self.assertEqual(
            audit["status"],
            "current_docs_artifact_references_missing_paths",
        )
        self.assertEqual(audit["counts"]["references_checked"], 2)
        self.assertEqual(audit["counts"]["ignored_references"], 2)
        self.assertEqual(audit["counts"]["missing_references"], 1)
        self.assertEqual(
            audit["missing_references"][0]["reference"],
            "artifacts/missing.json",
        )

    def test_writer_emits_json_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            doc = root / "doc.md"
            out = root / "artifact.json"
            report = root / "report.md"
            doc.write_text("", encoding="utf-8")

            audit = write_current_docs_artifact_reference_check(
                doc_paths=[doc],
                out_path=out,
                report_path=report,
            )

            self.assertTrue(out.exists())
            self.assertTrue(report.exists())

        self.assertEqual(audit["counts"]["missing_references"], 0)


if __name__ == "__main__":
    unittest.main()
