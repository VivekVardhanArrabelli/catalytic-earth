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
- Silently accept a mismatch. A declared publication, site or structure that the
  packaged record does not carry is recorded as a conflict, and a case the
  packaged records do not resolve is recorded as unresolved. Neither is dropped,
  and neither is upgraded to a match.
- Confuse membership with support. Identifiers the case carries are checked
  again against its individual relations, so a publication from one evidence
  relation and a site from another are reported as the conflict they are rather
  than as a confirmed pair.
- Flatten source roles. A functional-observation source and the primary citation
  of a deposited structure are different things; a citation in a role these
  records do not enumerate is kept as separately sourced external context rather
  than being called a contradiction or quietly swapped for one that matches.

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

from .external_sources import (
    ACTIONS,
    MATCH_STATUSES,
    ExternalSourceError,
    load_ledger,
    record_contribution,
)

__all__ = [
    "MATCH_STATUSES",
    "import_result",
    "registered_artifact",
    "resolve_case",
]

_MAX_ARTIFACT_BYTES = 64 * 1024 * 1024
_MAX_CONTEXT_ENTRIES = 40
_MAX_PREVIEW_BYTES = 256 * 1024


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
    # One bundle per packaged relation, so a declared publication, site and
    # structure can be checked against the same relation instead of against
    # three independent sets. A relation this case does not claim is kept and
    # marked rather than dropped: it is reference site context, not assayed
    # support, and the difference is what the relation check reads.
    relations = []
    for relation in view["relations"]:
        functional = relation.get("functional_evidence") or {}
        structures = (relation.get("protein_structure_context") or {}).get(
            "structures", []
        )
        relations.append(
            {
                "case_bound": case_ref in (functional.get("case_ids") or []),
                "publications": sorted(
                    {
                        evidence_id
                        for observation in functional.get("matched_observations") or []
                        for evidence_id in observation.get("evidence_ids", [])
                    }
                ),
                "relation_id": relation.get("relation_id"),
                "sites": [relation["site_id"]] if relation.get("site_id") else [],
                # Database accessions for the deposited structure, kept apart
                # from the functional-observation sources above.
                "structure_evidence_ids": sorted(
                    {
                        evidence_id
                        for structure in structures
                        for evidence_id in structure.get("evidence_ids", [])
                    }
                ),
                "structures": sorted(
                    {
                        structure["pdb_id"]
                        for structure in structures
                        if structure.get("pdb_id")
                    }
                ),
            }
        )
    return {
        "kind": "mechanism_evidence_case",
        "case_id": case_ref,
        "publications": publications,
        "question": (case.get("question") or {}).get("statement"),
        "relations": relations,
        "sites": sorted({site for entry in relations for site in entry["sites"]}),
        "structure_evidence_ids": sorted(
            {
                evidence_id
                for entry in relations
                for evidence_id in entry["structure_evidence_ids"]
            }
        ),
        "structures": sorted(
            {structure for entry in relations for structure in entry["structures"]}
        ),
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
    # The exact sources this comparison is built from: the providers its own
    # observations and parameters resolve through, plus the evidence pointers
    # the comparison itself declares. A text prefix of the study id would admit
    # every sibling study whose key starts the same way -- tk2024 and tktf for a
    # tk_2020 comparison -- so source identity is read, never inferred from a
    # shared enzyme family.
    sources = {
        provider["source"]
        for entry in observations
        for provider in (entry.get("provider"), entry.get("parameter_provider"))
        if isinstance(provider, dict) and provider.get("source")
    }
    sources.update(
        evidence["source"]
        for evidence in comparison.get("evidence") or []
        if isinstance(evidence, dict) and evidence.get("source")
    )
    # The retained primary files this study binds, by their own hashes.
    publications = sorted(
        {
            witness["source_url"]
            for witness in projection.get("source_witnesses", [])
            if witness.get("source_url")
            and any(
                binding.get("source") in sources
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
        # A comparison is its own relation: these constructs and these exact
        # sources belong together, and nothing else in the projection does.
        "relations": [
            {
                "case_bound": True,
                "publications": publications,
                "relation_id": case_ref,
                "sites": constructs,
                "structure_evidence_ids": [],
                "structures": [],
            }
        ],
        "sites": constructs,
        "sources": sorted(sources),
        "structure_evidence_ids": [],
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
        "relations": [],
        "resolved": False,
        "sites": [],
        "structure_evidence_ids": [],
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


def registered_artifact(
    sha256: str, path: Path | str | None = None
) -> dict[str, Any]:
    """Read back one saved output the ledger already registered.

    The digest is the identity and the only key. A digest the ledger does not
    carry is refused, so this reads no path a caller supplies and exposes no
    file the repository did not record. The file is hashed again on the way out:
    one that changed after it was recorded is reported as changed rather than
    served under a record it no longer matches, and one that is gone is reported
    as gone rather than reconstructed.

    Text is returned as text for the interface to escape and display. Anything
    that is not valid UTF-8 text is described and not returned as content, so
    no imported markup is ever handed back to a page to render.
    """
    digest = sha256.strip().lower() if isinstance(sha256, str) else ""
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise ExternalSourceError("a sha256 digest is required")

    recorded_in: list[str] = []
    reference: dict[str, Any] | None = None
    for record in load_ledger(path).get("contributions", []):
        for entry in (record.get("result") or {}).get("artifacts", []):
            if entry.get("sha256") == digest:
                recorded_in.append(record["contribution_id"])
                reference = reference or entry
    if reference is None:
        raise ExternalSourceError(f"no saved artifact is registered under {digest}")

    described = {
        "bytes": reference["bytes"],
        "media_type": reference["media_type"],
        "name": reference["name"],
        "recorded_in": sorted(set(recorded_in)),
        "sha256": digest,
    }
    saved = Path(reference["path"])
    if not saved.is_file():
        return dict(
            described,
            available=False,
            reason=(
                "the recorded file is no longer at the path it was imported "
                "from; its hash and size remain on the record"
            ),
        )
    raw = saved.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        return dict(
            described,
            available=False,
            reason=(
                "the file at the recorded path no longer matches the digest that "
                "was imported, so it is not served as that result"
            ),
        )
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        return dict(
            described,
            available=True,
            is_text=False,
            reason="not UTF-8 text; download it to open in its own application",
        )
    if "\x00" in decoded:
        return dict(
            described,
            available=True,
            is_text=False,
            reason="contains NUL bytes; download it to open in its own application",
        )
    return dict(
        described,
        available=True,
        is_text=True,
        text=decoded[:_MAX_PREVIEW_BYTES],
        truncated=len(decoded) > _MAX_PREVIEW_BYTES,
    )


def _check(
    declared: str | None,
    available: list[str],
    label: str,
    *,
    absent_status: str = "conflict",
    absent_reason: str | None = None,
) -> dict[str, Any]:
    """Compare one declared identifier with what the packaged record carries.

    This is membership and nothing more: the declared identifier is either one
    the case carries or it is not. ``absent_status`` exists because absence
    means different things in different roles -- a structure the enumerated set
    contradicts is not the same as a citation the record never enumerates.
    """
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
        "reason": absent_reason or (
            f"the packaged record does not carry this {label}; it carries "
            + ", ".join(available[:6])
        ),
        "status": absent_status,
    }


def _publication_check(
    record: dict[str, Any], publication: str | None, structure_id: str | None
) -> dict[str, Any]:
    """Check a declared publication in the role the packaged record keeps it in.

    A case's publications are the sources of its functional observations. The
    primary citation of a deposited structure is a different role, and these
    records do not enumerate it: every structure evidence id they carry is a
    database accession. So a publication the case does not carry is a
    contradiction of the functional sources only when the result is not scoped
    to a structure the case really carries. Where it is, the record has nothing
    of that role to contradict, and the declared citation is kept as separately
    sourced external context instead.

    It is still not a match, and the declared value is never replaced by a
    carried one to obtain one.
    """
    available = record.get("publications", [])
    structural_citations = [
        evidence_id
        for evidence_id in record.get("structure_evidence_ids", [])
        if evidence_id.startswith("paper:")
    ]
    if publication and publication in structural_citations:
        return {
            "declared": publication,
            "label": "publication",
            "reason": (
                "carried as a primary citation of a deposited structure, not as "
                "a functional-observation source"
            ),
            "status": "confirmed",
        }
    if (
        publication
        and available
        and publication not in available
        and not structural_citations
        and structure_id
        and structure_id in record.get("structures", [])
    ):
        return _check(
            publication,
            available,
            "publication",
            absent_status="external_context",
            absent_reason=(
                f"this result is scoped to structure {structure_id}, which the "
                "packaged record carries; the record's publications are its "
                "functional-observation sources and it enumerates no primary "
                "citation for its deposited structures, so this citation is kept "
                "as separately sourced external context and is neither confirmed "
                "nor contradicted here"
            ),
        )
    return _check(publication, available, "publication")


def _relation_check(
    record: dict[str, Any],
    declared: dict[str, str | None],
    statuses: dict[str, str],
) -> dict[str, Any]:
    """Check that the carried identifiers belong to one supported relation.

    Membership alone says only that the case mentions an identifier somewhere.
    This asks the narrower question an association actually needs: does one
    packaged relation carry all of them together? A publication drawn from one
    evidence relation and a site drawn from another are both present in the
    case and still do not support each other.
    """
    fields = {"publication": "publications", "site": "sites", "structure": "structures"}
    carried = {
        label: value
        for label, value in declared.items()
        if value and statuses.get(label) == "confirmed"
    }
    summary = ", ".join(f"{label} {value}" for label, value in sorted(carried.items()))
    if len(carried) < 2:
        return {
            "declared": summary or None,
            "label": "relation",
            "reason": (
                "at least two identifiers the packaged record carries are needed "
                "before they can be placed in one relation"
            ),
            "status": "unresolved",
        }
    # A publication may be carried by a relation in either role it has: as a
    # functional-observation source, or as a citation of the structure that
    # relation deposits. Both are that relation carrying it.
    def carries(entry: dict[str, Any], label: str, value: str) -> bool:
        if label == "publication":
            return value in entry["publications"] or (
                value in entry["structure_evidence_ids"]
            )
        return value in entry[fields[label]]

    supporting = [
        entry["relation_id"]
        for entry in record.get("relations", [])
        if all(carries(entry, label, value) for label, value in carried.items())
    ]
    if supporting:
        return {
            "declared": summary,
            "label": "relation",
            "reason": "carried together by " + ", ".join(supporting[:4]),
            "status": "confirmed",
        }
    return {
        "declared": summary,
        "label": "relation",
        "reason": (
            "the packaged record carries each of these, but no single relation "
            "carries them together; they are drawn from different evidence "
            "relations and this result is not evidence that they belong to one"
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
    structure_id: str | None = None,
    context: dict[str, str] | None = None,
    note: str | None = None,
    path: Path | str | None = None,
) -> dict[str, Any]:
    """Record one saved external output against the case it answers.

    ``artifacts`` are paths to the files the tool actually produced. ``context``
    holds the scientific values the output reported, kept as the tool stated
    them; they are recorded as external context and never merged into the
    packaged record. They are also never compared with anything: an identifier
    is checked only when it is declared as ``publication``, ``site_id`` or
    ``structure_id``, because hashing an artifact does not establish that a
    context string was read out of it.
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
        _publication_check(record, publication, structure_id),
        _check(site_id, record.get("sites", []), "site"),
    ]
    if structure_id:
        checks.append(_check(structure_id, record.get("structures", []), "structure"))
    checks.append(
        _relation_check(
            record,
            {"publication": publication, "site": site_id, "structure": structure_id},
            {entry["label"]: entry["status"] for entry in checks},
        )
    )

    # A relation that could not be evaluated is not a verdict either way, so it
    # does not lower the status; every check that was actually made does. A
    # conflict outranks a gap, a gap outranks unverified external context, and
    # only checks that all confirmed leave a confirmation standing.
    weighed = [
        entry["status"]
        for entry in checks
        if not (entry["label"] == "relation" and entry["status"] == "unresolved")
    ]
    if not record["resolved"]:
        match_status = "unresolved"
    elif "conflict" in weighed:
        match_status = "conflict"
    elif "unresolved" in weighed:
        match_status = "unresolved"
    elif "external_context" in weighed:
        match_status = "external_context"
    else:
        match_status = "confirmed"

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
        "declared_structure": structure_id,
        "packaged_publications": record.get("publications", []),
        "packaged_question": record.get("question"),
        "packaged_relations": [
            {
                "case_bound": entry["case_bound"],
                "publications": entry["publications"],
                "relation_id": entry["relation_id"],
                "sites": entry["sites"],
                "structures": entry["structures"],
            }
            for entry in record.get("relations", [])
        ],
        "packaged_sites": record.get("sites", []),
        "packaged_structure_evidence_ids": record.get("structure_evidence_ids", []),
        "packaged_structures": record.get("structures", []),
    }
    result["semantics"] = {
        "checked": (
            "Each declared identifier is checked for membership in the packaged "
            "case, and the ones the case carries are then checked for membership "
            "in one shared relation. That is the whole of what a confirmation "
            "means here: declared identifiers found in the case and carried "
            "together by it. It is not a reading of the output's scientific "
            "content, and it does not authenticate the tool that produced it."
        ),
        "context": (
            "Context fields are recorded as the caller supplied them. They are "
            "not extracted from the artifact and take no part in any check; "
            "declare a publication, site or structure to have one compared."
        ),
        "external_context": (
            "An identifier in a role the packaged record does not enumerate is "
            "kept as separately sourced external context: not confirmed, and not "
            "contradicted either."
        ),
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
    parser.add_argument("--structure", default=None, dest="structure_id",
                        help="PDB id the result is scoped to, checked against the case")
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
            structure_id=args.structure_id,
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
