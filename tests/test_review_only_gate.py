import json
from pathlib import Path
import tempfile
import unittest

from catalytic_earth.review_only_gate import validate_review_only_zero_import_artifacts


class ReviewOnlyGateTest(unittest.TestCase):
    def test_validates_closed_review_only_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.json"
            path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "artifact_id": "ok",
                            "method": "test",
                            "review_only": True,
                            "ready_for_label_import": False,
                            "import_ready_candidate_count": 0,
                            "countable_label_candidate_count": 0,
                            "curated_label_registry_edited": False,
                            "fingerprint_registry_edited": False,
                            "artifact_upload_or_removal_performed": False,
                        }
                    }
                ),
                encoding="utf-8",
            )

            validation = validate_review_only_zero_import_artifacts([path])

        self.assertTrue(validation["metadata"]["valid"])
        self.assertEqual(validation["metadata"]["blocker_count"], 0)
        self.assertTrue(validation["rows"][0]["valid"])

    def test_fails_open_import_or_registry_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.json"
            path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "artifact_id": "bad",
                            "method": "test",
                            "review_only": True,
                            "ready_for_label_import": True,
                            "import_ready_candidate_count": 1,
                            "countable_label_candidate_count": 0,
                            "new_external_rows_frozen": 2,
                            "curated_label_registry_edited": True,
                            "fingerprint_registry_edited": False,
                            "artifact_upload_or_removal_performed": False,
                            "removal_allowed_set_true": True,
                        }
                    }
                ),
                encoding="utf-8",
            )

            validation = validate_review_only_zero_import_artifacts([path])

        self.assertFalse(validation["metadata"]["valid"])
        self.assertEqual(validation["metadata"]["blocker_count"], 1)
        self.assertEqual(
            validation["rows"][0]["blockers"],
            [
                "ready_for_label_import_not_false",
                "import_ready_candidate_count_not_zero",
                "curated_label_registry_edited_not_false",
                "removal_allowed_set_true",
                "new_external_rows_frozen_not_zero",
            ],
        )

    def test_accepts_counts_from_decision_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.json"
            path.write_text(
                json.dumps(
                    {
                        "metadata": {
                            "artifact_id": "decision-counts",
                            "method": "test",
                            "review_only": True,
                            "ready_for_label_import": False,
                            "curated_label_registry_edited": False,
                            "fingerprint_registry_edited": False,
                            "artifact_upload_or_removal_performed": False,
                        },
                        "decision": {
                            "import_ready_candidate_count": 0,
                            "countable_label_candidate_count": 0,
                        },
                    }
                ),
                encoding="utf-8",
            )

            validation = validate_review_only_zero_import_artifacts([path])

        self.assertTrue(validation["metadata"]["valid"])
        self.assertEqual(validation["rows"][0]["import_ready_candidate_count"], 0)
        self.assertEqual(validation["rows"][0]["countable_label_candidate_count"], 0)


if __name__ == "__main__":
    unittest.main()
