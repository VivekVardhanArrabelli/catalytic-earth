"""Return path for results produced by an external research suite.

The contribution ledger records that an external tool was asked to do
something. This module completes the other half: it takes the output that tool
actually saved, ties it to the exact case, publication, protein site and
operation it was asked about, and records it beside the packaged evidence.

What it will not do:

- Invent an output. Every artifact must be a file that exists; it is hashed and
  measured, and a missing file refuses the import.
- Merge external context into the protected atlas records. Results live in the
  ledger, are read back from there, and never rewrite packaged data.
- Silently accept a mismatch. A declared publication or site that the packaged
  record does not carry is recorded as a conflict, and a case the packaged
  records do not resolve is recorded as unresolved. Neither is dropped, and
  neither is upgraded to a match.

The association is validated against whichever packaged query owns the case, so
the same path serves different record families without an enzyme-specific
branch: a mechanism-evidence case and a perturbation comparison are resolved by
the same call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from pathlib import Path
from typing import Any

from .external_sources import ACTIONS, ExternalSourceError, record_contribution

__all__ = [
    "MATCH_STATUSES",
    "import_result",
    "resolve_case",
]

#: How a declared association compares with the packaged record.
MATCH_STATUSES = ("confirmed", "conflict", "unresolved")

_MAX_ARTIFACT_BYTES = 64 * 1024 * 1024
_MAX_CONTEXT_ENTRIES = 40


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    return Path.cwd()


def _mechanism_case(case_ref: str) -> dict[str, Any] | None:
    """Resolve a mechanism-evidence case and report what it actually carries."""
    from .adapter import evidence_view

    view = evidence_view()
    case = next(
        (entry for entry in view["cases"] if entry.get("case_id") == case_ref), None
    )
    if case is None:
        return None
    publications = sorted(
        {
            evidence_id
            for observation in view["observations"]
            if observation.get("case_id") == case_ref
            for evidence_id in observation.get("evidence_ids", [])
        }
    )
    sites = sorted(
        {
            relation["site_id"]
            for relation in view["relations"]
            if relation.get("site_id")
        }
    )
    structures = sorted(
        {
            structure["pdb_id"]
            for relation in view["relations"]
            for structure in (relation.get("protein_structure_context") or {}).get(
                "structures", []
            )
            if structure.get("pdb_id")
        }
    )
    return {
        "kind": "mechanism_evidence_case",
        "case_id": case_ref,
        "publications": publications,
        "question": (case.get("question") or {}).get("statement"),
        "sites": sites,
        "structures": structures,
    }


def _perturbation_comparison(case_ref: str) -> dict[str, Any] | None:
    """Resolve a perturbation comparison and report what it actually carries."""
    try:
        from ..atlas_perturbations import project
    except ImportError:  # pragma: no cover - the consumer is packaged
        return None

    projection = project(_repo_root())
    comparison = next(
        (
            entry
            for entry in projection.get("comparisons", [])
            if entry.get("id") == case_ref
        ),
        None,
    )
    if comparison is None:
        return None

    observation_ids = set(comparison.get("roles", {}).values()) | set(
        comparison.get("context_observations", []) or []
    )
    observations = [
        entry
        for entry in projection.get("observations", [])
        if entry.get("id") in observation_ids
    ]
    constructs = sorted(
        {entry["construct_id"] for entry in observations if entry.get("construct_id")}
    )
    # The retained primary files this study binds, by their own hashes.
    publications = sorted(
        {
            witness["source_url"]
            for witness in projection.get("source_witnesses", [])
            if witness.get("source_url")
            and any(
                binding.get("source", "").startswith(
                    str(comparison.get("study_id", "")).split("_")[0]
                )
                for binding in witness.get("source_bindings", [])
            )
        }
    )
    return {
        "kind": "perturbation_comparison",
        "case_id": case_ref,
        "constructs": constructs,
        "operation": comparison.get("operation"),
        "publications": publications,
        "question": comparison.get("scope"),
        "sites": constructs,
        "structures": [],
        "study_id": comparison.get("study_id"),
    }


def resolve_case(case_ref: str) -> dict[str, Any]:
    """Find the packaged record a declared case refers to.

    Both packaged families are tried in turn. An unresolved case is reported as
    unresolved rather than assumed, so a result can still be recorded without
    being credited with an association it does not have.
    """
    if not isinstance(case_ref, str) or not case_ref.strip():
        raise ExternalSourceError("case_ref is required")
    reference = case_ref.strip()
    for resolver in (_mechanism_case, _perturbation_comparison):
        try:
            found = resolver(reference)
        except Exception as exc:  # a resolver failure is reported, not hidden
            raise ExternalSourceError(
                f"could not resolve {reference!r}: {exc}"
            ) from exc
        if found:
            return dict(found, resolved=True)
    return {
        "case_id": reference,
        "kind": None,
        "publications": [],
        "resolved": False,
        "sites": [],
        "structures": [],
    }


def _artifact_reference(path: Path) -> dict[str, Any]:
    """Describe one saved output file by what is actually on disk."""
    if not path.is_file():
        raise ExternalSourceError(f"artifact {path} does not exist")
    size = path.stat().st_size
    if size == 0:
        raise ExternalSourceError(f"artifact {path} is empty")
    if size > _MAX_ARTIFACT_BYTES:
        raise ExternalSourceError(f"artifact {path} exceeds {_MAX_ARTIFACT_BYTES} bytes")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    media_type, _ = mimetypes.guess_type(path.name)
    return {
        "bytes": size,
        "media_type": media_type or "application/octet-stream",
        "name": path.name,
        "path": str(path),
        "sha256": digest.hexdigest(),
    }


def _check(declared: str | None, available: list[str], label: str) -> dict[str, Any]:
    """Compare one declared identifier with what the packaged record carries."""
    if not declared:
        return {"declared": None, "label": label, "status": "unresolved",
                "reason": f"no {label} was declared for this result"}
    if not available:
        return {"declared": declared, "label": label, "status": "unresolved",
                "reason": f"the packaged record carries no {label} to compare against"}
    if declared in available:
        return {"declared": declared, "label": label, "status": "confirmed",
                "reason": None}
    return {
        "declared": declared,
        "label": label,
        "reason": (
            f"the packaged record does not carry this {label}; it carries "
            + ", ".join(available[:6])
        ),
        "status": "conflict",
    }


def import_result(
    *,
    provider_suite: str,
    provider_tool: str,
    action: str,
    query: str,
    case_ref: str,
    artifacts: list[str | Path],
    publication: str | None = None,
    site_id: str | None = None,
    context: dict[str, str] | None = None,
    note: str | None = None,
    path: Path | str | None = None,
) -> dict[str, Any]:
    """Record one saved external output against the case it answers.

    ``artifacts`` are paths to the files the tool actually produced. ``context``
    holds the scientific values the output reported, kept as the tool stated
    them; they are recorded as external context and never merged into the
    packaged record.
    """
    if action not in ACTIONS:
        raise ExternalSourceError(f"action must be one of {ACTIONS}, got {action!r}")
    if not artifacts:
        raise ExternalSourceError(
            "at least one saved artifact is required; a result with no output "
            "is a request, not a result"
        )

    references = [_artifact_reference(Path(entry)) for entry in artifacts]

    fields = dict(context or {})
    if len(fields) > _MAX_CONTEXT_ENTRIES:
        raise ExternalSourceError(f"at most {_MAX_CONTEXT_ENTRIES} context entries")
    for key, value in fields.items():
        if not isinstance(key, str) or not key.strip():
            raise ExternalSourceError("every context key must be a non-empty string")
        if not isinstance(value, str) or not value.strip():
            raise ExternalSourceError(f"context value for {key!r} must be a non-empty string")

    record = resolve_case(case_ref)
    checks = [
        _check(publication, record.get("publications", []), "publication"),
        _check(site_id, record.get("sites", []), "site"),
    ]
    statuses = {entry["status"] for entry in checks}
    if not record["resolved"]:
        match_status = "unresolved"
    elif "conflict" in statuses:
        match_status = "conflict"
    elif statuses == {"confirmed"}:
        match_status = "confirmed"
    else:
        match_status = "unresolved"

    result = {
        "artifacts": references,
        "association": {},
        "context": fields,
        "match_status": match_status,
    }
    result["association"] = {
        "case_ref": case_ref,
        "case_kind": record.get("kind"),
        "case_resolved": record["resolved"],
        "checks": checks,
        "declared_publication": publication,
        "declared_site": site_id,
        "packaged_publications": record.get("publications", []),
        "packaged_question": record.get("question"),
        "packaged_sites": record.get("sites", []),
        "packaged_structures": record.get("structures", []),
    }
    result["semantics"] = {
        "conflicts": (
            "A declared identifier the packaged record does not carry is kept as "
            "a conflict. It is never dropped and never counted as a match."
        ),
        "separation": (
            "This is external context recorded beside the packaged evidence. It "
            "does not change, override or extend any packaged record."
        ),
        "unresolved": (
            "An unresolved case or an undeclared identifier stays unresolved. "
            "The result is still recorded, without the association it lacks."
        ),
    }

    return record_contribution(
        provider_suite=provider_suite,
        provider_tool=provider_tool,
        action=action,
        query=query,
        retrieved=[entry["sha256"] for entry in references],
        subject=site_id or case_ref,
        note=note,
        path=path,
        result=result,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m catalytic_earth.workbench.external_results",
        description=(
            "Record a saved external tool output against the case it answers. "
            "Run this only for output a real call actually produced."
        ),
    )
    parser.add_argument("--provider-suite", required=True)
    parser.add_argument("--provider-tool", required=True)
    parser.add_argument("--action", required=True, choices=ACTIONS)
    parser.add_argument("--query", required=True, help="the exact query sent")
    parser.add_argument("--case", required=True, dest="case_ref",
                        help="exact case or comparison id the result answers")
    parser.add_argument("--artifact", action="append", default=[], required=True,
                        help="path to a file the tool saved; repeatable")
    parser.add_argument("--publication", default=None)
    parser.add_argument("--site", default=None, dest="site_id")
    parser.add_argument("--context", action="append", default=[], metavar="KEY=VALUE",
                        help="a scientific value the output reported; repeatable")
    parser.add_argument("--note", default=None)
    parser.add_argument("--ledger", type=Path, default=None)
    parser.add_argument("--resolve-only", action="store_true",
                        help="report what the case resolves to and exit; writes nothing")
    args = parser.parse_args(argv)

    try:
        if args.resolve_only:
            print(json.dumps(resolve_case(args.case_ref), indent=2, sort_keys=True))
            return 0
        context: dict[str, str] = {}
        for pair in args.context:
            if "=" not in pair:
                parser.error(f"--context expects KEY=VALUE, got {pair!r}")
            key, value = pair.split("=", 1)
            context[key.strip()] = value.strip()
        record = import_result(
            provider_suite=args.provider_suite,
            provider_tool=args.provider_tool,
            action=args.action,
            query=args.query,
            case_ref=args.case_ref,
            artifacts=args.artifact,
            publication=args.publication,
            site_id=args.site_id,
            context=context,
            note=args.note,
            path=args.ledger,
        )
    except ExternalSourceError as exc:
        parser.error(str(exc))
        return 2
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
