"""Truth-governance validation for claims and evaluation exposure.

The governance files are deliberately small and source controlled.  Historical
artifacts remain immutable; these ledgers control how current claims may refer
to them and whether an evaluation surface can still be called fresh.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

CLAIM_STATUSES = {"Supported", "Diagnostic", "Superseded", "Retracted"}
EXPOSURE_STATES = {"frozen_unscored", "exposed", "exhausted"}
EXPOSURE_EVENT_TYPES = {"freeze", "score", "review", "correction"}
REQUIRED_CLAIM_IDS = {f"CE-{index:03d}" for index in range(1, 14)}

DEFAULT_CLAIM_LEDGER = Path("data/governance/claim_ledger.json")
DEFAULT_EXPOSURE_LEDGER = Path("data/governance/exposure_ledger.jsonl")
DEFAULT_EXPANSION_FREEZE = Path("data/governance/expansion_freeze.json")
DEFAULT_CLAIMS_DOC = Path("CLAIMS.md")
DEFAULT_ERRATA_DOC = Path("ERRATA.md")
DEFAULT_POLICY_DOC = Path("docs/ATLAS_TRUTH_POLICY.md")

_REQUIRED_POLICY_TERMS = {
    "Net reaction",
    "Source mechanism",
    "Mechanism hypothesis",
    "Mechanism family/fingerprint",
    "Protein annotation record",
    "Experimental observation",
    "Tier 0",
    "Tier 1",
    "Tier 2",
    "Tier 3",
    "Tier 4",
}


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_registry_rows(path: Path) -> list[dict[str, Any]]:
    payload = _read_json(path)
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict) or not isinstance(payload.get("shards"), list):
        raise ValueError(f"{path} must be a registry list or sharded manifest")
    rows: list[dict[str, Any]] = []
    root = path.parent.resolve()
    for shard in payload["shards"]:
        if not isinstance(shard, dict) or not isinstance(shard.get("path"), str):
            raise ValueError(f"{path} contains a malformed shard")
        shard_path = (path.parent / shard["path"]).resolve()
        if root != shard_path and root not in shard_path.parents:
            raise ValueError(f"registry shard escapes its directory: {shard['path']}")
        shard_text = shard_path.read_text(encoding="utf-8")
        expected_sha = shard.get("sha256")
        actual_sha = hashlib.sha256(shard_text.encode("utf-8")).hexdigest()
        if not isinstance(expected_sha, str) or actual_sha != expected_sha:
            raise ValueError(
                f"registry shard SHA-256 mismatch for {shard['path']}: "
                f"expected {expected_sha!r}, got {actual_sha}"
            )
        expected_bytes = shard.get("bytes")
        actual_bytes = len(shard_text.encode("utf-8"))
        if expected_bytes is not None and actual_bytes != expected_bytes:
            raise ValueError(f"registry shard byte count mismatch for {shard['path']}")
        shard_rows = json.loads(shard_text)
        if not isinstance(shard_rows, list):
            raise ValueError(f"{shard_path} must contain a list")
        expected_rows = shard.get("row_count")
        if expected_rows is not None and len(shard_rows) != expected_rows:
            raise ValueError(f"registry shard row count mismatch for {shard['path']}")
        rows.extend(shard_rows)
    if payload.get("row_count") is not None and len(rows) != payload["row_count"]:
        raise ValueError(f"{path} row_count does not match its shards")
    return rows


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_expansion_freeze(
    path: Path = DEFAULT_EXPANSION_FREEZE,
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else _project_root()
    payload = _read_json(root / path)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    if not isinstance(payload.get("frozen"), bool):
        raise ValueError(f"{path} frozen must be boolean")
    protected = payload.get("protected_paths")
    if not isinstance(protected, list) or not protected:
        raise ValueError(f"{path} requires protected_paths")
    for protected_path in protected:
        if not isinstance(protected_path, str) or not protected_path:
            raise ValueError(f"{path} contains an invalid protected path")
    expected_hashes = payload.get("expected_sha256")
    if not isinstance(expected_hashes, dict) or set(expected_hashes) != set(protected):
        raise ValueError(f"{path} expected_sha256 must cover every protected path exactly")
    for protected_path, digest in expected_hashes.items():
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"{path} has an invalid SHA-256 for {protected_path}")
    return payload


def validate_expansion_freeze(
    path: Path = DEFAULT_EXPANSION_FREEZE,
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Validate protected paths and, while frozen, their exact bytes."""
    root = (Path(repo_root) if repo_root is not None else _project_root()).resolve()
    freeze = load_expansion_freeze(path, repo_root=root)
    for protected_path in freeze["protected_paths"]:
        full_path = root / protected_path
        if not full_path.exists():
            raise ValueError(f"expansion freeze protects a missing path: {protected_path}")
        if not freeze["frozen"]:
            continue
        digest = hashlib.sha256(full_path.read_bytes()).hexdigest()
        expected = freeze["expected_sha256"][protected_path]
        if digest != expected:
            raise ValueError(
                f"protected registry hash drifted while expansion is frozen: {protected_path}"
            )
    return freeze


