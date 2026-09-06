"""Narrow build-time checks of declared primary-structure facts.

This module is deliberately not a general mmCIF implementation.  It parses the
small set of categories used by Atlas primary observed-state projections and
fails closed when those categories are malformed.  It validates deposited
identifiers, rows, and tokens; it does not validate prose, chemistry, curated
sequence mappings, source steps, or mechanism applicability.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
from typing import Any

from catalytic_earth.canonical_hash import canonical_file_sha256


SOURCE_AUDIT_SCHEMA_VERSION = "catalytic-earth.primary-structure-source-audit.v1"

_CATEGORIES = {
    "_atom_site",
    "_chem_comp",
    "_chem_comp_atom",
    "_chem_comp_bond",
    "_entry",
    "_entity",
    "_pdbx_nonpoly_scheme",
    "_pdbx_poly_seq_scheme",
    "_struct_conn",
    "_struct_site",
}
_MISSING = {".", "?"}
_INTEGER_RE = re.compile(r"^[+-]?[0-9]+$")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, context: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{context} must be an object")
    return value


def _array(value: Any, context: str) -> list[Any]:
    _require(isinstance(value, list), f"{context} must be an array")
    return value


def _text(value: Any, context: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{context} must be nonempty text")
    return value


@dataclass(frozen=True)
class _Token:
    value: str
    line: int
    quoted: bool


def _line_tokens(line: str, line_number: int) -> list[_Token]:
    result: list[_Token] = []
    index = 0
    while index < len(line):
        while index < len(line) and line[index].isspace():
            index += 1
        if index == len(line) or line[index] == "#":
            break
        if line[index] in {"'", '"'}:
            quote = line[index]
            index += 1
            start = index
            while index < len(line):
                if line[index] == quote and (
                    index + 1 == len(line)
                    or line[index + 1].isspace()
                    or line[index + 1] == "#"
                ):
                    result.append(_Token(line[start:index], line_number, True))
                    index += 1
                    break
                index += 1
            else:
                raise ValueError(f"mmCIF line {line_number} has an unterminated quote")
            continue
        start = index
        while index < len(line) and not line[index].isspace():
            index += 1
        result.append(_Token(line[start:index], line_number, False))
    return result


def _tokenize_mmcif(text: str) -> list[_Token]:
    _require(isinstance(text, str) and "\x00" not in text, "mmCIF text is invalid")
    lines = text.splitlines()
    tokens: list[_Token] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        line_number = index + 1
        if line.startswith(";"):
            content = [line[1:]]
            index += 1
            while index < len(lines) and not lines[index].startswith(";"):
                content.append(lines[index])
                index += 1
            _require(index < len(lines), f"mmCIF line {line_number} has no text-field terminator")
            _require(
                lines[index] == ";",
                f"mmCIF line {index + 1} has text after a semicolon terminator",
            )
            tokens.append(_Token("\n".join(content), line_number, True))
            index += 1
            continue
        tokens.extend(_line_tokens(line, line_number))
        index += 1
    return tokens


def _is_control(token: _Token) -> bool:
    if token.quoted:
        return False
    lowered = token.value.lower()
    return (
        token.value.startswith("_")
        or lowered in {"loop_", "stop_", "global_"}
        or lowered.startswith("data_")
        or lowered.startswith("save_")
    )


def _category(tag: str) -> str:
    return tag.split(".", 1)[0].lower()


def _field(tag: str) -> str:
    _require("." in tag, f"unsupported mmCIF data name {tag!r}")
    return tag.split(".", 1)[1].lower()


def _parse_mmcif_categories(text: str) -> dict[str, list[dict[str, str]]]:
    """Parse selected categories, rejecting malformed token/row boundaries."""

    tokens = _tokenize_mmcif(text)
    tables: dict[str, list[dict[str, str]]] = {category: [] for category in _CATEGORIES}
    scalar_rows: dict[str, dict[str, str]] = {}
    data_blocks = 0
    index = 0
    while index < len(tokens):
        token = tokens[index]
        lowered = token.value.lower()
        if not token.quoted and lowered.startswith("data_"):
            data_blocks += 1
            index += 1
            continue
        if not token.quoted and (
            lowered in {"global_"} or lowered.startswith("save_")
        ):
            raise ValueError(f"unsupported mmCIF control token at line {token.line}")
        if not token.quoted and lowered == "stop_":
            raise ValueError(f"unexpected mmCIF stop_ at line {token.line}")
        if not token.quoted and lowered == "loop_":
            index += 1
            headers: list[_Token] = []
            while (
                index < len(tokens)
                and not tokens[index].quoted
                and tokens[index].value.startswith("_")
            ):
                headers.append(tokens[index])
                index += 1
            _require(headers, f"mmCIF loop at line {token.line} has no headers")
            categories = {_category(header.value) for header in headers}
            _require(
                len(categories) == 1,
                f"mmCIF loop at line {token.line} mixes categories",
            )
            values: list[_Token] = []
            while index < len(tokens) and not _is_control(tokens[index]):
                values.append(tokens[index])
                index += 1
            _require(
                len(values) % len(headers) == 0,
                f"mmCIF loop at line {token.line} has an incomplete row",
            )
            category = next(iter(categories))
            if category in tables:
                fields = [_field(header.value) for header in headers]
                _require(
                    len(fields) == len(set(fields)),
                    f"mmCIF loop at line {token.line} repeats a field",
                )
                for offset in range(0, len(values), len(headers)):
                    row_tokens = values[offset : offset + len(headers)]
                    tables[category].append(
                        {field: item.value for field, item in zip(fields, row_tokens)}
                    )
            if index < len(tokens) and tokens[index].value.lower() == "stop_":
                index += 1
            continue
        if not token.quoted and token.value.startswith("_"):
            _require(index + 1 < len(tokens), f"mmCIF tag at line {token.line} has no value")
            value = tokens[index + 1]
            _require(
                not _is_control(value),
                f"mmCIF tag at line {token.line} has no scalar value",
            )
            category = _category(token.value)
            if category in tables:
                row = scalar_rows.setdefault(category, {})
                field = _field(token.value)
                _require(field not in row, f"mmCIF scalar field {token.value!r} repeats")
                row[field] = value.value
            index += 2
            continue
        raise ValueError(f"unexpected mmCIF token at line {token.line}: {token.value!r}")
    _require(data_blocks == 1, "mmCIF must contain exactly one data block")
    for category, row in scalar_rows.items():
        tables[category].append(row)
    return tables


def _integer(value: Any, context: str) -> int:
    _require(isinstance(value, str) and _INTEGER_RE.fullmatch(value), f"{context} is not an integer")
    return int(value)


def _optional_integer(value: Any, context: str) -> int | None:
    if value in _MISSING:
        return None
    return _integer(value, context)


def _float(value: Any, context: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{context} is not numeric") from exc
    _require(math.isfinite(result), f"{context} is not finite")
    return result


def _required_fields(row: dict[str, str], fields: set[str], context: str) -> None:
    missing = fields - set(row)
    _require(not missing, f"{context} lacks fields {sorted(missing)}")


def _safe_bound_path(binding: dict[str, Any], repo_root: Path) -> Path:
    relative_text = _text(binding.get("path"), "primary source binding path")
    posix = PurePosixPath(relative_text)
    windows = PureWindowsPath(relative_text)
    _require(
        "\\" not in relative_text
        and not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and relative_text == posix.as_posix()
        and "." not in posix.parts
        and ".." not in posix.parts,
        "primary source binding path is not repository-relative",
    )
    path = (repo_root / Path(posix)).resolve()
    _require(repo_root in path.parents and path.is_file(), "primary source binding is missing")
    _require(
        canonical_file_sha256(path) == binding.get("sha256"),
        "primary source binding hash differs",
    )
    return path


def _structure_binding(
    annotation: dict[str, Any],
    bindings: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows = [
        item
        for item in _array(annotation.get("evidence"), "annotation evidence")
        if isinstance(item, dict)
        and item.get("evidence_role") == "direct_support"
        and item.get("source_kind") == "primary_structure_record"
    ]
    _require(len(rows) == 1, "observed-state annotation needs one primary structure source")
    binding_id = _text(rows[0].get("source_binding_id"), "structure evidence binding ID")
    binding = bindings.get(binding_id)
    _require(
        binding is not None and binding.get("artifact_kind") == "primary_source",
        "structure evidence does not bind primary source bytes",
    )
    return binding


def _site_id(
    rows: list[dict[str, str]],
    *,
    author_chain: str,
    author_component: str,
    author_number: int,
) -> str | None:
    matches = []
    for row in rows:
        fields = {"id", "pdbx_auth_asym_id", "pdbx_auth_comp_id", "pdbx_auth_seq_id"}
        _required_fields(row, fields, "_struct_site row")
        raw_number = row["pdbx_auth_seq_id"]
        if (
            row["pdbx_auth_asym_id"] == author_chain
            and row["pdbx_auth_comp_id"] == author_component
            and raw_number not in _MISSING
            and _integer(raw_number, "_struct_site author number") == author_number
        ):
            matches.append(row["id"])
    _require(len(matches) <= 1, "multiple structure sites select one instance")
    return matches[0] if matches else None


def _nonpoly_source_alias(
    rows: list[dict[str, str]],
    fact: dict[str, Any],
) -> tuple[str | None, int | None]:
    required = {
        "asym_id",
        "entity_id",
        "mon_id",
        "pdb_seq_num",
        "auth_seq_num",
        "pdb_mon_id",
        "auth_mon_id",
        "pdb_strand_id",
    }
    matches = []
    for row in rows:
        _required_fields(row, required, "_pdbx_nonpoly_scheme row")
        if (
            row["asym_id"] == fact["label_asym_id"]
            and row["entity_id"] == fact["label_entity_id"]
            and row["mon_id"] == fact["label_component_id"]
            and row["pdb_strand_id"] == fact["atom_author_chain_id"]
            and row["pdb_mon_id"] == fact["atom_author_component_id"]
            and _integer(row["pdb_seq_num"], "nonpoly PDB number")
            == fact["atom_author_residue_number"]
        ):
            matches.append(row)
    _require(len(matches) == 1, "nonpoly source-author identity is ambiguous or missing")
    row = matches[0]
    component = None if row["auth_mon_id"] in _MISSING else row["auth_mon_id"]
    number = _optional_integer(row["auth_seq_num"], "nonpoly source-author number")
    _require((component is None) == (number is None), "nonpoly source-author fields differ")
    return component, number


def _polymer_alias_exists(rows: list[dict[str, str]], fact: dict[str, Any]) -> None:
    required = {
        "asym_id",
        "entity_id",
        "mon_id",
        "seq_id",
        "pdb_mon_id",
        "pdb_seq_num",
        "pdb_strand_id",
    }
    matches = []
    for row in rows:
        _required_fields(row, required, "_pdbx_poly_seq_scheme row")
        if (
            row["asym_id"] == fact["label_asym_id"]
            and row["entity_id"] == fact["label_entity_id"]
            and row["mon_id"] == fact["label_component_id"]
            and _integer(row["seq_id"], "polymer label sequence ID")
            == fact["label_seq_id"]
            and row["pdb_strand_id"] == fact["atom_author_chain_id"]
            and row["pdb_mon_id"] == fact["atom_author_component_id"]
            and _integer(row["pdb_seq_num"], "polymer PDB number")
            == fact["atom_author_residue_number"]
        ):
            matches.append(row)
    _require(len(matches) == 1, "polymer sequence identity is ambiguous or missing")


def _audit_component_identity(
    claim: dict[str, Any],
    tables: dict[str, list[dict[str, str]]],
) -> None:
    entity = _object(claim.get("observed_entity"), "observed entity")
    component_id = _text(entity.get("source_component_id"), "observed component")
    entity_id = _text(entity.get("entity_id"), "observed entity ID")

    component_rows = []
    for row in tables["_chem_comp"]:
        _required_fields(row, {"id", "name", "type"}, "_chem_comp row")
        if row["id"] == component_id:
            component_rows.append(row)
    _require(len(component_rows) == 1, "observed component identity is ambiguous or missing")
    _require(
        component_rows[0]["name"] == entity.get("source_description"),
        "observed component description differs from raw mmCIF",
    )

    entity_rows = []
    for row in tables["_entity"]:
        _required_fields(row, {"id", "type", "pdbx_description"}, "_entity row")
        if row["id"] == entity_id:
            entity_rows.append(row)
    _require(len(entity_rows) == 1, "observed entity identity is ambiguous or missing")
    expected_type = {
        "polymer_component": "polymer",
        "nonpolymer_component": "non-polymer",
    }.get(entity.get("entity_context"))
    _require(expected_type is not None, "observed entity context is invalid")
    _require(entity_rows[0]["type"] == expected_type, "observed entity type differs from raw mmCIF")
    if expected_type == "non-polymer":
        _require(
            entity_rows[0]["pdbx_description"] == entity.get("source_description"),
            "observed entity description differs from raw mmCIF",
        )


def _audit_protein_context(
    claim: dict[str, Any],
    tables: dict[str, list[dict[str, str]]],
) -> None:
    structure = _object(claim.get("structure_context"), "structure context")
    entity = _object(claim.get("observed_entity"), "observed entity")
    model_id = structure.get("model_id")
    _require(type(model_id) is int and model_id > 0, "structure model is invalid")
    protein_entities = set(_array(structure.get("protein_entity_ids"), "protein entities"))
    label_chains = set(_array(structure.get("protein_label_asym_ids"), "protein label chains"))
    author_chains = set(_array(structure.get("protein_author_chain_ids"), "protein author chains"))
    _require(protein_entities and label_chains and author_chains, "protein context is empty")

    entity_types = {}
    for row in tables["_entity"]:
        _required_fields(row, {"id", "type"}, "_entity row")
        entity_types[row["id"]] = row["type"]
    _require(
        all(entity_types.get(item) == "polymer" for item in protein_entities),
        "declared protein entity is not a raw polymer entity",
    )

    observed: set[tuple[str, str, str]] = set()
    for row in tables["_atom_site"]:
        _required_fields(
            row,
            {"label_asym_id", "label_entity_id", "auth_asym_id", "pdbx_pdb_model_num"},
            "_atom_site row",
        )
        if (
            row["label_entity_id"] in protein_entities
            and _integer(row["pdbx_pdb_model_num"], "protein atom-site model") == model_id
        ):
            observed.add((row["label_asym_id"], row["label_entity_id"], row["auth_asym_id"]))

    if entity.get("entity_context") == "nonpolymer_component":
        _require(
            {item[0] for item in observed} == label_chains
            and {item[1] for item in observed} == protein_entities
            and {item[2] for item in observed} == author_chains,
            "declared protein context differs from raw model-bound polymer chains",
        )
    else:
        _require(
            all(
                any(row[0] == label and row[2] in author_chains for row in observed)
                for label in label_chains
            )
            and all(
                any(row[2] == author and row[0] in label_chains for row in observed)
                for author in author_chains
            ),
            "declared selected protein chain is absent from the raw model",
        )


def _derive_instances(
    claim: dict[str, Any],
    tables: dict[str, list[dict[str, str]]],
) -> tuple[list[dict[str, Any]], list[set[str]]]:
    structure = _object(claim.get("structure_context"), "structure_context")
    entity = _object(claim.get("observed_entity"), "observed_entity")
    model_id = structure.get("model_id")
    _require(type(model_id) is int and model_id > 0, "structure model is invalid")
    entity_context = entity.get("entity_context")
    _require(entity_context in {"polymer_component", "nonpolymer_component"}, "entity context is invalid")
    atom_rows = tables["_atom_site"]
    _require(atom_rows, "mmCIF lacks _atom_site")
    fields = {
        "label_atom_id",
        "label_comp_id",
        "label_asym_id",
        "label_entity_id",
        "label_seq_id",
        "auth_seq_id",
        "auth_comp_id",
        "auth_asym_id",
        "pdbx_pdb_model_num",
    }
    grouped: dict[tuple[Any, ...], set[str]] = {}
    protein_author_chains = set(_array(structure.get("protein_author_chain_ids"), "protein author chains"))
    protein_label_chains = set(_array(structure.get("protein_label_asym_ids"), "protein label chains"))
    for row in atom_rows:
        _required_fields(row, fields, "_atom_site row")
        if (
            row["label_entity_id"] != entity.get("entity_id")
            or row["label_comp_id"] != entity.get("source_component_id")
            or _integer(row["pdbx_pdb_model_num"], "atom-site model") != model_id
            or (
                entity_context == "polymer_component"
                and (
                    row["label_asym_id"] not in protein_label_chains
                    or row["auth_asym_id"] not in protein_author_chains
                )
            )
        ):
            continue
        key = (
            row["label_asym_id"],
            row["label_entity_id"],
            row["label_comp_id"],
            _optional_integer(row["label_seq_id"], "atom-site label sequence ID"),
            row["auth_asym_id"],
            row["auth_comp_id"],
            _integer(row["auth_seq_id"], "atom-site author number"),
        )
        grouped.setdefault(key, set()).add(row["label_atom_id"])
    _require(grouped, "declared observed component has no model-bound atom-site rows")

    facts: list[dict[str, Any]] = []
    atom_sets: list[set[str]] = []
    for key in sorted(grouped, key=lambda item: (item[0], item[2], item[6])):
        fact = {
            "label_asym_id": key[0],
            "label_entity_id": key[1],
            "label_component_id": key[2],
            "label_seq_id": key[3],
            "atom_author_chain_id": key[4],
            "atom_author_component_id": key[5],
            "atom_author_residue_number": key[6],
        }
        if entity_context == "nonpolymer_component":
            source_component, source_number = _nonpoly_source_alias(
                tables["_pdbx_nonpoly_scheme"], fact
            )
        else:
            _require(fact["label_seq_id"] is not None, "polymer component lacks label position")
            _polymer_alias_exists(tables["_pdbx_poly_seq_scheme"], fact)
            source_component, source_number = None, None
        fact.update(
            {
                "source_author_component_id": source_component,
                "source_author_residue_number": source_number,
                "structure_site_id": _site_id(
                    tables["_struct_site"],
                    author_chain=fact["atom_author_chain_id"],
                    author_component=fact["atom_author_component_id"],
                    author_number=fact["atom_author_residue_number"],
                ),
            }
        )
        facts.append(fact)
        atom_sets.append(grouped[key])
    return facts, atom_sets


def _connection_label_components(row: dict[str, str]) -> set[str]:
    result = set()
    for side in (1, 2, 3):
        value = row.get(f"ptnr{side}_label_comp_id")
        if value is not None and value not in _MISSING:
            result.add(value)
    return result


def _audit_connection_inventory(
    annotation: dict[str, Any],
    tables: dict[str, list[dict[str, str]]],
) -> int:
    edges = _array(
        _object(annotation.get("projection_excerpt"), "projection excerpt").get("support_edges"),
        "support edges",
    )
    inventory_edges = [row for row in edges if row.get("edge_kind") == "deposited_connection_inventory"]
    if not inventory_edges:
        return 0
    _require(len(inventory_edges) == 1, "connection inventory edge is ambiguous")
    expected = _object(inventory_edges[0].get("extracted_values"), "connection inventory")
    queried = _text(expected.get("queried_component_id"), "queried connection component")
    rows = tables["_struct_conn"]
    for row in rows:
        _required_fields(
            row,
            {"id", "ptnr1_label_comp_id", "ptnr2_label_comp_id"},
            "_struct_conn row",
        )
    _require(len({row["id"] for row in rows}) == len(rows), "raw connection IDs repeat")
    components = sorted({item for row in rows for item in _connection_label_components(row)})
    matching = sum(queried in _connection_label_components(row) for row in rows)
    actual = {
        "queried_component_id": queried,
        "attachment_context": "absent_from_deposited_struct_conn",
        "struct_conn_row_count": len(rows),
        "matching_component_row_count": matching,
        "connected_component_ids": components,
    }
    _require(actual == expected, "deposited struct_conn inventory differs from raw mmCIF")
    return len(rows)


def _endpoint_from_connection(
    row: dict[str, str],
    side: int,
    atom_rows: list[dict[str, str]],
    model_id: int,
) -> dict[str, Any]:
    prefix = f"ptnr{side}_"
    label_asym = row[prefix + "label_asym_id"]
    label_component = row[prefix + "label_comp_id"]
    label_seq = _optional_integer(row[prefix + "label_seq_id"], "connection label sequence ID")
    label_atom = row[prefix + "label_atom_id"]
    author_asym = row[f"ptnr{side}_auth_asym_id"]
    author_component = row[f"ptnr{side}_auth_comp_id"]
    author_number = _integer(row[f"ptnr{side}_auth_seq_id"], "connection author number")
    entity_ids = {
        atom["label_entity_id"]
        for atom in atom_rows
        if atom.get("label_asym_id") == label_asym
        and atom.get("label_comp_id") == label_component
        and _optional_integer(atom.get("label_seq_id"), "endpoint atom label sequence ID")
        == label_seq
        and atom.get("label_atom_id") == label_atom
        and atom.get("auth_asym_id") == author_asym
        and atom.get("auth_comp_id") == author_component
        and _integer(atom.get("auth_seq_id"), "endpoint atom author number")
        == author_number
        and _integer(atom.get("pdbx_pdb_model_num"), "endpoint atom model") == model_id
    }
    _require(len(entity_ids) == 1, "connection endpoint does not resolve to one atom-site entity")
    return {
        "label_asym_id": label_asym,
        "label_entity_id": next(iter(entity_ids)),
        "label_component_id": label_component,
        "label_seq_id": label_seq,
        "atom_author_chain_id": author_asym,
        "atom_author_component_id": author_component,
        "atom_author_residue_number": author_number,
        "atom_name": label_atom,
    }


def _audit_attachments(
    claim: dict[str, Any],
    tables: dict[str, list[dict[str, str]]],
) -> int:
    attachments = _array(claim.get("protein_attachments"), "protein attachments")
    entity = _object(claim.get("observed_entity"), "observed entity")
    structure = _object(claim.get("structure_context"), "structure context")
    rows = tables["_struct_conn"]
    required = {
        "id",
        "conn_type_id",
        "ptnr1_label_asym_id",
        "ptnr1_label_comp_id",
        "ptnr1_label_seq_id",
        "ptnr1_label_atom_id",
        "ptnr1_auth_asym_id",
        "ptnr1_auth_comp_id",
        "ptnr1_auth_seq_id",
        "ptnr2_label_asym_id",
        "ptnr2_label_comp_id",
        "ptnr2_label_seq_id",
        "ptnr2_label_atom_id",
        "ptnr2_auth_asym_id",
        "ptnr2_auth_comp_id",
        "ptnr2_auth_seq_id",
        "pdbx_dist_value",
        "pdbx_value_order",
    }
    for row in rows:
        _required_fields(row, required, "_struct_conn row")
    component = entity.get("source_component_id")
    relevant = [row for row in rows if component in _connection_label_components(row)]
    _require(
        {row["id"] for row in relevant}
        == {attachment.get("connection_id") for attachment in attachments},
        "declared attachments do not cover every raw component connection",
    )
    row_by_id = {row["id"]: row for row in relevant}
    _require(len(row_by_id) == len(relevant), "raw connection IDs repeat")
    model_id = structure.get("model_id")
    _require(type(model_id) is int, "structure model is invalid")
    for attachment in attachments:
        row = row_by_id[attachment["connection_id"]]
        endpoint1 = _endpoint_from_connection(row, 1, tables["_atom_site"], model_id)
        endpoint2 = _endpoint_from_connection(row, 2, tables["_atom_site"], model_id)
        ligand = _object(attachment.get("ligand_endpoint"), "ligand endpoint")
        protein = _object(attachment.get("protein_endpoint"), "protein endpoint")
        _require(
            (endpoint1 == protein and endpoint2 == ligand)
            or (endpoint2 == protein and endpoint1 == ligand),
            f"raw connection {row['id']} endpoints differ",
        )
        raw_order = row["pdbx_value_order"]
        actual_code = None if raw_order in _MISSING else raw_order
        _require(
            row["conn_type_id"] == attachment.get("raw_conn_type")
            and _float(row["pdbx_dist_value"], "connection distance")
            == attachment.get("distance_angstrom")
            and raw_order == attachment.get("source_bond_order_token")
            and actual_code == attachment.get("source_bond_order_code"),
            f"raw connection {row['id']} type, distance, or order differs",
        )
    return len(relevant)


def _raw_bond_exists(
    rows: list[dict[str, str]],
    *,
    component: str,
    atom_ids: list[str],
    value_order: str,
) -> bool:
    matches = [
        row
        for row in rows
        if row.get("comp_id") == component
        and [row.get("atom_id_1"), row.get("atom_id_2")] == atom_ids
        and row.get("value_order") == value_order
    ]
    _require(len(matches) <= 1, "raw component bond repeats")
    return len(matches) == 1


def _audit_declared_bonds_and_atoms(
    annotation: dict[str, Any],
    atom_sets: list[set[str]],
    tables: dict[str, list[dict[str, str]]],
) -> int:
    claim = _object(annotation.get("claim"), "observed-state claim")
    observations = _array(claim.get("chemical_observations"), "chemical observations")
    entity = _object(claim.get("observed_entity"), "observed entity")
    component = _text(entity.get("source_component_id"), "observed component")
    bond_rows = tables["_chem_comp_bond"]
    checked = 0

    typed_dictionary = [
        row
        for row in observations
        if row.get("observation_kind") == "deposited_component_dictionary_bond_order"
    ]
    modeled_inventory = [
        row
        for row in observations
        if row.get("observation_kind") == "deposited_modeled_instance_atom_inventory"
    ]
    dictionary_atom_rows = []
    for row in tables["_chem_comp_atom"]:
        _required_fields(row, {"comp_id", "atom_id"}, "_chem_comp_atom row")
        if row["comp_id"] == component:
            dictionary_atom_rows.append(row["atom_id"])
    dictionary_atoms = set(dictionary_atom_rows)
    _require(dictionary_atoms, "observed component has no dictionary atoms")
    _require(
        len(dictionary_atoms) == len(dictionary_atom_rows),
        "observed component repeats a dictionary atom ID",
    )
    for observation in typed_dictionary:
        atom_ids = _array(observation.get("source_atom_ids"), "dictionary bond atoms")
        _require(len(atom_ids) == 2 and all(isinstance(item, str) for item in atom_ids), "dictionary bond atoms are invalid")
        order = _text(observation.get("source_bond_order_code"), "dictionary bond order")
        _require(
            _raw_bond_exists(bond_rows, component=component, atom_ids=atom_ids, value_order=order),
            "declared component dictionary bond differs from raw mmCIF",
        )
        checked += 1
    for observation in modeled_inventory:
        indices = _array(observation.get("modeled_instance_indices"), "modeled instance indices")
        _require(indices == list(range(len(atom_sets))), "modeled atom inventory coverage differs")
        omitted = _array(observation.get("omitted_atom_ids"), "omitted atom IDs")
        _require(
            all(
                isinstance(atom, str)
                and atom in dictionary_atoms
                and all(atom not in atoms for atoms in atom_sets)
                for atom in omitted
            ),
            "declared omitted atom is not a dictionary atom absent from every modeled instance",
        )
        checked += 1

    # Older v3 rows keep bond endpoints in a hash-bound locator rather than the
    # chemical observation.  Verify every such exact locator against the raw table.
    excerpt = _object(annotation.get("projection_excerpt"), "projection excerpt")
    locators = _array(excerpt.get("locators"), "projection locators")
    for locator in locators:
        values = locator.get("extracted_values") if isinstance(locator, dict) else None
        if not isinstance(values, dict) or not {
            "component_id",
            "atom_id_1",
            "atom_id_2",
            "value_order",
        } <= set(values):
            continue
        _require(
            _raw_bond_exists(
                bond_rows,
                component=values["component_id"],
                atom_ids=[values["atom_id_1"], values["atom_id_2"]],
                value_order=values["value_order"],
            ),
            "projection bond locator differs from raw mmCIF",
        )
        checked += 1

    if entity.get("state_kind") == "protein_ligand_covalent_adduct":
        attachments = _array(claim.get("protein_attachments"), "protein attachments")
        attached_atoms = {row["ligand_endpoint"]["atom_name"] for row in attachments}
        raw_conflicts: set[tuple[str, str, str]] = set()
        for row in bond_rows:
            if row.get("comp_id") != component:
                continue
            atom1, atom2 = row.get("atom_id_1"), row.get("atom_id_2")
            if atom1 in attached_atoms and all(atom2 not in atoms for atoms in atom_sets):
                raw_conflicts.add((atom1, atom2, row.get("value_order", "")))
            elif atom2 in attached_atoms and all(atom1 not in atoms for atoms in atom_sets):
                raw_conflicts.add((atom1, atom2, row.get("value_order", "")))
        declared_conflicts = {
            (
                row["source_atom_ids"][0],
                row["source_atom_ids"][1],
                row["source_bond_order_code"],
            )
            for row in typed_dictionary
        }
        _require(
            raw_conflicts == declared_conflicts,
            "raw dictionary/model discrepancy differs from the declared reconciliation",
        )
        reconciliation = _object(claim.get("chemical_reconciliation"), "chemical reconciliation")
        _require(
            (not raw_conflicts and reconciliation.get("status") == "source_scopes_separated")
            or (
                raw_conflicts
                and reconciliation.get("status")
                == "unresolved_component_dictionary_vs_bound_instance_and_connection"
            ),
            "chemical reconciliation status differs from raw dictionary/model facts",
        )
    return checked


def _audit_annotation(
    annotation: dict[str, Any],
    bindings: dict[str, dict[str, Any]],
    repo_root: Path,
) -> dict[str, Any]:
    annotation_id = _text(annotation.get("annotation_id"), "annotation ID")
    claim = _object(annotation.get("claim"), f"{annotation_id} claim")
    binding = _structure_binding(annotation, bindings)
    path = _safe_bound_path(binding, repo_root)
    try:
        cif_text = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeError as exc:
        raise ValueError(f"{annotation_id} primary structure is not UTF-8") from exc
    tables = _parse_mmcif_categories(cif_text)
    entry_rows = tables["_entry"]
    _require(len(entry_rows) == 1 and "id" in entry_rows[0], "mmCIF entry identity is missing")
    structure = _object(claim.get("structure_context"), "structure context")
    _require(entry_rows[0]["id"].upper() == structure.get("pdb_id"), "mmCIF entry identity differs")

    _audit_component_identity(claim, tables)
    _audit_protein_context(claim, tables)
    raw_instances, atom_sets = _derive_instances(claim, tables)
    _require(
        raw_instances == claim.get("structure_instances"),
        f"{annotation_id} structure instances differ from raw mmCIF",
    )
    inventory_rows = _audit_connection_inventory(annotation, tables)
    if claim["observed_entity"].get("state_kind") == "protein_ligand_covalent_adduct":
        attachment_rows = _audit_attachments(claim, tables)
    else:
        attachment_rows = 0
    bond_checks = _audit_declared_bonds_and_atoms(annotation, atom_sets, tables)
    return {
        "annotation_id": annotation_id,
        "pdb_id": structure["pdb_id"],
        "source_sha256": binding["sha256"],
        "structure_instance_count": len(raw_instances),
        "connection_inventory_row_count": inventory_rows,
        "attachment_count": attachment_rows,
        "bond_and_atom_check_count": bond_checks,
    }


def audit_primary_structure_evidence(
    sidecar: dict[str, Any],
    repo_root: str | Path,
) -> dict[str, Any]:
    """Recheck declared observed-state structure facts against hash-bound mmCIF.

    Call this only after ``validate_primary_evidence`` has validated the sidecar,
    bundle binding, projection equality, and review pin.  This function repeats
    the direct source-file hash check before parsing, then audits only factual
    deposited rows used by ``primary_observed_state_context`` annotations.
    """

    sidecar = _object(sidecar, "primary-evidence sidecar")
    root = Path(repo_root).resolve()
    _require(root.is_dir(), "repo_root is not a directory")
    binding_rows = _array(sidecar.get("source_bindings"), "source bindings")
    bindings: dict[str, dict[str, Any]] = {}
    for index, raw_binding in enumerate(binding_rows):
        binding = _object(raw_binding, f"source binding {index}")
        binding_id = _text(binding.get("binding_id"), f"source binding {index} ID")
        _require(binding_id not in bindings, "source binding IDs repeat")
        bindings[binding_id] = binding
    annotations = [
        _object(item, "annotation")
        for item in _array(sidecar.get("annotations"), "annotations")
        if isinstance(item, dict)
        and item.get("annotation_kind") == "primary_observed_state_context"
    ]
    rows = [_audit_annotation(annotation, bindings, root) for annotation in annotations]
    _require(rows, "sidecar has no primary observed-state contexts to audit")
    return {
        "schema_version": SOURCE_AUDIT_SCHEMA_VERSION,
        "annotation_count": len(rows),
        "structure_count": len({row["pdb_id"] for row in rows}),
        "annotations": rows,
        "scope": (
            "hash-bound deposited mmCIF rows only; prose, chemistry, curated mappings, "
            "source steps, and mechanism applicability remain unaudited"
        ),
    }
