from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .geometry_head import (
    SECONDARY_PREFIX,
    _evaluate_head,
    _geometry_feature_vector,
    _is_primary_role,
    _split_train_cal,
    _training_label_with_none,
    _wave_masks_by_entry,
)
from .geometry_retrieval import run_geometry_retrieval
from .labels import load_labels
from .structure import (
    atom_position,
    ligand_context_from_atoms,
    missing_position_detail,
    pairwise_distances,
    parse_atom_site_loop,
    pocket_context_from_atoms,
    residue_centroid,
    select_residue_atoms,
)


ALPHAFOLD_CIF_URL = "https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v{version}.cif"
ALPHAFOLD_VERSION_ORDER = (6, 5, 4, 3, 2, 1)
USER_AGENT = "CatalyticEarth/0.0.1 research prototype"
HAND_ROUTER_THRESHOLD = 0.4115


def build_predicted_geometry_robustness_audit(
    *,
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    experimental_geometry_retrieval: dict[str, Any],
    labels: list[Any],
    wave1_audit: dict[str, Any],
    backend: str = "alphafold_db",
    alphafold_version: str = "auto",
    split_assignment: str = "heldout",
    random_state: int = 702,
    cal_fraction: float = 0.2,
    hidden_layer_size: int = 32,
    max_rows: int = 0,
    fetcher: Any | None = None,
) -> dict[str, Any]:
    """Score the frozen geometry stack on predicted structures.

    The predicted-structure path swaps only the coordinate source for selected
    M-CSA rows. It does not edit labels, thresholds, or production scoring, and
    it does not train/calibrate on heldout rows.
    """
    if backend == "esmfold":
        return _blocked_audit(
            blocker="local_esmfold_runtime_or_weights_unavailable",
            detail=(
                "ESMFold inference is not run by this audit unless a local "
                "runtime and weights are already staged. No model-weight "
                "download was attempted. Stage ESMFold PDB/mmCIF files keyed by "
                "current702 sequence_id/accession, or install a local esmfold "
                "runtime, then add that backend as a coordinate supplier."
            ),
            label_manifest=label_manifest,
            split_assignment=split_assignment,
            backend=backend,
        )
    if backend != "alphafold_db":
        return _blocked_audit(
            blocker="unsupported_predicted_structure_backend",
            detail=(
                f"backend={backend!r}; only alphafold_db is implemented without "
                "local model-weight downloads"
            ),
            label_manifest=label_manifest,
            split_assignment=split_assignment,
            backend=backend,
        )

    target_rows, excluded_target_rows = _target_manifest_row_selection(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        split_assignment=split_assignment,
        max_rows=max_rows,
    )
    predicted_geometry = build_alphafold_predicted_geometry_features(
        label_manifest_rows=target_rows,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        alphafold_version=alphafold_version,
        fetcher=fetcher,
    )
    predicted_retrieval = run_geometry_retrieval(predicted_geometry)
    hand_rows = _hand_router_rows(
        target_rows=target_rows,
        predicted_geometry=predicted_geometry,
        predicted_retrieval=predicted_retrieval,
        wave1_audit=wave1_audit,
        threshold=HAND_ROUTER_THRESHOLD,
    )
    hand_metrics = _metrics_with_missing(hand_rows, mask_mode="canonical")
    hand_metrics_wave1 = _metrics_with_missing(hand_rows, mask_mode="wave1_readthrough")
    head_results = _geometry_head_transfer_results(
        label_manifest=label_manifest,
        experimental_geometry_features=experimental_geometry_features,
        experimental_geometry_retrieval=experimental_geometry_retrieval,
        predicted_geometry_features=predicted_geometry,
        predicted_geometry_retrieval=predicted_retrieval,
        wave1_audit=wave1_audit,
        random_state=random_state,
        cal_fraction=cal_fraction,
        hidden_layer_size=hidden_layer_size,
    )
    experimental_reference = (
        wave1_audit.get("geometry_baseline_reexport", {})
        if isinstance(wave1_audit, dict)
        else {}
    )
    experimental_reference_metrics = experimental_reference.get(
        "metrics_canonical_masks", {}
    )
    headline = _headline(
        predicted_hand_metrics=hand_metrics,
        experimental_hand_metrics=experimental_reference_metrics,
        head_results=head_results,
    )
    return {
        "artifact_id": "v3_predicted_geometry_robustness_audit_current702_20260529",
        "schema_version": "predicted_geometry_robustness_audit.v1",
        "created_utc": _utc_now_iso(),
        "status": "complete",
        "guardrails": {
            "label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
            "global_threshold_changed": False,
            "heldout_labels_used_for_fit_or_threshold": False,
            "large_model_downloads_performed": False,
            "coordinate_download_scope": (
                "AlphaFoldDB mmCIF coordinate files fetched transiently by "
                "UniProt accession; raw coordinates are not committed"
            ),
        },
        "scope": {
            "split_assignment": split_assignment,
            "split_manifest_row_count": sum(
                1
                for row in label_manifest.get("rows", [])
                if isinstance(row, dict)
                and row.get("split_assignment") == split_assignment
            ),
            "requested_row_count": len(target_rows),
            "excluded_row_count": len(excluded_target_rows),
            "excluded_role_counts": dict(
                sorted(
                    Counter(
                        str(row.get("benchmark_role") or "unknown")
                        for row in excluded_target_rows
                    ).items()
                )
            ),
            "excluded_rows": excluded_target_rows,
            "backend": backend,
            "alphafold_version": alphafold_version,
            "hand_router_threshold": HAND_ROUTER_THRESHOLD,
            "target_definition": (
                "current702 M-CSA rows in the requested split with existing "
                "experimental geometry evidence and sequence-position mapping"
            ),
        },
        "source_artifacts": {
            "label_manifest": "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json",
            "experimental_geometry_features": "artifacts/v3_geometry_features_1025.json",
            "experimental_geometry_retrieval": "artifacts/v3_geometry_retrieval_1025.json",
            "wave1_2_audit": "artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json",
            "threshold_source": "artifacts/v3_geometry_label_eval_1025_preview_batch.json",
        },
        "predicted_geometry_features": predicted_geometry,
        "predicted_geometry_retrieval": predicted_retrieval,
        "hand_router_on_predicted_geometry": {
            "threshold": HAND_ROUTER_THRESHOLD,
            "metrics_canonical_masks": hand_metrics,
            "metrics_wave1_readthrough_masks": hand_metrics_wave1,
            "per_bin_results": _per_bin_metrics_with_missing(hand_rows),
            "rows": hand_rows,
        },
        "geometry_heads_on_predicted_geometry": head_results,
        "experimental_geometry_reference": {
            "hand_router_metrics_canonical_masks": experimental_reference_metrics,
            "source": "artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json",
        },
        "headline": headline,
    }