def assert_expansion_write_allowed(
    target: Path,
    *,
    repo_root: Path | None = None,
) -> None:
    """Block protected checkout registries while the truth-reset freeze is active."""
    root = (Path(repo_root) if repo_root is not None else _project_root()).resolve()
    if not (root / DEFAULT_EXPANSION_FREEZE).exists():
        return
    freeze = load_expansion_freeze(repo_root=root)
    if not freeze["frozen"]:
        return
    target_path = Path(target)
    resolved_target = (root / target_path).resolve() if not target_path.is_absolute() else target_path.resolve()
    protected = {(root / relative).resolve() for relative in freeze["protected_paths"]}
    if resolved_target in protected:
        raise ValueError(
            f"truth-reset expansion freeze blocks writes to {resolved_target}; "
            f"see {DEFAULT_EXPANSION_FREEZE} and CLAIMS.md CE-012"
        )


def _parse_timestamp(value: str, *, field: str, event_id: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{event_id} {field} must be an ISO-8601 UTC timestamp ending in Z")
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{event_id} {field} is not a valid timestamp: {value}") from exc


def load_claim_ledger(path: Path = DEFAULT_CLAIM_LEDGER) -> list[dict[str, Any]]:
    payload = _read_json(Path(path))
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON list")
    return payload


def validate_claim_ledger(
    path: Path = DEFAULT_CLAIM_LEDGER,
    *,
    repo_root: Path = Path("."),
    claims_doc: Path = DEFAULT_CLAIMS_DOC,
) -> dict[str, int]:
    repo_root = Path(repo_root)
    path = repo_root / path
    claims = load_claim_ledger(path)
    seen: set[str] = set()
    status_counts = {status: 0 for status in sorted(CLAIM_STATUSES)}

    for row_number, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            raise ValueError(f"claim row {row_number} must be an object")
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or not re.fullmatch(r"CE-\d{3}", claim_id):
            raise ValueError(f"claim row {row_number} has invalid claim_id: {claim_id!r}")
        if claim_id in seen:
            raise ValueError(f"duplicate claim_id: {claim_id}")
        seen.add(claim_id)

        status = claim.get("status")
        if status not in CLAIM_STATUSES:
            raise ValueError(f"{claim_id} has invalid status: {status!r}")
        status_counts[status] += 1

        for field in ("claim", "current_wording", "rationale"):
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                raise ValueError(f"{claim_id} requires non-empty {field}")

        evidence = claim.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            raise ValueError(f"{claim_id} requires at least one evidence path")
        for evidence_path in evidence:
            if not isinstance(evidence_path, str) or not evidence_path:
                raise ValueError(f"{claim_id} has an invalid evidence path")
            if not (repo_root / evidence_path).exists():
                raise ValueError(f"{claim_id} evidence path does not exist: {evidence_path}")

    missing = REQUIRED_CLAIM_IDS - seen
    if missing:
        raise ValueError(f"claim ledger is missing required claims: {sorted(missing)}")

    claims_text = (repo_root / claims_doc).read_text(encoding="utf-8")
    for claim in claims:
        claim_id = claim["claim_id"]
        if claim_id not in claims_text:
            raise ValueError(f"{claims_doc} does not include {claim_id}")
        expected_status = f"**Status:** {claim['status']}"
        if expected_status not in claims_text:
            raise ValueError(f"{claims_doc} does not show {claim_id} as {claim['status']}")

    return {"claims": len(claims), **{f"claims_{k.lower()}": v for k, v in status_counts.items()}}


def validate_registry_claim_counts(repo_root: Path = Path(".")) -> dict[str, int]:
    repo_root = Path(repo_root)
    curated = _load_registry_rows(repo_root / "data/registries/curated_mechanism_labels.json")
    expansion = _load_registry_rows(repo_root / "data/registries/external_bronze_labels.json")
    combined = [*curated, *expansion]

    actual = {
        "current702_rows": len(curated),
        "current702_bronze": sum(row.get("tier") == "bronze" for row in curated),
        "current702_silver": sum(row.get("tier") == "silver" for row in curated),
        "current702_gold": sum(row.get("tier") == "gold" for row in curated),
        "current702_automation_curated": sum(
            row.get("review_status") == "automation_curated" for row in curated
        ),
        "current702_author_reviewed": sum(
            row.get("review_status") == "expert_reviewed" for row in curated
        ),
        "combined_rows": len(combined),
        "combined_positive_assignments": sum(
            row.get("label_type") == "seed_fingerprint" for row in combined
        ),
        "combined_oos_records": sum(row.get("label_type") == "out_of_scope" for row in combined),
    }
    expected = {
        "current702_rows": 702,
        "current702_bronze": 685,
        "current702_silver": 17,
        "current702_gold": 0,
        "current702_automation_curated": 683,
        "current702_author_reviewed": 19,
        "combined_rows": 10001,
        "combined_positive_assignments": 8305,
        "combined_oos_records": 1696,
    }
    if actual != expected:
        differences = {
            key: {"expected": expected[key], "actual": actual[key]}
            for key in expected
            if actual[key] != expected[key]
        }
        raise ValueError(f"canonical claim counts drifted: {differences}")
    return actual


def validate_evaluation_claim_counts(repo_root: Path = Path(".")) -> dict[str, int]:
    repo_root = Path(repo_root)
    chemistry = _read_json(repo_root / "artifacts/v3_mechanism_from_chemistry_gold702_eval.json")
    mcsa = _read_json(
        repo_root / "artifacts/v3_heldout_oneshot_eval_result_current702_20260628.json"
    )
    swissprot = _read_json(
        repo_root / "artifacts/v3_swissprot_pdbholo_gold_heldout_eval_result_current702_20260629.json"
    )
    option_b = _read_json(
        repo_root / "artifacts/v3_option_b_heldout_preregistration_current702_20260628.json"
    )
    observed = {
        "chemistry_coarse_correct": chemistry["headline"]["coarse_correct"],
        "chemistry_scored": chemistry["headline"]["coarse_scored"],
        "chemistry_exact_correct": chemistry["headline"]["correct"],
        "mcsa_inscope_recovered": int(mcsa["heldout_result"]["inscope_recovery"].split("/")[0]),
        "mcsa_inscope_total": int(mcsa["heldout_result"]["inscope_recovery"].split("/")[1]),
        "mcsa_oos_false_positives": int(
            mcsa["heldout_result"]["oos_false_positives"].split("/")[0]
        ),
        "mcsa_oos_total": int(mcsa["heldout_result"]["oos_false_positives"].split("/")[1]),
        "swissprot_inscope_recovered": swissprot["in_scope"]["recovered"],
        "swissprot_inscope_total": swissprot["in_scope"]["n"],
        "swissprot_metal_recovered": swissprot["in_scope_failure_decomposition"][
            "metal_dependent_hydrolase"
        ]["recovered"],
        "swissprot_metal_total": swissprot["in_scope_failure_decomposition"][
            "metal_dependent_hydrolase"
        ]["n"],
        "swissprot_oos_false_positives": swissprot["oos"]["false_positives"],
        "swissprot_oos_total": swissprot["oos"]["n"],
        "option_b_frozen_rows": option_b["frozen_heldout_set"]["counts"]["total"],
    }
    expected = {
        "chemistry_coarse_correct": 160,
        "chemistry_scored": 210,
        "chemistry_exact_correct": 65,
        "mcsa_inscope_recovered": 35,
        "mcsa_inscope_total": 47,
        "mcsa_oos_false_positives": 15,
        "mcsa_oos_total": 79,
        "swissprot_inscope_recovered": 45,
        "swissprot_inscope_total": 64,
        "swissprot_metal_recovered": 2,
        "swissprot_metal_total": 16,
        "swissprot_oos_false_positives": 2,
        "swissprot_oos_total": 72,
        "option_b_frozen_rows": 22,
    }
    if observed != expected:
        differences = {
            key: {"expected": expected[key], "actual": observed[key]}
            for key in expected
            if observed[key] != expected[key]
        }
        raise ValueError(f"canonical evaluation counts drifted: {differences}")
    return observed


def load_exposure_ledger(path: Path = DEFAULT_EXPOSURE_LEDGER) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number} is not valid JSON") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number} must be a JSON object")
            rows.append(row)
    return rows


