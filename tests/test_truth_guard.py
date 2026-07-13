from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.truth_guard import (
    _load_registry_rows,
    append_exposure_event,
    assert_expansion_write_allowed,
    load_exposure_ledger,
    validate_expansion_freeze,
    validate_exposure_events,
    validate_truth_governance,
)


class TruthGuardTests(unittest.TestCase):
    def _event(
        self,
        event_id: str,
        *,
        state_after: str,
        event_type: str,
        effective_at: str,
    ) -> dict[str, object]:
        return {
            "event_id": event_id,
            "surface_id": "surface:test",
            "event_type": event_type,
            "state_after": state_after,
            "effective_at": effective_at,
            "recorded_at": "2026-07-13T20:30:00Z",
            "historical_backfill": False,
            "row_count": 3,
            "scope": "three deterministic test rows",
            "source_artifacts": ["evidence.json"],
            "note": "test event",
        }

    def test_repository_truth_governance_validates(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        result = validate_truth_governance(repo_root)

        self.assertEqual(result["claims"], 13)
        self.assertEqual(result["exposure_events"], 9)
        self.assertEqual(result["exposure_surfaces"], 4)
        self.assertEqual(result["frozen_unscored_surfaces"], 1)
        self.assertEqual(result["expansion_freeze_active"], 1)
        self.assertEqual(result["combined_positive_assignments"], 8305)
        self.assertEqual(result["combined_oos_records"], 1696)
        self.assertEqual(result["chemistry_exact_correct"], 65)
        self.assertEqual(result["swissprot_metal_recovered"], 2)

    def test_expansion_freeze_blocks_protected_registry(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]

        with self.assertRaisesRegex(ValueError, "expansion freeze blocks writes"):
            assert_expansion_write_allowed(
                Path("data/registries/external_bronze_labels.json"),
                repo_root=repo_root,
            )

    def test_expansion_freeze_allows_unprotected_output(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        assert_expansion_write_allowed(Path("work/corrective_audit.md"), repo_root=repo_root)

    def test_expansion_freeze_detects_direct_registry_drift(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            governance = root / "data/governance"
            governance.mkdir(parents=True)
            protected = root / "data/registry.json"
            protected.write_text("original\n", encoding="utf-8")
            (governance / "expansion_freeze.json").write_text(
                json.dumps(
                    {
                        "frozen": True,
                        "protected_paths": ["data/registry.json"],
                        "expected_sha256": {"data/registry.json": "0" * 64},
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "hash drifted"):
                validate_expansion_freeze(repo_root=root)

    def test_sharded_registry_detects_drift_beneath_unchanged_manifest(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            shard = root / "registry.shards/part-00000.json"
            shard.parent.mkdir()
            shard.write_text('[{"entry_id":"changed"}]\n', encoding="utf-8")
            manifest = root / "registry.json"
            manifest.write_text(
                json.dumps(
                    {
                        "shards": [
                            {
                                "path": "registry.shards/part-00000.json",
                                "row_count": 1,
                                "bytes": 3,
                                "sha256": "0" * 64,
                            }
                        ],
                        "row_count": 1,
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "shard SHA-256 mismatch"):
                _load_registry_rows(manifest)

    def test_exhausted_surface_cannot_be_reset(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evidence.json").write_text("{}\n", encoding="utf-8")
            events = [
                self._event(
                    "EXP-0001",
                    state_after="exhausted",
                    event_type="score",
                    effective_at="2026-07-01T00:00:00Z",
                ),
                self._event(
                    "EXP-0002",
                    state_after="frozen_unscored",
                    event_type="freeze",
                    effective_at="2026-07-02T00:00:00Z",
                ),
            ]

            with self.assertRaisesRegex(ValueError, "reset exhausted surface"):
                validate_exposure_events(events, repo_root=root)

    def test_exposed_surface_cannot_be_refrozen(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evidence.json").write_text("{}\n", encoding="utf-8")
            events = [
                self._event(
                    "EXP-0001",
                    state_after="exposed",
                    event_type="score",
                    effective_at="2026-07-01T00:00:00Z",
                ),
                self._event(
                    "EXP-0002",
                    state_after="frozen_unscored",
                    event_type="freeze",
                    effective_at="2026-07-02T00:00:00Z",
                ),
            ]

            with self.assertRaisesRegex(ValueError, "make exposed surface"):
                validate_exposure_events(events, repo_root=root)

    def test_append_assigns_next_id_and_preserves_existing_line(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "evidence.json"
            evidence.write_text("{}\n", encoding="utf-8")
            ledger = root / "ledger.jsonl"
            first = self._event(
                "EXP-0001",
                state_after="frozen_unscored",
                event_type="freeze",
                effective_at="2026-07-01T00:00:00Z",
            )
            first_line = json.dumps(first, separators=(",", ":"), sort_keys=True) + "\n"
            ledger.write_text(first_line, encoding="utf-8")

            second = self._event(
                "EXP-9999",
                state_after="exhausted",
                event_type="score",
                effective_at="2026-07-02T00:00:00Z",
            )
            second.pop("event_id")
            appended = append_exposure_event(second, Path("ledger.jsonl"), repo_root=root)

            self.assertEqual(appended["event_id"], "EXP-0002")
            self.assertTrue(ledger.read_text(encoding="utf-8").startswith(first_line))
            self.assertEqual(len(load_exposure_ledger(ledger)), 2)


if __name__ == "__main__":
    unittest.main()
