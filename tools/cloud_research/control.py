#!/usr/bin/env python3
"""Cooperative cross-clone research control on one append-only Git ref.

This controller serializes repository research; it does not provision, stop, or
otherwise control a compute provider. Provider deadlines and termination fields
are evidence used to fail closed, not claims that a GPU was actually stopped.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


CONTROL_REF = "refs/heads/codex/cloud-research-control"
STATE_PATH = "state.json"
SCHEMA = "catalytic-earth.cloud-research-control.v1"
JOB_CAP_CENTS = 800
MONTH_CAP_CENTS = 5_000
PROVIDER_STATUSES = {
    "launch_pending", "queued", "running", "succeeded", "failed",
    "cancelled", "terminated", "unknown",
}
TERMINAL_PROVIDER_STATUSES = {"succeeded", "failed", "cancelled", "terminated"}
LEDGER_STATUSES = {"reserved", "spent", "failed", "unknown"}
COST_CATEGORIES = {"compute", "controller", "storage"}


class ControlError(RuntimeError):
    """A fail-closed state, policy, or Git control error."""


class CasConflict(ControlError):
    """The remote control ref changed before this update was published."""


@dataclass(frozen=True)
class Snapshot:
    head: str | None
    state: dict[str, object]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ControlError(f"invalid timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise ControlError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def chicago_timezone() -> ZoneInfo:
    try:
        return ZoneInfo("America/Chicago")
    except ZoneInfoNotFoundError as exc:
        raise ControlError(
            "America/Chicago timezone data is unavailable; install system tzdata"
        ) from exc


def _calendar_month(value: datetime) -> str:
    return value.astimezone(chicago_timezone()).strftime("%Y-%m")


def usd_to_cents(value: str) -> int:
    try:
        amount = Decimal(value)
        if not amount.is_finite():
            raise InvalidOperation
        cents = amount * 100
        if amount < 0 or cents != cents.to_integral_value():
            raise ControlError("USD amounts must be non-negative with at most two decimals")
        return int(cents)
    except (InvalidOperation, ValueError, OverflowError) as exc:
        raise ControlError(f"invalid USD amount: {value}") from exc


def _valid_branch(branch: object) -> bool:
    return (
        isinstance(branch, str)
        and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", branch))
        and ".." not in branch
        and "//" not in branch
        and not branch.endswith(("/", ".", ".lock"))
    )


def _valid_durable_ref(value: object) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(
        r"(?!file:)[a-z][a-z0-9+.-]*://[A-Za-z0-9._:/+-]+", value
    ))


def empty_state() -> dict[str, object]:
    return {
        "schema_version": SCHEMA,
        "active_run_id": None,
        "phase": "idle",
        "coordinator": {
            "owner": None,
            "epoch": 0,
            "heartbeat_at": None,
            "lease_expires_at": None,
        },
        "recovery": {"required": False, "claimed_at": None, "previous_owner": None},
        "checkpoint": {
            "workers_terminal": False,
            "repository_branch": None,
            "repository_commit": None,
        },
        "job": None,
        "job_history": [],
        "budget": {
            "currency": "USD",
            "funding_source": "prime_intellect_usd_authorization",
            "job_cap_cents": JOB_CAP_CENTS,
            "calendar_month_cap_cents": MONTH_CAP_CENTS,
            "timezone": "America/Chicago",
            "reconciled_months": [],
            "ledger": [],
        },
    }


def _require_exact_keys(value: object, keys: set[str], label: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ControlError(f"invalid {label} fields")
    return value


def _entry_exposure(entry: dict[str, object]) -> int:
    spent = int(entry["spent_cents"])
    return spent if entry["status"] == "spent" else max(int(entry["reserved_cents"]), spent)


def _job_exposure(state: dict[str, object], job_id: str) -> int:
    ledger = state["budget"]["ledger"]  # type: ignore[index]
    return sum(_entry_exposure(entry) for entry in ledger if entry["job_id"] == job_id)


def _month_exposure(state: dict[str, object], month: str) -> int:
    ledger = state["budget"]["ledger"]  # type: ignore[index]
    return sum(_entry_exposure(entry) for entry in ledger if entry["calendar_month"] == month)


def validate_state(state: dict[str, object]) -> None:
    _require_exact_keys(
        state,
        {"schema_version", "active_run_id", "phase", "coordinator", "recovery", "checkpoint",
         "job", "job_history", "budget"},
        "state",
    )
    if state["schema_version"] != SCHEMA:
        raise ControlError("unsupported control-state schema")
    coordinator = _require_exact_keys(
        state["coordinator"], {"owner", "epoch", "heartbeat_at", "lease_expires_at"}, "coordinator"
    )
    if not isinstance(coordinator["epoch"], int) or coordinator["epoch"] < 0:
        raise ControlError("invalid coordinator epoch")
    recovery = _require_exact_keys(
        state["recovery"], {"required", "claimed_at", "previous_owner"}, "recovery"
    )
    if not isinstance(recovery["required"], bool):
        raise ControlError("invalid recovery flag")
    checkpoint = _require_exact_keys(
        state["checkpoint"], {"workers_terminal", "repository_branch", "repository_commit"},
        "checkpoint",
    )
    if not isinstance(checkpoint["workers_terminal"], bool):
        raise ControlError("invalid worker checkpoint")
    if checkpoint["repository_branch"] is not None and not _valid_branch(
        checkpoint["repository_branch"]
    ):
        raise ControlError("invalid checkpoint branch")
    if checkpoint["repository_commit"] is not None and not re.fullmatch(
        r"[0-9a-f]{40}|[0-9a-f]{64}", str(checkpoint["repository_commit"])
    ):
        raise ControlError("invalid checkpoint commit")
    budget = _require_exact_keys(
        state["budget"],
        {"currency", "funding_source", "job_cap_cents", "calendar_month_cap_cents", "timezone",
         "reconciled_months", "ledger"},
        "budget",
    )
    if (budget["currency"], budget["funding_source"], budget["job_cap_cents"],
            budget["calendar_month_cap_cents"], budget["timezone"]) != (
        "USD", "prime_intellect_usd_authorization", JOB_CAP_CENTS, MONTH_CAP_CENTS,
        "America/Chicago"
    ):
        raise ControlError("budget policy differs from the authorized limits")
    if not isinstance(budget["ledger"], list):
        raise ControlError("budget ledger must be a list")
    if not isinstance(budget["reconciled_months"], list) or any(
        not isinstance(month, str) or not re.fullmatch(r"\d{4}-\d{2}", month)
        for month in budget["reconciled_months"]
    ):
        raise ControlError("invalid reconciled month list")
    seen_costs: set[str] = set()
    for entry in budget["ledger"]:
        item = _require_exact_keys(
            entry,
            {"cost_id", "run_id", "job_id", "category", "status", "calendar_month",
             "recorded_at", "reserved_cents", "spent_cents"},
            "ledger entry",
        )
        if not all(isinstance(item[key], str) and item[key] for key in ("cost_id", "run_id", "job_id")):
            raise ControlError("ledger identifiers must be non-empty strings")
        if item["cost_id"] in seen_costs:
            raise ControlError("duplicate ledger cost_id")
        seen_costs.add(str(item["cost_id"]))
        if item["category"] not in COST_CATEGORIES or item["status"] not in LEDGER_STATUSES:
            raise ControlError("invalid ledger category or status")
        if not re.fullmatch(r"\d{4}-\d{2}", str(item["calendar_month"])):
            raise ControlError("invalid ledger calendar month")
        parse_time(str(item["recorded_at"]))
        if any(not isinstance(item[key], int) or item[key] < 0 for key in ("reserved_cents", "spent_cents")):
            raise ControlError("ledger amounts must be non-negative integer cents")

    if not isinstance(state["job_history"], list):
        raise ControlError("job history must be a list")
    seen_jobs: set[str] = set()
    seen_idempotency_keys: set[str] = set()
    for entry in state["job_history"]:
        item = _require_exact_keys(
            entry,
            {"run_id", "job_id", "provider_job_id", "spec_sha256", "idempotency_key",
             "provider_status", "deadline_at", "completed_at", "artifact_ref",
             "artifact_sha256", "termination_receipt", "repository_branch",
             "repository_commit"},
            "job history entry",
        )
        if not all(isinstance(item[key], str) and item[key] for key in (
            "run_id", "job_id", "spec_sha256", "idempotency_key", "artifact_ref",
            "artifact_sha256", "termination_receipt", "repository_branch",
            "repository_commit",
        )):
            raise ControlError("completed job fields must be non-empty strings")
        if item["provider_job_id"] is not None and not isinstance(item["provider_job_id"], str):
            raise ControlError("invalid completed provider job id")
        if item["provider_status"] not in TERMINAL_PROVIDER_STATUSES:
            raise ControlError("completed job has a non-terminal provider status")
        if not re.fullmatch(r"[0-9a-f]{64}", str(item["spec_sha256"])):
            raise ControlError("invalid completed job spec SHA-256")
        if not re.fullmatch(r"[0-9a-f]{64}", str(item["artifact_sha256"])):
            raise ControlError("invalid completed artifact SHA-256")
        if not _valid_durable_ref(item["artifact_ref"]):
            raise ControlError("invalid completed durable artifact reference")
        if not _valid_branch(item["repository_branch"]) or not re.fullmatch(
            r"[0-9a-f]{40}|[0-9a-f]{64}", str(item["repository_commit"])
        ):
            raise ControlError("invalid completed repository checkpoint")
        parse_time(str(item["deadline_at"]))
        parse_time(str(item["completed_at"]))
        if item["job_id"] in seen_jobs or item["idempotency_key"] in seen_idempotency_keys:
            raise ControlError("completed job identity was reused")
        seen_jobs.add(str(item["job_id"]))
        seen_idempotency_keys.add(str(item["idempotency_key"]))

    active = state["active_run_id"]
    if active is None:
        if state["phase"] != "idle" or state["job"] is not None or coordinator["owner"] is not None:
            raise ControlError("idle state retains active ownership or job state")
        return
    if not isinstance(active, str) or not active or state["phase"] not in {
        "researching", "waiting_compute", "finalizing"
    }:
        raise ControlError("invalid active run state")
    if not isinstance(coordinator["owner"], str) or not coordinator["owner"]:
        raise ControlError("active run lacks a coordinator owner")
    parse_time(str(coordinator["heartbeat_at"]))
    parse_time(str(coordinator["lease_expires_at"]))
    if state["job"] is not None:
        job = _require_exact_keys(
            state["job"],
            {"job_id", "provider_job_id", "spec_sha256", "idempotency_key", "provider_status",
             "deadline_at", "compute_cost_id", "artifact_ref", "artifact_sha256",
             "artifacts_retrieved", "repository_checkpointed", "termination_confirmed",
             "termination_receipt"},
            "job",
        )
        if not all(isinstance(job[key], str) and job[key] for key in
                   ("job_id", "spec_sha256", "idempotency_key", "compute_cost_id")):
            raise ControlError("job identifiers must be non-empty strings")
        if not re.fullmatch(r"[0-9a-f]{64}", str(job["spec_sha256"])):
            raise ControlError("job spec_sha256 must be lowercase hex")
        if job["provider_job_id"] is not None and not isinstance(job["provider_job_id"], str):
            raise ControlError("invalid provider job id")
        if job["provider_status"] not in PROVIDER_STATUSES:
            raise ControlError("invalid provider status")
        parse_time(str(job["deadline_at"]))
        if job["artifact_ref"] is not None and not _valid_durable_ref(job["artifact_ref"]):
            raise ControlError("artifact_ref must be a credential-free durable URI")
        if job["artifact_sha256"] is not None and not re.fullmatch(
            r"[0-9a-f]{64}", str(job["artifact_sha256"])
        ):
            raise ControlError("invalid artifact SHA-256")
        if any(not isinstance(job[key], bool) for key in
               ("artifacts_retrieved", "repository_checkpointed", "termination_confirmed")):
            raise ControlError("invalid job completion evidence")
        if job["termination_receipt"] is not None and (
            not isinstance(job["termination_receipt"], str)
            or not re.fullmatch(r"[A-Za-z0-9._:/+-]+", job["termination_receipt"])
        ):
            raise ControlError("invalid termination receipt")


def _lease_is_live(state: dict[str, object], now: datetime) -> bool:
    coordinator = state["coordinator"]  # type: ignore[assignment]
    expires = coordinator["lease_expires_at"]
    return expires is not None and now < parse_time(str(expires))


def _set_lease(state: dict[str, object], owner: str, now: datetime, seconds: int, *, bump: bool) -> None:
    if not owner or seconds <= 0 or seconds > 3600:
        raise ControlError("owner is required and lease must be 1..3600 seconds")
    coordinator = state["coordinator"]  # type: ignore[assignment]
    coordinator["owner"] = owner
    if bump:
        coordinator["epoch"] += 1
    coordinator["heartbeat_at"] = format_time(now)
    coordinator["lease_expires_at"] = format_time(now + timedelta(seconds=seconds))


def _require_owner(state: dict[str, object], owner: str, epoch: int, now: datetime) -> None:
    if state["active_run_id"] is None:
        raise ControlError("no active run")
    coordinator = state["coordinator"]  # type: ignore[assignment]
    if coordinator["owner"] != owner or coordinator["epoch"] != epoch:
        raise ControlError("stale or non-owner coordinator")
    if not _lease_is_live(state, now):
        raise ControlError("coordinator lease expired; claim recovery with a new epoch")


def start_run(state: dict[str, object], run_id: str, owner: str, now: datetime, lease_seconds: int) -> dict[str, object]:
    validate_state(state)
    if state["active_run_id"] is not None or not run_id:
        raise ControlError("another run is active or run_id is empty")
    result = copy.deepcopy(state)
    result.update({"active_run_id": run_id, "phase": "researching", "job": None})
    result["recovery"] = {"required": False, "claimed_at": None, "previous_owner": None}
    result["checkpoint"] = {
        "workers_terminal": False,
        "repository_branch": None,
        "repository_commit": None,
    }
    _set_lease(result, owner, now, lease_seconds, bump=True)
    validate_state(result)
    return result


def claim_recovery(state: dict[str, object], owner: str, now: datetime, lease_seconds: int) -> dict[str, object]:
    validate_state(state)
    if state["active_run_id"] is None:
        raise ControlError("no active run to recover")
    if _lease_is_live(state, now):
        raise ControlError("coordinator lease is still live")
    result = copy.deepcopy(state)
    previous_owner = result["coordinator"]["owner"]  # type: ignore[index]
    _set_lease(result, owner, now, lease_seconds, bump=True)
    result["recovery"] = {
        "required": True,
        "claimed_at": format_time(now),
        "previous_owner": previous_owner,
    }
    validate_state(result)
    return result


def heartbeat(state: dict[str, object], owner: str, epoch: int, now: datetime, lease_seconds: int) -> dict[str, object]:
    validate_state(state)
    _require_owner(state, owner, epoch, now)
    result = copy.deepcopy(state)
    _set_lease(result, owner, now, lease_seconds, bump=False)
    return result


def reconcile_month(
    state: dict[str, object], owner: str, epoch: int, now: datetime
) -> dict[str, object]:
    """Attest that existing Prime/provider charges for this month were imported."""
    validate_state(state)
    _require_owner(state, owner, epoch, now)
    result = copy.deepcopy(state)
    month = _calendar_month(now)
    months = result["budget"]["reconciled_months"]  # type: ignore[index]
    if month not in months:
        months.append(month)
        months.sort()
    validate_state(result)
    return result


def checkpoint_run(
    state: dict[str, object], owner: str, epoch: int, now: datetime, *,
    repository_branch: str, repository_commit: str,
    verify_remote: Callable[[str, str], None],
) -> dict[str, object]:
    """Record the durable Git checkpoint after all run workers have stopped."""
    validate_state(state)
    _require_owner(state, owner, epoch, now)
    if not _valid_branch(repository_branch) or not re.fullmatch(
        r"[0-9a-f]{40}|[0-9a-f]{64}", repository_commit
    ):
        raise ControlError("checkpoint requires a branch and full Git object id")
    job = state["job"]
    if job is not None and (
        job["provider_status"] not in TERMINAL_PROVIDER_STATUSES
        or not job["artifacts_retrieved"]
        or not job["artifact_ref"]
        or not job["artifact_sha256"]
        or not job["termination_confirmed"]
        or not job["termination_receipt"]
    ):
        raise ControlError("checkpoint requires terminal compute and retrieved durable artifacts")
    verify_remote(repository_branch, repository_commit)
    result = copy.deepcopy(state)
    result["checkpoint"] = {
        "workers_terminal": True,
        "repository_branch": repository_branch,
        "repository_commit": repository_commit,
    }
    if result["job"] is not None:
        result["job"]["repository_checkpointed"] = True
    validate_state(result)
    return result


def _budget_overrun(state: dict[str, object]) -> bool:
    ledger = state["budget"]["ledger"]  # type: ignore[index]
    jobs = {str(entry["job_id"]) for entry in ledger}
    months = {str(entry["calendar_month"]) for entry in ledger}
    return any(_job_exposure(state, job) > JOB_CAP_CENTS for job in jobs) or any(
        _month_exposure(state, month) > MONTH_CAP_CENTS for month in months
    )


def _put_cost(
    state: dict[str, object], entry: dict[str, object], *, enforce_caps: bool
) -> None:
    ledger = state["budget"]["ledger"]  # type: ignore[index]
    prior = next((item for item in ledger if item["cost_id"] == entry["cost_id"]), None)
    if prior is not None:
        for key in ("run_id", "job_id", "category", "calendar_month", "reserved_cents"):
            if prior[key] != entry[key]:
                raise ControlError(f"cost entry cannot change {key}")
        transitions = {
            "reserved": LEDGER_STATUSES,
            "unknown": {"unknown", "failed", "spent"},
            "failed": {"failed", "spent"},
            "spent": {"spent"},
        }
        if entry["status"] not in transitions[prior["status"]] or entry["spent_cents"] < prior["spent_cents"]:
            raise ControlError("invalid cost settlement transition")
        ledger[ledger.index(prior)] = entry
    else:
        ledger.append(entry)
    if enforce_caps and _job_exposure(state, str(entry["job_id"])) > JOB_CAP_CENTS:
        raise ControlError("$8 per-job authorization would be exceeded")
    if enforce_caps and _month_exposure(state, str(entry["calendar_month"])) > MONTH_CAP_CENTS:
        raise ControlError("$50 America/Chicago calendar-month authorization would be exceeded")


def register_job(
    state: dict[str, object], owner: str, epoch: int, now: datetime, *, job_id: str,
    provider_job_id: str | None, spec_sha256: str, idempotency_key: str,
    provider_status: str, deadline: datetime, reserve_cents: int,
) -> dict[str, object]:
    validate_state(state)
    _require_owner(state, owner, epoch, now)
    if state["job"] is not None or not job_id or not idempotency_key or deadline <= now:
        raise ControlError("job already exists, job_id is empty, or deadline is not future")
    if reserve_cents <= 0:
        raise ControlError("a paid job requires a positive worst-case reservation")
    if _budget_overrun(state):
        raise ControlError("an existing job or month exceeds its authorization; new paid work is blocked")
    if any(
        entry["job_id"] == job_id or entry["idempotency_key"] == idempotency_key
        or entry["spec_sha256"] == spec_sha256
        or (provider_job_id is not None and entry["provider_job_id"] == provider_job_id)
        for entry in state["job_history"]
    ) or any(entry["job_id"] == job_id for entry in state["budget"]["ledger"]):
        raise ControlError("job, spec, provider job, or idempotency identity was already used")
    month = _calendar_month(now)
    if _calendar_month(deadline) != month:
        raise ControlError("job deadline crosses an America/Chicago month boundary")
    if month not in state["budget"]["reconciled_months"]:  # type: ignore[index]
        raise ControlError("current America/Chicago month charges are not reconciled")
    if provider_status not in PROVIDER_STATUSES - TERMINAL_PROVIDER_STATUSES:
        raise ControlError("a new job must have a non-terminal provider status")
    result = copy.deepcopy(state)
    result["checkpoint"] = {
        "workers_terminal": False,
        "repository_branch": None,
        "repository_commit": None,
    }
    cost_id = f"compute-reservation:{job_id}"
    result["job"] = {
        "job_id": job_id,
        "provider_job_id": provider_job_id,
        "spec_sha256": spec_sha256,
        "idempotency_key": idempotency_key,
        "provider_status": provider_status,
        "deadline_at": format_time(deadline),
        "compute_cost_id": cost_id,
        "artifact_ref": None,
        "artifact_sha256": None,
        "artifacts_retrieved": False,
        "repository_checkpointed": False,
        "termination_confirmed": False,
        "termination_receipt": None,
    }
    result["phase"] = "waiting_compute"
    _put_cost(result, {
        "cost_id": cost_id,
        "run_id": result["active_run_id"],
        "job_id": job_id,
        "category": "compute",
        "status": "reserved",
        "calendar_month": month,
        "recorded_at": format_time(now),
        "reserved_cents": reserve_cents,
        "spent_cents": 0,
    }, enforce_caps=True)
    validate_state(result)
    return result


def record_cost(
    state: dict[str, object], owner: str, epoch: int, now: datetime, *, cost_id: str,
    job_id: str, category: str, status: str, reserved_cents: int | None,
    spent_cents: int | None, incurred_at: datetime,
) -> dict[str, object]:
    validate_state(state)
    _require_owner(state, owner, epoch, now)
    job = state["job"]
    if job is not None and job["job_id"] != job_id:
        raise ControlError("cost must belong to the active job while one exists")
    if category not in COST_CATEGORIES or status not in LEDGER_STATUSES:
        raise ControlError("cost uses an unrecognized category or status")
    result = copy.deepcopy(state)
    ledger = result["budget"]["ledger"]  # type: ignore[index]
    prior = next((item for item in ledger if item["cost_id"] == cost_id), None)
    entry = {
        "cost_id": cost_id,
        "run_id": prior["run_id"] if prior else result["active_run_id"],
        "job_id": job_id,
        "category": category,
        "status": status,
        "calendar_month": (prior["calendar_month"] if prior else _calendar_month(incurred_at)),
        "recorded_at": format_time(now),
        "reserved_cents": int(prior["reserved_cents"] if prior and reserved_cents is None else (reserved_cents or 0)),
        "spent_cents": int(prior["spent_cents"] if prior and spent_cents is None else (spent_cents or 0)),
    }
    if status == "reserved" and entry["reserved_cents"] <= 0:
        raise ControlError("a future cost reservation must be positive")
    # Actual, failed, and unknown charges are facts and remain recordable above
    # a cap. New reservations are authorization decisions and fail at the cap.
    _put_cost(result, entry, enforce_caps=(status == "reserved"))
    validate_state(result)
    return result


def update_job(
    state: dict[str, object], owner: str, epoch: int, now: datetime, *,
    provider_status: str | None = None, provider_job_id: str | None = None,
    artifact_ref: str | None = None, artifact_sha256: str | None = None,
    artifacts_retrieved: bool = False, termination_confirmed: bool = False,
    termination_receipt: str | None = None,
) -> dict[str, object]:
    validate_state(state)
    _require_owner(state, owner, epoch, now)
    if state["job"] is None:
        raise ControlError("no active job")
    if state["checkpoint"]["workers_terminal"]:
        raise ControlError("run is already checkpointed")
    result = copy.deepcopy(state)
    job = result["job"]
    if provider_job_id:
        if job["provider_job_id"] not in (None, provider_job_id):
            raise ControlError("provider job id is immutable once recorded")
        job["provider_job_id"] = provider_job_id
    if provider_status:
        if provider_status not in PROVIDER_STATUSES:
            raise ControlError("invalid provider status")
        if job["provider_status"] in TERMINAL_PROVIDER_STATUSES and provider_status not in TERMINAL_PROVIDER_STATUSES:
            raise ControlError("terminal provider state cannot return to a live/unknown state")
        job["provider_status"] = provider_status
    if artifact_ref is not None:
        if job["artifact_ref"] not in (None, artifact_ref):
            raise ControlError("artifact reference is immutable once recorded")
        job["artifact_ref"] = artifact_ref
    if artifact_sha256 is not None:
        if job["artifact_sha256"] not in (None, artifact_sha256):
            raise ControlError("artifact SHA-256 is immutable once recorded")
        job["artifact_sha256"] = artifact_sha256
    if termination_receipt is not None:
        if job["termination_receipt"] not in (None, termination_receipt):
            raise ControlError("termination receipt is immutable once recorded")
        job["termination_receipt"] = termination_receipt
    job["artifacts_retrieved"] = job["artifacts_retrieved"] or artifacts_retrieved
    job["termination_confirmed"] = job["termination_confirmed"] or termination_confirmed
    result["phase"] = "finalizing" if job["provider_status"] in TERMINAL_PROVIDER_STATUSES else "waiting_compute"
    validate_state(result)
    return result


def complete_run(state: dict[str, object], owner: str, epoch: int, now: datetime) -> dict[str, object]:
    validate_state(state)
    _require_owner(state, owner, epoch, now)
    checkpoint = state["checkpoint"]
    if not checkpoint["workers_terminal"] or not checkpoint["repository_branch"] or not checkpoint["repository_commit"]:
        raise ControlError("workers must stop and repository work must be durably checkpointed")
    job = state["job"]
    if job is not None and (
        job["provider_status"] not in TERMINAL_PROVIDER_STATUSES
        or not job["artifacts_retrieved"]
        or not job["artifact_ref"]
        or not job["artifact_sha256"]
        or not job["repository_checkpointed"]
        or not job["termination_confirmed"]
        or not job["termination_receipt"]
    ):
        raise ControlError("job is live/unknown or lacks retrieval, checkpoint, or termination evidence")
    result = copy.deepcopy(state)
    if job is not None:
        result["job_history"].append({
            "run_id": result["active_run_id"],
            "job_id": job["job_id"],
            "provider_job_id": job["provider_job_id"],
            "spec_sha256": job["spec_sha256"],
            "idempotency_key": job["idempotency_key"],
            "provider_status": job["provider_status"],
            "deadline_at": job["deadline_at"],
            "completed_at": format_time(now),
            "artifact_ref": job["artifact_ref"],
            "artifact_sha256": job["artifact_sha256"],
            "termination_receipt": job["termination_receipt"],
            "repository_branch": checkpoint["repository_branch"],
            "repository_commit": checkpoint["repository_commit"],
        })
    result.update({"active_run_id": None, "phase": "idle", "job": None})
    result["coordinator"].update({"owner": None, "heartbeat_at": None, "lease_expires_at": None})  # type: ignore[union-attr]
    result["recovery"] = {"required": False, "claimed_at": None, "previous_owner": None}
    result["checkpoint"] = {
        "workers_terminal": False,
        "repository_branch": None,
        "repository_commit": None,
    }
    validate_state(result)
    return result


def _git(cwd: Path, args: list[str], *, input_text: str | None = None, env: dict[str, str] | None = None) -> str:
    process = subprocess.run(
        # Git plumbing consumes exact bytes. Text-mode stdin turns LF into CRLF
        # on Windows, making mktree store a filename ending in a carriage return.
        ["git", *args], cwd=cwd,
        input=input_text.encode("utf-8") if input_text is not None else None,
        capture_output=True,
        env=env, check=False,
    )
    if process.returncode:
        raise ControlError("Git control operation failed; credentials and remote output are suppressed")
    return process.stdout.decode("utf-8").strip()


class GitRefStore:
    """Git-backed CAS store; normal non-force pushes are the compare-and-swap."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()
        self.origin_url = _git(self.repo_root, ["remote", "get-url", "origin"])

    def _temporary_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory(prefix="ce-control-")
        root = Path(temp.name)
        _git(root, ["init", "--bare", "--quiet"])
        _git(root, ["remote", "add", "origin", self.origin_url])
        return temp, root

    def read(self) -> Snapshot:
        temp, root = self._temporary_repo()
        try:
            listing = _git(root, ["ls-remote", "--refs", "origin", CONTROL_REF])
            if not listing:
                state = empty_state()
                validate_state(state)
                return Snapshot(None, state)
            _git(root, ["fetch", "--quiet", "--no-tags", "origin", f"{CONTROL_REF}:refs/control/current"])
            head = _git(root, ["rev-parse", "refs/control/current"])
            raw = _git(root, ["show", f"{head}:{STATE_PATH}"])
            state = json.loads(raw)
            validate_state(state)
            return Snapshot(head, state)
        finally:
            temp.cleanup()

    def verify_checkpoint(self, branch: str, commit: str) -> None:
        """Require the checkpoint commit to be the current origin branch tip."""
        if not _valid_branch(branch) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
            raise ControlError("invalid repository checkpoint")
        ref = f"refs/heads/{branch}"
        process = subprocess.run(
            ["git", "check-ref-format", ref], cwd=self.repo_root,
            text=True, capture_output=True, check=False,
        )
        if process.returncode:
            raise ControlError("invalid repository checkpoint branch")
        listing = _git(self.repo_root, ["ls-remote", "--refs", "origin", ref])
        tips = [line.split()[0] for line in listing.splitlines() if line.strip()]
        if tips != [commit]:
            raise ControlError("checkpoint commit is not the verified origin branch tip")

    def compare_and_swap(self, expected_head: str | None, state: dict[str, object], message: str) -> str:
        validate_state(state)
        temp, root = self._temporary_repo()
        try:
            listing = _git(root, ["ls-remote", "--refs", "origin", CONTROL_REF])
            current = listing.split()[0] if listing else None
            if current != expected_head:
                raise CasConflict("control ref changed; re-read before retrying")
            if current:
                _git(root, ["fetch", "--quiet", "--no-tags", "origin", f"{CONTROL_REF}:refs/control/current"])
            payload = json.dumps(state, indent=2, sort_keys=True) + "\n"
            blob = _git(root, ["hash-object", "-w", "--stdin"], input_text=payload)
            tree = _git(root, ["mktree"], input_text=f"100644 blob {blob}\t{STATE_PATH}\n")
            commit_args = ["commit-tree", tree, "-m", message]
            if current:
                commit_args[2:2] = ["-p", current]
            stamp = format_time(utc_now())
            env = {
                **os.environ,
                "GIT_AUTHOR_NAME": "Catalytic Earth controller",
                "GIT_AUTHOR_EMAIL": "controller@catalytic-earth.invalid",
                "GIT_COMMITTER_NAME": "Catalytic Earth controller",
                "GIT_COMMITTER_EMAIL": "controller@catalytic-earth.invalid",
                "GIT_AUTHOR_DATE": stamp,
                "GIT_COMMITTER_DATE": stamp,
            }
            commit = _git(root, commit_args, env=env)
            process = subprocess.run(
                ["git", "push", "--porcelain", "origin", f"{commit}:{CONTROL_REF}"],
                cwd=root, text=True, capture_output=True, check=False,
            )
            if process.returncode:
                output = (process.stdout + process.stderr).lower()
                if "rejected" in output or "non-fast-forward" in output or "fetch first" in output:
                    raise CasConflict("control ref changed; re-read before retrying")
                raise ControlError("remote rejected the control update; output is suppressed")
            return commit
        finally:
            temp.cleanup()