def validate_exposure_events(
    events: Iterable[dict[str, Any]],
    *,
    repo_root: Path = Path("."),
) -> dict[str, int]:
    repo_root = Path(repo_root)
    state_by_surface: dict[str, str] = {}
    seen_ids: set[str] = set()
    last_effective_at: datetime | None = None
    event_count = 0

    for index, event in enumerate(events, start=1):
        event_count += 1
        event_id = event.get("event_id")
        expected_id = f"EXP-{index:04d}"
        if event_id != expected_id:
            raise ValueError(f"exposure event {index} must be {expected_id}, got {event_id!r}")
        if event_id in seen_ids:
            raise ValueError(f"duplicate exposure event_id: {event_id}")
        seen_ids.add(event_id)

        surface_id = event.get("surface_id")
        if not isinstance(surface_id, str) or not surface_id.strip():
            raise ValueError(f"{event_id} requires a surface_id")
        event_type = event.get("event_type")
        if event_type not in EXPOSURE_EVENT_TYPES:
            raise ValueError(f"{event_id} has invalid event_type: {event_type!r}")
        state_after = event.get("state_after")
        if state_after not in EXPOSURE_STATES:
            raise ValueError(f"{event_id} has invalid state_after: {state_after!r}")

        effective_at = _parse_timestamp(event.get("effective_at"), field="effective_at", event_id=event_id)
        _parse_timestamp(event.get("recorded_at"), field="recorded_at", event_id=event_id)
        if last_effective_at is not None and effective_at < last_effective_at:
            raise ValueError(f"{event_id} effective_at is earlier than the preceding event")
        last_effective_at = effective_at

        if not isinstance(event.get("historical_backfill"), bool):
            raise ValueError(f"{event_id} historical_backfill must be boolean")
        if not isinstance(event.get("scope"), str) or not event["scope"].strip():
            raise ValueError(f"{event_id} requires a non-empty scope")
        row_count = event.get("row_count")
        if not isinstance(row_count, int) or isinstance(row_count, bool) or row_count <= 0:
            raise ValueError(f"{event_id} row_count must be a positive integer")

        source_artifacts = event.get("source_artifacts")
        if not isinstance(source_artifacts, list) or not source_artifacts:
            raise ValueError(f"{event_id} requires source_artifacts")
        for source_path in source_artifacts:
            if not isinstance(source_path, str) or not (repo_root / source_path).exists():
                raise ValueError(f"{event_id} source artifact does not exist: {source_path!r}")

        previous_state = state_by_surface.get(surface_id)
        if previous_state == "exhausted" and state_after != "exhausted":
            raise ValueError(f"{event_id} attempts to reset exhausted surface {surface_id}")
        if previous_state == "exposed" and state_after == "frozen_unscored":
            raise ValueError(f"{event_id} attempts to make exposed surface {surface_id} fresh")
        if event_type == "freeze" and state_after != "frozen_unscored":
            raise ValueError(f"{event_id} freeze events must end frozen_unscored")
        if event_type == "score" and state_after == "frozen_unscored":
            raise ValueError(f"{event_id} score events cannot remain frozen_unscored")
        state_by_surface[surface_id] = state_after

    if not event_count:
        raise ValueError("exposure ledger must contain at least one event")
    return {
        "exposure_events": event_count,
        "exposure_surfaces": len(state_by_surface),
        "exhausted_surfaces": sum(state == "exhausted" for state in state_by_surface.values()),
        "frozen_unscored_surfaces": sum(
            state == "frozen_unscored" for state in state_by_surface.values()
        ),
    }


