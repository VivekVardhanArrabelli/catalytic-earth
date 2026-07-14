"""Strict Atlas-3 mechanism records, local SQLite materialization, and query result."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from typing import Any


KERNEL_SCHEMA_VERSION = "catalytic-earth.atlas3-kernel.v1"
RECORD_SCHEMA_VERSION = "catalytic-earth.mechanism-record.v2"
COMPILER_VERSION = "catalytic-earth.atlas3-compiler.v1"
RUNTIME_SCHEMA_VERSION = "catalytic-earth.atlas3-runtime-result.v1"
EXPECTED_CASE_IDS = {
    "atlas3.mcm-pfre.radical",
    "atlas3.mnsod-ecoli.redox",
    "atlas3.tem1-ecoli.covalent",
}
EXPECTED_CASE_BINDINGS = {
    "atlas3.mcm-pfre.radical": {"ec_number": "5.4.99.2", "rhea_record_id": "RHEA:22888"},
    "atlas3.mnsod-ecoli.redox": {"ec_number": "1.15.1.1", "rhea_record_id": "RHEA:20696"},
    "atlas3.tem1-ecoli.covalent": {"ec_number": "3.5.2.6", "rhea_record_id": "RHEA:20401"},
}
OBJECT_TIERS = {
    "net_reaction": 0,
    "source_mechanism": 1,
    "mechanism_hypothesis": 2,
}
OBJECT_STATUSES = {
    "net_reaction": {"source_assertion"},
    "source_mechanism": {
        "curated_source_proposal",
        "abstained_no_direct_source_mechanism",
    },
    "mechanism_hypothesis": {"bounded_hypothesis"},
}
KERNEL_FIELDS = {
    "schema_version",
    "compiler_version",
    "selection_sha256",
    "source_snapshot_set_sha256",
    "compilation_spec_sha256",
    "source_manifest_retrieved_at",
    "case_count",
    "record_count",
    "records",
    "claim_boundary",
}
RECORD_FIELDS = {
    "schema_version",
    "record_id",
    "case_id",
    "object_type",
    "evidence_tier",
    "label",
    "fixture_only",
    "status",
    "biological_scope",
    "reaction",
    "mechanism_steps",
    "sites",
    "evidence",
    "counterevidence",
    "uncertainties",
    "claim_boundary",
    "provenance",
}
SCOPE_FIELDS = {
    "case_label",
    "organism",
    "ec_number",
    "uniprot_ids",
    "pdb_ids",
    "assay_candidate",
}
REACTION_FIELDS = {
    "source_id",
    "source_record_id",
    "directionality",
    "equation",
    "participants",
}
PARTICIPANT_FIELDS = {"chebi_id", "name"}
STEP_FIELDS = {
    "step_id",
    "order",
    "summary",
    "transformation",
    "catalyst_site_ids",
    "evidence_ids",
    "confidence",
    "source_step_id",
}
SITE_FIELDS = {
    "site_id",
    "uniprot_id",
    "residue_name",
    "sequence_position",
    "numbering_system",
    "roles",
    "pdb_mapping",
    "evidence_ids",
    "mapping_status",
    "notes",
}
PDB_MAPPING_FIELDS = {
    "pdb_id",
    "chain_ids",
    "author_position",
    "label_position",
    "numbering_note",
}
EVIDENCE_FIELDS = {
    "evidence_id",
    "source_id",
    "source_record_id",
    "evidence_role",
    "applicability",
    "uri",
    "retrieval_status",
    "snapshot_sha256",
}
COUNTEREVIDENCE_FIELDS = {
    "counterevidence_id",
    "summary",
    "evidence_ids",
    "effect",
    "disposition",
}
UNCERTAINTY_FIELDS = {"uncertainty_id", "summary", "status", "abstention"}
CLAIM_BOUNDARY_FIELDS = {"supports", "does_not_support"}
PROVENANCE_FIELDS = {
    "selection_sha256",
    "source_snapshot_set_sha256",
    "compilation_spec_sha256",
    "compiler_version",
}


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _exact_keys(value: Any, expected: set[str], context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{context} keys differ; missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )
    return value


def _nonempty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must be a non-empty string")
    return value


def _string_list(value: Any, context: str, *, allow_empty: bool = True) -> list[str]:
    if (
        not isinstance(value, list)
        or (not allow_empty and not value)
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        qualifier = "non-empty " if not allow_empty else ""
        raise ValueError(f"{context} must be a {qualifier}list of non-empty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{context} contains duplicates")
    return value


def _validate_claim_boundary(value: Any, context: str) -> None:
    boundary = _exact_keys(value, CLAIM_BOUNDARY_FIELDS, context)
    _string_list(boundary["supports"], f"{context}.supports", allow_empty=False)
    _string_list(
        boundary["does_not_support"],
        f"{context}.does_not_support",
        allow_empty=False,
    )


def _validate_reaction(value: Any, context: str) -> None:
    reaction = _exact_keys(value, REACTION_FIELDS, context)
    if reaction["source_id"] != "Rhea":
        raise ValueError(f"{context}.source_id must be Rhea")
    _nonempty_string(reaction["source_record_id"], f"{context}.source_record_id")
    if reaction["directionality"] != "undirected":
        raise ValueError(f"{context}.directionality must preserve the undirected Rhea record")
    _nonempty_string(reaction["equation"], f"{context}.equation")
    participants = reaction["participants"]
    if not isinstance(participants, list) or not participants:
        raise ValueError(f"{context}.participants must be non-empty")
    identifiers: list[str] = []
    for index, raw in enumerate(participants):
        participant = _exact_keys(
            raw, PARTICIPANT_FIELDS, f"{context}.participants[{index}]"
        )
        identifier = _nonempty_string(
            participant["chebi_id"], f"{context}.participants[{index}].chebi_id"
        )
        if not identifier.startswith("CHEBI:"):
            raise ValueError(f"{context}.participants[{index}] has a non-ChEBI identifier")
        _nonempty_string(participant["name"], f"{context}.participants[{index}].name")
        identifiers.append(identifier)
    if len(identifiers) != len(set(identifiers)):
        raise ValueError(f"{context}.participants repeats an identifier")


def _validate_record(
    value: Any,
    index: int,
    *,
    wrapper: dict[str, Any],
    manifest_records: dict[tuple[str, str], dict[str, Any]] | None,
) -> None:
    context = f"kernel.records[{index}]"
    record = _exact_keys(value, RECORD_FIELDS, context)
    if record["schema_version"] != RECORD_SCHEMA_VERSION:
        raise ValueError(f"{context}.schema_version differs")
    _nonempty_string(record["record_id"], f"{context}.record_id")
    if record["case_id"] not in EXPECTED_CASE_IDS:
        raise ValueError(f"{context}.case_id is outside the frozen Atlas-3 set")
    object_type = record["object_type"]
    if object_type not in OBJECT_TIERS:
        raise ValueError(f"{context}.object_type is unsupported")
    if record["evidence_tier"] != OBJECT_TIERS[object_type]:
        raise ValueError(f"{context}.evidence_tier differs from its object type")
    if record["status"] not in OBJECT_STATUSES[object_type]:
        raise ValueError(f"{context}.status differs from its object type")
    _nonempty_string(record["label"], f"{context}.label")
    if record["fixture_only"] is not False:
        raise ValueError(f"{context} cannot be a fixture")

    scope = _exact_keys(record["biological_scope"], SCOPE_FIELDS, f"{context}.biological_scope")
    for field in ("case_label", "organism", "ec_number"):
        _nonempty_string(scope[field], f"{context}.biological_scope.{field}")
    _string_list(
        scope["uniprot_ids"], f"{context}.biological_scope.uniprot_ids", allow_empty=False
    )
    _string_list(scope["pdb_ids"], f"{context}.biological_scope.pdb_ids", allow_empty=False)
    if not isinstance(scope["assay_candidate"], bool):
        raise ValueError(f"{context}.biological_scope.assay_candidate must be boolean")
    _validate_reaction(record["reaction"], f"{context}.reaction")

    evidence = record["evidence"]
    if not isinstance(evidence, list) or not evidence:
        raise ValueError(f"{context}.evidence must be non-empty")
    evidence_ids: set[str] = set()
    for evidence_index, raw in enumerate(evidence):
        evidence_context = f"{context}.evidence[{evidence_index}]"
        item = _exact_keys(raw, EVIDENCE_FIELDS, evidence_context)
        evidence_id = _nonempty_string(item["evidence_id"], f"{evidence_context}.evidence_id")
        if evidence_id in evidence_ids:
            raise ValueError(f"{context}.evidence repeats {evidence_id}")
        evidence_ids.add(evidence_id)
        for field in (
            "source_id",
            "source_record_id",
            "evidence_role",
            "applicability",
            "uri",
            "retrieval_status",
        ):
            _nonempty_string(item[field], f"{evidence_context}.{field}")
        digest = item["snapshot_sha256"]
        if digest is not None and (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise ValueError(f"{evidence_context}.snapshot_sha256 must be null or lowercase SHA-256")
        if manifest_records is not None:
            key = item["source_id"], item["source_record_id"]
            manifest = manifest_records.get(key)
            if manifest is None:
                raise ValueError(f"{evidence_context} is absent from the source manifest")
            expected = {
                "source_id": manifest["source_id"],
                "source_record_id": manifest["record_id"],
                "evidence_role": manifest["evidence_role"],
                "applicability": manifest["applicability"],
                "uri": manifest["uri"],
                "retrieval_status": manifest["retrieval_status"],
                "snapshot_sha256": manifest["snapshot_sha256"],
            }
            actual = {key_name: item[key_name] for key_name in expected}
            if actual != expected:
                raise ValueError(f"{evidence_context} differs from the source manifest")

    sites = record["sites"]
    if not isinstance(sites, list):
        raise ValueError(f"{context}.sites must be a list")
    site_ids: set[str] = set()
    for site_index, raw in enumerate(sites):
        site_context = f"{context}.sites[{site_index}]"
        site = _exact_keys(raw, SITE_FIELDS, site_context)
        site_id = _nonempty_string(site["site_id"], f"{site_context}.site_id")
        if site_id in site_ids:
            raise ValueError(f"{context}.sites repeats {site_id}")
        site_ids.add(site_id)
        for field in ("uniprot_id", "residue_name", "numbering_system", "mapping_status", "notes"):
            _nonempty_string(site[field], f"{site_context}.{field}")
        if not isinstance(site["sequence_position"], int) or isinstance(
            site["sequence_position"], bool
        ) or site["sequence_position"] <= 0:
            raise ValueError(f"{site_context}.sequence_position must be a positive integer")
        _string_list(site["roles"], f"{site_context}.roles", allow_empty=False)
        site_evidence = _string_list(
            site["evidence_ids"], f"{site_context}.evidence_ids", allow_empty=False
        )
        if not set(site_evidence).issubset(evidence_ids):
            raise ValueError(f"{site_context}.evidence_ids do not resolve in the record")
        mapping = _exact_keys(
            site["pdb_mapping"], PDB_MAPPING_FIELDS, f"{site_context}.pdb_mapping"
        )
        _nonempty_string(mapping["pdb_id"], f"{site_context}.pdb_mapping.pdb_id")
        _string_list(
            mapping["chain_ids"],
            f"{site_context}.pdb_mapping.chain_ids",
            allow_empty=False,
        )
        for field in ("author_position", "label_position"):
            if not isinstance(mapping[field], int) or isinstance(mapping[field], bool) or mapping[field] <= 0:
                raise ValueError(f"{site_context}.pdb_mapping.{field} must be positive")
        _nonempty_string(
            mapping["numbering_note"], f"{site_context}.pdb_mapping.numbering_note"
        )

    steps = record["mechanism_steps"]
    if not isinstance(steps, list):
        raise ValueError(f"{context}.mechanism_steps must be a list")
    step_ids: set[str] = set()
    for step_index, raw in enumerate(steps):
        step_context = f"{context}.mechanism_steps[{step_index}]"
        step = _exact_keys(raw, STEP_FIELDS, step_context)
        step_id = _nonempty_string(step["step_id"], f"{step_context}.step_id")
        if step_id in step_ids:
            raise ValueError(f"{context}.mechanism_steps repeats {step_id}")
        step_ids.add(step_id)
        if step["order"] != step_index + 1:
            raise ValueError(f"{step_context}.order must be contiguous and one-based")
        for field in ("summary", "transformation", "confidence"):
            _nonempty_string(step[field], f"{step_context}.{field}")
        if step["confidence"] not in {
            "source_curated",
            "supported_bounded",
            "plausible_unresolved",
        }:
            raise ValueError(f"{step_context}.confidence is unsupported")
        catalysts = _string_list(step["catalyst_site_ids"], f"{step_context}.catalyst_site_ids")
        if not set(catalysts).issubset(site_ids):
            raise ValueError(f"{step_context}.catalyst_site_ids do not resolve in the record")
        step_evidence = _string_list(
            step["evidence_ids"], f"{step_context}.evidence_ids", allow_empty=False
        )
        if not set(step_evidence).issubset(evidence_ids):
            raise ValueError(f"{step_context}.evidence_ids do not resolve in the record")
        if step["source_step_id"] is not None and (
            not isinstance(step["source_step_id"], int)
            or isinstance(step["source_step_id"], bool)
            or step["source_step_id"] <= 0
        ):
            raise ValueError(f"{step_context}.source_step_id must be null or positive")

    counterevidence = record["counterevidence"]
    if not isinstance(counterevidence, list):
        raise ValueError(f"{context}.counterevidence must be a list")
    counter_ids: set[str] = set()
    for counter_index, raw in enumerate(counterevidence):
        counter_context = f"{context}.counterevidence[{counter_index}]"
        counter = _exact_keys(raw, COUNTEREVIDENCE_FIELDS, counter_context)
        counter_id = _nonempty_string(
            counter["counterevidence_id"], f"{counter_context}.counterevidence_id"
        )
        if counter_id in counter_ids:
            raise ValueError(f"{context}.counterevidence repeats {counter_id}")
        counter_ids.add(counter_id)
        for field in ("summary", "effect", "disposition"):
            _nonempty_string(counter[field], f"{counter_context}.{field}")
        counter_evidence = _string_list(
            counter["evidence_ids"], f"{counter_context}.evidence_ids", allow_empty=False
        )
        if not set(counter_evidence).issubset(evidence_ids):
            raise ValueError(f"{counter_context}.evidence_ids do not resolve in the record")

    uncertainties = record["uncertainties"]
    if not isinstance(uncertainties, list):
        raise ValueError(f"{context}.uncertainties must be a list")
    uncertainty_ids: set[str] = set()
    for uncertainty_index, raw in enumerate(uncertainties):
        uncertainty_context = f"{context}.uncertainties[{uncertainty_index}]"
        uncertainty = _exact_keys(raw, UNCERTAINTY_FIELDS, uncertainty_context)
        uncertainty_id = _nonempty_string(
            uncertainty["uncertainty_id"], f"{uncertainty_context}.uncertainty_id"
        )
        if uncertainty_id in uncertainty_ids:
            raise ValueError(f"{context}.uncertainties repeats {uncertainty_id}")
        uncertainty_ids.add(uncertainty_id)
        for field in ("summary", "abstention"):
            _nonempty_string(uncertainty[field], f"{uncertainty_context}.{field}")
        if uncertainty["status"] != "open":
            raise ValueError(f"{uncertainty_context}.status must remain open")

    _validate_claim_boundary(record["claim_boundary"], f"{context}.claim_boundary")
    provenance = _exact_keys(record["provenance"], PROVENANCE_FIELDS, f"{context}.provenance")
    expected_provenance = {
        "selection_sha256": wrapper["selection_sha256"],
        "source_snapshot_set_sha256": wrapper["source_snapshot_set_sha256"],
        "compilation_spec_sha256": wrapper["compilation_spec_sha256"],
        "compiler_version": wrapper["compiler_version"],
    }
    if provenance != expected_provenance:
        raise ValueError(f"{context}.provenance differs from the kernel wrapper")

    if object_type == "net_reaction" and (steps or sites):
        raise ValueError(f"{context} must not fabricate mechanism steps or sites at Tier 0")
    if record["status"] == "abstained_no_direct_source_mechanism" and (steps or sites):
        raise ValueError(f"{context} must remain empty when the source mechanism is absent")
    if object_type == "mechanism_hypothesis" and (not steps or not sites or not uncertainties):
        raise ValueError(f"{context} requires steps, grounded sites, and open uncertainty")


def validate_atlas3_kernel(
    value: Any,
    *,
    selection: dict[str, Any] | None = None,
    source_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate the complete nine-object kernel and its frozen provenance bindings."""
    kernel = _exact_keys(value, KERNEL_FIELDS, "kernel")
    if kernel["schema_version"] != KERNEL_SCHEMA_VERSION:
        raise ValueError("unsupported Atlas-3 kernel schema")
    if kernel["compiler_version"] != COMPILER_VERSION:
        raise ValueError("unsupported Atlas-3 compiler version")
    for field in (
        "selection_sha256",
        "source_snapshot_set_sha256",
        "compilation_spec_sha256",
    ):
        digest = kernel[field]
        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise ValueError(f"kernel.{field} must be a lowercase SHA-256")
    _nonempty_string(kernel["source_manifest_retrieved_at"], "kernel.source_manifest_retrieved_at")
    if not kernel["source_manifest_retrieved_at"].endswith("Z"):
        raise ValueError("kernel.source_manifest_retrieved_at must be UTC")
    if kernel["case_count"] != 3 or kernel["record_count"] != 9:
        raise ValueError("Atlas-3 kernel must contain exactly three cases and nine objects")
    _validate_claim_boundary(kernel["claim_boundary"], "kernel.claim_boundary")

    manifest_records: dict[tuple[str, str], dict[str, Any]] | None = None
    if source_manifest is not None:
        if kernel["source_snapshot_set_sha256"] != source_manifest.get("snapshot_set_sha256"):
            raise ValueError("kernel is not bound to the checked source snapshot set")
        if kernel["selection_sha256"] != source_manifest.get("selection_sha256"):
            raise ValueError("kernel/source manifest selection bindings differ")
        if kernel["source_manifest_retrieved_at"] != source_manifest.get("retrieved_at"):
            raise ValueError("kernel/source manifest retrieval times differ")
        manifest_records = {
            (record["source_id"], record["record_id"]): record
            for record in source_manifest.get("records", [])
        }

    records = kernel["records"]
    if not isinstance(records, list) or len(records) != 9:
        raise ValueError("kernel.records must contain nine objects")
    for index, record in enumerate(records):
        _validate_record(
            record,
            index,
            wrapper=kernel,
            manifest_records=manifest_records,
        )
    record_ids = [record["record_id"] for record in records]
    if len(record_ids) != len(set(record_ids)):
        raise ValueError("kernel record IDs must be unique")

    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_case[record["case_id"]].append(record)
    if set(by_case) != EXPECTED_CASE_IDS:
        raise ValueError("kernel case set differs from the frozen Atlas-3 selection")
    for case_id, case_records in by_case.items():
        objects = {record["object_type"]: record for record in case_records}
        if len(case_records) != 3 or set(objects) != set(OBJECT_TIERS):
            raise ValueError(f"{case_id} must have exactly one Tier 0, Tier 1, and Tier 2 object")
        reactions = [record["reaction"] for record in case_records]
        if any(reaction != reactions[0] for reaction in reactions[1:]):
            raise ValueError(f"{case_id} records disagree on the frozen net reaction")
        scopes = [record["biological_scope"] for record in case_records]
        if any(scope != scopes[0] for scope in scopes[1:]):
            raise ValueError(f"{case_id} records disagree on biological scope")
        binding = EXPECTED_CASE_BINDINGS[case_id]
        if scopes[0]["ec_number"] != binding["ec_number"]:
            raise ValueError(f"{case_id} EC number differs from the frozen kernel binding")
        if reactions[0]["source_record_id"] != binding["rhea_record_id"]:
            raise ValueError(f"{case_id} Rhea record differs from the frozen kernel binding")
        if not objects["mechanism_hypothesis"]["counterevidence"]:
            raise ValueError(f"{case_id} Tier-2 hypothesis must preserve counterevidence")

    mnsod_source = next(
        record
        for record in by_case["atlas3.mnsod-ecoli.redox"]
        if record["object_type"] == "source_mechanism"
    )
    if mnsod_source["status"] != "abstained_no_direct_source_mechanism":
        raise ValueError("MnSOD source mechanism must abstain from Cu/Zn same-EC transfer")
    for case_id in EXPECTED_CASE_IDS - {"atlas3.mnsod-ecoli.redox"}:
        source_record = next(
            record for record in by_case[case_id] if record["object_type"] == "source_mechanism"
        )
        if source_record["status"] != "curated_source_proposal":
            raise ValueError(f"{case_id} direct M-CSA source proposal is missing")

    if selection is not None:
        from .atlas_selection import validate_atlas3_selection

        selection_summary = validate_atlas3_selection(selection)
        if kernel["selection_sha256"] != selection_summary["selection_sha256"]:
            raise ValueError("kernel is not bound to the frozen Atlas-3 selection")
        selected_cases = {case["case_id"]: case for case in selection["cases"]}
        for case_id, case_records in by_case.items():
            selected = selected_cases[case_id]
            scope = case_records[0]["biological_scope"]
            direct_uniprot = sorted(
                handle["record_id"]
                for handle in selected["source_handles"]
                if handle["source_id"] == "UniProtKB" and handle["applicability"] == "direct"
            )
            direct_pdb = sorted(
                handle["record_id"]
                for handle in selected["source_handles"]
                if handle["source_id"] == "PDB" and handle["applicability"] == "direct"
            )
            if scope != {
                "case_label": selected["label"],
                "organism": selected["organism"],
                "ec_number": EXPECTED_CASE_BINDINGS[case_id]["ec_number"],
                "uniprot_ids": direct_uniprot,
                "pdb_ids": direct_pdb,
                "assay_candidate": selected["assay_candidate"],
            }:
                raise ValueError(f"{case_id} scope differs from the frozen selection")
            hypothesis = next(
                record
                for record in case_records
                if record["object_type"] == "mechanism_hypothesis"
            )
            if hypothesis["record_id"] != selected["target_record_id"]:
                raise ValueError(f"{case_id} hypothesis ID differs from the frozen target")
            if sorted(
                participant["chebi_id"] for participant in hypothesis["reaction"]["participants"]
            ) != sorted(selected["reaction_participant_ids"]):
                raise ValueError(f"{case_id} reaction participants differ from selection")

    return {
        "schema_version": KERNEL_SCHEMA_VERSION,
        "case_count": 3,
        "record_count": 9,
        "kernel_sha256": canonical_sha256(kernel),
        "object_type_counts": dict(sorted(Counter(record["object_type"] for record in records).items())),
        "evidence_tier_counts": dict(
            sorted(Counter(str(record["evidence_tier"]) for record in records).items())
        ),
    }


