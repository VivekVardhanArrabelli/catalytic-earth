# Task spec — wire predicted-geometry recovery into the silver gate + implement grafting

Author: handoff for the next automation instance. Date: 2026-06-15.
Read this AFTER `docs/project_state.md` (top bullets) + `docs/decision_log.md` (newest-first)
+ `work/handoff.md` (top block), and verify every number against the live registry.

## Why this exists (honest framing — NOT a missed track)

The bronze->silver promotion gate (`bronze_silver_promotion_preview.py`) scores
`silver_ready` only when the annotated cofactor is PRESENT in coordinates (true holo). On
2026-06-14 the `holo_structure_promotion` lane unblocked the rows that HAVE an experimental
holo PDB: `silver_ready` 0 -> 260 across 24 fingerprints, using REAL experimental cofactor
presence (no reconstruction needed). Verify current numbers; they may have grown.

That leaves the larger bucket: ~2,275 `blocked_pending_structure` (+ a few `blocked_apo`)
rows that are chemistry-corroborated but APO-ONLY or PREDICTED-ONLY (AlphaFold is inherently
apo). The predicted-geometry RECONSTRUCTION work already exists for exactly these rows, but
two extensions were never finished:

  A. The leakage-safe **fusion-recovery** harness was built but **never wired into the
     promotion gate** as a recovery path.
  B. Literal **template grafting** of a canonical holo cofactor into an apo/predicted
     structure was **fidelity-probed but never implemented** (only "would a rigid graft stay
     proximal?" is scored; no coordinates are ever placed).

This spec is those two tasks. It is the path to extend silver beyond the rows that already
have experimental holo.

## What already exists (audited 2026-06-15 — reuse, do not rebuild)

- `sequence_cofactor_channel.py` — MATURE. Leakage-safe sequence -> cofactor-presence channel
  (ESM2 embeddings + mionic metal predictions -> `predicted_cofactor_families`).
  `_fused_geometry_features(predicted_geometry, cofactor_channel)` injects predicted cofactor
  families into `ligand_context.cofactor_families` of an apo predicted structure (feature-level
  fusion, NOT 3D atom placement).
- `predicted_geometry_recovery.py` — MATURE. Leakage-safe in-distribution recovery harness:
  scores the hand router on experimental vs predicted-apo vs cofactor-fused geometry; honest
  read is on OUT-OF-SAMPLE calibration rows (channel was fit on train).
- `cofactor_fusion_operating_point.py` — MATURE. Precision side (OOS false positives) + two
  dials: recalibrated abstention threshold, and sequence-supported suppression.
- `predicted_geometry_robustness.py` — MATURE. Degradation measurement, `cofactor_apo_loss`,
  `cofactor_restoration_probe` (idealized upper bound: inject EXPERIMENTAL proximal cofactor),
  `build_cofactor_graft_fidelity_probe` (rotation/translation-invariant catalytic-residue
  pairwise-distance check of whether a rigid graft WOULD stay within a proximity cutoff;
  "No coordinates are superposed, no model is fit"), ESMFold2 apo backend.
- `bronze_silver_promotion_preview.py` — the gate. `structure_confirmability` returns
  `holo` / `apo` / `none`; the corroborated-but-apo branch already emits the decision
  `blocked_apo_needs_cofactor_fusion` — the literal hook for Task A.
- `holo_structure_promotion.py` (2026-06-14) — the REAL-holo lane (complementary; do not
  conflate). Its `holo_pdb_confirmation` provenance + `structure_confirmability` honoring it
  is the template to mirror for a recovered-geometry provenance block.

## NON-NEGOTIABLE guardrails (carry from the project discipline)

- The **heldout one-shot is SPENT** (decision_log "HELDOUT ONE-SHOT SPENT"). Develop and
  report ONLY on in-distribution train/calibration rows; the calibration split is the honest
  out-of-sample read. NEVER read or tune against the heldout bundle.
- Leakage wall: the sequence cofactor channel is the deploy-available signal (sequence only);
  EC/name/prose/lane stay excluded_context; structure stays review-only mechanism context,
  never a predictive feature.
- Frozen `curated_mechanism_labels.json` (702, sha `5eec9bef…`) NEVER written; print its sha
  before/after any apply. Registry changes go ONLY to `external_bronze_labels.json` via
  non-destructive preview + EXPLICIT `--apply`.
- Keep the honest counters SEPARATE. A recovered-geometry silver candidate is NOT the same as
  a real-holo silver candidate is NOT a tier flip — give it its OWN decision string and its
  OWN counter. Do not inflate `silver_ready` by merging recovery into real-holo.
- Measure first, non-destructive. Stop at the honest ceiling; do not game any metric.
- NOTE before you touch the registry: `external_bronze_labels.json` is at GitHub's 51.5 MB
  soft limit. Consider the LFS/split task first (it is a separate spec) so pushes do not
  degrade.

---

## TASK A — wire fusion-recovery into the promotion gate (leakage-safe recovery path)

Goal: for chemistry-corroborated APO-ONLY / PREDICTED-ONLY rows, let the gate emit a
SEPARATE, honest "silver via recovered geometry" decision when (and only when) the
deploy-available recovery actually supports it — instead of a flat `blocked_apo` /
`blocked_pending_structure`.

Definition of "recovery supported" for a row (ALL must hold, all leakage-safe):
  1. chemistry corroborates (the gate's existing nearest-centroid == assigned AND cohesion
     >= threshold) — reuse `assess_row_against_centroids`;
  2. the row's required cofactor family (the fingerprint's defining cofactor) is SUPPORTED by
     the sequence cofactor channel for this row's accession (reuse
     `sequence_cofactor_channel` predicted_cofactor_families + the
     FINGERPRINT_REQUIRED_COFACTOR_FAMILY map already in that module);
  3. a predicted (AFDB/ESMFold2) structure is available for the row; and
  4. the graft-fidelity check passes for that structure (reuse
     `build_cofactor_graft_fidelity_probe` logic: the predicted active-site scaffold is
     preserved well enough that the cofactor would stay within the proximity cutoff).