def validate_exposure_ledger(
    path: Path = DEFAULT_EXPOSURE_LEDGER,
    *,
    repo_root: Path = Path("."),
) -> dict[str, int]:
    repo_root = Path(repo_root)
    events = load_exposure_ledger(repo_root / path)
    return validate_exposure_events(events, repo_root=repo_root)


def append_exposure_event(
    event: dict[str, Any],
    path: Path = DEFAULT_EXPOSURE_LEDGER,
    *,
    repo_root: Path = Path("."),
) -> dict[str, Any]:
    """Append one event after validating the complete resulting ledger."""
    repo_root = Path(repo_root)
    full_path = repo_root / path
    existing = load_exposure_ledger(full_path)
    candidate = dict(event)
    candidate.setdefault("event_id", f"EXP-{len(existing) + 1:04d}")
    validate_exposure_events([*existing, candidate], repo_root=repo_root)
    with full_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(candidate, separators=(",", ":"), sort_keys=True) + "\n")
    return candidate


def validate_truth_documents(repo_root: Path = Path(".")) -> dict[str, int]:
    repo_root = Path(repo_root)
    required = [DEFAULT_CLAIMS_DOC, DEFAULT_ERRATA_DOC, DEFAULT_POLICY_DOC]
    for relative_path in required:
        if not (repo_root / relative_path).exists():
            raise ValueError(f"missing truth-governance document: {relative_path}")

    policy_text = (repo_root / DEFAULT_POLICY_DOC).read_text(encoding="utf-8")
    missing_terms = sorted(term for term in _REQUIRED_POLICY_TERMS if term not in policy_text)
    if missing_terms:
        raise ValueError(f"truth policy is missing required terms: {missing_terms}")

    errata_text = (repo_root / DEFAULT_ERRATA_DOC).read_text(encoding="utf-8")
    for erratum_id in ("ER-001", "ER-002", "ER-003", "ER-004", "ER-005", "ER-006"):
        if erratum_id not in errata_text:
            raise ValueError(f"{DEFAULT_ERRATA_DOC} is missing {erratum_id}")

    active_markers = {
        Path("README.md"): "Truth-governance gate",
        Path("docs/MAP.md"): "Truth reset that precedes further scaling",
        Path("docs/CURRENT_STATE.md"): "2026-07-13 truth reset",
        Path("docs/CURRENT_DECISIONS.md"): "2026-07-13: Truth reset",
    }
    for relative_path, marker in active_markers.items():
        text = (repo_root / relative_path).read_text(encoding="utf-8")
        if marker not in text:
            raise ValueError(f"{relative_path} is missing current truth marker: {marker}")

    freeze = validate_expansion_freeze(repo_root=repo_root)
    if freeze.get("claim_id") != "CE-012":
        raise ValueError(f"{DEFAULT_EXPANSION_FREEZE} must reference CE-012")

    return {
        "truth_documents": len(required) + len(active_markers),
        "expansion_freeze_active": int(freeze["frozen"]),
        "protected_registry_paths": len(freeze["protected_paths"]),
    }


def validate_truth_governance(repo_root: Path = Path(".")) -> dict[str, int]:
    repo_root = Path(repo_root)
    return {
        **validate_claim_ledger(repo_root=repo_root),
        **validate_registry_claim_counts(repo_root=repo_root),
        **validate_evaluation_claim_counts(repo_root=repo_root),
        **validate_exposure_ledger(repo_root=repo_root),
        **validate_truth_documents(repo_root=repo_root),
    }