def materialize_atlas3_sqlite(kernel: dict[str, Any]) -> sqlite3.Connection:
    """Materialize the nine typed objects into an in-memory, dependency-free database."""
    validate_atlas3_kernel(kernel)
    connection = sqlite3.connect(":memory:")
    connection.executescript(
        """
        CREATE TABLE cases (
            case_id TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            organism TEXT NOT NULL,
            ec_number TEXT NOT NULL,
            assay_candidate INTEGER NOT NULL,
            key_abstention TEXT NOT NULL
        );
        CREATE TABLE records (
            record_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            object_type TEXT NOT NULL,
            evidence_tier INTEGER NOT NULL,
            status TEXT NOT NULL,
            step_count INTEGER NOT NULL,
            site_count INTEGER NOT NULL
        );
        CREATE TABLE evidence (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            evidence_id TEXT NOT NULL,
            applicability TEXT NOT NULL,
            PRIMARY KEY (record_id, evidence_id)
        );
        CREATE TABLE uncertainties (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            uncertainty_id TEXT NOT NULL,
            status TEXT NOT NULL,
            abstention TEXT NOT NULL,
            PRIMARY KEY (record_id, uncertainty_id)
        );
        CREATE TABLE counterevidence (
            record_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            counterevidence_id TEXT NOT NULL,
            effect TEXT NOT NULL,
            PRIMARY KEY (record_id, counterevidence_id)
        );
        """
    )
    records_by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in kernel["records"]:
        records_by_case[record["case_id"]].append(record)
    for case_id in sorted(records_by_case):
        hypothesis = next(
            record
            for record in records_by_case[case_id]
            if record["object_type"] == "mechanism_hypothesis"
        )
        scope = hypothesis["biological_scope"]
        connection.execute(
            "INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?)",
            (
                case_id,
                scope["case_label"],
                scope["organism"],
                scope["ec_number"],
                int(scope["assay_candidate"]),
                hypothesis["uncertainties"][0]["abstention"],
            ),
        )
    for record in kernel["records"]:
        connection.execute(
            "INSERT INTO records VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                record["record_id"],
                record["case_id"],
                record["object_type"],
                record["evidence_tier"],
                record["status"],
                len(record["mechanism_steps"]),
                len(record["sites"]),
            ),
        )
        connection.executemany(
            "INSERT INTO evidence VALUES (?, ?, ?, ?)",
            [
                (
                    record["record_id"],
                    record["case_id"],
                    evidence["evidence_id"],
                    evidence["applicability"],
                )
                for evidence in record["evidence"]
            ],
        )
        connection.executemany(
            "INSERT INTO uncertainties VALUES (?, ?, ?, ?, ?)",
            [
                (
                    record["record_id"],
                    record["case_id"],
                    uncertainty["uncertainty_id"],
                    uncertainty["status"],
                    uncertainty["abstention"],
                )
                for uncertainty in record["uncertainties"]
            ],
        )
        connection.executemany(
            "INSERT INTO counterevidence VALUES (?, ?, ?, ?)",
            [
                (
                    record["record_id"],
                    record["case_id"],
                    counter["counterevidence_id"],
                    counter["effect"],
                )
                for counter in record["counterevidence"]
            ],
        )
    connection.commit()
    return connection


