"""Small, wheel-installed, deterministic Catalytic Earth core command."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from importlib.resources import files
from pathlib import Path
from typing import Any, Sequence

from .atlas10_kernel import build_atlas10_runtime_result
from .atlas_kernel import build_atlas3_runtime_result, canonical_sha256
from .schema import MechanismRecord, SCHEMA_VERSION


GOLDEN_INPUT = "release_data/golden_input_v1.json"
GOLDEN_EXPECTED = "release_data/golden_expected_v1.json"
ATLAS3_KERNEL = "atlas_data/atlas3_kernel.json"
ATLAS3_QUERY = "atlas_data/case_truth_summary.sql"
ATLAS3_EXPECTED = "atlas_data/case_truth_summary_expected.json"
ATLAS10_KERNEL = "atlas_data/atlas10_kernel.json"
ATLAS10_CONVERGENT_QUERY = "atlas_data/atlas10_convergent_strategy.sql"
ATLAS10_DIVERGENT_QUERY = "atlas_data/atlas10_shared_fold_divergent_chemistry.sql"
ATLAS10_EXPECTED = "atlas_data/atlas10_runtime_expected.json"


def _resource_bytes(relative_path: str) -> bytes:
    return files("catalytic_earth").joinpath(relative_path).read_bytes()


def _canonical_sha(value: Any) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def verified_structural_context() -> dict[str, Any]:
    """Load the reviewed coordinate projection, without raw mmCIF or a network."""
    prefix = "structural_context_data/"
    expected = json.loads(_resource_bytes(prefix + "expected.json"))
    if expected.get("schema_version") != "catalytic-earth.atlas-structural-context-package.v1":
        raise ValueError("unsupported structural-context package")
    assets = {}
    for name, digest in expected["files"].items():
        if Path(name).name != name or "\\" in name:
            raise ValueError("unsafe structural-context asset name")
        raw = _resource_bytes(prefix + name)
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError("structural-context asset differs from expected hash")
        assets[name] = raw
    spec = json.loads(assets["spec.json"])
    review = json.loads(assets["review.json"])
    for name in ("spec.json", "bundle.json"):
        if review.get(name.replace(".json", "_sha256")) != hashlib.sha256(assets[name]).hexdigest():
            raise ValueError("structural-context source review is stale")
    if spec["atlas10_binding"]["sha256"] != hashlib.sha256(_resource_bytes(ATLAS10_KERNEL)).hexdigest():
        raise ValueError("structural-context Atlas-10 binding differs")
    return json.loads(assets["bundle.json"])


def verified_transformations(mcsa_id: str = "M0187") -> dict[str, Any]:
    from .atlas_transformation_query import TRANSFORMATION_SETS, normalize_mcsa_id
    from .atlas_transformations import validate_transformations

    key = normalize_mcsa_id(mcsa_id)
    if key not in TRANSFORMATION_SETS:
        raise ValueError("unknown transformation set")
    prefix = "transformation_data/" + TRANSFORMATION_SETS[key]["package_prefix"]
    expected = json.loads(_resource_bytes(prefix + "expected.json"))
    if expected.get("schema_version") != "catalytic-earth.transformation-package.v1":
        raise ValueError("unsupported transformation package")
    raw = _resource_bytes(prefix + "transformations.json")
    attribution = _resource_bytes(prefix + "attribution.md")
    if hashlib.sha256(raw).hexdigest() != expected["transformations_sha256"]:
        raise ValueError("transformation package differs from its expected hash")
    if hashlib.sha256(attribution).hexdigest() != expected["attribution_sha256"]:
        raise ValueError("transformation attribution differs from its expected hash")
    value = json.loads(raw)
    validate_transformations(value, atlas10_bundle=json.loads(_resource_bytes(ATLAS10_KERNEL)))
    if any(row["record_binding"]["mcsa_id"] != key for row in value["transformations"]):
        raise ValueError("packaged transformation set belongs to another source record")
    return value


def verified_mechanism_evidence() -> dict[str, Any]:
    """Load the reviewed case and verify its packaged factual source projections."""
    prefix = "mechanism_evidence_data/"
    expected = json.loads(_resource_bytes(prefix + "expected.json"))
    if expected.get("schema_version") != "catalytic-earth.mechanism-evidence-package.v1":
        raise ValueError("unsupported mechanism evidence package")
    for name, digest in expected["files"].items():
        if Path(name).name != name or "\\" in name:
            raise ValueError("mechanism evidence package filenames must be local")
        if hashlib.sha256(_resource_bytes(prefix + name)).hexdigest() != digest:
            raise ValueError(f"mechanism evidence package differs from its expected hash: {name}")
    if not {"evidence.json", "attribution.md"} <= expected["files"].keys():
        raise ValueError("mechanism evidence package is incomplete")
    value = json.loads(_resource_bytes(prefix + "evidence.json"))
    for binding in value["source_bindings"]:
        name = binding["path"].rsplit("/", 1)[-1]
        if expected["files"].get(name) != binding["sha256"]:
            raise ValueError("mechanism evidence source binding differs from its packaged projection")
    return value


def verified_panel_comparisons() -> dict[str, Any]:
    from .atlas_partial_panels import validate_panel_comparisons

    prefix = "panel_comparison_data/"
    expected = json.loads(_resource_bytes(prefix + "expected.json"))
    if expected.get("schema_version") != "catalytic-earth.partial-panel-package.v1":
        raise ValueError("unsupported partial-panel package")
    raw = _resource_bytes(prefix + "comparisons.json")
    attribution = _resource_bytes(prefix + "attribution.md")
    if hashlib.sha256(raw).hexdigest() != expected["comparisons_sha256"]:
        raise ValueError("partial-panel package differs from its expected hash")
    if hashlib.sha256(attribution).hexdigest() != expected["attribution_sha256"]:
        raise ValueError("partial-panel attribution differs from its expected hash")
    value = json.loads(raw)
    validate_panel_comparisons(value, atlas10_bundle=json.loads(_resource_bytes(ATLAS10_KERNEL)))
    return value


def verified_candidate_events() -> dict[str, Any]:
    """Load the separate unreviewed event catalog with its content bindings."""
    from .atlas_candidate_events import validate_candidate_event_catalog

    prefix = "candidate_event_data/"
    expected = json.loads(_resource_bytes(prefix + "expected.json"))
    if expected.get("schema_version") != "catalytic-earth.candidate-event-package.v1":
        raise ValueError("unsupported candidate event package")
    raw = _resource_bytes(prefix + "catalog.json")
    attribution = _resource_bytes(prefix + "attribution.md")
    if hashlib.sha256(raw).hexdigest() != expected.get("catalog_sha256"):
        raise ValueError("candidate event catalog differs from its expected hash")
    if hashlib.sha256(attribution).hexdigest() != expected.get("attribution_sha256"):
        raise ValueError("candidate event attribution differs from its expected hash")
    value = json.loads(raw)
    validate_candidate_event_catalog(value)
    return value


def build_golden_result() -> dict[str, Any]:
    raw = _resource_bytes(GOLDEN_INPUT)
    payload = json.loads(raw)
    if payload.get("schema_version") != "catalytic-earth.golden-input.v1":
        raise ValueError("unsupported golden input schema")
    records = [MechanismRecord.from_dict(row) for row in payload.get("records", [])]
    if not records or not all(record.fixture_only for record in records):
        raise ValueError("golden input must contain fixture-only records")
    record_ids = [record.record_id for record in records]
    if len(record_ids) != len(set(record_ids)):
        raise ValueError("golden input record IDs must be unique")
    result = {
        "schema_version": "catalytic-earth.golden-result.v1",
        "mechanism_record_schema": SCHEMA_VERSION,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "record_count": len(records),
        "record_ids": sorted(record_ids),
        "object_type_counts": dict(sorted(Counter(r.object_type for r in records).items())),
        "evidence_tier_counts": dict(
            sorted(Counter(str(r.evidence_tier) for r in records).items())
        ),
        "negative_observation_count": sum(
            r.object_type == "experimental_observation" and r.outcome == "negative"
            for r in records
        ),
        "fixture_only": True,
        "seed": 0,
        "network_used": False,
        "external_binary_used": False,
        "accelerator_used": False,
    }
    return result


def verified_golden_result() -> dict[str, Any]:
    result = build_golden_result()
    expected = json.loads(_resource_bytes(GOLDEN_EXPECTED))
    digest = _canonical_sha(result)
    expected_digest = expected.get("result_sha256")
    if digest != expected_digest:
        raise ValueError(
            f"golden result hash mismatch: expected {expected_digest}, computed {digest}"
        )
    return {
        **result,
        "result_sha256": digest,
        "matches_expected": True,
        "what_it_claims": expected["what_it_claims"],
        "what_it_does_not_claim": expected["what_it_does_not_claim"],
    }


def verified_atlas3_result() -> dict[str, Any]:
    """Reproduce the first biological kernel and its local truth-boundary query."""
    kernel = json.loads(_resource_bytes(ATLAS3_KERNEL))
    query_sql = _resource_bytes(ATLAS3_QUERY).decode("utf-8")
    expected = json.loads(_resource_bytes(ATLAS3_EXPECTED))
    result = build_atlas3_runtime_result(kernel, query_sql)
    digest = canonical_sha256(result)
    checks = {
        "kernel_sha256": result["kernel_sha256"],
        "query_sha256": result["query_sha256"],
        "runtime_result_sha256": digest,
        "query_rows": result["query_rows"],
    }
    if any(expected.get(field) != value for field, value in checks.items()):
        raise ValueError("Atlas-3 kernel/query result differs from the packaged expectation")
    return {
        **result,
        "runtime_result_sha256": digest,
        "matches_expected": True,
        "what_it_claims": expected["what_it_claims"],
        "what_it_does_not_claim": expected["what_it_does_not_claim"],
    }


def verified_atlas10_result() -> dict[str, Any]:
    """Reproduce the immutable Atlas-3 plus seven-case Atlas-10 query surface."""
    inherited_kernel = json.loads(_resource_bytes(ATLAS3_KERNEL))
    kernel = json.loads(_resource_bytes(ATLAS10_KERNEL))
    queries = {
        "atlas10.query.convergent-strategy": _resource_bytes(
            ATLAS10_CONVERGENT_QUERY
        ).decode("utf-8"),
        "atlas10.query.shared-fold-divergent-chemistry": _resource_bytes(
            ATLAS10_DIVERGENT_QUERY
        ).decode("utf-8"),
    }
    expected = json.loads(_resource_bytes(ATLAS10_EXPECTED))
    result = build_atlas10_runtime_result(kernel, inherited_kernel, queries)
    digest = canonical_sha256(result)
    checks = {
        "kernel_sha256": result["kernel_sha256"],
        "inherited_kernel_sha256": result["inherited_kernel_sha256"],
        "query_sha256": result["query_sha256"],
        "runtime_result_sha256": digest,
        "relationship_query_results": result["relationship_query_results"],
    }
    if any(expected.get(field) != value for field, value in checks.items()):
        raise ValueError("Atlas-10 kernel/query result differs from the packaged expectation")
    return {
        **result,
        "runtime_result_sha256": digest,
        "matches_expected": True,
    }


def verified_source_drafts(batch_name: str = "default") -> dict[str, Any]:
    """Read the reviewed source projections without requiring a checkout or network."""
    from .atlas_drafts import validate_source_drafts
    from .atlas_draft_batch import DEFAULT_BATCH, resolve_batch

    batch = resolve_batch(batch_name)
    stem = "source_drafts" if batch == DEFAULT_BATCH else batch.batch_id.replace("-", "_")
    raw = _resource_bytes(f"draft_data/{stem}.json")
    expected = json.loads(_resource_bytes(f"draft_data/{stem}_expected.json"))
    attribution = _resource_bytes(f"draft_data/{stem}_attribution.md")
    if expected.get("schema_version") != "catalytic-earth.source-drafts-package.v1":
        raise ValueError("unsupported source draft package")
    if hashlib.sha256(raw).hexdigest() != expected.get("bundle_sha256"):
        raise ValueError("source draft package differs from its expected hash")
    if hashlib.sha256(attribution).hexdigest() != expected.get("attribution_sha256"):
        raise ValueError("source draft attribution differs from its expected hash")
    bundle = json.loads(raw)
    validate_source_drafts(bundle)
    return bundle


def _chebi_argument(value: str) -> str:
    from .atlas_draft_index import normalize_chebi_id

    try:
        return normalize_chebi_id(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def _pattern_atom_argument(value: str) -> tuple[str, str]:
    if value.count(":") != 1:
        raise argparse.ArgumentTypeError("expected ELEMENT:VARIABLE, such as C:x")
    element, variable = value.split(":")
    if not element or not variable:
        raise argparse.ArgumentTypeError("expected ELEMENT:VARIABLE, such as C:x")
    return element, variable


def _mechanism_component_argument(value: str) -> str:
    from .atlas_draft_index import normalize_mechanism_component

    try:
        return normalize_mechanism_component(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def _step_cofactor_argument(value: str) -> str:
    from .atlas_step_evidence import normalize_step_filters

    try:
        return normalize_step_filters(cofactors=[value])["cofactors"][0]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def _observed_component_argument(value: str) -> str:
    from .atlas_draft_query import normalize_observed_state_filters

    try:
        return normalize_observed_state_filters(observed_components=[value])["observed_components"][0]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def verified_primary_evidence(
    batch_name: str = "default", *, bundle: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load optional reviewed annotations separately from immutable source records."""
    from .atlas_draft_batch import DEFAULT_BATCH, resolve_batch
    from .atlas_primary_evidence import validate_primary_evidence

    batch = resolve_batch(batch_name)
    stem = "source_drafts" if batch == DEFAULT_BATCH else batch.batch_id.replace("-", "_")
    expected = json.loads(_resource_bytes(f"draft_data/{stem}_expected.json"))
    if expected.get("schema_version") != "catalytic-earth.source-drafts-package.v1":
        raise ValueError("unsupported source draft package")
    if "primary_evidence_sha256" not in expected:
        return None
    raw = _resource_bytes(f"draft_data/{stem}_primary_evidence.json")
    if hashlib.sha256(raw).hexdigest() != expected["primary_evidence_sha256"]:
        raise ValueError("primary evidence package differs from its expected hash")
    primary = json.loads(raw)
    validate_primary_evidence(
        primary, bundle=verified_source_drafts(batch_name) if bundle is None else bundle,
    )
    return primary


