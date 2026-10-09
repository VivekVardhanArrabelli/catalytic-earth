from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "cloud_research" / "control.py"
SPEC = importlib.util.spec_from_file_location("cloud_research_control", MODULE_PATH)
assert SPEC and SPEC.loader
control = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = control
SPEC.loader.exec_module(control)

try:
    control.chicago_timezone()
    HAS_CHICAGO_TZ = True
except control.ControlError:
    HAS_CHICAGO_TZ = False


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def accept_test_checkpoint(_branch: str, _commit: str) -> None:
    """Pure policy tests inject a verifier; Git tests exercise the real one."""


def finish_job(
    state: dict[str, object], owner: str, epoch: int, now: datetime, *, suffix: str
) -> dict[str, object]:
    state = control.update_job(
        state, owner, epoch, now,
        provider_status="terminated",
        artifact_ref=f"s3://catalytic-earth/{suffix}.tar",
        artifact_sha256="a" * 64,
        artifacts_retrieved=True,
        termination_confirmed=True,
        termination_receipt=f"prime:termination:{suffix}",
    )
    return control.checkpoint_run(
        state, owner, epoch, now,
        repository_branch=f"codex/{suffix}",
        repository_commit="b" * 40,
        verify_remote=accept_test_checkpoint,
    )


class GitControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.remote = root / "remote.git"
        self.clone_a = root / "clone-a"
        self.clone_b = root / "clone-b"
        git(root, "init", "--bare", str(self.remote))
        git(root, "clone", str(self.remote), str(self.clone_a))
        git(root, "clone", str(self.remote), str(self.clone_b))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def publish_checkpoint(self, branch: str) -> str:
        marker = self.clone_a / "checkpoint.txt"
        marker.write_text(branch, encoding="utf-8")
        git(self.clone_a, "add", "checkpoint.txt")
        git(
            self.clone_a, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
            "commit", "-m", "checkpoint",
        )
        commit = git(self.clone_a, "rev-parse", "HEAD")
        git(self.clone_a, "push", "origin", f"HEAD:refs/heads/{branch}")
        return commit

    def test_separate_clones_race_on_existing_control_ref(self) -> None:
        stores = [control.GitRefStore(self.clone_a), control.GitRefStore(self.clone_b)]
        now = datetime(2026, 10, 9, 15, 0, tzinfo=timezone.utc)
        initial = stores[0].read()
        active = control.start_run(initial.state, "run", "owner", now, 300)
        stores[0].compare_and_swap(initial.head, active, "initialize")
        barrier = threading.Barrier(2)

        def contend(index: int) -> str:
            snapshot = stores[index].read()
            state = control.heartbeat(
                snapshot.state, "owner", 1, now + timedelta(seconds=index + 1), 300
            )
            barrier.wait(timeout=10)
            try:
                stores[index].compare_and_swap(snapshot.head, state, f"race-{index}")
                return "won"
            except control.CasConflict:
                return "lost"

        with ThreadPoolExecutor(max_workers=2) as executor:
            outcomes = list(executor.map(contend, range(2)))
        self.assertEqual(sorted(outcomes), ["lost", "won"])

    def test_remote_checkpoint_rejects_local_or_fabricated_commit(self) -> None:
        store = control.GitRefStore(self.clone_a)
        branch = "codex/durable-run"
        commit = self.publish_checkpoint(branch)
        store.verify_checkpoint(branch, commit)
        with self.assertRaises(control.ControlError):
            store.verify_checkpoint(branch, "f" * 40)
        with self.assertRaises(control.ControlError):
            store.verify_checkpoint("codex/missing", commit)

    def test_prepare_outputs_expected_head_and_state_without_push(self) -> None:
        store = control.GitRefStore(self.clone_a)
        now = control.utc_now()
        snapshot = store.read()
        state = control.start_run(snapshot.state, "run", "owner", now, 3600)
        head = store.compare_and_swap(snapshot.head, state, "start")
        process = subprocess.run(
            [
                sys.executable, str(MODULE_PATH), "--repo-root", str(self.clone_a),
                "--prepare", "heartbeat", "--owner", "owner", "--epoch", "1",
                "--lease-seconds", "3599",
            ],
            check=True, capture_output=True, text=True,
        )
        prepared = json.loads(process.stdout)
        after = store.read()
        self.assertEqual(prepared["expected_head"], head)
        self.assertEqual(prepared["action"], "heartbeat")
        self.assertEqual(prepared["proposed_state"]["active_run_id"], "run")
        self.assertEqual(after.head, head)
        self.assertEqual(after.state, state)

    @unittest.skipUnless(HAS_CHICAGO_TZ, "America/Chicago timezone data unavailable")
    def test_expired_owner_is_fenced_and_recovery_retains_live_job(self) -> None:
        store = control.GitRefStore(self.clone_a)
        start = datetime(2026, 10, 9, 15, 0, tzinfo=timezone.utc)
        snapshot = store.read()
        state = control.start_run(snapshot.state, "run-a", "owner-a", start, 60)
        head = store.compare_and_swap(snapshot.head, state, "start")
        state = control.reconcile_month(state, "owner-a", 1, start + timedelta(milliseconds=1))
        state = control.register_job(
            state, "owner-a", 1, start + timedelta(seconds=1),
            job_id="job-a", provider_job_id="provider-a", spec_sha256="a" * 64,
            idempotency_key="idem-a", provider_status="running",
            deadline=start + timedelta(hours=1), reserve_cents=500,
        )
        head = store.compare_and_swap(head, state, "job")
        stale_update = control.update_job(
            state, "owner-a", 1, start + timedelta(seconds=59), provider_status="unknown"
        )

        with self.assertRaises(control.ControlError):
            control.claim_recovery(state, "owner-b", start + timedelta(seconds=30), 60)
        recovered = control.claim_recovery(state, "owner-b", start + timedelta(seconds=61), 60)
        self.assertEqual(recovered["active_run_id"], "run-a")
        self.assertEqual(recovered["job"], state["job"])
        self.assertTrue(recovered["recovery"]["required"])
        recovered_head = store.compare_and_swap(head, recovered, "recover")

        with self.assertRaises(control.CasConflict):
            control.GitRefStore(self.clone_b).compare_and_swap(head, stale_update, "stale")
        with self.assertRaises(control.ControlError):
            control.heartbeat(recovered, "owner-a", 1, start + timedelta(seconds=62), 60)
        unknown = control.update_job(
            recovered, "owner-b", 2, start + timedelta(seconds=62), provider_status="unknown"
        )
        with self.assertRaises(control.ControlError):
            control.complete_run(unknown, "owner-b", 2, start + timedelta(seconds=63))
        terminal = control.update_job(
            unknown, "owner-b", 2, start + timedelta(seconds=63),
            provider_status="terminated", artifact_ref="s3://ce/job-a.tar",
            artifact_sha256="c" * 64, artifacts_retrieved=True,
            termination_confirmed=True, termination_receipt="prime:termination:job-a",
        )
        branch = "codex/recovered-run"
        commit = self.publish_checkpoint(branch)
        terminal = control.checkpoint_run(
            terminal, "owner-b", 2, start + timedelta(seconds=64),
            repository_branch=branch, repository_commit=commit,
            verify_remote=store.verify_checkpoint,
        )
        idle = control.complete_run(terminal, "owner-b", 2, start + timedelta(seconds=65))
        self.assertIsNone(idle["active_run_id"])
        self.assertEqual(idle["job_history"][0]["idempotency_key"], "idem-a")
        self.assertNotEqual(recovered_head, head)