def run_atlas3_query(kernel: dict[str, Any], query_sql: str) -> list[dict[str, Any]]:
    if not isinstance(query_sql, str) or not query_sql.strip():
        raise ValueError("Atlas-3 query must be non-empty SQL")
    connection = materialize_atlas3_sqlite(kernel)
    try:
        cursor = connection.execute(query_sql)
        columns = [description[0] for description in cursor.description or []]
        return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]
    finally:
        connection.close()


def build_atlas3_runtime_result(
    kernel: dict[str, Any], query_sql: str
) -> dict[str, Any]:
    summary = validate_atlas3_kernel(kernel)
    rows = run_atlas3_query(kernel, query_sql)
    return {
        "schema_version": RUNTIME_SCHEMA_VERSION,
        "kernel_schema_version": KERNEL_SCHEMA_VERSION,
        "record_schema_version": RECORD_SCHEMA_VERSION,
        "kernel_sha256": summary["kernel_sha256"],
        "query_sha256": hashlib.sha256(query_sql.encode("utf-8")).hexdigest(),
        "case_count": summary["case_count"],
        "record_count": summary["record_count"],
        "object_type_counts": summary["object_type_counts"],
        "evidence_tier_counts": summary["evidence_tier_counts"],
        "source_mechanism_abstention_count": sum(
            record["status"] == "abstained_no_direct_source_mechanism"
            for record in kernel["records"]
        ),
        "open_uncertainty_count": sum(
            len(record["uncertainties"]) for record in kernel["records"]
        ),
        "query_rows": rows,
        "network_used": False,
        "external_binary_used": False,
        "accelerator_used": False,
    }
