"""Build source-bound deposit contexts from declarative mmCIF selections.

The projector preserves exact selected source rows and may invoke the shared
biological-assembly projector for declared coordinate selections.  Scientific
interpretations remain data: the runtime only checks that each assertion cites
declared row, atom-selection, or distance-pair identifiers.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
from typing import Any

from .atlas_assembly_context import project_assembly
from .atlas_primary_source_check import parse_mmcif_categories
from .canonical_hash import canonical_file_sha256


SPEC_SCHEMA_VERSION = "catalytic-earth.deposit-context-spec.v1"
BUNDLE_SCHEMA_VERSION = "catalytic-earth.deposit-context.v1"
REVIEW_SCHEMA_VERSION = "catalytic-earth.deposit-context-review.v1"
REVIEW_DECISION = "accept_source_scoped_deposit_context"

_SPEC_FIELDS = {
    "schema_version",
    "packet_id",
    "source_binding",
    "row_selections",
    "interpretation",
}
_SOURCE_BINDING_FIELDS = {"path", "sha256"}
_ROW_SELECTION_FIELDS = {
    "selection_id",
    "category",
    "match",
    "expected_row_count",
}
_INTERPRETATION_FIELDS = {"assertions", "not_established"}
_ASSERTION_FIELDS = {
    "assertion_id",
    "status",
    "statement",
    "supporting_selection_ids",
}
_ASSERTION_STATUSES = {
    "computed_coordinate_description",
    "deposited_source_assertion",
    "project_interpretation",
    "unresolved_source_conflict",
}
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")
_SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_json_bytes(value: Any) -> bytes:
    """Return deterministic finite JSON bytes used for generated projections."""

    try:
        return (
            json.dumps(
                value,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("deposit context must be finite plain JSON") from exc


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    _require(
        isinstance(value, list) and (not nonempty or bool(value)),
        f"{label} must be a{' nonempty' if nonempty else 'n'} array",
    )
    return value


def _exact(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    row = _object(value, label)
    actual = set(row)
    _require(
        actual == fields,
        f"{label} fields differ; missing={sorted(fields - actual)}, "
        f"extra={sorted(actual - fields)}",
    )
    return row


def _text(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and bool(value.strip()),
        f"{label} must be nonempty text",
    )
    return value


def _identifier(value: Any, label: str) -> str:
    result = _text(value, label)
    _require(_ID_RE.fullmatch(result) is not None, f"{label} is invalid")
    return result


def _safe_bound_path(
    binding: Any, *, repo_root: Path, label: str = "source binding"
) -> tuple[dict[str, str], Path]:
    row = _exact(binding, _SOURCE_BINDING_FIELDS, label)
    relative = _text(row["path"], f"{label}.path")
    posix = PurePosixPath(relative)
    windows = PureWindowsPath(relative)
    _require(
        "\\" not in relative
        and not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and relative == posix.as_posix()
        and "." not in posix.parts
        and ".." not in posix.parts,
        f"{label}.path must be a safe repository-relative POSIX path",
    )
    digest = row["sha256"]
    _require(
        isinstance(digest, str) and _SHA_RE.fullmatch(digest) is not None,
        f"{label}.sha256 must be a lowercase SHA-256",
    )
    path = (repo_root / Path(posix)).resolve()
    _require(
        repo_root in path.parents and path.is_file(),
        f"{label} is missing or outside the repository",
    )
    _require(
        canonical_file_sha256(path) == digest,
        f"{label} hash differs",
    )
    return {"path": relative, "sha256": digest}, path


def _row_projections(
    selections: Any, *, tables: dict[str, list[dict[str, str]]]
) -> tuple[list[dict[str, Any]], set[str]]:
    declarations = _array(selections, "row_selections", nonempty=True)
    projections: list[dict[str, Any]] = []
    identifiers: set[str] = set()
    for index, raw in enumerate(declarations):
        label = f"row_selections[{index}]"
        declaration = _exact(raw, _ROW_SELECTION_FIELDS, label)
        selection_id = _identifier(
            declaration["selection_id"], f"{label}.selection_id"
        )
        _require(selection_id not in identifiers, "row selection IDs repeat")
        identifiers.add(selection_id)
        category = _text(declaration["category"], f"{label}.category")
        _require(category == category.lower(), f"{label}.category must be lowercase")
        _require(category in tables, f"{label}.category is unsupported")
        source_rows = tables[category]
        _require(source_rows, f"{label}.category has no deposited rows")

        match = _object(declaration["match"], f"{label}.match")
        _require(
            all(isinstance(key, str) and bool(key) for key in match),
            f"{label}.match fields must be nonempty strings",
        )
        _require(
            all(isinstance(value, str) for value in match.values()),
            f"{label}.match values must be raw mmCIF strings",
        )
        for field in match:
            _require(
                all(field in row for row in source_rows),
                f"{label}.match field {field!r} is absent from deposited {category} rows",
            )
        expected = declaration["expected_row_count"]
        _require(
            type(expected) is int and expected > 0,
            f"{label}.expected_row_count must be a positive integer",
        )
        matched = [
            row
            for row in source_rows
            if all(row[field] == value for field, value in match.items())
        ]
        _require(
            len(matched) == expected,
            f"{label} selected {len(matched)} rows; expected {expected}",
        )
        projections.append(
            {
                "selection_id": selection_id,
                "category": category,
                "match": copy.deepcopy(match),
                "expected_row_count": expected,
                "rows": copy.deepcopy(matched),
            }
        )
    return projections, identifiers


def _assembly_projection(
    spec: dict[str, Any], *, cif_text: str
) -> tuple[dict[str, Any] | None, set[str]]:
    if "assembly_spec" not in spec:
        return None, set()
    assembly_spec = _object(spec["assembly_spec"], "assembly_spec")
    projection = project_assembly(cif_text, assembly_spec)
    identifiers: list[str] = []
    for index, selection in enumerate(
        _array(assembly_spec.get("selections"), "assembly_spec.selections")
    ):
        row = _object(selection, f"assembly_spec.selections[{index}]")
        identifiers.append(
            _identifier(
                row.get("selection_id"),
                f"assembly_spec.selections[{index}].selection_id",
            )
        )
    for index, pair in enumerate(
        _array(assembly_spec.get("distance_pairs"), "assembly_spec.distance_pairs")
    ):
        row = _object(pair, f"assembly_spec.distance_pairs[{index}]")
        identifiers.append(
            _identifier(
                row.get("pair_id"),
                f"assembly_spec.distance_pairs[{index}].pair_id",
            )
        )
    _require(
        len(identifiers) == len(set(identifiers)),
        "assembly selection and distance-pair IDs repeat",
    )
    return projection, set(identifiers)


def _interpretation(value: Any, *, declared_ids: set[str]) -> dict[str, Any]:
    interpretation = _exact(value, _INTERPRETATION_FIELDS, "interpretation")
    assertions = _array(
        interpretation["assertions"], "interpretation.assertions", nonempty=True
    )
    assertion_ids: set[str] = set()
    for index, raw in enumerate(assertions):
        label = f"interpretation.assertions[{index}]"
        assertion = _exact(raw, _ASSERTION_FIELDS, label)
        assertion_id = _identifier(assertion["assertion_id"], f"{label}.assertion_id")
        _require(assertion_id not in assertion_ids, "interpretation assertion IDs repeat")
        assertion_ids.add(assertion_id)
        _require(
            assertion["status"] in _ASSERTION_STATUSES,
            f"{label}.status is unsupported",
        )
        _text(assertion["statement"], f"{label}.statement")
        support = _array(
            assertion["supporting_selection_ids"],
            f"{label}.supporting_selection_ids",
            nonempty=True,
        )
        _require(
            all(isinstance(item, str) and _ID_RE.fullmatch(item) for item in support),
            f"{label}.supporting_selection_ids are invalid",
        )
        _require(
            len(support) == len(set(support)),
            f"{label}.supporting_selection_ids repeat",
        )
        missing = set(support) - declared_ids
        _require(
            not missing,
            f"{label} references undeclared selection IDs {sorted(missing)}",
        )
    boundaries = _array(
        interpretation["not_established"],
        "interpretation.not_established",
        nonempty=True,
    )
    _require(
        all(isinstance(item, str) and bool(item.strip()) for item in boundaries),
        "interpretation.not_established entries must be nonempty text",
    )
    _require(
        len(boundaries) == len(set(boundaries)),
        "interpretation.not_established entries repeat",
    )
    return copy.deepcopy(interpretation)


def build_deposit_context(
    spec: dict[str, Any], *, source_path: Path
) -> dict[str, Any]:
    """Build one deterministic deposit context from a validated bound source."""

    required = set(_SPEC_FIELDS)
    allowed = required | {"assembly_spec"}
    top = _object(spec, "deposit-context spec")
    _require(
        required <= set(top) <= allowed,
        "deposit-context spec fields differ; "
        f"missing={sorted(required - set(top))}, extra={sorted(set(top) - allowed)}",
    )
    _require(
        top["schema_version"] == SPEC_SCHEMA_VERSION,
        "unsupported deposit-context spec",
    )
    packet_id = _identifier(top["packet_id"], "packet_id")
    binding = _exact(top["source_binding"], _SOURCE_BINDING_FIELDS, "source_binding")
    _require(
        canonical_file_sha256(source_path) == binding["sha256"],
        "source binding hash differs",
    )
    try:
        cif_text = source_path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        raise ValueError("deposit source is not readable UTF-8 mmCIF") from exc
    tables = parse_mmcif_categories(cif_text)
    rows, row_ids = _row_projections(top["row_selections"], tables=tables)
    assembly, assembly_ids = _assembly_projection(top, cif_text=cif_text)
    overlap = row_ids & assembly_ids
    _require(
        not overlap,
        f"selection IDs repeat across row and assembly declarations: {sorted(overlap)}",
    )
    interpretation = _interpretation(
        top["interpretation"], declared_ids=row_ids | assembly_ids
    )
    bundle = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "packet_id": packet_id,
        "spec_payload_sha256": hashlib.sha256(canonical_json_bytes(top)).hexdigest(),
        "source_binding": copy.deepcopy(binding),
        "row_selection_count": len(rows),
        "selected_row_count": sum(len(row["rows"]) for row in rows),
        "row_selections": rows,
        "assembly_projection": assembly,
        "interpretation": interpretation,
        "claim_boundary": {
            "source_rows": (
                "parsed values from hash-bound mmCIF rows selected by declared "
                "string equality and count"
            ),
            "coordinate_geometry": (
                "declared assembly atoms and Euclidean distances; no bond or joint-state inference"
                if assembly is not None
                else "not projected"
            ),
            "interpretation": (
                "explicitly supplied project statements requiring source review; "
                "not semantically validated or inferred by runtime"
            ),
            "does_not_establish": [
                "chemical normalization or ligand equivalence",
                "reaction, mechanism, source-step, or catalytic-role applicability",
                "productive geometry, solution population, rate, or design competence",
            ],
        },
    }
    canonical_json_bytes(bundle)
    return bundle


def _packet_path(packet: Path, *, repo_root: Path) -> Path:
    candidate = packet if packet.is_absolute() else repo_root / packet
    result = candidate.resolve()
    _require(
        repo_root in result.parents and result.is_dir(),
        "deposit-context packet is missing or outside the repository",
    )
    return result


def load_and_build_deposit_context(
    packet: Path, repo_root: Path
) -> dict[str, Any]:
    """Load a repository packet and build its deterministic projection."""

    root = repo_root.resolve()
    _require(root.is_dir(), "repo_root is not a directory")
    packet_path = _packet_path(Path(packet), repo_root=root)
    spec_path = packet_path / "spec.json"
    _require(spec_path.is_file(), "deposit-context spec.json is missing")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    binding, source_path = _safe_bound_path(
        _object(spec, "deposit-context spec").get("source_binding"),
        repo_root=root,
    )
    result = build_deposit_context(spec, source_path=source_path)
    _require(result["source_binding"] == binding, "source binding changed during build")
    return result


def check_deposit_context(packet: Path, repo_root: Path) -> dict[str, Any]:
    """Rebuild a packet and require exact projection and source-review pins."""

    root = repo_root.resolve()
    packet_path = _packet_path(Path(packet), repo_root=root)
    result = load_and_build_deposit_context(packet_path, root)
    projection_path = packet_path / "projection.json"
    review_path = packet_path / "review.json"
    _require(projection_path.is_file(), "deposit-context projection.json is missing")
    _require(review_path.is_file(), "deposit-context review.json is missing")
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    _require(projection == result, "deposit-context projection is stale")
    review = _object(
        json.loads(review_path.read_text(encoding="utf-8")),
        "deposit-context review",
    )
    _require(
        review.get("schema_version") == REVIEW_SCHEMA_VERSION,
        "deposit-context review schema differs",
    )
    _require(
        review.get("decision") == REVIEW_DECISION,
        "deposit-context review decision differs",
    )
    source_path = _safe_bound_path(
        json.loads((packet_path / "spec.json").read_text(encoding="utf-8"))[
            "source_binding"
        ],
        repo_root=root,
    )[1]
    expected_pins = {
        "spec.json": canonical_file_sha256(packet_path / "spec.json"),
        "projection.json": canonical_file_sha256(projection_path),
        "source": canonical_file_sha256(source_path),
    }
    _require(
        review.get("reviewed_sha256") == expected_pins,
        "deposit-context source-review pins are stale",
    )
    return result
