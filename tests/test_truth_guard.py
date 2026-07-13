from __future__ import annotations

import json
import hashlib
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.truth_guard import (
    _load_registry_rows,
    append_exposure_event,
    assert_evaluation_request_allowed,
    assert_expansion_write_allowed,
    compute_one_shot_status,
    load_exposure_ledger,
    load_exposure_rows,
    preregistration_sha256,
    validate_expansion_freeze,
    validate_exposure_events,
    validate_exposure_rows,
    validate_preregistration_contract,
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

        self.assertEqual(result["claims"], 16)
        self.assertEqual(result["exposure_events"], 9)
        self.assertEqual(result["exposure_surfaces"], 4)
        self.assertEqual(result["frozen_unscored_surfaces"], 1)
        self.assertEqual(result["expansion_freeze_active"], 1)
        self.assertEqual(result["combined_positive_assignments"], 8305)
        self.assertEqual(result["combined_oos_records"], 1696)
        self.assertEqual(result["chemistry_exact_correct"], 65)
        self.assertEqual(result["swissprot_metal_recovered"], 2)
        self.assertEqual(result["exposure_rows"], 1000)
        self.assertEqual(result["independent_eligible_rows"], 22)
        self.assertEqual(result["drifted_first_exposure_sources"], 0)

    def test_row_memory_computes_one_shot_status(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        result = validate_exposure_rows(repo_root=repo_root)

        self.assertEqual(result["exposure_row_surfaces"], 4)
        self.assertEqual(
            compute_one_shot_status("offmcsa.option_b.bronze22", repo_root=repo_root),
            "available_once",
        )
        self.assertEqual(
            compute_one_shot_status("mcsa.current702.heldout140", repo_root=repo_root),
            "spent",
        )

    def test_evaluator_refuses_spent_independent_claim(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        rows = load_exposure_rows(repo_root / "data/governance/exposure_rows.jsonl")
        heldout = [
            row["row_id"]
            for row in rows
            if row["surface_id"] == "mcsa.current702.heldout140"
        ]

        with self.assertRaisesRegex(ValueError, "not eligible for an independent test"):
            assert_evaluation_request_allowed(
                "mcsa.current702.heldout140",
                heldout,
                claimed_role="independent_test",
                namespace="evaluation/mcsa",
                repo_root=repo_root,
            )

    def test_evaluator_protects_frozen_surface_and_requires_exact_set(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        rows = load_exposure_rows(repo_root / "data/governance/exposure_rows.jsonl")
        option_b = [
            row["row_id"]
            for row in rows
            if row["surface_id"] == "offmcsa.option_b.bronze22"
        ]

        decision = assert_evaluation_request_allowed(
            "offmcsa.option_b.bronze22",
            option_b,
            claimed_role="independent_test",
            namespace="evaluation/option-b",
            repo_root=repo_root,
        )
        self.assertEqual(decision["one_shot_status"], "available_once")
        with self.assertRaisesRegex(ValueError, "entire frozen row set"):
            assert_evaluation_request_allowed(
                "offmcsa.option_b.bronze22",
                option_b[:-1],
                claimed_role="independent_test",
                namespace="evaluation/option-b",
                repo_root=repo_root,
            )
        with self.assertRaisesRegex(ValueError, "protected from development use"):
            assert_evaluation_request_allowed(
                "offmcsa.option_b.bronze22",
                option_b,
                claimed_role="development",
                namespace="development/option-b",
                repo_root=repo_root,
            )

    def test_posthoc_requires_separate_namespace(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        rows = load_exposure_rows(repo_root / "data/governance/exposure_rows.jsonl")
        row_id = next(
            row["row_id"]
            for row in rows
            if row["surface_id"] == "mcsa.current702.heldout140"
        )
        with self.assertRaisesRegex(ValueError, "posthoc/"):
            assert_evaluation_request_allowed(
                "mcsa.current702.heldout140",
                [row_id],
                claimed_role="posthoc",
                namespace="analysis/mcsa",
                repo_root=repo_root,
            )

    def test_preregistration_contract_binds_required_fields_and_role(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        manifest_path = repo_root / "data/governance/exposure_rows_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
        ).strip()
        contract = {
            "schema_version": "catalytic-earth.preregistration.v1",
            "preregistration_id": "test.option-b.v1",
            "registered_at": "2026-07-13T21:00:00Z",
            "code_commit": commit,
            "data_hashes": {
                "data/governance/exposure_rows_manifest.json": hashlib.sha256(
                    manifest_path.read_bytes()
                ).hexdigest()
            },
            "surface_id": "offmcsa.option_b.bronze22",
            "row_id_set_sha256": manifest["surfaces"][
                "offmcsa.option_b.bronze22"
            ]["row_id_set_sha256"],
            "claimed_role": "independent_test",
            "namespace": "evaluation/option-b",
            "threshold": {"name": "combined_score", "value": 0.44155, "comparison": ">="},
            "metric": {
                "name": "exact_proxy_family_recovery",
                "aggregation": "micro",
                "higher_is_better": True,
            },
            "seed": 0,
            "endpoint": {
                "name": "option-b bronze proxy recovery",
                "population": "all 22 frozen rows",
                "unit": "protein-label record",
                "decision_rule": "report all predictions and exact proxy matches once",
            },
        }
        contract["signature"] = {
            "algorithm": "sha256",
            "digest": preregistration_sha256(contract),
        }
        self.assertIs(
            validate_preregistration_contract(contract, repo_root=repo_root), contract
        )

        contract["claimed_role"] = "development"
        contract["signature"]["digest"] = preregistration_sha256(contract)
        with self.assertRaisesRegex(ValueError, "protected from development use"):
            validate_preregistration_contract(contract, repo_root=repo_root)

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
