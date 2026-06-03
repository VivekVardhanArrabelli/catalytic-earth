from __future__ import annotations

import hashlib
import json
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
from .fingerprints import load_fingerprints
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


def build_predicted_geometry_distillation_audit(
    *,
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    wave1_audit: dict[str, Any],
    backend: str = "alphafold_db",
    alphafold_version: str = "auto",
    random_state: int = 702,
    cal_fraction: float = 0.2,
    hidden_layer_size: int = 32,
    max_rows: int = 0,
    fetcher: Any | None = None,
) -> dict[str, Any]:
    """Train/calibrate heads on predicted geometry and evaluate heldout once."""
    if backend == "esmfold":
        return _blocked_audit(
            blocker="local_esmfold_runtime_or_weights_unavailable",
            detail=(
                "ESMFold inference is not run by this audit unless a local "
                "runtime and weights are already staged. No model-weight "
                "download was attempted."
            ),
            label_manifest=label_manifest,
            split_assignment="all",
            backend=backend,
            artifact_id="v3_predicted_geometry_distillation_audit_current702_20260529",
            schema_version="predicted_geometry_distillation_audit.v1",
        )
    if backend != "alphafold_db":
        return _blocked_audit(
            blocker="unsupported_predicted_structure_backend",
            detail=f"backend={backend!r}; only alphafold_db is implemented",
            label_manifest=label_manifest,
            split_assignment="all",
            backend=backend,
            artifact_id="v3_predicted_geometry_distillation_audit_current702_20260529",
            schema_version="predicted_geometry_distillation_audit.v1",
        )

    target_rows, excluded_rows = _target_manifest_row_selection(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        split_assignment=None,
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
    heldout_target_rows = [
        row for row in target_rows if row.get("split_assignment") == "heldout"
    ]
    hand_rows = _hand_router_rows(
        target_rows=heldout_target_rows,
        predicted_geometry=predicted_geometry,
        predicted_retrieval=predicted_retrieval,
        wave1_audit=wave1_audit,
        threshold=HAND_ROUTER_THRESHOLD,
    )
    hand_metrics = _metrics_with_missing(hand_rows, mask_mode="canonical")
    wrong_rows = _classified_wrong_hand_router_rows(hand_rows)
    head_results = _geometry_head_predicted_train_results(
        label_manifest=label_manifest,
        predicted_geometry_features=predicted_geometry,
        predicted_geometry_retrieval=predicted_retrieval,
        wave1_audit=wave1_audit,
        random_state=random_state,
        cal_fraction=cal_fraction,
        hidden_layer_size=hidden_layer_size,
    )
    return {
        "artifact_id": "v3_predicted_geometry_distillation_audit_current702_20260529",
        "schema_version": "predicted_geometry_distillation_audit.v1",
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
            "backend": backend,
            "alphafold_version": alphafold_version,
            "label_manifest_row_count": len(
                [row for row in label_manifest.get("rows", []) if isinstance(row, dict)]
            ),
            "target_row_count": len(target_rows),
            "target_split_counts": dict(
                sorted(Counter(str(row.get("split_assignment")) for row in target_rows).items())
            ),
            "excluded_row_count": len(excluded_rows),
            "excluded_split_counts": dict(
                sorted(
                    Counter(str(row.get("split_assignment")) for row in excluded_rows).items()
                )
            ),
            "excluded_role_counts": dict(
                sorted(
                    Counter(
                        str(row.get("benchmark_role") or "unknown")
                        for row in excluded_rows
                    ).items()
                )
            ),
            "excluded_rows": excluded_rows,
            "target_definition": (
                "current702 M-CSA rows with existing experimental geometry evidence "
                "and accession-compatible sequence-position mappings; train/cal and "
                "heldout all use AlphaFoldDB predicted geometry as input"
            ),
        },
        "source_artifacts": {
            "label_manifest": "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json",
            "graph": "artifacts/v1_graph_1025.json",
            "experimental_geometry_features": "artifacts/v3_geometry_features_1025.json",
            "wave1_2_audit": "artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json",
        },
        "predicted_geometry_summary": {
            "metadata": predicted_geometry["metadata"],
            "status_counts": dict(
                sorted(
                    Counter(str(entry.get("status")) for entry in predicted_geometry["entries"]).items()
                )
            ),
            "split_status_counts": _split_status_counts(predicted_geometry["entries"]),
            "lightweight_rows": _lightweight_predicted_geometry_rows(
                predicted_geometry["entries"]
            ),
        },
        "wrong_hand_router_rows": {
            "summary": {
                "wrong_nonabstained_primary_count": len(wrong_rows),
                "true_mechanism_channel_counts": dict(
                    sorted(Counter(row["true_mechanism_channel"] for row in wrong_rows).items())
                ),
                "called_mechanism_channel_counts": dict(
                    sorted(Counter(row["called_mechanism_channel"] for row in wrong_rows).items())
                ),
            },
            "rows": wrong_rows,
        },
        "hand_router_on_predicted_heldout_geometry": {
            "threshold": HAND_ROUTER_THRESHOLD,
            "metrics_canonical_masks": hand_metrics,
            "per_bin_results": _per_bin_metrics_with_missing(hand_rows),
            "rows": hand_rows,
        },
        "predicted_geometry_distillation_heads": head_results,
        "distillation_answer": _distillation_answer(
            hand_metrics=hand_metrics,
            head_results=head_results,
            wrong_rows=wrong_rows,
        ),
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


def write_predicted_geometry_distillation_audit(
    *,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_features_path: Path,
    wave1_audit_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    backend: str = "alphafold_db",
    alphafold_version: str = "auto",
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
    with wave1_audit_path.open("r", encoding="utf-8") as handle:
        wave1_audit = json.load(handle)
    audit = build_predicted_geometry_distillation_audit(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        wave1_audit=wave1_audit,
        backend=backend,
        alphafold_version=alphafold_version,
        random_state=random_state,
        cal_fraction=cal_fraction,
        hidden_layer_size=hidden_layer_size,
        max_rows=max_rows,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_distillation_markdown_report(audit), encoding="utf-8")
    return audit


def build_predicted_geometry_in_distribution_atlas_retrieval(
    *,
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    heldout_predicted_geometry_audit: dict[str, Any] | None = None,
    backend: str = "alphafold_db",
    alphafold_version: str = "auto",
    max_rows: int = 0,
    fetcher: Any | None = None,
) -> dict[str, Any]:
    """Build predicted-geometry retrieval for current702 in-distribution atlas rows.

    The atlas here is the train/in-distribution rows with a mechanism
    fingerprint. This is the missing deployment-regime normalization surface for
    atlas-percentile novelty methods; heldout labels are not used for fitting or
    threshold selection.
    """
    if backend != "alphafold_db":
        return _blocked_audit(
            blocker="unsupported_predicted_structure_backend",
            detail=f"backend={backend!r}; only alphafold_db is implemented",
            label_manifest=label_manifest,
            split_assignment="in_distribution",
            backend=backend,
            artifact_id=(
                "v3_predicted_geometry_in_distribution_atlas_retrieval_current702_20260601"
            ),
            schema_version="predicted_geometry_atlas_retrieval.v1",
        )

    manifest_rows = [
        row for row in label_manifest.get("rows", []) if isinstance(row, dict)
    ]
    atlas_expected_rows = [
        row
        for row in manifest_rows
        if row.get("split_assignment") == "in_distribution"
        and (row.get("fingerprint_id") or row.get("mechanism_fingerprint_id"))
    ]
    selected_all, excluded_all = _target_manifest_row_selection(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        split_assignment="in_distribution",
        max_rows=0,
    )
    atlas_expected_ids = {
        str(row.get("entry_id") or "") for row in atlas_expected_rows
    }
    selected_by_entry = {
        str(row.get("entry_id") or ""): row
        for row in selected_all
        if str(row.get("entry_id") or "") in atlas_expected_ids
    }
    excluded_rows = [
        row
        for row in excluded_all
        if str(row.get("entry_id") or "") in atlas_expected_ids
    ]
    selected_rows = [
        selected_by_entry[str(row.get("entry_id") or "")]
        for row in atlas_expected_rows
        if str(row.get("entry_id") or "") in selected_by_entry
    ]
    truncated = False
    if max_rows and len(selected_rows) > max_rows:
        selected_rows = selected_rows[:max_rows]
        truncated = True

    predicted_geometry = build_alphafold_predicted_geometry_features(
        label_manifest_rows=selected_rows,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        alphafold_version=alphafold_version,
        fetcher=fetcher,
    )
    atlas_retrieval = run_geometry_retrieval(predicted_geometry)
    atlas_results = _enriched_predicted_retrieval_results(
        retrieval_results=atlas_retrieval.get("results", []),
        manifest_rows=manifest_rows,
        predicted_entries=predicted_geometry.get("entries", []),
    )
    heldout_results = _heldout_predicted_retrieval_results(
        heldout_predicted_geometry_audit or {}, manifest_rows=manifest_rows
    )
    combined_results = sorted(
        heldout_results + atlas_results,
        key=lambda row: _entry_sort_key(str(row.get("entry_id") or "")),
    )

    status_counts = Counter(
        str(entry.get("status")) for entry in predicted_geometry.get("entries", [])
    )
    missing_reasons = Counter(str(row.get("reason")) for row in excluded_rows)
    for entry in predicted_geometry.get("entries", []):
        status = str(entry.get("status"))
        if status != "ok":
            missing_reasons[status] += 1
    atlas_ok_ids = {
        str(row.get("entry_id") or "")
        for row in atlas_results
        if row.get("status") == "ok"
        and row.get("top_fingerprints")
    }
    top1_counts = Counter(
        str(row.get("top1_fingerprint_id"))
        for row in atlas_results
        if row.get("status") == "ok" and row.get("top1_fingerprint_id")
    )

    return {
        "artifact_id": (
            "v3_predicted_geometry_in_distribution_atlas_retrieval_current702_20260601"
        ),
        "schema_version": "predicted_geometry_atlas_retrieval.v1",
        "created_utc": _utc_now_iso(),
        "status": "complete",
        "scope": {
            "split_assignment": "in_distribution",
            "atlas_definition": (
                "current702 in_distribution rows with a non-null mechanism "
                "fingerprint_id/mechanism_fingerprint_id"
            ),
            "backend": backend,
            "alphafold_version": alphafold_version,
            "max_rows": max_rows,
            "truncated_by_max_rows": truncated,
        },
        "guardrails": {
            "label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "ontology_registry_edited": False,
            "production_scoring_changed": False,
            "global_threshold_changed": False,
            "heldout_labels_used_for_fit_or_threshold": False,
            "large_model_downloads_performed": False,
            "raw_coordinates_committed": False,
            "coordinate_download_scope": (
                "AlphaFoldDB mmCIF coordinate files fetched transiently for "
                "current702 in_distribution atlas accessions; raw coordinates "
                "are not committed"
            ),
        },
        "source_artifacts": {
            "label_manifest": "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json",
            "graph": "artifacts/v1_graph_1025.json",
            "experimental_geometry_features": "artifacts/v3_geometry_features_1025.json",
            "heldout_predicted_geometry_audit": (
                "artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json"
                if heldout_predicted_geometry_audit
                else None
            ),
        },
        "counts": {
            "atlas_rows_expected": len(atlas_expected_rows),
            "atlas_rows_selected_for_predicted_geometry": len(selected_rows),
            "atlas_retrieval_result_count": len(atlas_results),
            "atlas_rows_scored_ok": len(atlas_ok_ids),
            "atlas_rows_missing": max(len(atlas_expected_rows) - len(atlas_ok_ids), 0),
            "heldout_predicted_retrieval_rows_carried": len(heldout_results),
            "combined_results_count": len(combined_results),
            "atlas_status_counts": dict(sorted(status_counts.items())),
            "missing_reason_counts": dict(sorted(missing_reasons.items())),
            "atlas_top1_fingerprint_counts": dict(sorted(top1_counts.items())),
        },
        "predicted_geometry_summary": {
            "metadata": predicted_geometry.get("metadata", {}),
            "lightweight_rows": _lightweight_predicted_geometry_rows(
                predicted_geometry.get("entries", [])
            ),
        },
        "atlas_predicted_geometry_retrieval": {
            **{k: v for k, v in atlas_retrieval.items() if k != "results"},
            "results": atlas_results,
        },
        "result_sets": {
            "atlas_entry_ids": sorted(atlas_expected_ids, key=_entry_sort_key),
            "atlas_scored_ok_entry_ids": sorted(atlas_ok_ids, key=_entry_sort_key),
            "heldout_entry_ids_carried": sorted(
                {str(row.get("entry_id") or "") for row in heldout_results},
                key=_entry_sort_key,
            ),
        },
        "next_methods_unblocked": [
            "eval-mechanism-abstention-gate with predicted-geometry atlas percentiles",
            "atlas Mahalanobis / percentile novelty diagnostics in deployment geometry",
        ],
        "results": combined_results,
    }


def write_predicted_geometry_in_distribution_atlas_retrieval(
    *,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_features_path: Path,
    heldout_predicted_geometry_audit_path: Path | None,
    out_path: Path,
    report_path: Path | None = None,
    backend: str = "alphafold_db",
    alphafold_version: str = "auto",
    max_rows: int = 0,
) -> dict[str, Any]:
    with label_manifest_path.open("r", encoding="utf-8") as handle:
        label_manifest = json.load(handle)
    with graph_path.open("r", encoding="utf-8") as handle:
        graph = json.load(handle)
    with experimental_geometry_features_path.open("r", encoding="utf-8") as handle:
        experimental_geometry_features = json.load(handle)
    heldout_audit = None
    if heldout_predicted_geometry_audit_path is not None:
        with heldout_predicted_geometry_audit_path.open("r", encoding="utf-8") as handle:
            heldout_audit = json.load(handle)
    audit = build_predicted_geometry_in_distribution_atlas_retrieval(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        heldout_predicted_geometry_audit=heldout_audit,
        backend=backend,
        alphafold_version=alphafold_version,
        max_rows=max_rows,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _predicted_geometry_atlas_retrieval_markdown_report(audit, out_path),
            encoding="utf-8",
        )
    return audit


def _enriched_predicted_retrieval_results(
    *,
    retrieval_results: list[dict[str, Any]],
    manifest_rows: list[dict[str, Any]],
    predicted_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    manifest_by_entry = {
        str(row.get("entry_id") or ""): row
        for row in manifest_rows
        if row.get("entry_id")
    }
    predicted_by_entry = {
        str(row.get("entry_id") or ""): row
        for row in predicted_entries
        if row.get("entry_id")
    }
    out: list[dict[str, Any]] = []
    for row in retrieval_results:
        entry_id = str(row.get("entry_id") or "")
        manifest = manifest_by_entry.get(entry_id, {})
        predicted = predicted_by_entry.get(entry_id, {})
        predicted_accession = predicted.get("accession")
        manifest_accession = manifest.get("accession")
        top = (row.get("top_fingerprints") or [{}])[0]
        enriched = dict(row)
        enriched.update(
            {
                "accession": predicted_accession or manifest_accession,
                "manifest_accession": manifest_accession,
                "predicted_geometry_accession": predicted_accession,
                "sequence_id": manifest.get("sequence_id") or predicted.get("sequence_id"),
                "sequence_sha256": manifest.get("sequence_sha256"),
                "split_assignment": manifest.get("split_assignment")
                or predicted.get("split_assignment"),
                "benchmark_role": manifest.get("benchmark_role")
                or predicted.get("benchmark_role"),
                "true_fingerprint_id": manifest.get("fingerprint_id")
                or manifest.get("mechanism_fingerprint_id"),
                "predicted_geometry_status": predicted.get("status") or row.get("status"),
                "predicted_pdb_id": predicted.get("pdb_id") or row.get("pdb_id"),
                "predicted_geometry_accession_repair": predicted.get(
                    "predicted_geometry_accession_repair"
                ),
                "experimental_pdb_id": predicted.get("experimental_pdb_id"),
                "predicted_resolved_residue_count": predicted.get(
                    "resolved_residue_count"
                ),
                "predicted_missing_positions": predicted.get("missing_positions"),
                "top1_fingerprint_id": top.get("fingerprint_id"),
                "top1_score": top.get("score"),
                "top1_role_match_fraction": top.get("role_match_fraction"),
                "top1_cofactor_context_score": top.get("cofactor_context_score"),
                "top1_cofactor_evidence_level": top.get("cofactor_evidence_level"),
                "missingness_reason": (
                    None if row.get("status") == "ok" else row.get("status")
                ),
            }
        )
        out.append(enriched)
    return sorted(out, key=lambda item: _entry_sort_key(str(item.get("entry_id") or "")))


def _heldout_predicted_retrieval_results(
    heldout_audit: dict[str, Any],
    *,
    manifest_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    retrieval = heldout_audit.get("predicted_geometry_retrieval", {})
    features = heldout_audit.get("predicted_geometry_features", {})
    return _enriched_predicted_retrieval_results(
        retrieval_results=retrieval.get("results", []),
        manifest_rows=manifest_rows,
        predicted_entries=features.get("entries", []),
    )


def _predicted_geometry_atlas_retrieval_markdown_report(
    audit: dict[str, Any],
    out_path: Path,
) -> str:
    counts = audit.get("counts", {})
    missing = counts.get("missing_reason_counts", {})
    top1 = counts.get("atlas_top1_fingerprint_counts", {})
    command = (
        "PYTHONPATH=src python -m catalytic_earth.cli "
        "eval-mechanism-abstention-gate "
        f"--geometry-retrieval {out_path} "
        "--out artifacts/v3_mechanism_abstention_gate_eval_predicted_atlas_current702_20260601.json "
        "--report work/mechanism_abstention_gate_eval_predicted_atlas_current702_20260601.md"
    )
    lines = [
        "# Predicted-Geometry In-Distribution Atlas Retrieval",
        "",
        f"Run: {audit.get('created_utc')}",
        "",
        "Deployment-regime AlphaFoldDB retrieval for the current702 "
        "`in_distribution` fingerprint atlas rows. No labels, registries, "
        "thresholds, production scoring, or splits were changed.",
        "",
        "## Counts",
        "",
        f"- Atlas rows expected: {counts.get('atlas_rows_expected')}",
        "- Rows selected for predicted-geometry coordinate swap: "
        f"{counts.get('atlas_rows_selected_for_predicted_geometry')}",
        f"- Retrieval rows emitted for atlas: {counts.get('atlas_retrieval_result_count')}",
        f"- Rows scored ok: {counts.get('atlas_rows_scored_ok')}",
        f"- Rows missing/unusable: {counts.get('atlas_rows_missing')}",
        "- Heldout predicted retrieval rows carried for direct gate reruns: "
        f"{counts.get('heldout_predicted_retrieval_rows_carried')}",
        f"- Combined retrieval rows: {counts.get('combined_results_count')}",
        "",
        "## Missingness",
        "",
    ]
    if missing:
        for reason, count in missing.items():
            lines.append(f"- {reason}: {count}")
    else:
        lines.append("- none")
    lines.extend(["", "## Atlas Top1 Fingerprints", ""])
    if top1:
        for fingerprint_id, count in top1.items():
            lines.append(f"- {fingerprint_id}: {count}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Output",
            "",
            f"- Artifact: `{out_path}`",
            "- The top-level `results` array combines the new atlas rows with the "
            "previous heldout predicted-geometry retrieval rows so the existing "
            "`eval-mechanism-abstention-gate` loader can consume one path.",
            "- The atlas-only rows are also preserved under "
            "`atlas_predicted_geometry_retrieval.results`.",
            "",
            "## Next Method Unblocked",
            "",
            "Run the predicted-geometry atlas-percentile gate:",
            "",
            "```bash",
            command,
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def _target_manifest_row_selection(
    *,
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    split_assignment: str | None,
    max_rows: int,
    allow_accession_compatible_residue_subset: bool = False,
    allow_best_real_sequence_accession: bool = False,
    allow_missing_experimental_geometry_if_sequence_positions: bool = False,
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
        if split_assignment is not None and row.get("split_assignment") != split_assignment:
            continue
        if not entry_id.startswith("m_csa:"):
            excluded_rows.append(_excluded_target_row(row, "not_m_csa_entry"))
            continue
        residue_nodes = residues_by_entry.get(entry_id, [])
        accession = str(row.get("accession") or row.get("sequence_id") or "")
        experimental = experimental_by_entry.get(entry_id)
        if not experimental or experimental.get("status") != "ok":
            if (
                allow_missing_experimental_geometry_if_sequence_positions
                and experimental
                and _has_reference_sequence_positions(residue_nodes, accession)
            ):
                repaired = dict(row)
                repaired["predicted_geometry_accession_repair"] = {
                    "policy": (
                        "reference_sequence_positions_without_experimental_"
                        "structure_positions"
                    ),
                    "experimental_geometry_status": experimental.get("status"),
                    "selected_accession": accession,
                    "selected_residue_count": _reference_sequence_position_count(
                        residue_nodes, accession
                    ),
                    "total_residue_node_count": len(residue_nodes),
                }
                rows.append(repaired)
                if max_rows and len(rows) >= max_rows:
                    break
                continue
            excluded_rows.append(
                _excluded_target_row(
                    row,
                    f"experimental_geometry_not_ok:{(experimental or {}).get('status')}",
                )
            )
            continue
        if _has_reference_sequence_positions(residue_nodes, accession):
            rows.append(dict(row))
            if max_rows and len(rows) >= max_rows:
                break
            continue
        repaired_row = _accession_repaired_target_row(
            row,
            residue_nodes,
            accession,
            allow_accession_compatible_residue_subset=(
                allow_accession_compatible_residue_subset
            ),
            allow_best_real_sequence_accession=allow_best_real_sequence_accession,
        )
        if repaired_row is None:
            excluded_rows.append(
                _excluded_target_row(row, "missing_accession_compatible_sequence_positions")
            )
            continue
        rows.append(repaired_row)
        if max_rows and len(rows) >= max_rows:
            break
    return rows, excluded_rows


def _excluded_target_row(row: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "entry_id": row.get("entry_id"),
        "accession": row.get("accession"),
        "split_assignment": row.get("split_assignment"),
        "benchmark_role": row.get("benchmark_role"),
        "fingerprint_id": row.get("fingerprint_id")
        or row.get("mechanism_fingerprint_id"),
        "reason": reason,
    }


def _accession_repaired_target_row(
    row: dict[str, Any],
    residue_nodes: list[dict[str, Any]],
    accession: str,
    *,
    allow_accession_compatible_residue_subset: bool,
    allow_best_real_sequence_accession: bool,
) -> dict[str, Any] | None:
    if allow_accession_compatible_residue_subset:
        selected_count = _reference_sequence_position_count(residue_nodes, accession)
        if selected_count >= 2:
            repaired = dict(row)
            repaired["predicted_geometry_accession_repair"] = {
                "policy": "manifest_accession_compatible_residue_subset",
                "original_accession": accession,
                "selected_accession": accession,
                "selected_residue_count": selected_count,
                "total_residue_node_count": len(residue_nodes),
                "skipped_nonmatching_residue_count": max(
                    len(residue_nodes) - selected_count,
                    0,
                ),
            }
            return repaired

    if allow_best_real_sequence_accession:
        best = _best_real_sequence_accession(row, residue_nodes, accession)
        if best is not None:
            selected_accession, selected_count = best
            repaired = dict(row)
            repaired["original_accession"] = accession
            repaired["original_sequence_id"] = row.get("sequence_id")
            repaired["accession"] = selected_accession
            repaired["sequence_id"] = selected_accession
            repaired["predicted_geometry_accession_repair"] = {
                "policy": "best_real_sequence_accession_by_active_site_coverage",
                "original_accession": accession,
                "selected_accession": selected_accession,
                "selected_residue_count": selected_count,
                "total_residue_node_count": len(residue_nodes),
                "skipped_nonmatching_residue_count": max(
                    len(residue_nodes) - selected_count,
                    0,
                ),
            }
            return repaired

    return None


def _best_real_sequence_accession(
    row: dict[str, Any],
    residue_nodes: list[dict[str, Any]],
    current_accession: str,
) -> tuple[str, int] | None:
    accessions = [
        str(accession)
        for accession in row.get("real_sequence_accessions", [])
        if accession
    ]
    if current_accession and current_accession not in accessions:
        accessions.append(current_accession)
    scored = [
        (accession, _reference_sequence_position_count(residue_nodes, accession))
        for accession in accessions
    ]
    eligible = [
        item
        for item in scored
        if item[1] >= 2 and item[0] != current_accession
    ]
    if not eligible:
        return None
    return sorted(eligible, key=lambda item: (-item[1], item[0]))[0]


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
        "original_accession": manifest_row.get("original_accession"),
        "original_sequence_id": manifest_row.get("original_sequence_id"),
        "predicted_geometry_accession_repair": manifest_row.get(
            "predicted_geometry_accession_repair"
        ),
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
        "original_accession": manifest_row.get("original_accession"),
        "original_sequence_id": manifest_row.get("original_sequence_id"),
        "predicted_geometry_accession_repair": manifest_row.get(
            "predicted_geometry_accession_repair"
        ),
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


def _geometry_head_predicted_train_results(
    *,
    label_manifest: dict[str, Any],
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

    predicted_rows, predicted_missing = _model_rows(
        label_manifest=label_manifest,
        geometry_features=predicted_geometry_features,
        geometry_retrieval=predicted_geometry_retrieval,
        wave1_audit=wave1_audit,
    )
    train_source = [
        row
        for row in predicted_rows
        if row.get("split_assignment") == "in_distribution"
        and row.get("geometry_status") == "ok"
    ]
    heldout = [
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
    if not train_primary or not cal_rows or not heldout:
        return {
            "status": "blocked",
            "blocker": "insufficient_rows_for_predicted_geometry_distillation",
            "detail": (
                f"train_primary={len(train_primary)} cal={len(cal_rows)} "
                f"heldout={len(heldout)}"
            ),
            "predicted_missing_rows": predicted_missing,
        }

    logistic = make_pipeline(
        DictVectorizer(sparse=False),
        StandardScaler(),
        LogisticRegression(max_iter=2000, random_state=random_state),
    )
    mlp = make_pipeline(
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
        mlp.fit(train_x, train_y)
        mlp_oos_aware.fit(train_all_x, train_all_y)

    wave_masks = _wave_masks_by_entry(wave1_audit)
    logistic_result = _evaluate_head(
        track_id="geometry_feature_logistic_predicted_train_predicted_eval",
        display_name="Geometry-feature logistic predicted-train predicted-eval",
        model=logistic,
        cal_rows=cal_rows,
        heldout_rows=heldout,
        wave_masks=wave_masks,
    )
    mlp_result = _evaluate_head(
        track_id="geometry_feature_mlp_32_predicted_train_predicted_eval",
        display_name=f"Geometry-feature MLP-{hidden_layer_size} predicted-train predicted-eval",
        model=mlp,
        cal_rows=cal_rows,
        heldout_rows=heldout,
        wave_masks=wave_masks,
    )
    mlp_oos_aware_result = _evaluate_head(
        track_id="geometry_feature_mlp_32_oos_aware_predicted_train_predicted_eval",
        display_name=(
            f"Geometry-feature OOS-aware MLP-{hidden_layer_size} "
            "predicted-train predicted-eval"
        ),
        model=mlp_oos_aware,
        cal_rows=cal_rows,
        heldout_rows=heldout,
        wave_masks=wave_masks,
        abstain_class="__none_of_above__",
    )
    return {
        "status": "complete",
        "protocol": {
            "train_coordinates": "AlphaFoldDB predicted geometry",
            "calibration_coordinates": "AlphaFoldDB predicted in-distribution geometry only",
            "evaluation_coordinates": "AlphaFoldDB predicted heldout geometry only",
            "supervision": "current M-CSA/current702 mechanism labels",
            "threshold_policy": (
                "lowest max-probability threshold with zero nonprimary/OOS "
                "false positives on predicted-geometry calibration rows; no "
                "heldout tuning"
            ),
            "random_state": random_state,
            "cal_fraction": cal_fraction,
            "hidden_layer_size": hidden_layer_size,
        },
        "row_counts": {
            "predicted_feature_rows": len(predicted_rows),
            "predicted_missing_rows": predicted_missing,
            "train_source_row_count": len(train_source),
            "train_all_row_count": len(train_all),
            "train_primary_row_count": len(train_primary),
            "cal_row_count": len(cal_rows),
            "heldout_available_row_count": len(heldout),
            "train_primary_class_counts": dict(
                sorted(Counter(train_y).items())
            ),
        },
        "models": {
            "logistic_predicted_train_predicted_eval": logistic_result,
            "mlp_32_predicted_train_predicted_eval": mlp_result,
            "mlp_32_oos_aware_predicted_train_predicted_eval": mlp_oos_aware_result,
        },
    }


def _classified_wrong_hand_router_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fingerprints = {fingerprint.id: fingerprint.to_dict() for fingerprint in load_fingerprints()}
    wrong_rows: list[dict[str, Any]] = []
    for row in rows:
        if not row.get("canonical_primary_support_mask"):
            continue
        if not row.get("predicted_geometry_joined") or row.get("abstained"):
            continue
        if row.get("called_fingerprint_id") == row.get("true_fingerprint_id"):
            continue
        true_fp = fingerprints.get(str(row.get("true_fingerprint_id")), {})
        called_fp = fingerprints.get(str(row.get("called_fingerprint_id")), {})
        true_cofactors = true_fp.get("cofactors", []) or []
        called_cofactors = called_fp.get("cofactors", []) or []
        wrong_rows.append(
            {
                "entry_id": row.get("entry_id"),
                "sequence_id": row.get("sequence_id"),
                "structural_neighborhood_bin": row.get("structural_neighborhood_bin"),
                "true_fingerprint_id": row.get("true_fingerprint_id"),
                "true_cofactors": true_cofactors,
                "true_mechanism_channel": (
                    "cofactor_defined" if true_cofactors else "cofactor_independent"
                ),
                "called_fingerprint_id": row.get("called_fingerprint_id"),
                "called_cofactors": called_cofactors,
                "called_mechanism_channel": (
                    "cofactor_defined" if called_cofactors else "cofactor_independent"
                ),
                "top1_score": row.get("top1_score"),
                "experimental_pdb_id": row.get("experimental_pdb_id"),
                "predicted_pdb_id": row.get("predicted_pdb_id"),
                "predicted_resolved_residue_count": row.get(
                    "predicted_resolved_residue_count"
                ),
                "predicted_missing_positions": row.get("predicted_missing_positions"),
            }
        )
    return wrong_rows


def _split_status_counts(entries: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    split_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for entry in entries:
        split_counts[str(entry.get("split_assignment"))][str(entry.get("status"))] += 1
    return {
        split: dict(sorted(counter.items()))
        for split, counter in sorted(split_counts.items())
    }


def _lightweight_predicted_geometry_rows(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "entry_id": entry.get("entry_id"),
            "accession": entry.get("accession"),
            "split_assignment": entry.get("split_assignment"),
            "benchmark_role": entry.get("benchmark_role"),
            "status": entry.get("status"),
            "experimental_pdb_id": entry.get("experimental_pdb_id"),
            "predicted_pdb_id": entry.get("pdb_id"),
            "resolved_residue_count": entry.get("resolved_residue_count"),
            "missing_positions": entry.get("missing_positions"),
            "proximal_ligand_count": len(
                entry.get("ligand_context", {}).get("proximal_ligands", []) or []
            ),
            "nearby_residue_count": entry.get("pocket_context", {}).get(
                "nearby_residue_count"
            ),
        }
        for entry in sorted(entries, key=lambda item: _entry_sort_key(str(item.get("entry_id"))))
    ]


def _distillation_answer(
    *,
    hand_metrics: dict[str, Any],
    head_results: dict[str, Any],
    wrong_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    if head_results.get("status") != "complete":
        return {
            "status": "blocked",
            "interpretation": head_results.get("blocker", "head_results_unavailable"),
        }
    mlp_oos = head_results["models"]["mlp_32_oos_aware_predicted_train_predicted_eval"][
        "heldout_metrics"
    ]
    logistic = head_results["models"]["logistic_predicted_train_predicted_eval"][
        "heldout_metrics"
    ]
    hand_primary = hand_metrics.get("primary_accuracy_available")
    mlp_primary = mlp_oos.get("primary_accuracy_available")
    if (
        mlp_oos.get("primary_wrong_nonabstained_count", 0) == 0
        and mlp_oos.get("primary_abstention_count", 0) > 0
    ):
        interpretation = (
            "predicted_geometry_distillation_stays_disciplined_but_is_abstention_limited"
        )
    elif mlp_primary is not None and hand_primary is not None and mlp_primary > hand_primary:
        interpretation = "predicted_geometry_distillation_recovers_beyond_hand_router"
    else:
        interpretation = "predicted_geometry_distillation_does_not_recover_clean_geometry"
    return {
        "status": "complete",
        "hand_router_predicted_primary_accuracy_available": hand_primary,
        "logistic_predicted_primary_accuracy_available": logistic.get(
            "primary_accuracy_available"
        ),
        "mlp_32_oos_aware_predicted_primary_accuracy_available": mlp_primary,
        "mlp_32_oos_aware_oos_or_secondary_false_positive_rate_available": (
            mlp_oos.get("oos_or_secondary_false_positive_rate_available")
        ),
        "mlp_minus_hand_primary_accuracy": (
            round(float(mlp_primary) - float(hand_primary), 6)
            if mlp_primary is not None and hand_primary is not None
            else None
        ),
        "wrong_hand_router_true_channel_counts": dict(
            sorted(Counter(row["true_mechanism_channel"] for row in wrong_rows).items())
        ),
        "interpretation": interpretation,
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
            if isinstance(item, dict)
            and item.get("is_reference", True)
            and item.get("resid")
        ]
        if not candidates:
            continue
        matching = [
            item
            for item in candidates
            if not item.get("uniprot_id") or str(item.get("uniprot_id")) == accession
        ]
        if not matching:
            continue
        source = matching[0]
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


def _reference_sequence_position_count(
    residue_nodes: list[dict[str, Any]],
    accession: str,
) -> int:
    count = 0
    for node in residue_nodes:
        candidates = [
            item
            for item in node.get("sequence_positions", [])
            if isinstance(item, dict)
            and item.get("is_reference", True)
            and item.get("resid")
        ]
        if any(
            not item.get("uniprot_id") or str(item.get("uniprot_id")) == accession
            for item in candidates
        ):
            count += 1
    return count


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
    artifact_id: str = "v3_predicted_geometry_robustness_audit_current702_20260529",
    schema_version: str = "predicted_geometry_robustness_audit.v1",
) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "schema_version": schema_version,
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


def _distillation_markdown_report(audit: dict[str, Any]) -> str:
    if audit.get("status") != "complete":
        return (
            "# Predicted Geometry Distillation Audit\n\n"
            f"Status: `{audit.get('status')}`\n\n"
            f"Blocker: `{audit.get('blocker')}`\n\n"
            f"Detail: {audit.get('detail')}\n"
        )
    scope = audit["scope"]
    predicted_meta = audit["predicted_geometry_summary"]["metadata"]
    hand = audit["hand_router_on_predicted_heldout_geometry"][
        "metrics_canonical_masks"
    ]
    wrong = audit["wrong_hand_router_rows"]
    answer = audit["distillation_answer"]
    heads = audit["predicted_geometry_distillation_heads"]
    lines = [
        "# Predicted Geometry Distillation Audit",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "This trains/calibrates geometry heads on AlphaFoldDB-predicted in-distribution geometry and evaluates AlphaFoldDB-predicted heldout geometry once. Current M-CSA/current702 labels are the teacher labels. No labels, registries, ontologies, production scoring, imports, or global thresholds were edited.",
        "",
        "## Cheap Error-Mode Fork",
        "",
        f"- Wrong non-abstained hand-router primary rows: {wrong['summary']['wrong_nonabstained_primary_count']}.",
        f"- True-channel counts: {wrong['summary']['true_mechanism_channel_counts']}.",
        f"- Called-channel counts: {wrong['summary']['called_mechanism_channel_counts']}.",
        "",
        "| Entry | True fingerprint | True channel | Called fingerprint | Score |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for row in wrong["rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["entry_id"]),
                    str(row["true_fingerprint_id"]),
                    str(row["true_mechanism_channel"]),
                    str(row["called_fingerprint_id"]),
                    str(row["top1_score"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Distillation Result",
            "",
            f"- Target rows: {scope['target_row_count']}/{scope['label_manifest_row_count']} current702 rows; split counts {scope['target_split_counts']}.",
            f"- AlphaFoldDB geometry availability: {predicted_meta['ok_entry_count']}/{predicted_meta['entry_count']} ok; {predicted_meta['fetch_failure_count']} fetch failures; {predicted_meta['entries_with_proximal_ligands']} rows with proximal ligands.",
            f"- Hand router on predicted heldout geometry: {hand['primary_correct_count']}/{hand['primary_support_count']} primary correct, {hand['primary_abstention_count']} abstained, {hand['primary_wrong_nonabstained_count']} wrong nonabstained; OOS/sec FP rate {hand['oos_or_secondary_false_positive_rate_available']}.",
        ]
    )
    if heads.get("status") == "complete":
        for key, label in [
            ("logistic_predicted_train_predicted_eval", "Logistic"),
            ("mlp_32_predicted_train_predicted_eval", "MLP-32"),
            ("mlp_32_oos_aware_predicted_train_predicted_eval", "OOS-aware MLP-32"),
        ]:
            metrics = heads["models"][key]["heldout_metrics"]
            lines.append(
                f"- {label}: {metrics['primary_correct_count']}/{metrics['primary_support_count']} "
                f"primary correct, {metrics['primary_abstention_count']} abstained, "
                f"{metrics['primary_wrong_nonabstained_count']} wrong nonabstained; "
                f"OOS/sec FP rate {metrics['oos_or_secondary_false_positive_rate_available']}."
            )
    else:
        lines.append(f"- Head training blocked: {heads.get('blocker')}.")
    lines.extend(
        [
            f"- Interpretation: {answer['interpretation']}.",
            "",
            "## Caveat",
            "",
            "This is still an active-site-position-known experiment: M-CSA catalytic residue identities, roles, and sequence positions are used to extract predicted geometry. It tests degraded-coordinate robustness, not active-site localization from raw sequence.",
            "",
        ]
    )
    return "\n".join(lines)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