def verified_reaction_correspondence(
    batch_name: str = "default", *, bundle: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load curated net-reaction correspondence separately from source chemistry."""
    from .atlas_draft_batch import DEFAULT_BATCH, resolve_batch
    from .atlas_reaction_correspondence import validate_reaction_correspondence

    batch = resolve_batch(batch_name)
    stem = "source_drafts" if batch == DEFAULT_BATCH else batch.batch_id.replace("-", "_")
    expected = json.loads(_resource_bytes(f"draft_data/{stem}_expected.json"))
    if expected.get("schema_version") != "catalytic-earth.source-drafts-package.v1":
        raise ValueError("unsupported source draft package")
    if "reaction_correspondence_sha256" not in expected:
        return None
    raw = _resource_bytes(f"draft_data/{stem}_reaction_correspondence.json")
    if hashlib.sha256(raw).hexdigest() != expected["reaction_correspondence_sha256"]:
        raise ValueError("reaction correspondence package differs from its expected hash")
    attribution = _resource_bytes(f"draft_data/{stem}_reaction_attribution.md")
    if hashlib.sha256(attribution).hexdigest() != expected.get("reaction_attribution_sha256"):
        raise ValueError("reaction attribution package differs from its expected hash")
    sidecar = json.loads(raw)
    validate_reaction_correspondence(
        sidecar, bundle=verified_source_drafts(batch_name) if bundle is None else bundle,
    )
    return sidecar


def verified_step_evidence(
    batch_name: str = "default", *, bundle: dict[str, Any] | None = None,
    primary_evidence: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Load opt-in step context without altering immutable source drafts."""
    from .atlas_draft_batch import DEFAULT_BATCH, resolve_batch
    from .atlas_step_evidence import validate_step_evidence

    batch = resolve_batch(batch_name)
    stem = "source_drafts" if batch == DEFAULT_BATCH else batch.batch_id.replace("-", "_")
    expected = json.loads(_resource_bytes(f"draft_data/{stem}_expected.json"))
    if expected.get("schema_version") != "catalytic-earth.source-drafts-package.v1":
        raise ValueError("unsupported source draft package")
    if "step_evidence_sha256" not in expected:
        return None
    raw = _resource_bytes(f"draft_data/{stem}_step_evidence.json")
    if hashlib.sha256(raw).hexdigest() != expected["step_evidence_sha256"]:
        raise ValueError("step evidence package differs from its expected hash")
    sidecar = json.loads(raw)
    source_bundle = verified_source_drafts(batch_name) if bundle is None else bundle
    primary = (
        verified_primary_evidence(batch_name, bundle=source_bundle)
        if primary_evidence is None else primary_evidence
    )
    validate_step_evidence(
        sidecar, bundle=source_bundle,
        primary_evidence=primary if sidecar.get("primary_evidence_binding") is not None else None,
    )
    return sidecar


def build_parser() -> argparse.ArgumentParser:
    from .atlas_draft_batch import BATCHES
    from .atlas_primary_evidence import PRIMARY_OBSERVED_STATE_KINDS

    parser = argparse.ArgumentParser(
        prog="catalytic-earth",
        description="Deterministic, dependency-free Catalytic Earth core",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    reproduce = subparsers.add_parser(
        "reproduce", help="reproduce and verify the canonical fixture result"
    )
    reproduce.add_argument("--output", type=Path, help="optional JSON output path")
    atlas3 = subparsers.add_parser(
        "atlas3", help="reproduce the first three-case biological Atlas kernel"
    )
    atlas3.add_argument("--output", type=Path, help="optional JSON output path")
    atlas10 = subparsers.add_parser(
        "atlas10", help="reproduce the ten-case Atlas relationship-query surface"
    )
    atlas10.add_argument("--output", type=Path, help="optional JSON output path")
    structural_context = subparsers.add_parser(
        "atlas-structural-context",
        help="compare deposited catalytic atoms with chemical state and alternate conformations",
        description="Source-bound coordinate evidence, not productive design restraints. Filters retain complete matching contexts and their limitations.",
    )
    structural_context.add_argument("--case-id", help="exact Atlas case identifier")
    structural_context.add_argument("--pdb-id", help="exact PDB identifier, e.g. 1SUP")
    structural_context.add_argument("--site-id", help="exact canonical site identifier, e.g. P00782:S328")
    structural_context.add_argument("--output", type=Path, help="optional new JSON file; existing files are never overwritten")
    transformations = subparsers.add_parser(
        "atlas-transformations", help="query source-state atom and bond changes offline",
        description="Select a reviewed M-CSA record or use --all for the catalog. With neither option, reproduce the original M0187 query.",
    )
    transformations.add_argument("--mcsa-id", help="filter an exact M-CSA identifier, e.g. M0187")
    transformations.add_argument("--all", action="store_true", help="query all separately reviewed transformation sets")
    transformations.add_argument("--output", type=Path, help="optional JSON output path")
    transformation_sites = subparsers.add_parser(
        "atlas-transformation-sites",
        help="link changed source atoms to declared catalytic residues and protein structures offline",
        description="Preserve each transformation's review and exact proposal/step evidence. A residue correspondence does not identify a deposited atom or validate an intermediate.",
    )
    transformation_sites.add_argument("--mcsa-id", help="filter an exact M-CSA identifier, e.g. M0173")
    transformation_sites.add_argument("--source-atom", help="filter a before-panel atom token, e.g. a44; requires --mcsa-id")
    transformation_sites.add_argument("--site-id", help="filter an exact atlas site identifier, e.g. P35049:S204")
    transformation_sites.add_argument("--output", type=Path, help="optional new JSON file; existing files are never overwritten")
    mechanism_evidence = subparsers.add_parser(
        "atlas-mechanism-evidence",
        help="inspect a reviewed retrospective mechanism case and its published observations offline",
        description="Filters select observations while retaining the full case, competing explanations and limits. This is source review, not a new experiment or independent expert validation.",
    )
    mechanism_evidence.add_argument("--variant", help="exact variant identifier, e.g. H297N or K166R")
    mechanism_evidence.add_argument("--endpoint", choices=("turnover", "isotope_exchange", "structure"))
    mechanism_evidence.add_argument("--output", type=Path, help="optional new JSON file; existing files are never overwritten")
    comparisons = subparsers.add_parser(
        "atlas-panel-comparisons", help="query partial source-panel changes and unresolved coverage offline"
    )
    comparisons.add_argument("--mcsa-id", help="filter an exact M-CSA identifier, e.g. M0173")
    comparisons.add_argument("--output", type=Path, help="optional JSON output path")
    candidates = subparsers.add_parser(
        "atlas-candidates",
        help="extract an unreviewed adjacent-panel candidate from a local M-CSA snapshot",
        description="Read retained source bytes offline. Exact replay does not confer scientific review or experimental validation.",
    )
    candidates.add_argument("--source", type=Path, required=True, help="local retained M-CSA JSON snapshot")
    candidates.add_argument("--mechanism-id", type=int, required=True)
    candidates.add_argument("--before-step", type=int, required=True, help="compare this source panel with the next step's source panel")
    candidates.add_argument("--preserve-context", action="store_true", help="retain supported unchanged stereo/coordinate annotations as uninterpreted context")
    candidates.add_argument("--output", type=Path, help="optional new JSON file; existing files are never overwritten")
    events = subparsers.add_parser(
        "atlas-candidate-events", help="search unreviewed candidates by exact bond and charge changes offline",
        description="Require all changes within one retained candidate. Matches are literal drawing-level edits, not mechanism equivalence. With no change clauses, list candidates with eligible edits.",
    )
    events.add_argument("--bond", nargs=4, action="append", metavar=("E1", "E2", "BEFORE", "AFTER"),
                        help="require an undirected element-pair bond change; order 0 means no bond; repeat for AND")
    events.add_argument("--charge", nargs=3, action="append", metavar=("ELEMENT", "BEFORE", "AFTER"),
                        help="require an exact element formal-charge change; repeat for AND")
    events.add_argument("--support", choices=("after_graph_confirmed", "source_arrow_only", "any"),
                        default="after_graph_confirmed", help="support required of each matching edit (default: after_graph_confirmed)")
    events.add_argument("--mcsa-id", help="filter an exact M-CSA identifier, e.g. M0219")
    events.add_argument("--output", type=Path, help="optional new JSON file; existing files are never overwritten")
    patterns = subparsers.add_parser(
        "atlas-candidate-patterns", help="require candidate edits on the same named source atoms offline",
        description="Name atoms as ELEMENT:VARIABLE, such as C:x. Reuse a name to require the same before-panel source node; different names require distinct nodes. All edits must occur within one unreviewed candidate.",
    )
    patterns.add_argument("--bond", nargs=4, action="append", metavar=("ATOM1", "ATOM2", "BEFORE", "AFTER"),
                          help="require a bond change, e.g. --bond C:x C:y 0 1; repeat for AND")
    patterns.add_argument("--charge", nargs=3, action="append", metavar=("ATOM", "BEFORE", "AFTER"),
                          help="require a charge change, e.g. --charge C:x -1 0; repeat for AND")
    patterns.add_argument("--support", choices=("after_graph_confirmed", "source_arrow_only", "any"),
                          default="after_graph_confirmed", help="support required of each matching edit (default: after_graph_confirmed)")
    patterns.add_argument("--mcsa-id", help="filter an exact M-CSA identifier, e.g. M0219")
    patterns.add_argument("--output", type=Path, help="optional new JSON file; existing files are never overwritten")
    drafts = subparsers.add_parser(
        "atlas-drafts", help="query source-scoped mechanisms, states and abstentions offline"
    )
    drafts.add_argument(
        "--batch", choices=[*sorted(BATCHES), "all"], default="default",
        help="select a source batch, or query all separately (default: original four records)",
    )
    drafts.add_argument("--mcsa-id", help="filter an exact M-CSA identifier, e.g. M0107")
    drafts.add_argument("--assembly", help="filter the source-described assembly mode")
    drafts.add_argument("--text", help="search source chemistry and state descriptions")
    drafts.add_argument(
        "--mechanism-component", action="append", type=_mechanism_component_argument,
        metavar="SOURCE_LABEL",
        help="require an exact source event label; repeat for AND within one proposal",
    )
    drafts.add_argument(
        "--participant", action="append", type=_chebi_argument, metavar="CHEBI_ID",
        help="require an exact source ChEBI participant on either side; repeat for AND",
    )
    drafts.add_argument(
        "--reactant", action="append", type=_chebi_argument, metavar="CHEBI_ID",
        help="require a ChEBI participant on the source's left side; repeat for AND",
    )
    drafts.add_argument(
        "--product", action="append", type=_chebi_argument, metavar="CHEBI_ID",
        help="require a ChEBI participant on the source's right side; repeat for AND",
    )
    drafts.add_argument("--steps", action="store_true", help="include source steps and electron flows")
    drafts.add_argument(
        "--step-evidence", action="store_true",
        help="include optional reviewed step-context annotations with exact source witnesses",
    )
    drafts.add_argument(
        "--step-cofactor", action="append", type=_step_cofactor_argument,
        metavar="SOURCE_LABEL",
        help="require an exact cofactor label witnessed in one source step; repeat for AND",
    )
    drafts.add_argument(
        "--step-enzyme-context", action="append",
        choices=["active_site", "extra_enzymatic", "unresolved"],
        help="filter the explicitly supported enzyme context of one source step",
    )
    drafts.add_argument(
        "--step-source-assertion", action="append",
        choices=["explicitly_inferred", "explicitly_assumed", "source_silent"],
        help="filter exact infer/assume markers; source_silent does not mean observed",
    )
    drafts.add_argument(
        "--observed-state-context", action="store_true",
        help="include typed primary structural contexts with evidence and unresolved conflicts",
    )
    drafts.add_argument(
        "--observed-state", action="append", choices=sorted(PRIMARY_OBSERVED_STATE_KINDS),
        help="require a reviewed state kind; matches record context, not a source step",
    )
    drafts.add_argument(
        "--observed-component", action="append", type=_observed_component_argument,
        metavar="DEPOSITED_LABEL",
        help="require an exact deposited component label in one typed context; repeat for AND",
    )
    drafts.add_argument("--output", type=Path, help="optional JSON output path")
    subparsers.add_parser("claims", help="print the exact golden-result claim boundary")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "reproduce":
        result = verified_golden_result()
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "atlas3":
        result = verified_atlas3_result()
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "atlas10":
        result = verified_atlas10_result()
        # Keep the historical runtime result/hash reproducible, while placing
        # current source clarifications beside the affected relationship rows.
        context = verified_structural_context()
        result["current_structure_annotations"] = [
            {
                "case_id": row["case_id"], "pdb_id": row["pdb_id"],
                "context_id": row["context_id"],
                "interpretation": row["interpretation"],
                "inspect_command": "catalytic-earth atlas-structural-context --pdb-id " + row["pdb_id"],
            }
            for row in context["structures"]
        ]
        result["current_annotation_hash_scope"] = "Current annotations are separate from the frozen runtime_result_sha256; their package and review hashes are checked independently."
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "atlas-structural-context":
        from .atlas_structural_context import query_structural_context

        try:
            result = query_structural_context(
                verified_structural_context(), case_id=args.case_id,
                pdb_id=args.pdb_id, site_id=args.site_id,
            )
        except ValueError as exc:
            parser.error(str(exc))
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
        print(rendered, end="")
        return 0
    if args.command == "atlas-drafts":
        from .atlas_draft_batch import BATCHES
        from .atlas_draft_catalog import query_source_draft_batches
        from .atlas_draft_query import query_source_drafts

        filters = {
            "mcsa_id": args.mcsa_id, "assembly": args.assembly,
            "text": args.text, "include_steps": args.steps,
            "participants": args.participant or (), "reactants": args.reactant or (),
            "products": args.product or (),
            "mechanism_components": args.mechanism_component or (),
            "cofactors": args.step_cofactor or (),
            "enzyme_contexts": args.step_enzyme_context or (),
            "source_assertions": args.step_source_assertion or (),
            "include_observed_state_context": args.observed_state_context,
            "observed_states": args.observed_state or (),
            "observed_components": args.observed_component or (),
        }
        use_step_evidence = bool(
            args.step_evidence or args.step_cofactor
            or args.step_enzyme_context or args.step_source_assertion
        )
        if args.batch == "all":
            bundles = {name: verified_source_drafts(name) for name in sorted(BATCHES)}
            evidence = {
                name: verified_primary_evidence(name, bundle=bundle)
                for name, bundle in bundles.items()
            }
            result = query_source_draft_batches(
                bundles, primary_evidence_by_batch=evidence,
                step_evidence_by_batch={
                    name: verified_step_evidence(
                        name, bundle=bundle, primary_evidence=evidence[name],
                    ) for name, bundle in bundles.items()
                } if use_step_evidence else None,
                reaction_correspondence_by_batch={
                    name: verified_reaction_correspondence(name, bundle=bundle)
                    for name, bundle in bundles.items()
                },
                **filters,
            )
        else:
            bundle = verified_source_drafts(args.batch)
            primary = verified_primary_evidence(args.batch, bundle=bundle)
            result = query_source_drafts(
                bundle, **filters,
                primary_evidence=primary,
                reaction_correspondence=verified_reaction_correspondence(
                    args.batch, bundle=bundle,
                ),
                step_evidence=verified_step_evidence(
                    args.batch, bundle=bundle, primary_evidence=primary,
                ) if use_step_evidence else None,
            )
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "atlas-transformations":
        from .atlas_transformation_query import (
            TRANSFORMATION_SETS, normalize_mcsa_id, query_transformation_sets, query_transformations,
        )

        mcsa_id = normalize_mcsa_id(args.mcsa_id)
        atlas10 = json.loads(_resource_bytes(ATLAS10_KERNEL))
        if args.all:
            result = query_transformation_sets(
                {key: verified_transformations(key) for key in TRANSFORMATION_SETS},
                atlas10_bundle=atlas10, mcsa_id=mcsa_id,
            )
        else:
            key = mcsa_id if mcsa_id in TRANSFORMATION_SETS else "M0187"
            result = query_transformations(
                verified_transformations(key), atlas10_bundle=atlas10, mcsa_id=mcsa_id,
            )
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "atlas-transformation-sites":
        from .atlas_transformation_query import TRANSFORMATION_SETS
        from .atlas_transformation_sites import query_transformation_sites

        try:
            atlas10 = json.loads(_resource_bytes(ATLAS10_KERNEL))
            expected = json.loads(_resource_bytes(ATLAS10_EXPECTED))
            if _canonical_sha(atlas10) != expected.get("kernel_sha256"):
                raise ValueError("Atlas-10 site context differs from the packaged expectation")
            result = query_transformation_sites(
                {key: verified_transformations(key) for key in TRANSFORMATION_SETS},
                atlas10_bundle=atlas10,
                mcsa_id=args.mcsa_id, source_atom_id=args.source_atom, site_id=args.site_id,
            )
        except ValueError as exc:
            parser.error(str(exc))
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
        print(rendered, end="")
        return 0
    if args.command == "atlas-mechanism-evidence":
        from .atlas_mechanism_evidence import query_mechanism_evidence

        try:
            atlas10 = json.loads(_resource_bytes(ATLAS10_KERNEL))
            expected = json.loads(_resource_bytes(ATLAS10_EXPECTED))
            if _canonical_sha(atlas10) != expected.get("kernel_sha256"):
                raise ValueError("Atlas-10 context differs from the packaged expectation")
            result = query_mechanism_evidence(
                verified_mechanism_evidence(), atlas10_bundle=atlas10,
                transformation_values={"M0187": verified_transformations("M0187")},
                variant=args.variant, endpoint=args.endpoint,
            )
        except ValueError as exc:
            parser.error(str(exc))
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
        print(rendered, end="")
        return 0
    if args.command == "atlas-panel-comparisons":
        from .atlas_partial_panel_query import query_panel_comparisons

        result = query_panel_comparisons(
            verified_panel_comparisons(), atlas10_bundle=json.loads(_resource_bytes(ATLAS10_KERNEL)),
            mcsa_id=args.mcsa_id,
        )
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
        print(rendered, end="")
        return 0
    if args.command == "atlas-candidate-patterns":
        from .atlas_candidate_patterns import query_candidate_patterns

        try:
            clauses = []
            for atom1, atom2, before, after in (args.bond or []):
                e1, v1 = _pattern_atom_argument(atom1)
                e2, v2 = _pattern_atom_argument(atom2)
                clauses.append({"kind": "bond", "elements": [e1, e2], "variables": [v1, v2],
                                "before": int(before), "after": int(after)})
            for atom, before, after in (args.charge or []):
                element, variable = _pattern_atom_argument(atom)
                clauses.append({"kind": "charge", "elements": [element], "variables": [variable],
                                "before": int(before), "after": int(after)})
            result = query_candidate_patterns(
                verified_candidate_events(), clauses=clauses, mcsa_id=args.mcsa_id, support=args.support,
            )
        except (ValueError, argparse.ArgumentTypeError) as exc:
            parser.error(str(exc))
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
        print(rendered, end="")
        return 0
    if args.command == "atlas-candidate-events":
        from .atlas_candidate_events import query_candidate_events

        try:
            clauses = [
                {"kind": "bond", "elements": [e1, e2], "before": int(before), "after": int(after)}
                for e1, e2, before, after in (args.bond or [])
            ] + [
                {"kind": "charge", "elements": [element], "before": int(before), "after": int(after)}
                for element, before, after in (args.charge or [])
            ]
            result = query_candidate_events(
                verified_candidate_events(), clauses=clauses, mcsa_id=args.mcsa_id, support=args.support,
            )
        except ValueError as exc:
            parser.error(str(exc))
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
        print(rendered, end="")
        return 0
    if args.command == "atlas-candidates":
        from .atlas_candidate_extraction import extract_panel_candidate

        extractor = extract_panel_candidate
        if args.preserve_context:
            from .atlas_context_candidates import extract_context_panel_candidate

            extractor = extract_context_panel_candidate
        result = extractor(
            args.source.read_bytes(), mechanism_id=args.mechanism_id,
            before_step_id=args.before_step,
        )
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
        print(rendered, end="")
        return 0
    if args.command == "claims":
        expected = json.loads(_resource_bytes(GOLDEN_EXPECTED))
        print(expected["what_it_claims"])
        print(expected["what_it_does_not_claim"])
        return 0
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
