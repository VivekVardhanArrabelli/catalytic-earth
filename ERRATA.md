# Catalytic Earth errata

**Effective:** 2026-07-13

This file corrects public-facing interpretations without deleting the original
artifacts. Artifact bytes and historical session records remain available for
audit. `CLAIMS.md` is the canonical current claim ledger.

## ER-001 — M-CSA holdout independence

- **Affected claim:** CE-005.
- **Previous wording:** the June 28 M-CSA surface was never-touched,
  leakage-safe independent validation and supported a deployment claim.
- **Correction:** the 126 later-frozen rows came from a heldout partition that
  had already been scored, including in the June 4 cofactor-fusion artifact.
  The June 28 numbers remain a retrospective diagnostic, but the surface was
  not independent and is permanently exhausted.
- **Required citation:**
  `data/governance/exposure_ledger.jsonl`, events EXP-0001, EXP-0002,
  EXP-0004, EXP-0005, and EXP-0009.

## ER-002 — chemistry endpoint

- **Affected claim:** CE-003.
- **Previous wording:** chemistry recovered 76% of mechanisms.
- **Correction:** 160/210 (76.19%) is coarse cofactor-bucket consistency.
  Exact fingerprint recovery was 65/210 (30.95%) on the featurizable,
  centroid-covered positive subset. Both numbers must be shown together.
- **Required caveat:** the similarity distributions did not establish a useful
  ID/OOS abstention boundary by themselves.

## ER-003 — current702 quality tier

- **Affected claim:** CE-001.
- **Previous wording:** `current702` is expert-curated gold or contains project
  gold labels.
- **Correction:** it is a project benchmark surface with 685 bronze, 17
  silver, and zero project-gold rows; 683 rows were automation-curated and 19
  author-reviewed. Upstream expert sources do not make downstream automated
  transfers independently reviewed.

## ER-004 — what 10,001 counts

- **Affected claim:** CE-002.
- **Previous wording:** 10,001 mechanisms were mapped.
- **Correction:** the total combines 8,305 positive fingerprint assignments
  and 1,696 OOS protein-label records. It counts neither distinct net reactions
  nor independently established catalytic mechanisms.

## ER-005 — undefined global coverage percentage

- **Affected claim:** CE-004.
- **Previous wording:** 57 fingerprints/54 families cover about 2% of known
  mechanism space.
- **Correction:** the percentage is withdrawn. No common unit or denominator
  was defined across reactions, mechanisms, families, fingerprints, EC
  classes, and protein records.

## ER-006 — Swiss-Prot/PDB-holo gold and deployment wording

- **Affected claim:** CE-006.
- **Previous wording:** the June 29 surface was independent mechanism gold,
  showed fail-safe deployment readiness, and was the last non-lab rung.
- **Correction:** it is a spent EC-proxy surface. Overall recovery was 45/64,
  including 2/16 metal, with 2/72 OOS false positives. Its labels were produced
  by a fixed EC-to-family mapping, not independent stepwise-mechanism
  adjudication. The 40% OOS ceiling was too permissive for deployment, and the
  three-family success view is post-hoc.

## Propagation rule

Current entry documents must link to this file and `CLAIMS.md`. Historical
documents may preserve old wording only when clearly marked historical or
superseded. Generated interfaces must expose corrections next to affected
results rather than requiring users to discover this file separately.
