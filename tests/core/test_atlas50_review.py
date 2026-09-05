from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from catalytic_earth.atlas50_phase_b import PHASE_B_RELATIVE, canonical_json_bytes
from catalytic_earth.atlas50_review import (
    SUBMISSIONS_RELATIVE,
    build_review_status,
    build_template,
    load_review_context,
    main as review_main,
    record_submission,
    validate_submission_file,
)


ROOT = Path(__file__).resolve().parents[2]
PHASE_B = ROOT / PHASE_B_RELATIVE


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Atlas50ReviewIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = _load(PHASE_B / "review_spec.json")
        crosswalk = _load(PHASE_B / "crosswalk_review_queue.json")["packets"][0]
        panel = _load(PHASE_B / "panel_review_queue.json")["packets"][0]
        cls.crosswalk_packet = crosswalk
        cls.panel_packet = panel
        cls.packets = {
            crosswalk["packet_id"]: crosswalk,
            panel["packet_id"]: panel,
        }

    def test_load_context_binds_all_frozen_packets(self) -> None:
        spec, packets = load_review_context(ROOT)

        self.assertEqual(spec["spec_id"], self.spec["spec_id"])
        self.assertEqual(len(packets), 97)
        self.assertEqual(
            {packet["packet_type"] for packet in packets.values()},
            {"crosswalk", "panel"},
        )

    def test_templates_are_intentionally_invalid_and_make_no_decisions(self) -> None:
        for packet in (self.crosswalk_packet, self.panel_packet):
            with self.subTest(packet_type=packet["packet_type"]):
                template = build_template(packet, self.spec)

                self.assertEqual(template["submission_id"], "")
                self.assertEqual(template["reviewer"]["reviewer_id"], "")
                self.assertEqual(template["decision"]["outcome"], "")
                self.assertIsNone(template["reviewer"]["project_author"])
                self.assertFalse(template["independent_annotation_claimed"])
                with tempfile.TemporaryDirectory() as temporary:
                    path = Path(temporary) / "template.json"
                    path.write_bytes(canonical_json_bytes(template))
                    with self.assertRaisesRegex(ValueError, "submission id missing"):
                        validate_submission_file(path, self.packets, self.spec)

    def test_submission_parser_rejects_duplicate_keys_and_nonfinite_values(self) -> None:
        submission = self._valid_submission(self.crosswalk_packet, "review.parser")
        encoded = json.dumps(submission, ensure_ascii=False)
        duplicate_key = (
            encoded[:-1] + ', "submission_id": "review.parser.duplicate"}'
        ).encode("utf-8")
        nonfinite = copy.deepcopy(submission)
        nonfinite["decision"]["uncertainty"] = [float("nan")]

        cases = (
            (duplicate_key, "duplicate JSON key: submission_id"),
            (json.dumps(nonfinite).encode("utf-8"), "non-finite JSON value: NaN"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            for index, (raw, expected) in enumerate(cases):
                with self.subTest(expected=expected):
                    path = Path(temporary) / f"submission-{index}.json"
                    path.write_bytes(raw)
                    with self.assertRaisesRegex(ValueError, expected):
                        validate_submission_file(path, self.packets, self.spec)

    def test_record_preserves_raw_bytes_under_hashed_id_without_temp_residue(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            submission = self._valid_submission(
                self.crosswalk_packet, "review.raw-bytes"
            )
            raw = (json.dumps(submission, indent=4, ensure_ascii=False) + "\n\n").encode(
                "utf-8"
            )
            incoming = Path(temporary) / "incoming.json"
            incoming.write_bytes(raw)

            destination = record_submission(root, incoming, self.packets, self.spec)

            expected_name = (
                hashlib.sha256(submission["submission_id"].encode("utf-8")).hexdigest()
                + ".json"
            )
            self.assertEqual(destination.name, expected_name)
            self.assertEqual(destination.read_bytes(), raw)
            self.assertEqual(
                list(destination.parent.parent.glob(".review-intake-*")), []
            )
            status = build_review_status(root, self.packets, self.spec)
            self.assertEqual(status["valid_submission_count"], 1)
            entry = next(
                row["submissions"][0]
                for row in status["packets"]
                if row["submissions"]
            )
            self.assertEqual(entry["sha256"], hashlib.sha256(raw).hexdigest())

    def test_record_rejects_an_existing_submission_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            submission = self._valid_submission(
                self.crosswalk_packet, "review.duplicate"
            )
            first = Path(temporary) / "first.json"
            second = Path(temporary) / "second.json"
            first.write_bytes(canonical_json_bytes(submission))
            changed = copy.deepcopy(submission)
            changed["decision"]["rationale"] = "A second assertion with the same ID."
            second.write_bytes(canonical_json_bytes(changed))
            record_submission(root, first, self.packets, self.spec)

            with self.assertRaisesRegex(ValueError, "duplicate submission ID"):
                record_submission(root, second, self.packets, self.spec)

    def test_failed_atomic_publish_leaves_no_partial_record_or_temp_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            submission = self._valid_submission(
                self.crosswalk_packet, "review.atomic-failure"
            )
            incoming = Path(temporary) / "incoming.json"
            incoming.write_bytes(canonical_json_bytes(submission))
            expected = root / SUBMISSIONS_RELATIVE / (
                hashlib.sha256(submission["submission_id"].encode("utf-8")).hexdigest()
                + ".json"
            )

            with mock.patch(
                "catalytic_earth.atlas50_review.os.link",
                side_effect=FileExistsError("simulated exclusive-publish collision"),
            ):
                with self.assertRaises(FileExistsError):
                    record_submission(root, incoming, self.packets, self.spec)

            self.assertFalse(expected.exists())
            self.assertEqual(list(expected.parent.iterdir()), [])
            self.assertEqual(list(expected.parent.parent.glob(".review-intake-*")), [])

    def test_status_rejects_duplicate_ids_and_invalid_existing_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            directory = root / SUBMISSIONS_RELATIVE
            directory.mkdir(parents=True)
            submission = self._valid_submission(
                self.crosswalk_packet, "review.duplicate-scan"
            )
            (directory / "one.json").write_bytes(canonical_json_bytes(submission))
            changed = copy.deepcopy(submission)
            changed["decision"]["rationale"] = "Different assertion, duplicate ID."
            (directory / "two.json").write_bytes(canonical_json_bytes(changed))

            with self.assertRaisesRegex(ValueError, "duplicate submission ID"):
                build_review_status(root, self.packets, self.spec)

            (directory / "two.json").write_bytes(b'{"incomplete": true}\n')
            with self.assertRaisesRegex(ValueError, "unknown packet ID"):
                build_review_status(root, self.packets, self.spec)

    def test_status_rejects_namespace_path_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            directory = root / SUBMISSIONS_RELATIVE
            directory.parent.mkdir(parents=True)
            directory.write_text("not a directory", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "must be a directory"):
                build_review_status(root, self.packets, self.spec)

    @unittest.skipIf(os.name == "nt", "symlink creation is not reliable on Windows CI")
    def test_status_rejects_symlinked_namespace_ancestors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            phase_b = root / PHASE_B_RELATIVE
            phase_b.parent.mkdir(parents=True)
            outside = Path(temporary) / "outside"
            outside.mkdir()
            phase_b.symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "contains a symlink"):
                build_review_status(root, self.packets, self.spec)

    def test_status_retains_unresolved_conflicts_and_distinct_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            directory = root / SUBMISSIONS_RELATIVE
            directory.mkdir(parents=True)
            accepted = self._valid_submission(
                self.crosswalk_packet, "review.accepted"
            )
            unresolved = self._valid_submission(
                self.crosswalk_packet, "review.unresolved"
            )
            unresolved["reviewer"]["reviewer_id"] = "reviewer.unresolved"
            unresolved["decision"].update(
                {
                    "outcome": "unresolved",
                    "rationale": "The available packet does not resolve the mapping.",
                    "uncertainty": ["unresolved"],
                }
            )
            unresolved["decision"]["field_decisions"] = {
                "classification": "unresolved",
                "source_links": {
                    key: "unresolved"
                    for key in self.spec["crosswalk_review_contract"][
                        "required_source_keys"
                    ]
                },
            }
            unresolved["conflicts"] = [
                {"field": "classification", "alternative": "aggregation"}
            ]
            (directory / "accepted.json").write_bytes(
                canonical_json_bytes(accepted)
            )
            (directory / "unresolved.json").write_bytes(
                canonical_json_bytes(unresolved)
            )

            status = build_review_status(
                root,
                {self.crosswalk_packet["packet_id"]: self.crosswalk_packet},
                self.spec,
            )

            row = status["packets"][0]
            self.assertEqual(status["valid_submission_count"], 2)
            self.assertEqual(status["packets_requiring_resolution"], 1)
            self.assertTrue(row["multiple_decision_variants"])
            self.assertTrue(row["requires_resolution"])
            self.assertEqual(
                {item["decision"]["outcome"] for item in row["submissions"]},
                {"accept_machine_draft", "unresolved"},
            )
            retained = next(
                item
                for item in row["submissions"]
                if item["submission_id"] == "review.unresolved"
            )
            self.assertEqual(retained["conflicts"], unresolved["conflicts"])
            self.assertEqual(
                retained["decision"]["uncertainty"], ["unresolved"]
            )

    def test_committed_submission_deletion_and_edit_are_rejected(self) -> None:
        for mutation, expected in (
            ("delete", "deleted or replaced"),
            ("edit", "append-only submission changed"),
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = self._init_repository(Path(temporary))
                submission = self._valid_submission(
                    self.crosswalk_packet, f"review.committed-{mutation}"
                )
                incoming = Path(temporary) / "incoming.json"
                incoming.write_bytes(canonical_json_bytes(submission))
                destination = record_submission(
                    root, incoming, self.packets, self.spec
                )
                self._git(root, "add", "--", destination.relative_to(root).as_posix())
                self._git(root, "commit", "-qm", "record review assertion")

                if mutation == "delete":
                    destination.unlink()
                else:
                    changed = copy.deepcopy(submission)
                    changed["decision"]["rationale"] = "Edited after commit."
                    destination.write_bytes(canonical_json_bytes(changed))

                with self.assertRaisesRegex(ValueError, expected):
                    build_review_status(root, self.packets, self.spec)

    def test_older_baseline_ref_rejects_a_rewrite_committed_on_head(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            submission = self._valid_submission(
                self.crosswalk_packet, "review.baseline"
            )
            incoming = Path(temporary) / "incoming.json"
            incoming.write_bytes(canonical_json_bytes(submission))
            destination = record_submission(root, incoming, self.packets, self.spec)
            relative = destination.relative_to(root).as_posix()
            self._git(root, "add", "--", relative)
            self._git(root, "commit", "-qm", "record original assertion")
            baseline = self._git(root, "rev-parse", "HEAD").stdout.strip()
            changed = copy.deepcopy(submission)
            changed["decision"]["rationale"] = "Rewrite committed on the branch."
            destination.write_bytes(canonical_json_bytes(changed))
            self._git(root, "add", "--", relative)
            self._git(root, "commit", "-qm", "rewrite assertion")

            current = build_review_status(root, self.packets, self.spec)
            self.assertEqual(current["valid_submission_count"], 1)
            with self.assertRaisesRegex(ValueError, "append-only submission changed"):
                build_review_status(
                    root, self.packets, self.spec, baseline_ref=baseline
                )

    def test_cli_protects_output_paths_and_exports_only_an_invalid_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._init_repository(Path(temporary))
            packet = self.crosswalk_packet
            packets = {packet["packet_id"]: packet}
            in_repository = root / "review-draft.json"
            existing = Path(temporary) / "existing.json"
            existing.write_bytes(b"preserve these bytes\n")
            exported = Path(temporary) / "exported.json"
            stderr = io.StringIO()
            stdout = io.StringIO()
            context = mock.patch(
                "catalytic_earth.atlas50_review.load_review_context",
                return_value=(self.spec, packets),
            )
            with context, mock.patch("sys.stderr", stderr), mock.patch(
                "sys.stdout", stdout
            ):
                with self.assertRaisesRegex(SystemExit, "1"):
                    review_main(
                        [
                            "template",
                            "--packet-id",
                            packet["packet_id"],
                            "--output",
                            str(in_repository),
                        ],
                        repo_root=root,
                    )
                self.assertFalse(in_repository.exists())
                self.assertIn("outside the repository", stderr.getvalue())

                stderr.seek(0)
                stderr.truncate(0)
                with self.assertRaisesRegex(SystemExit, "1"):
                    review_main(
                        [
                            "template",
                            "--packet-id",
                            packet["packet_id"],
                            "--output",
                            str(existing),
                        ],
                        repo_root=root,
                    )
                self.assertEqual(existing.read_bytes(), b"preserve these bytes\n")

                self.assertEqual(
                    review_main(
                        [
                            "template",
                            "--packet-id",
                            packet["packet_id"],
                            "--output",
                            str(exported),
                        ],
                        repo_root=root,
                    ),
                    0,
                )
                template = json.loads(exported.read_bytes())
                self.assertEqual(template["submission_id"], "")
                self.assertEqual(template["decision"]["outcome"], "")

                stderr.seek(0)
                stderr.truncate(0)
                with self.assertRaisesRegex(SystemExit, "1"):
                    review_main(
                        ["validate", "--submission", str(exported)],
                        repo_root=root,
                    )
                self.assertIn("submission id missing", stderr.getvalue())

    def _valid_submission(self, packet: dict, submission_id: str) -> dict:
        if packet["packet_type"] == "crosswalk":
            field_decisions = {
                "classification": "accept_machine_draft",
                "source_links": {
                    key: (
                        "confirm_explicit_gap"
                        if link["gap_reason"]
                        else "confirm_candidate_mapping"
                    )
                    for key, link in packet["machine_draft"]["source_links"].items()
                },
            }
            outcome = "accept_machine_draft"
        else:
            field_decisions = {
                dimension: "accept_machine_draft_gate"
                for dimension in self.spec["panel_review_contract"][
                    "review_dimensions"
                ]
            }
            outcome = (
                "accept_proposed_include"
                if packet["machine_draft"]["proposed_disposition"]
                == "propose_include"
                else "accept_fail_closed_exclusion"
            )
        return {
            "schema_version": "catalytic-earth.atlas50-review-submission.v1",
            "submission_id": submission_id,
            "packet_id": packet["packet_id"],
            "packet_type": packet["packet_type"],
            "packet_sha256": hashlib.sha256(canonical_json_bytes(packet)).hexdigest(),
            "reviewer": {
                "reviewer_id": "reviewer.contract-test",
                "reviewer_display_name": "Contract Test Reviewer",
                "expertise_context": "Synthetic fixture for intake contract tests",
                "reviewed_on": "2026-07-14",
                "project_author": False,
            },
            "attestation": self.spec["reviewer_evidence_contract"][
                "required_attestation"
            ],
            "decision": {
                "outcome": outcome,
                "rationale": "Synthetic assertion used only to test intake behavior.",
                "uncertainty": [],
                "field_decisions": field_decisions,
            },
            "evidence_references": [],
            "conflicts": [],
            "submitted_at": "2026-07-14T00:00:00Z",
            "independent_annotation_claimed": False,
        }

    def _init_repository(self, parent: Path) -> Path:
        root = parent / "repo"
        root.mkdir()
        self._git(root, "init", "-q")
        self._git(root, "commit", "--allow-empty", "-qm", "baseline")
        return root

    def _git(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "git",
                "-c",
                "user.name=Atlas Review Test",
                "-c",
                "user.email=atlas-review-test@example.invalid",
                *args,
            ],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