Implementation outline:
  - New module `recovered_geometry_promotion.py` (mirror `holo_structure_promotion.py`'s
    discipline: non-destructive preview + explicit apply; provenance-only registry write; row
    count unchanged; frozen sha printed before/after; cache to git-ignored data/cache/).
  - For each candidate row, compute the four conditions and, when all hold, record
    `evidence.structure_provenance.recovered_geometry_confirmation` =
    {predicted_structure_handle, required_cofactor_family, channel_support_score,
    graft_stays_within_cutoff, graft_proximity_margin_angstrom, recovery_basis:
    "sequence_cofactor_channel_fusion+graft_fidelity", calibration_membership, created_utc}.
  - Extend `bronze_silver_promotion_preview`:
    * `structure_confirmability` (or a sibling) recognizes a recovered_geometry_confirmation
      and returns a NEW state, e.g. `recovered` (do NOT return `holo` — keep it distinct).
    * `assess_promotion` maps `recovered` (for a corroborated row) to a NEW decision string
      `silver_ready_via_recovered_geometry_pending_geometry_run`, counted SEPARATELY from
      `silver_ready_pending_geometry_run`. Add a `recovered_ready_count` alongside
      `silver_ready_count` in the audit.
  - Honesty: only score rows in the train/cal manifest; rows whose recovery would need a
    heldout-bundle structure are reported as coverage gaps, never as supported. The channel is
    consumed FROZEN (no refit). Report the calibration-row (out-of-sample) numbers as the
    headline; train rows are an in-sample reference only.

Acceptance / definition of done:
  - Preview artifact + work report showing, per fingerprint: candidates, recovery-supported,
    blocked-by-each-condition (so the abstention is legible).
  - The promotion preview now reports `recovered_ready_count` > 0 on the real registry,
    SEPARATE from `silver_ready_count`; `blocked_pending_structure` drops by exactly the
    recovered count.
  - Offline unit tests (stub channel + stub graft-fidelity), including: a row that fails each
    of the four conditions stays blocked; a row meeting all four becomes
    `silver_ready_via_recovered_geometry_*`; the real-holo path is unchanged.
  - `validate` ok (702 / 37 fp); frozen byte-unchanged (sha printed); full offline suite = the
    known 10 baseline failures + 1 numpy collection error, no NEW regressions; leakage wall
    intact; counters SEPARATE.

---

## TASK B — implement real template grafting (beyond the fidelity probe)