def build_alphafold_predicted_geometry_features(
    *,
    label_manifest_rows: list[dict[str, Any]],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    alphafold_version: str = "auto",
    fetcher: Any | None = None,
) -> dict[str, Any]:
    residues_by_entry = _residue_nodes_by_entry(graph)
    experimental_by_entry = {
        str(row.get("entry_id")): row
        for row in experimental_geometry_features.get("entries", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    fetcher = fetcher or fetch_alphafold_cif
    cif_cache: dict[str, dict[str, Any]] = {}
    entries: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, Any]] = []

    for manifest_row in label_manifest_rows:
        entry_id = str(manifest_row.get("entry_id") or "")
        accession = str(manifest_row.get("accession") or manifest_row.get("sequence_id") or "")
        experimental_row = experimental_by_entry.get(entry_id, {})
        residue_nodes = residues_by_entry.get(entry_id, [])
        if not entry_id or not accession:
            entries.append(_failed_predicted_entry(manifest_row, "missing_entry_or_accession"))
            continue
        if accession not in cif_cache:
            try:
                text, meta = fetcher(accession, version=alphafold_version)
                atoms = parse_atom_site_loop(text)
                meta = {
                    **meta,
                    "byte_count": len(text.encode("utf-8")),
                    "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "atom_site_row_count": len(atoms),
                }
                cif_cache[accession] = {"atoms": atoms, "meta": meta}
            except Exception as exc:  # source failures should become artifact evidence
                failure = {
                    "entry_id": entry_id,
                    "accession": accession,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
                fetch_failures.append(failure)
                cif_cache[accession] = {"atoms": [], "meta": {"fetch_error": failure}}
        cached = cif_cache[accession]
        atoms = cached["atoms"]
        if not atoms:
            entries.append(
                _failed_predicted_entry(
                    manifest_row,
                    "predicted_structure_fetch_failed",
                    experimental_row=experimental_row,
                    source_meta=cached.get("meta", {}),
                )
            )
            continue
        entries.append(
            _predicted_entry_from_atoms(
                manifest_row=manifest_row,
                experimental_row=experimental_row,
                residue_nodes=residue_nodes,
                accession=accession,
                atoms=atoms,
                source_meta=cached.get("meta", {}),
            )
        )

    return {
        "metadata": {
            "artifact": "alphafold_predicted_active_site_geometry_features",
            "schema_version": "predicted_geometry_features.v1",
            "source": "AlphaFoldDB mmCIF by current702 UniProt accession",
            "entry_count": len(entries),
            "ok_entry_count": sum(1 for entry in entries if entry.get("status") == "ok"),
            "entries_with_pairwise_geometry": sum(
                1 for entry in entries if entry.get("pairwise_distances_angstrom")
            ),
            "entries_with_proximal_ligands": sum(
                1
                for entry in entries
                if entry.get("ligand_context", {}).get("proximal_ligands")
            ),
            "entries_with_pocket_context": sum(
                1
                for entry in entries
                if entry.get("pocket_context", {}).get("nearby_residue_count", 0) > 0
            ),
            "unique_accession_count": len({entry.get("accession") for entry in entries}),
            "fetch_failure_count": len(fetch_failures),
            "fetch_failures_sample": fetch_failures[:20],
            "mechanism_text_snippets_used": False,
            "entry_names_used_for_score": False,
            "active_site_roles_source": (
                "M-CSA catalytic residue annotations are retained to isolate "
                "coordinate-source degradation; this is not a bare-sequence "
                "active-site localization test"
            ),
        },
        "entries": entries,
    }


def fetch_alphafold_cif(
    accession: str,
    *,
    version: str = "auto",
    timeout: int = 30,
) -> tuple[str, dict[str, Any]]:
    cleaned = accession.strip()
    if not cleaned:
        raise ValueError("accession is required")
    versions = ALPHAFOLD_VERSION_ORDER if version == "auto" else (int(version),)
    errors: list[str] = []
    for candidate_version in versions:
        url = ALPHAFOLD_CIF_URL.format(
            accession=cleaned,
            version=candidate_version,
        )
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8", errors="replace"), {
                    "backend": "alphafold_db",
                    "accession": cleaned,
                    "alphafold_version": candidate_version,
                    "url": url,
                    "http_status": getattr(response, "status", None),
                }
        except HTTPError as exc:
            errors.append(f"v{candidate_version}: HTTP {exc.code}")
        except URLError as exc:
            errors.append(f"v{candidate_version}: {exc.reason}")
    raise RuntimeError(
        f"AlphaFoldDB mmCIF unavailable for {cleaned}; tried {', '.join(errors)}"
    )