@unittest.skipUnless(HAS_CHICAGO_TZ, "America/Chicago timezone data unavailable")
class BudgetPolicyTests(unittest.TestCase):
    NOW = datetime(2026, 10, 9, 15, 0, tzinfo=timezone.utc)

    def active_job(self, reserve_cents: int = 750) -> dict[str, object]:
        state = control.start_run(control.empty_state(), "run", "owner", self.NOW, 900)
        state = control.reconcile_month(state, "owner", 1, self.NOW)
        return control.register_job(
            state, "owner", 1, self.NOW, job_id="job", provider_job_id=None,
            spec_sha256="b" * 64, idempotency_key="idem", provider_status="launch_pending",
            deadline=self.NOW + timedelta(hours=1), reserve_cents=reserve_cents,
        )

    def test_per_job_cap_refuses_reservations_but_records_actual_overrun(self) -> None:
        state = self.active_job()
        state = control.record_cost(
            state, "owner", 1, self.NOW, cost_id="storage", job_id="job",
            category="storage", status="reserved", reserved_cents=25,
            spent_cents=0, incurred_at=self.NOW,
        )
        state = control.record_cost(
            state, "owner", 1, self.NOW, cost_id="controller", job_id="job",
            category="controller", status="unknown", reserved_cents=25,
            spent_cents=0, incurred_at=self.NOW,
        )
        self.assertEqual(control._job_exposure(state, "job"), 800)
        with self.assertRaises(control.ControlError):
            control.record_cost(
                state, "owner", 1, self.NOW, cost_id="future", job_id="job",
                category="storage", status="reserved", reserved_cents=1,
                spent_cents=0, incurred_at=self.NOW,
            )
        overrun = control.record_cost(
            state, "owner", 1, self.NOW, cost_id="actual", job_id="job",
            category="storage", status="spent", reserved_cents=0,
            spent_cents=1, incurred_at=self.NOW,
        )
        self.assertEqual(control._job_exposure(overrun, "job"), 801)
        self.assertTrue(control._budget_overrun(overrun))
        overrun = finish_job(overrun, "owner", 1, self.NOW, suffix="overrun")
        overrun = control.complete_run(overrun, "owner", 1, self.NOW)
        overrun = control.start_run(overrun, "next-run", "next-owner", self.NOW, 900)
        overrun = control.reconcile_month(overrun, "next-owner", 2, self.NOW)
        with self.assertRaises(control.ControlError):
            control.register_job(
                overrun, "next-owner", 2, self.NOW, job_id="next-job",
                provider_job_id=None, spec_sha256="e" * 64,
                idempotency_key="next-idem", provider_status="running",
                deadline=self.NOW + timedelta(hours=1), reserve_cents=1,
            )

    def test_calendar_month_cap_persists_across_completed_runs(self) -> None:
        state = control.empty_state()
        now = self.NOW
        for index in range(6):
            owner = f"owner-{index}"
            state = control.start_run(state, f"run-{index}", owner, now, 900)
            epoch = state["coordinator"]["epoch"]
            state = control.reconcile_month(state, owner, epoch, now)
            state = control.register_job(
                state, owner, epoch, now, job_id=f"job-{index}", provider_job_id=None,
                spec_sha256=f"{index:x}" * 64, idempotency_key=f"idem-{index}",
                provider_status="running", deadline=now + timedelta(hours=1), reserve_cents=800,
            )
            state = finish_job(state, owner, epoch, now, suffix=f"run-{index}")
            state = control.complete_run(state, owner, epoch, now)
            now += timedelta(minutes=1)
        state = control.start_run(state, "run-6", "owner-6", now, 900)
        epoch = state["coordinator"]["epoch"]
        state = control.reconcile_month(state, "owner-6", epoch, now)
        with self.assertRaises(control.ControlError):
            control.register_job(
                state, "owner-6", epoch, now, job_id="job-6", provider_job_id=None,
                spec_sha256="f" * 64, idempotency_key="idem-6", provider_status="running",
                deadline=now + timedelta(hours=1), reserve_cents=201,
            )
        accepted = control.register_job(
            state, "owner-6", epoch, now, job_id="job-6", provider_job_id=None,
            spec_sha256="f" * 64, idempotency_key="idem-6", provider_status="running",
            deadline=now + timedelta(hours=1), reserve_cents=200,
        )
        self.assertEqual(control._month_exposure(accepted, "2026-10"), 5_000)

    def test_reconciliation_month_boundary_delayed_cost_and_identity_reuse(self) -> None:
        state = control.start_run(control.empty_state(), "run-a", "owner-a", self.NOW, 900)
        with self.assertRaises(control.ControlError):
            control.register_job(
                state, "owner-a", 1, self.NOW, job_id="job-a", provider_job_id=None,
                spec_sha256="c" * 64, idempotency_key="idem-a", provider_status="running",
                deadline=self.NOW + timedelta(hours=1), reserve_cents=100,
            )
        state = control.reconcile_month(state, "owner-a", 1, self.NOW)
        with self.assertRaises(control.ControlError):
            control.register_job(
                state, "owner-a", 1, self.NOW, job_id="zero", provider_job_id=None,
                spec_sha256="0" * 64, idempotency_key="zero", provider_status="running",
                deadline=self.NOW + timedelta(hours=1), reserve_cents=0,
            )
        month_end = datetime(2026, 11, 1, 4, 30, tzinfo=timezone.utc)
        month_state = control.start_run(control.empty_state(), "month-run", "month-owner", month_end, 900)
        month_state = control.reconcile_month(month_state, "month-owner", 1, month_end)
        with self.assertRaises(control.ControlError):
            control.register_job(
                month_state, "month-owner", 1, month_end, job_id="crossing",
                provider_job_id=None, spec_sha256="d" * 64,
                idempotency_key="idem-crossing", provider_status="running",
                deadline=month_end + timedelta(hours=2), reserve_cents=100,
            )

        state = control.register_job(
            state, "owner-a", 1, self.NOW, job_id="job-a", provider_job_id=None,
            spec_sha256="c" * 64, idempotency_key="idem-a", provider_status="running",
            deadline=self.NOW + timedelta(hours=1), reserve_cents=100,
        )
        state = finish_job(state, "owner-a", 1, self.NOW, suffix="job-a")
        state = control.complete_run(state, "owner-a", 1, self.NOW)
        state = control.start_run(state, "run-b", "owner-b", self.NOW, 900)
        settled = control.record_cost(
            state, "owner-b", 2, self.NOW, cost_id="compute-reservation:job-a",
            job_id="job-a", category="compute", status="spent",
            reserved_cents=None, spent_cents=73, incurred_at=self.NOW,
        )
        self.assertEqual(control._job_exposure(settled, "job-a"), 73)
        with self.assertRaises(control.ControlError):
            control.register_job(
                settled, "owner-b", 2, self.NOW, job_id="retry",
                provider_job_id=None, spec_sha256="c" * 64,
                idempotency_key="idem-a", provider_status="running",
                deadline=self.NOW + timedelta(hours=1), reserve_cents=100,
            )

    def test_checkpoint_is_required_and_invalidated_by_new_job(self) -> None:
        state = control.start_run(control.empty_state(), "run", "owner", self.NOW, 900)
        with self.assertRaises(control.ControlError):
            control.complete_run(state, "owner", 1, self.NOW)
        state = control.checkpoint_run(
            state, "owner", 1, self.NOW, repository_branch="codex/pre-job",
            repository_commit="d" * 40, verify_remote=accept_test_checkpoint,
        )
        state = control.reconcile_month(state, "owner", 1, self.NOW)
        state = control.register_job(
            state, "owner", 1, self.NOW, job_id="job", provider_job_id=None,
            spec_sha256="1" * 64, idempotency_key="idem", provider_status="running",
            deadline=self.NOW + timedelta(hours=1), reserve_cents=100,
        )
        self.assertFalse(state["checkpoint"]["workers_terminal"])
        state = control.update_job(
            state, "owner", 1, self.NOW, provider_status="terminated",
            artifact_ref="s3://ce/job.tar", artifact_sha256="2" * 64,
            artifacts_retrieved=True, termination_confirmed=True,
            termination_receipt="prime:termination:job",
        )
        with self.assertRaises(control.ControlError):
            control.complete_run(state, "owner", 1, self.NOW)


class MoneyParsingTests(unittest.TestCase):
    def test_non_finite_usd_is_refused_without_conversion_exception(self) -> None:
        for value in ("NaN", "sNaN", "Infinity", "-Infinity"):
            with self.subTest(value=value), self.assertRaises(control.ControlError):
                control.usd_to_cents(value)
        self.assertEqual(control.usd_to_cents("8.00"), 800)


if __name__ == "__main__":
    unittest.main()
