# Fresh Leakage-Safe Downstream Evaluation Design

Status: design artifact only; not implemented, not a benchmark result.

Created: 2026-06-14

## Purpose

The existing heldout one-shot has been spent. Future performance claims need a fresh
evaluation surface that is frozen before model, threshold, or admission changes are
selected against it.

This design separates three things:

- Atlas growth and registry curation.
- Train/calibration development for source-free predictive features.
- A future frozen evaluation surface that is read once for a documented claim.

## Non-Negotiable Leakage Wall

- EC numbers, Rhea IDs, UniProt names/prose, source lane names, admission handles,
  labels, and curation status are excluded from predictive features.
- EC/Rhea/source annotations may be used only for scoping, stratification, and audit
  reporting under `excluded_context`.
- Counted corroboration remains mechanism-first: Rhea/cofactor/cosubstrate,
  active-site, domain, cluster, or structure evidence. EC alone never admits a row.
- The frozen current702 registry remains read-only and is not rewritten or enlarged.

## Proposed Surfaces

1. **Development train/calibration surface**
   - Built only from currently admitted bronze/silver rows whose labels are already
     accepted by the registry gates.
   - Used for feature engineering, threshold selection, abstention policy, and
     family-level calibration.
   - Can be refreshed as registries grow, but every refresh must record row hashes
     and exclude any future eval candidates.

2. **Prospective shadow-eval queue**
   - Newly sourced rows held back before feature or threshold development sees them.
   - Rows must pass the normal mechanism-first admission gates, novelty checks, and
     source-contract validation.
   - The queue is review-only until explicitly frozen; no benchmark claim attaches
     to this queue.

3. **Frozen downstream eval surface**
   - Selected from the shadow queue after source review closes.
   - Frozen by row IDs, source hashes, feature-input hashes, and excluded-context
     hashes before any scoring run.
   - Read once for the final downstream claim. Any additional reads are labeled as
     post-hoc diagnostics, not benchmark selection.

## Stratification

The frozen surface should report both macro and family-stratified results:

- Mechanism family.
- Tier at freeze time: bronze, silver-ready, silver-confirmed.
- Structure state: holo, apo, predicted/unknown, no PDB.
- Corroborator class: Rhea/cofactor, active-site, domain, cluster, structure.
- Source family/lane and organism diversity as excluded-context audit fields only.

At least one split should stress high-risk growth areas: metallopeptidase,
metallophosphoesterase/nuclease, racemase/epimerase, glycosyltransferase,
hydrolase/phosphatase, and redox/cofactor families.

## Minimum Freeze Artifact

Before scoring, write an artifact with:

- Eval row IDs and source accessions.
- Registry manifest hash and current702 SHA.
- Feature-input hashes for every source-free predictive feature.
- Excluded-context hashes for EC/Rhea/source/audit metadata.
- Declaration that no heldout one-shot rows or threshold decisions were reused.
- A command that can reproduce the exact row set without writing registries.

## Acceptance Bar

The first valid implementation should pass:

- Registry validation and loader tests.
- Leakage/source-contract tests.
- Novelty/admission tests.
- A freeze/replay test proving row IDs and feature-input hashes are stable.
- A report test proving EC/Rhea/source text appear only in excluded-context fields.

## Current Recommendation

Do not implement the frozen downstream eval until the next shadow queue has enough
mechanism diversity to avoid another tiny one-shot. In the meantime, keep producing
train/calibration-only diagnostics and freeze candidates without using them to tune
thresholds.