def write_predicted_geometry_robustness_audit(
    *,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_features_path: Path,
    experimental_geometry_retrieval_path: Path,
    labels_path: Path,
    wave1_audit_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    backend: str = "alphafold_db",
    alphafold_version: str = "auto",
    split_assignment: str = "heldout",
    random_state: int = 702,
    cal_fraction: float = 0.2,
    hidden_layer_size: int = 32,
    max_rows: int = 0,
) -> dict[str, Any]:
    with label_manifest_path.open("r", encoding="utf-8") as handle:
        label_manifest = json.load(handle)
    with graph_path.open("r", encoding="utf-8") as handle:
        graph = json.load(handle)
    with experimental_geometry_features_path.open("r", encoding="utf-8") as handle:
        experimental_geometry_features = json.load(handle)
    with experimental_geometry_retrieval_path.open("r", encoding="utf-8") as handle:
        experimental_geometry_retrieval = json.load(handle)
    with wave1_audit_path.open("r", encoding="utf-8") as handle:
        wave1_audit = json.load(handle)
    audit = build_predicted_geometry_robustness_audit(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        experimental_geometry_retrieval=experimental_geometry_retrieval,
        labels=load_labels(labels_path),
        wave1_audit=wave1_audit,
        backend=backend,
        alphafold_version=alphafold_version,
        split_assignment=split_assignment,
        random_state=random_state,
        cal_fraction=cal_fraction,
        hidden_layer_size=hidden_layer_size,
        max_rows=max_rows,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_markdown_report(audit), encoding="utf-8")
    return audit


