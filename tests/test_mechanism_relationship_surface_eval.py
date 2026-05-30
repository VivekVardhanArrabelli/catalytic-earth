"""Unit tests for the D11 mechanism relationship surface evaluator.

These are pure-stdlib tests with synthetic vectors -- no embeddings, models, or
network. They pin the relationship semantics, the atlas-only robust scaling, and
the rank-metric aggregation that the D11 hygiene surface comparison relies on.
"""

from __future__ import annotations

import json
from pathlib import Path

from catalytic_earth.mechanism_relationship_surface_eval import (
    apply_robust,
    build_mechanism_relationship_surface_eval,
    evaluate_relationship_surface,
    load_fingerprint_family_map,
    relationship_type,
    robust_standardizer,
)

FAMILY_MAP = {
    "ser_his_acid_hydrolase": "hydrolysis",
    "metal_dependent_hydrolase": "hydrolysis",
    "flavin_monooxygenase": "flavin_redox",
    "flavin_dehydrogenase_reductase": "flavin_redox",
    "heme_peroxidase_oxidase": "heme_redox",
}


def test_relationship_type_ladder():
    # exact beats family beats cofactor beats unrelated.
    assert relationship_type("flavin_monooxygenase", "flavin_monooxygenase", FAMILY_MAP) == "exact"
    assert (
        relationship_type("ser_his_acid_hydrolase", "metal_dependent_hydrolase", FAMILY_MAP)
        == "family"
    )
    # Shared cofactor but different ontology family: inject a cofactor map so the
    # two share a normalized cofactor while the family_map keeps them apart.
    cofactor_map = {"flavin_monooxygenase": "flavin", "other_flavin": "flavin"}
    assert (
        relationship_type(
            "flavin_monooxygenase", "other_flavin", FAMILY_MAP, cofactor_map=cofactor_map
        )
        == "cofactor"
    )
    assert relationship_type("ser_his_acid_hydrolase", "heme_peroxidase_oxidase", FAMILY_MAP) == "unrelated"
    assert relationship_type(None, "heme_peroxidase_oxidase", FAMILY_MAP) == "unrelated"


def test_robust_standardizer_centers_atlas():
    atlas = [[0.0, 10.0], [2.0, 14.0], [4.0, 18.0]]
    medians, scales = robust_standardizer(atlas)
    assert medians == [2.0, 14.0]
    # IQR positive and used to scale.
    assert all(s > 0 for s in scales)
    centered = apply_robust([2.0, 14.0], medians, scales)
    assert centered == [0.0, 0.0]


def test_evaluate_surface_perfect_separation():
    # Three fingerprints, each query sits on top of its exact atlas twin.
    def row(entry, fp, vec):
        return {"entry_id": entry, "true_fingerprint_id": fp, "vector": vec}

    atlas = [
        row("a1", "flavin_monooxygenase", [1.0, 0.0, 0.0]),
        row("a2", "flavin_dehydrogenase_reductase", [0.9, 0.1, 0.0]),
        row("a3", "metal_dependent_hydrolase", [0.0, 0.0, 1.0]),
    ]
    queries = [
        row("q1", "flavin_monooxygenase", [0.98, 0.02, 0.0]),
        row("q2", "metal_dependent_hydrolase", [0.0, 0.05, 0.97]),
    ]
    result = evaluate_relationship_surface(
        surface_id="synthetic",
        display_name="synthetic",
        surface_kind="test",
        queries=queries,
        atlas=atlas,
        family_map=FAMILY_MAP,
        variants=("cosine",),
    )
    m = result["metrics_by_variant"]["cosine"]
    # q1's nearest is its exact twin; q2's nearest is its exact twin.
    assert m["exact_top1_rate"] == 1.0
    # q1 should see its flavin family-mate (a2) within top-3.
    assert m["family_top3_any_rate"] == 1.0
    assert result["candidate_pool_count"] == 3
    assert result["relationship_query_count"] == 2


def test_self_excluded_from_atlas_by_entry_id():
    # A query that also appears in the atlas must not match itself.
    def row(entry, fp, vec):
        return {"entry_id": entry, "true_fingerprint_id": fp, "vector": vec}

    shared = row("dup", "flavin_monooxygenase", [1.0, 0.0])
    atlas = [shared, row("other", "metal_dependent_hydrolase", [0.0, 1.0])]
    result = evaluate_relationship_surface(
        surface_id="s",
        display_name="s",
        surface_kind="test",
        queries=[shared],
        atlas=atlas,
        family_map=FAMILY_MAP,
        variants=("cosine",),
    )
    # Only a non-self, unrelated neighbor remains -> no exact hit.
    assert result["metrics_by_variant"]["cosine"]["exact_top1_rate"] == 0.0


def test_build_from_real_artifacts_if_present():
    # Integration smoke: if the persisted PLM embeddings exist, the PLM surface
    # should beat the k-mer control. Skips cleanly when artifacts are absent.
    esm = Path("artifacts/representation_tracks/esm2_150m/esm2_150m_embeddings_current702_20260525.jsonl")
    ont = Path("data/registries/mechanism_ontology.json")
    kmer = Path("artifacts/v3_sequence_embedding_sidecar_current702_kmer_20260529.jsonl")
    if not (esm.exists() and ont.exists()):
        return
    audit = build_mechanism_relationship_surface_eval(
        esm2_150m_path=esm,
        ontology_path=ont,
        kmer_path=kmer if kmer.exists() else None,
    )
    plm = next(s for s in audit["surfaces"] if s["surface_id"] == "esm2_150m_whole_sequence")
    assert plm["candidate_pool_count"] == 184
    assert plm["metrics_by_variant"]["cosine"]["exact_top1_rate"] > 0.4
    if kmer.exists():
        assert audit["surface_comparison"]["verdict"] == "plm_organizes_relationship_space_better"


def test_load_family_map_from_registry_if_present():
    ont = Path("data/registries/mechanism_ontology.json")
    if not ont.exists():
        return
    fam = load_fingerprint_family_map(ont)
    # Both hydrolases share the hydrolysis family in the real registry.
    assert fam.get("ser_his_acid_hydrolase") == fam.get("metal_dependent_hydrolase")