def _payload(snapshot: Snapshot, *, action: str, now: datetime) -> dict[str, object]:
    month = _calendar_month(now)
    return {
        "action": action,
        "control_ref": CONTROL_REF,
        "head": snapshot.head,
        "budget_exposure": {
            "calendar_month": month,
            "month_cents": _month_exposure(snapshot.state, month),
            "month_cap_cents": MONTH_CAP_CENTS,
            "over_cap": _budget_overrun(snapshot.state),
        },
        "state": snapshot.state,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--prepare", action="store_true",
        help="print a proposed CAS update for an external GitHub writer without pushing",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    for name in ("start", "claim"):
        command = commands.add_parser(name)
        if name == "start":
            command.add_argument("--run-id", required=True)
        command.add_argument("--owner", required=True)
        command.add_argument("--lease-seconds", type=int, default=900)
    heartbeat_parser = commands.add_parser("heartbeat")
    heartbeat_parser.add_argument("--owner", required=True)
    heartbeat_parser.add_argument("--epoch", type=int, required=True)
    heartbeat_parser.add_argument("--lease-seconds", type=int, default=900)
    reconcile = commands.add_parser("reconcile-month")
    reconcile.add_argument("--owner", required=True)
    reconcile.add_argument("--epoch", type=int, required=True)
    checkpoint = commands.add_parser("checkpoint")
    checkpoint.add_argument("--owner", required=True)
    checkpoint.add_argument("--epoch", type=int, required=True)
    checkpoint.add_argument("--repository-branch", required=True)
    checkpoint.add_argument("--repository-commit", required=True)
    job = commands.add_parser("register-job")
    job.add_argument("--owner", required=True); job.add_argument("--epoch", type=int, required=True)
    job.add_argument("--job-id", required=True); job.add_argument("--provider-job-id")
    job.add_argument("--spec-sha256", required=True); job.add_argument("--idempotency-key", required=True)
    job.add_argument("--provider-status", default="launch_pending", choices=sorted(PROVIDER_STATUSES))
    job.add_argument("--deadline", required=True); job.add_argument("--reserve-usd", required=True)
    update = commands.add_parser("update-job")
    update.add_argument("--owner", required=True); update.add_argument("--epoch", type=int, required=True)
    update.add_argument("--provider-job-id"); update.add_argument("--provider-status", choices=sorted(PROVIDER_STATUSES))
    update.add_argument("--artifact-ref"); update.add_argument("--artifact-sha256")
    update.add_argument("--artifacts-retrieved", action="store_true")
    update.add_argument("--termination-confirmed", action="store_true")
    update.add_argument("--termination-receipt")
    cost = commands.add_parser("record-cost")
    cost.add_argument("--owner", required=True); cost.add_argument("--epoch", type=int, required=True)
    cost.add_argument("--cost-id", required=True); cost.add_argument("--job-id", required=True)
    cost.add_argument("--category", required=True, choices=sorted(COST_CATEGORIES))
    cost.add_argument("--status", required=True, choices=sorted(LEDGER_STATUSES))
    cost.add_argument("--reserved-usd"); cost.add_argument("--spent-usd"); cost.add_argument("--incurred-at")
    complete = commands.add_parser("complete")
    complete.add_argument("--owner", required=True); complete.add_argument("--epoch", type=int, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    now = utc_now()
    try:
        store = GitRefStore(args.repo_root)
        snapshot = store.read()
        if args.command == "status":
            print(json.dumps(_payload(snapshot, action="status", now=now), sort_keys=True))
            return 0
        transitions: dict[str, Callable[[dict[str, object]], dict[str, object]]] = {
            "start": lambda state: start_run(state, args.run_id, args.owner, now, args.lease_seconds),
            "claim": lambda state: claim_recovery(state, args.owner, now, args.lease_seconds),
            "heartbeat": lambda state: heartbeat(state, args.owner, args.epoch, now, args.lease_seconds),
            "reconcile-month": lambda state: reconcile_month(state, args.owner, args.epoch, now),
            "checkpoint": lambda state: checkpoint_run(
                state, args.owner, args.epoch, now,
                repository_branch=args.repository_branch,
                repository_commit=args.repository_commit,
                verify_remote=store.verify_checkpoint,
            ),
            "register-job": lambda state: register_job(
                state, args.owner, args.epoch, now, job_id=args.job_id,
                provider_job_id=args.provider_job_id, spec_sha256=args.spec_sha256,
                idempotency_key=args.idempotency_key, provider_status=args.provider_status,
                deadline=parse_time(args.deadline), reserve_cents=usd_to_cents(args.reserve_usd),
            ),
            "update-job": lambda state: update_job(
                state, args.owner, args.epoch, now, provider_status=args.provider_status,
                provider_job_id=args.provider_job_id, artifacts_retrieved=args.artifacts_retrieved,
                artifact_ref=args.artifact_ref, artifact_sha256=args.artifact_sha256,
                termination_confirmed=args.termination_confirmed,
                termination_receipt=args.termination_receipt,
            ),
            "record-cost": lambda state: record_cost(
                state, args.owner, args.epoch, now, cost_id=args.cost_id, job_id=args.job_id,
                category=args.category, status=args.status,
                reserved_cents=usd_to_cents(args.reserved_usd) if args.reserved_usd is not None else None,
                spent_cents=usd_to_cents(args.spent_usd) if args.spent_usd is not None else None,
                incurred_at=parse_time(args.incurred_at) if args.incurred_at else now,
            ),
            "complete": lambda state: complete_run(state, args.owner, args.epoch, now),
        }
        state = transitions[args.command](snapshot.state)
        if args.prepare:
            print(json.dumps({
                "action": args.command,
                "control_ref": CONTROL_REF,
                "expected_head": snapshot.head,
                "proposed_state": state,
            }, sort_keys=True))
            return 0
        head = store.compare_and_swap(snapshot.head, state, f"cloud research control: {args.command}")
        print(json.dumps(_payload(Snapshot(head, state), action=args.command, now=now), sort_keys=True))
        return 0
    except CasConflict as exc:
        print(json.dumps({"error": "cas_conflict", "reason": str(exc)}), file=sys.stderr)
        return 3
    except (ControlError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": "refused", "reason": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