Goal: replace the idealized `cofactor_restoration_probe` (which injects the row's OWN
experimental cofactor — not deploy-available) with a deploy-available GRAFT: place a canonical
holo cofactor context, taken from a per-fingerprint HOLO TEMPLATE, into the apo/predicted
structure, then re-derive `ligand_context` from the grafted coordinates so the router scores
real (if approximate) cofactor geometry.

Why this is the harder, higher-value piece: Task A's fusion injects cofactor families at the
FEATURE level. A real graft produces actual coordinates, so it (a) feeds the geometry router
the way experimental holo does, and (b) makes the graft-fidelity probe a true precondition
rather than a standalone diagnostic.

Implementation outline (leakage-safe, deploy-available):
  - Build a per-fingerprint CANONICAL HOLO TEMPLATE library: for each cofactor-defined
    fingerprint, pick a representative experimental holo structure (one already confirmed by
    `holo_structure_promotion`!) and extract the cofactor's local atom context + its catalytic-
    residue anchor frame. The template is keyed by FINGERPRINT, never by the target row's own
    identity (no per-row leakage).
  - Rigid graft: superpose the template's catalytic-residue anchor frame onto the apo/predicted
    structure's corresponding catalytic residues (the residues the router already uses), then
    place the template cofactor atoms by that transform. Use `structure.py` helpers
    (`select_residue_atoms`, `residue_centroid`, `pairwise_distances`, `atom_position`).
  - Re-derive `ligand_context` from the grafted coordinates (`ligand_context_from_atoms`) so
    the router sees grafted cofactor geometry, not an injected feature flag.
  - Gate the graft by the EXISTING fidelity check (worst active-site distance distortion vs the
    template cofactor's proximity margin) — a graft that would not stay proximal is abstained.
  - Score recovery through `predicted_geometry_recovery.py`'s leakage-safe harness on the
    calibration rows; compare grafted-geometry recovery to the feature-fusion recovery and to
    the idealized restoration upper bound. The heldout is NOT read.

Acceptance / definition of done:
  - A grafting function that outputs grafted coordinates (or grafted ligand_context) for a
    (fingerprint-template, apo-structure) pair, deterministic, with the fidelity gate applied.
  - A recovery artifact comparing, on calibration rows: predicted-apo vs feature-fusion vs
    grafted-geometry vs idealized-restoration, with the grafted number BETWEEN fusion and the
    idealized bound (sanity), reported honestly with coverage gaps.
  - Once Task A is wired, the graft becomes the structure backing a
    `recovered_geometry_confirmation` (Task A condition 4 upgraded from "would-stay-proximal"
    to "grafted + stayed proximal").
  - Offline unit tests (synthetic template + synthetic apo): graft places atoms within cutoff
    when the scaffold is preserved, abstains when distorted; no per-row self-leak (template is
    fingerprint-keyed); deterministic.
  - All guardrails as Task A.

---

## Suggested order

1. (Pre-req, separate spec) registry LFS/split — so the gate-wiring apply does not push a
   51 MB+ blob.
2. TASK A first (wiring) — it reuses everything that exists and yields `recovered_ready_count`
   immediately; it is the smaller, higher-certainty win.
3. TASK B (real grafting) — upgrades Task A's condition 4 from "feasible" to "done" and gives
   the router real grafted geometry; larger and more uncertain.
4. Only then consider running the SEPARATE authorized geometry-confirmation to flip
   silver_ready (real-holo) AND recovered_ready rows to actual silver tier.

## First commands to orient (non-destructive, run these before coding)

    PYTHONPATH=src python -m catalytic_earth.cli validate
    # current gate state + how many corroborated rows are apo-only (Task A's candidate pool):
    PYTHONPATH=src python -m catalytic_earth.cli build-bronze-silver-promotion-preview --out /tmp/promo.json
    # inspect the existing recovery harness outputs / docstrings:
    #   src/catalytic_earth/predicted_geometry_recovery.py
    #   src/catalytic_earth/cofactor_fusion_operating_point.py
    #   src/catalytic_earth/predicted_geometry_robustness.py  (build_cofactor_graft_fidelity_probe)
    #   src/catalytic_earth/sequence_cofactor_channel.py      (_fused_geometry_features, FINGERPRINT_REQUIRED_COFACTOR_FAMILY)