def _target_manifest_row_selection(
    *,
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    split_assignment: str,
    max_rows: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    residues_by_entry = _residue_nodes_by_entry(graph)
    experimental_by_entry = {
        str(row.get("entry_id")): row
        for row in experimental_geometry_features.get("entries", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    rows: list[dict[str, Any]] = []
    excluded_rows: list[dict[str, Any]] = []
    for row in label_manifest.get("rows", []):
        if not isinstance(row, dict):
            continue
        entry_id = str(row.get("entry_id") or "")
        if row.get("split_assignment") != split_assignment:
            continue
        if not entry_id.startswith("m_csa:"):
            excluded_rows.append(_excluded_target_row(row, "not_m_csa_entry"))
            continue
        experimental = experimental_by_entry.get(entry_id)
        if not experimental or experimental.get("status") != "ok":
            excluded_rows.append(
                _excluded_target_row(
                    row,
                    f"experimental_geometry_not_ok:{(experimental or {}).get('status')}",
                )
            )
            continue
        residue_nodes = residues_by_entry.get(entry_id, [])
        accession = str(row.get("accession") or row.get("sequence_id") or "")
        if not _has_reference_sequence_positions(residue_nodes, accession):
            excluded_rows.append(
                _excluded_target_row(row, "missing_accession_compatible_sequence_positions")
            )
            continue
        rows.append(dict(row))
        if max_rows and len(rows) >= max_rows:
            break
    return rows, excluded_rows


def _excluded_target_row(row: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "entry_id": row.get("entry_id"),
        "accession": row.get("accession"),
        "benchmark_role": row.get("benchmark_role"),
        "fingerprint_id": row.get("fingerprint_id")
        or row.get("mechanism_fingerprint_id"),
        "reason": reason,
    }


def _predicted_entry_from_atoms(
    *,
    manifest_row: dict[str, Any],
    experimental_row: dict[str, Any],
    residue_nodes: list[dict[str, Any]],
    accession: str,
    atoms: list[dict[str, Any]],
    source_meta: dict[str, Any],
) -> dict[str, Any]:
    resolved: list[dict[str, Any]] = []
    missing_details: list[dict[str, Any]] = []
    positions = _reference_sequence_positions(residue_nodes, accession)
    for item in positions:
        residue_atoms = select_residue_atoms(
            atoms,
            chain_name=None,
            resid=item.get("resid"),
            code=item.get("code"),
        )
        if not residue_atoms:
            missing_details.append(missing_position_detail(atoms, item))
            continue
        resolved.append(
            {
                "residue_node_id": item.get("residue_node_id"),
                "code": item.get("code"),
                "chain_name": None,
                "resid": item.get("resid"),
                "atom_count": len(residue_atoms),
                "centroid": residue_centroid(residue_atoms),
                "ca": atom_position(residue_atoms, "CA"),
                "roles": item.get("roles", []),
                "sequence_position_uniprot_id": item.get("uniprot_id") or None,
            }
        )
    pairwise = pairwise_distances(resolved)
    status = "ok" if len(resolved) >= 2 else "insufficient_resolved_residues"
    return {
        "entry_id": manifest_row.get("entry_id"),
        "entry_name": None,
        "accession": accession,
        "sequence_id": manifest_row.get("sequence_id"),
        "benchmark_role": manifest_row.get("benchmark_role"),
        "split_assignment": manifest_row.get("split_assignment"),
        "status": status,
        "experimental_pdb_id": experimental_row.get("pdb_id"),
        "pdb_id": f"AF-{accession}-F1-model_v{source_meta.get('alphafold_version')}",
        "predicted_structure_source": source_meta,
        "residue_count": len(residue_nodes),
        "resolved_residue_count": len(resolved),
        "missing_positions": len(positions) - len(resolved),
        "missing_position_details": missing_details,
        "residues": resolved,
        "pairwise_distances_angstrom": pairwise,
        "ligand_context": ligand_context_from_atoms(atoms, resolved),
        "pocket_context": pocket_context_from_atoms(atoms, resolved),
        "mechanism_text_count": 0,
        "mechanism_text_snippets": [],
        "coordinate_swap": {
            "from": "experimental_m_csa_selected_pdb",
            "to": "alphafold_db_uniprot_model",
            "sequence_positions_used": True,
            "structure_positions_used_for_predicted_model": False,
        },
    }


def _failed_predicted_entry(
    manifest_row: dict[str, Any],
    reason: str,
    *,
    experimental_row: dict[str, Any] | None = None,
    source_meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "entry_id": manifest_row.get("entry_id"),
        "entry_name": None,
        "accession": manifest_row.get("accession"),
        "sequence_id": manifest_row.get("sequence_id"),
        "benchmark_role": manifest_row.get("benchmark_role"),
        "split_assignment": manifest_row.get("split_assignment"),
        "status": reason,
        "experimental_pdb_id": (experimental_row or {}).get("pdb_id"),
        "pdb_id": None,
        "predicted_structure_source": source_meta or {},
        "residue_count": 0,
        "resolved_residue_count": 0,
        "missing_positions": 0,
        "missing_position_details": [],
        "residues": [],
        "pairwise_distances_angstrom": [],
        "ligand_context": {
            "distance_cutoff_angstrom": 6.0,
            "proximal_ligands": [],
            "ligand_codes": [],
            "cofactor_families": [],
            "structure_ligands": [],
            "structure_ligand_codes": [],
            "structure_cofactor_families": [],
        },
        "pocket_context": {
            "distance_cutoff_angstrom": 8.0,
            "nearby_residue_count": 0,
            "nearby_residue_sites": [],
            "descriptors": {},
        },
        "mechanism_text_count": 0,
        "mechanism_text_snippets": [],
    }


def _hand_router_rows(
    *,
    target_rows: list[dict[str, Any]],
    predicted_geometry: dict[str, Any],
    predicted_retrieval: dict[str, Any],
    wave1_audit: dict[str, Any],
    threshold: float,
) -> list[dict[str, Any]]:
    geometry_by_entry = {
        str(row.get("entry_id")): row
        for row in predicted_geometry.get("entries", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    retrieval_by_entry = {
        str(row.get("entry_id")): row
        for row in predicted_retrieval.get("results", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    wave_masks = _wave_masks_by_entry(wave1_audit)
    rows: list[dict[str, Any]] = []
    for manifest_row in target_rows:
        entry_id = str(manifest_row.get("entry_id") or "")
        geometry_row = geometry_by_entry.get(entry_id, {})
        retrieval_row = retrieval_by_entry.get(entry_id, {})
        top = retrieval_row.get("top_fingerprints", [])
        top1 = top[0] if top else {}
        top1_id = top1.get("fingerprint_id")
        top1_score = float(top1.get("score", 0.0) or 0.0)
        available = geometry_row.get("status") == "ok"
        abstained = (not available) or top1_score < threshold
        true_fingerprint = manifest_row.get("fingerprint_id") or manifest_row.get(
            "mechanism_fingerprint_id"
        )
        called = None if abstained else top1_id
        masks = wave_masks.get(entry_id, {})
        is_primary = bool(
            masks.get("canonical_primary_support_mask")
            if masks
            else _is_primary_role(manifest_row.get("benchmark_role"))
        )
        exact = called == true_fingerprint if true_fingerprint else called is None
        if is_primary and abstained:
            exact = False
        rows.append(
            {
                "entry_id": entry_id,
                "benchmark_role": manifest_row.get("benchmark_role"),
                "split_assignment": manifest_row.get("split_assignment"),
                "sequence_id": manifest_row.get("sequence_id"),
                "sequence_sha256": manifest_row.get("sequence_sha256"),
                "label_type": manifest_row.get("label_type"),
                "structural_neighborhood_bin": masks.get(
                    "structural_neighborhood_bin", "unbinned"
                ),
                "true_fingerprint_id": true_fingerprint,
                "top1_fingerprint_id": top1_id,
                "top1_score": round(top1_score, 4),
                "called_fingerprint_id": called,
                "abstained": abstained,
                "exact_label_match": exact if available else False,
                "primary_top1_correct_if_applicable": (
                    (called == true_fingerprint)
                    if is_primary and available and not abstained
                    else None
                ),
                "canonical_primary_support_mask": is_primary,
                "canonical_oos_or_secondary_support_mask": bool(
                    masks.get("canonical_oos_or_secondary_support_mask")
                    if masks
                    else not is_primary
                ),
                "wave1_readthrough_primary_support_mask": bool(
                    masks.get("wave1_readthrough_primary_support_mask", is_primary)
                ),
                "wave1_readthrough_nonprimary_or_oos_mask": bool(
                    masks.get("wave1_readthrough_nonprimary_or_oos_mask", not is_primary)
                ),
                "pure_oos_support_mask": true_fingerprint is None,
                "secondary_probe_support_mask": str(
                    manifest_row.get("benchmark_role") or ""
                ).startswith(SECONDARY_PREFIX),
                "predicted_geometry_joined": available,
                "predicted_geometry_status": geometry_row.get("status"),
                "predicted_resolved_residue_count": geometry_row.get(
                    "resolved_residue_count", 0
                ),
                "predicted_missing_positions": geometry_row.get("missing_positions", 0),
                "experimental_pdb_id": geometry_row.get("experimental_pdb_id"),
                "predicted_pdb_id": geometry_row.get("pdb_id"),
            }
        )
    return sorted(rows, key=lambda row: _entry_sort_key(row["entry_id"]))


def _geometry_head_transfer_results(
    *,
    label_manifest: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    experimental_geometry_retrieval: dict[str, Any],
    predicted_geometry_features: dict[str, Any],
    predicted_geometry_retrieval: dict[str, Any],
    wave1_audit: dict[str, Any],
    random_state: int,
    cal_fraction: float,
    hidden_layer_size: int,
) -> dict[str, Any]:
    try:
        from sklearn.exceptions import ConvergenceWarning
        from sklearn.feature_extraction import DictVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.neural_network import MLPClassifier
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
    except Exception as exc:  # pragma: no cover - environment dependent
        return {
            "status": "blocked",
            "blocker": "sklearn_unavailable",
            "detail": f"{type(exc).__name__}: {exc}",
        }

    import warnings

    experimental_rows, experimental_missing = _model_rows(
        label_manifest=label_manifest,
        geometry_features=experimental_geometry_features,
        geometry_retrieval=experimental_geometry_retrieval,
        wave1_audit=wave1_audit,
    )
    predicted_rows, predicted_missing = _model_rows(
        label_manifest=label_manifest,
        geometry_features=predicted_geometry_features,
        geometry_retrieval=predicted_geometry_retrieval,
        wave1_audit=wave1_audit,
        split_assignment_filter="heldout",
    )
    train_source = [
        row
        for row in experimental_rows
        if row.get("split_assignment") == "in_distribution"
        and row.get("geometry_status") == "ok"
    ]
    predicted_heldout = [
        row
        for row in predicted_rows
        if row.get("split_assignment") == "heldout" and row.get("geometry_status") == "ok"
    ]
    train_all, cal_rows = _split_train_cal(
        train_source,
        cal_fraction=cal_fraction,
        random_state=random_state,
        train_test_split=train_test_split,
    )
    train_primary = [row for row in train_all if _is_primary_role(row["benchmark_role"])]
    if not train_primary or not cal_rows or not predicted_heldout:
        return {
            "status": "blocked",
            "blocker": "insufficient_rows_for_predicted_geometry_head_transfer",
            "detail": (
                f"train_primary={len(train_primary)} cal={len(cal_rows)} "
                f"predicted_heldout={len(predicted_heldout)}"
            ),
            "experimental_missing_rows": experimental_missing,
            "predicted_missing_rows": predicted_missing,
        }

    logistic = make_pipeline(
        DictVectorizer(sparse=False),
        StandardScaler(),
        LogisticRegression(max_iter=2000, random_state=random_state),
    )
    mlp_oos_aware = make_pipeline(
        DictVectorizer(sparse=False),
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=(hidden_layer_size,),
            activation="relu",
            alpha=0.001,
            max_iter=2000,
            random_state=random_state,
        ),
    )
    train_x = [row["features"] for row in train_primary]
    train_y = [str(row["true_fingerprint_id"]) for row in train_primary]
    train_all_x = [row["features"] for row in train_all]
    train_all_y = [_training_label_with_none(row) for row in train_all]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ConvergenceWarning)
        logistic.fit(train_x, train_y)
        mlp_oos_aware.fit(train_all_x, train_all_y)

    wave_masks = _wave_masks_by_entry(wave1_audit)
    logistic_result = _evaluate_head(
        track_id="geometry_feature_logistic_experimental_train_predicted_eval",
        display_name="Geometry-feature logistic experimental-train predicted-eval",
        model=logistic,
        cal_rows=cal_rows,
        heldout_rows=predicted_heldout,
        wave_masks=wave_masks,
    )
    mlp_result = _evaluate_head(
        track_id="geometry_feature_mlp_32_oos_aware_experimental_train_predicted_eval",
        display_name=(
            f"Geometry-feature OOS-aware MLP-{hidden_layer_size} "
            "experimental-train predicted-eval"
        ),
        model=mlp_oos_aware,
        cal_rows=cal_rows,
        heldout_rows=predicted_heldout,
        wave_masks=wave_masks,
        abstain_class="__none_of_above__",
    )
    return {
        "status": "complete",
        "protocol": {
            "train_coordinates": "experimental M-CSA/PDB geometry",
            "calibration_coordinates": "experimental in-distribution geometry only",
            "evaluation_coordinates": "AlphaFoldDB predicted heldout geometry only",
            "threshold_policy": (
                "same calibration policy as geometry_nonlinear_head audit; "
                "no predicted-heldout tuning"
            ),
            "random_state": random_state,
            "cal_fraction": cal_fraction,
            "hidden_layer_size": hidden_layer_size,
        },
        "row_counts": {
            "experimental_feature_rows": len(experimental_rows),
            "experimental_missing_rows": experimental_missing,
            "predicted_feature_rows": len(predicted_rows),
            "predicted_missing_rows": predicted_missing,
            "train_all_row_count": len(train_all),
            "train_primary_row_count": len(train_primary),
            "cal_row_count": len(cal_rows),
            "predicted_heldout_available_row_count": len(predicted_heldout),
        },
        "models": {
            "logistic_experimental_train_predicted_eval": logistic_result,
            "mlp_32_oos_aware_experimental_train_predicted_eval": mlp_result,
        },
    }


def _model_rows(
    *,
    label_manifest: dict[str, Any],
    geometry_features: dict[str, Any],
    geometry_retrieval: dict[str, Any],
    wave1_audit: dict[str, Any],
    split_assignment_filter: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    geometry_by_entry = {
        str(row.get("entry_id")): row
        for row in geometry_features.get("entries", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    retrieval_by_entry = {
        str(row.get("entry_id")): row
        for row in geometry_retrieval.get("results", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    wave_masks = _wave_masks_by_entry(wave1_audit)
    rows: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    for manifest_row in label_manifest.get("rows", []):
        if not isinstance(manifest_row, dict):
            continue
        if (
            split_assignment_filter is not None
            and manifest_row.get("split_assignment") != split_assignment_filter
        ):
            continue
        entry_id = str(manifest_row.get("entry_id") or "")
        if not entry_id:
            continue
        geometry_row = geometry_by_entry.get(entry_id)
        if geometry_row is None:
            missing.append({"entry_id": entry_id, "reason": "geometry_features_missing"})
            continue
        retrieval_row = retrieval_by_entry.get(entry_id, {})
        rows.append(
            {
                "entry_id": entry_id,
                "benchmark_role": manifest_row.get("benchmark_role"),
                "split_assignment": manifest_row.get("split_assignment"),
                "true_fingerprint_id": manifest_row.get("fingerprint_id")
                or manifest_row.get("mechanism_fingerprint_id"),
                "features": _geometry_feature_vector(geometry_row, retrieval_row),
                "geometry_status": geometry_row.get("status"),
                "structural_neighborhood_bin": (
                    wave_masks.get(entry_id, {}).get("structural_neighborhood_bin")
                    or "unbinned"
                ),
            }
        )
    return rows, missing


def _metrics_with_missing(
    rows: list[dict[str, Any]],
    *,
    mask_mode: str,
) -> dict[str, Any]:
    if mask_mode == "canonical":
        primary_rows = [row for row in rows if row["canonical_primary_support_mask"]]
        nonprimary_rows = [
            row for row in rows if row["canonical_oos_or_secondary_support_mask"]
        ]
    elif mask_mode == "wave1_readthrough":
        primary_rows = [row for row in rows if row["wave1_readthrough_primary_support_mask"]]
        nonprimary_rows = [
            row for row in rows if row["wave1_readthrough_nonprimary_or_oos_mask"]
        ]
    else:
        primary_rows = [row for row in rows if _is_primary_role(row.get("benchmark_role"))]
        nonprimary_rows = [row for row in rows if row not in primary_rows]
    available_rows = [row for row in rows if row["predicted_geometry_joined"]]
    available_primary = [row for row in primary_rows if row["predicted_geometry_joined"]]
    available_nonprimary = [
        row for row in nonprimary_rows if row["predicted_geometry_joined"]
    ]
    pure_oos_rows = [row for row in available_nonprimary if row["pure_oos_support_mask"]]
    secondary_rows = [
        row for row in available_nonprimary if row["secondary_probe_support_mask"]
    ]
    primary_correct = [
        row
        for row in available_primary
        if not row["abstained"]
        and row["called_fingerprint_id"] == row["true_fingerprint_id"]
    ]
    primary_wrong = [
        row
        for row in available_primary
        if not row["abstained"]
        and row["called_fingerprint_id"] != row["true_fingerprint_id"]
    ]
    nonprimary_fp = [row for row in available_nonprimary if not row["abstained"]]
    pure_oos_fp = [row for row in pure_oos_rows if not row["abstained"]]
    return {
        "row_count": len(rows),
        "available_count": len(available_rows),
        "missing_count": len(rows) - len(available_rows),
        "abstention_count": sum(1 for row in available_rows if row["abstained"]),
        "abstention_rate_available": _rate(
            sum(1 for row in available_rows if row["abstained"]),
            len(available_rows),
        ),
        "exact_label_match_count": sum(
            1 for row in available_rows if row["exact_label_match"]
        ),
        "exact_label_accuracy_available": _rate(
            sum(1 for row in available_rows if row["exact_label_match"]),
            len(available_rows),
        ),
        "primary_support_count": len(primary_rows),
        "primary_available_count": len(available_primary),
        "primary_missing_count": len(primary_rows) - len(available_primary),
        "primary_correct_count": len(primary_correct),
        "primary_abstention_count": sum(
            1 for row in available_primary if row["abstained"]
        ),
        "primary_wrong_nonabstained_count": len(primary_wrong),
        "primary_accuracy_all_rows": _rate(len(primary_correct), len(primary_rows)),
        "primary_accuracy_available": _rate(
            len(primary_correct), len(available_primary)
        ),
        "oos_or_secondary_support_count": len(nonprimary_rows),
        "oos_or_secondary_available_count": len(available_nonprimary),
        "oos_or_secondary_missing_count": len(nonprimary_rows) - len(available_nonprimary),
        "oos_or_secondary_abstention_count": sum(
            1 for row in available_nonprimary if row["abstained"]
        ),
        "oos_or_secondary_false_positive_count": len(nonprimary_fp),
        "oos_or_secondary_false_positive_rate_available": _rate(
            len(nonprimary_fp), len(available_nonprimary)
        ),
        "pure_oos_support_count": len(pure_oos_rows),
        "pure_oos_false_positive_count": len(pure_oos_fp),
        "pure_oos_false_positive_rate_available": _rate(
            len(pure_oos_fp), len(pure_oos_rows)
        ),
        "secondary_probe_support_count": len(secondary_rows),
        "secondary_probe_nonabstained_count": sum(
            1 for row in secondary_rows if not row["abstained"]
        ),
        "secondary_probe_exact_count": sum(
            1 for row in secondary_rows if row["exact_label_match"]
        ),
    }


def _per_bin_metrics_with_missing(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_bin: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_bin[str(row.get("structural_neighborhood_bin") or "unbinned")].append(row)
    return {
        bin_name: {
            "row_ids": [row["entry_id"] for row in bin_rows],
            "metrics": _metrics_with_missing(bin_rows, mask_mode="canonical"),
        }
        for bin_name, bin_rows in sorted(by_bin.items())
    }


def _headline(
    *,
    predicted_hand_metrics: dict[str, Any],
    experimental_hand_metrics: dict[str, Any],
    head_results: dict[str, Any],
) -> dict[str, Any]:
    experimental_primary = experimental_hand_metrics.get("primary_accuracy_available")
    predicted_primary = predicted_hand_metrics.get("primary_accuracy_available")
    mlp_primary = None
    if head_results.get("status") == "complete":
        mlp_primary = head_results["models"][
            "mlp_32_oos_aware_experimental_train_predicted_eval"
        ]["heldout_metrics"].get("primary_accuracy_available")
    if predicted_primary == 1.0 and predicted_hand_metrics.get("primary_missing_count") == 0:
        interpretation = "predicted_geometry_preserves_clean_hand_router_primary_result"
    elif predicted_hand_metrics.get("primary_wrong_nonabstained_count", 0) > 0:
        interpretation = (
            "predicted_geometry_introduces_wrong_primary_calls; robustness_not_raw_clean_geometry_accuracy_is_the_learned_model_job"
        )
    elif predicted_hand_metrics.get("primary_abstention_count", 0) > 0:
        interpretation = (
            "predicted_geometry_degrades_router_by_abstention; confidence_calibration_or_robust_representation_needed"
        )
    else:
        interpretation = "predicted_geometry_result_inconclusive"
    return {
        "experimental_hand_router_primary_accuracy_available": experimental_primary,
        "predicted_hand_router_primary_accuracy_available": predicted_primary,
        "predicted_hand_router_primary_correct_count": predicted_hand_metrics.get(
            "primary_correct_count"
        ),
        "predicted_hand_router_primary_support_count": predicted_hand_metrics.get(
            "primary_support_count"
        ),
        "predicted_hand_router_primary_available_count": predicted_hand_metrics.get(
            "primary_available_count"
        ),
        "predicted_hand_router_primary_missing_count": predicted_hand_metrics.get(
            "primary_missing_count"
        ),
        "predicted_hand_router_primary_abstention_count": predicted_hand_metrics.get(
            "primary_abstention_count"
        ),
        "predicted_hand_router_primary_wrong_nonabstained_count": predicted_hand_metrics.get(
            "primary_wrong_nonabstained_count"
        ),
        "predicted_hand_router_oos_or_secondary_false_positive_rate_available": (
            predicted_hand_metrics.get("oos_or_secondary_false_positive_rate_available")
        ),
        "mlp_32_oos_aware_predicted_primary_accuracy_available": mlp_primary,
        "interpretation": interpretation,
    }


def _residue_nodes_by_entry(graph: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    residues: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or node.get("type") != "catalytic_residue":
            continue
        entry_id = _entry_id_from_residue_node(str(node.get("id") or ""))
        if entry_id:
            residues[entry_id].append(node)
    return {
        entry_id: sorted(items, key=lambda node: _entry_sort_key(str(node.get("id") or "")))
        for entry_id, items in residues.items()
    }


def _reference_sequence_positions(
    residue_nodes: list[dict[str, Any]],
    accession: str,
) -> list[dict[str, Any]]:
    positions: list[dict[str, Any]] = []
    for node in residue_nodes:
        candidates = [
            item
            for item in node.get("sequence_positions", [])
            if isinstance(item, dict) and item.get("is_reference", True)
        ]
        if not candidates:
            continue
        matching = [
            item
            for item in candidates
            if not item.get("uniprot_id") or str(item.get("uniprot_id")) == accession
        ]
        source = matching[0] if matching else candidates[0]
        positions.append(
            {
                "residue_node_id": node.get("id"),
                "code": _three_letter_code(source.get("code")),
                "resid": source.get("resid"),
                "roles": node.get("roles", []),
                "uniprot_id": source.get("uniprot_id"),
            }
        )
    return positions


def _has_reference_sequence_positions(
    residue_nodes: list[dict[str, Any]],
    accession: str,
) -> bool:
    if not residue_nodes:
        return False
    for node in residue_nodes:
        candidates = [
            item
            for item in node.get("sequence_positions", [])
            if isinstance(item, dict) and item.get("is_reference", True) and item.get("resid")
        ]
        usable = [
            item
            for item in candidates
            if not item.get("uniprot_id") or str(item.get("uniprot_id")) == accession
        ]
        if not usable:
            return False
    return True


def _entry_id_from_residue_node(node_id: str) -> str | None:
    parts = node_id.split(":")
    if len(parts) < 2:
        return None
    return f"{parts[0]}:{parts[1]}"


def _entry_sort_key(value: str) -> tuple[str, int, str]:
    prefix, _, suffix = str(value).partition(":")
    digits = "".join(ch for ch in suffix if ch.isdigit())
    return (prefix, int(digits) if digits else -1, suffix)


def _three_letter_code(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().upper()
    if len(text) == 3:
        return text
    return {
        "A": "ALA",
        "R": "ARG",
        "N": "ASN",
        "D": "ASP",
        "C": "CYS",
        "Q": "GLN",
        "E": "GLU",
        "G": "GLY",
        "H": "HIS",
        "I": "ILE",
        "L": "LEU",
        "K": "LYS",
        "M": "MET",
        "F": "PHE",
        "P": "PRO",
        "S": "SER",
        "T": "THR",
        "W": "TRP",
        "Y": "TYR",
        "V": "VAL",
    }.get(text)


def _rate(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return round(numerator / denominator, 6)


def _blocked_audit(
    *,
    blocker: str,
    detail: str,
    label_manifest: dict[str, Any],
    split_assignment: str,
    backend: str,
) -> dict[str, Any]:
    return {
        "artifact_id": "v3_predicted_geometry_robustness_audit_current702_20260529",
        "schema_version": "predicted_geometry_robustness_audit.v1",
        "created_utc": _utc_now_iso(),
        "status": "blocked",
        "blocker": blocker,
        "detail": detail,
        "scope": {
            "backend": backend,
            "split_assignment": split_assignment,
            "label_manifest_row_count": len(label_manifest.get("rows", []) or []),
        },
        "guardrails": {
            "label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
            "global_threshold_changed": False,
            "heldout_labels_used_for_fit_or_threshold": False,
            "large_model_downloads_performed": False,
        },
    }


def _markdown_report(audit: dict[str, Any]) -> str:
    if audit.get("status") != "complete":
        return (
            "# Predicted Geometry Robustness Audit\n\n"
            f"Status: `{audit.get('status')}`\n\n"
            f"Blocker: `{audit.get('blocker')}`\n\n"
            f"Detail: {audit.get('detail')}\n"
        )
    hand = audit["hand_router_on_predicted_geometry"]["metrics_canonical_masks"]
    headline = audit["headline"]
    scope = audit["scope"]
    predicted_meta = audit["predicted_geometry_features"]["metadata"]
    head_status = audit["geometry_heads_on_predicted_geometry"].get("status")
    mlp_line = "- Geometry-head transfer: blocked."
    if head_status == "complete":
        mlp_metrics = audit["geometry_heads_on_predicted_geometry"]["models"][
            "mlp_32_oos_aware_experimental_train_predicted_eval"
        ]["heldout_metrics"]
        mlp_line = (
            "- OOS-aware MLP-32 transfer: "
            f"{mlp_metrics['primary_correct_count']}/{mlp_metrics['primary_support_count']} "
            f"primary correct, {mlp_metrics['primary_abstention_count']} abstained, "
            f"{mlp_metrics['primary_wrong_nonabstained_count']} wrong nonabstained."
        )
    lines = [
        "# Predicted Geometry Robustness Audit",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "This swaps experimental M-CSA/PDB coordinates for AlphaFoldDB predicted coordinates on the frozen current702 heldout rows. No labels, registries, ontologies, imports, production scoring, or global thresholds were edited.",
        "",
        "## Headline",
        "",
        f"- Targeted {scope['requested_row_count']}/{scope['split_manifest_row_count']} heldout rows; {scope['excluded_row_count']} heldout rows were excluded by missing/incompatible sequence-position or experimental-geometry prerequisites.",
        f"- AlphaFoldDB geometry availability: {predicted_meta['ok_entry_count']}/{predicted_meta['entry_count']} rows ok; {predicted_meta['fetch_failure_count']} fetch failures; {predicted_meta['entries_with_proximal_ligands']} rows with proximal ligands.",
        f"- Hand router on predicted geometry: {hand['primary_correct_count']}/{hand['primary_support_count']} primary correct, {hand['primary_abstention_count']} abstained, {hand['primary_wrong_nonabstained_count']} wrong nonabstained, {hand['primary_missing_count']} missing.",
        f"- Hand router OOS/sec false-positive rate: {hand['oos_or_secondary_false_positive_rate_available']}.",
        mlp_line,
        f"- Interpretation: {headline['interpretation']}.",
        "",
        "## Caveat",
        "",
        "This isolates coordinate-source degradation while still using curated M-CSA catalytic residue identities, roles, and sequence positions. It is not an active-site localization benchmark from bare sequence.",
        "",
        "## Per-bin Hand Router",
        "",
        "| Bin | Primary support | Primary available | Primary correct | Primary abstain | Primary wrong | OOS/sec support | OOS/sec FP rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for bin_name, payload in audit["hand_router_on_predicted_geometry"][
        "per_bin_results"
    ].items():
        metrics = payload["metrics"]
        lines.append(
            "| "
            + " | ".join(
                [
                    bin_name,
                    str(metrics["primary_support_count"]),
                    str(metrics["primary_available_count"]),
                    str(metrics["primary_correct_count"]),
                    str(metrics["primary_abstention_count"]),
                    str(metrics["primary_wrong_nonabstained_count"]),
                    str(metrics["oos_or_secondary_support_count"]),
                    str(metrics["oos_or_secondary_false_positive_rate_available"]),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
