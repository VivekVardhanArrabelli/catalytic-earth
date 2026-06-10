# Scaling Plan to 10k Mechanism Labels

Status: durable plan (2026-06-10). This is an entry point for future agents. Read
this first, then verify every claim below against the cited `docs/decision_log.md`
entries and source modules before acting — two grounding errors in the session that
produced this plan (ESM2, and apo-vs-holo promotion confirmability) both came from
asserting decision-claims without first reading the log. Treat any
performance/promotion/capability claim as requiring a decision-log citation.

---

## The one reframe everything depends on

**10k is not 10k rows. It is a balanced, non-redundant mechanism atlas where the
frozen 702 benchmark never moves and every label earns its place.** The repo's own
findings force this:

- Broad out-of-scope draining is **saturated** — a page-3/4 continuation over
  high-yield lanes "produced 2,793 continuation candidates but added **0** new
  candidate IDs"; the lesson is to split into new EC/keyword subqueries, not
  increase page depth (`decision_log.md`, handoff 2026-06-09).
- The positive classes are **30.8× imbalanced** (fingerprint Gini 0.51,
  positive:OOS 0.42) — coverage/redundancy governor, 2026-06-10.
- **26.7%** of what we already imported (456 of 1,710) would be re-throttled as
  near-duplicates by the novelty gate, concentrated in out_of_scope (373) and
  `metal_dependent_hydrolase` (71) — novelty gate self-audit, 2026-06-10.

So raw count is not the constraint; **diverse, honest supply is.** Chasing 10k of
the current 8 fingerprints by volume would manufacture redundancy and violate the
values.

---

## What is fixed, by our values (non-negotiable)

- **The frozen 702 benchmark is sacred.** `data/registries/curated_mechanism_labels.json`
  = 702 labels (562 in-distribution + 140 heldout); `coherence_audit_702` baseline;
  eval contract `sha256:731b94ebd3b4f7ae483a3cca75d2b8c3b88242024ecd9c364d70bdfcda6624ee`.
  All three are pinned by regression tests (`tests/test_geometry_artifact_regression.py`).
  The atlas grows in the **separate** expansion registry
  `data/registries/external_bronze_labels.json`; the benchmark is byte-unchanged. A
  v2 benchmark, if ever needed, is a **new** expert-reviewed freeze, never an edit of
  this one. The spent one-shot heldout read must not be re-run or tuned against
  (2026-06-04).
- **The leakage wall is absolute.** EC / protein-name / UniProt prose / curated text
  / `target_family_lane` stay in `excluded_context`, never predictive features; EC
  may decide **scope only**. Enforced in code by
  `labels._validate_external_out_of_scope_evidence_separation` and by
  `tests/test_leakage_closure.py`; the representation loop's featurizer has a unit
  test that mutates EC+name+lane+fingerprint and asserts the features are
  byte-identical.
- **The label gate is the only door in** (`src/catalytic_earth/`):
  `external_annotation_anchored_import.classify_row` (default = **HOLD**; a positive
  requires an annotation lane mapped to a fingerprint **and** the matching annotated
  cofactor class) → `labels.MechanismLabel.from_dict` (schema + leakage-separation
  validation) → `external_annotation_anchored_import.apply_external_annotation_anchored_import_to_registry`
  (dedup vs **both** registries, re-validate every label, **non-destructive
  append**, writes only the expansion registry). Nothing bypasses this. Review
  artifacts are **not** imports.
- **Bronze is honest.** `tier=bronze`, `review_status=automation_curated`,
  `evidence_basis=reviewed_swissprot_ec_rhea_cofactor_annotation`; structure/geometry
  confirmation is a **deferred** bronze→silver signal, not faked (2026-06-09 "the 10k
  unlock").
- **Do not scale model size.** The representation shootout settled it
  (`docs/wave1_representation_shootout.md`, 2026-05-26): ESM-2 150M (primary acc
  0.578), ESM-C, ProtT5, SaProt all **underperform** Foldseek (0.622) and the
  geometry baseline (1.000 on dense/near-orphan bins). "Do not scale models first."
  The Northstar Pivot (2026-05-31) showed the binding constraint is **feature
  overlap**, not the combiner. Use chemistry/geometry features only. The learned
  mechanism-feature embedding (Lever 2) is a recorded clean **negative** — it does
  not deployably beat geometry.
- **Safety scope** (`docs/safety_scope.md`): beneficial enzyme function only;
  outputs are hypotheses/candidates requiring wet-lab validation; never "confirmed"
  / "validated" without experimental backing.

---

## The pipeline (every new label runs this, in order)

```
reviewed UniProt/Swiss-Prot row (EC + cofactor + Rhea + active-site residues)
  → classify_row          scope from annotation; positive needs cofactor corroboration; else HOLD
  → governor              is this fingerprint/lane a hole / under-floor / over-cap?   (build-coverage-redundancy-audit)
  → novelty gate          admit only if it adds a new cluster/reaction/organism; throttle near-dups   (build-novelty-admission-gate-audit)
  → from_dict + writer    schema + leakage gate; dedup vs BOTH registries; non-destructive append
  → (later) promotion     bronze→silver ONLY via cofactor restoration/fusion, never apo geometry   (build-bronze-silver-promotion-preview)
```

The governor and novelty gate make growth diverse **by construction**; everything
else already existed. All four CLI tools above are non-destructive (write only to
`artifacts/` + `work/`, never a registry).

---

## The stages

### Stage 0 — Unblock sourcing (environment)
The cloud sandbox blocks UniProt (HTTP 403) and lacks mmseqs / ML backends, and the
hand-curated candidate pools are **drained**. A local/laptop env restores real
UniProt network and (on Mac) mmseqs. Nothing downstream proceeds without this.
Guardrails travel with the work regardless of env.

### Stage 1 — Close the holes (≈339 positive labels; highest value)
Source the holes and under-floor fingerprints to the **100-floor**, via targeted
EC/keyword **subqueries** (not deeper pages). Cap `metal_dependent_hydrolase` (308,
over the 250 ceiling, most redundant at 2.96 labels/distinct-reaction) — add none.

| fingerprint | combined | status | route |
| --- | --- | --- | --- |
| `ser_his_acid_hydrolase` | 42 (0 expansion) | HOLE | triad locator + acquisition contract: EC 3.4.21/3.4.16/3.1.1, **no cofactor**, coordinate Ser-His-Asp triad corroborated against annotated ACT_SITE (`build-ser-his-triad-locator-scan`). The one fingerprint the cofactor engine structurally can't reach. |
| `radical_sam_enzyme` | 10 | HOLE | disambiguation rule (Fe-S+SAM / CX3CX2C). The representation loop already proposed **14 candidates from our own OOS pile** — start there + fresh sourcing. |
| `cobalamin_radical_rearrangement` | 10 | HOLE | disambiguation rule (adenosylcobalamin + mutase EC 5.4.99/5.4.3/4.2.1.28/30/4.3.1.7). |
| `flavin_monooxygenase` | 43 | under-floor | EC 1.14.13/1.14.14, flavin no-heme. |
| `heme_peroxidase_oxidase` | 69 | under-floor | EC 1.11.1, heme. |
| `flavin_dehydrogenase_reductase` | 87 | under-floor | EC 1.3/1.6/1.8.1, flavin no-heme. |

Everything routes through the governor + novelty gate so orthologs are not
re-imported.

### Stage 2 — Grow the ontology (the bulk of the climb)
8 fingerprints × 250 cap ≈ **2,000 positives max** — so 10k honestly **requires more
mechanism families**. The coherence audit already flags this: `metal_dependent_hydrolase`
is a coarse bucket collapsing proteases/nucleases/phosphatases/deaminases, queued as
v2 splits. This is the repo's **Lever 4 — expand the family set**. Each new family /
v2 split is added the same disciplined way:

1. Define the fingerprint spec in `data/registries/mechanism_fingerprints.json`
   (cofactor chemistry + active-site residue-role signature + reaction-center bond
   change) and the family node in `data/registries/mechanism_ontology.json`.
2. Add a cofactor+EC rule to `external_cofactor_ec_disambiguation.DISAMBIGUATION_RULES`
   and lane mappings to `external_annotation_anchored_import.LANE_PRIMARY_FINGERPRINT`
   / `COFACTOR_FOR_FINGERPRINT`.
3. Source annotation-anchored bronze under the governor + novelty gate.

Breadth of chemistry, not depth of one bucket, is where 10k comes from.

### Stage 3 — Diverse OOS, novelty-gated
OOS is the abstention target and must keep growing in **coverage**, not redundancy.
Route every candidate through the novelty gate's cluster key
`(scope, full-EC, organism, sequence-length bin)`; admit only new
clusters/reactions/organisms. On Mac, upgrade the gate's metadata near-dup proxy to
true **mmseqs sequence clustering** — a strictly better dedup dimension than
metadata.

### Stage 4 — Bronze→silver promotion, the honest way
Promotion is gated by **cofactor presence in the coordinates**, and 103/104 of our
coordinate-bearing rows are **apo** — the geometry inverse-gate abstains on 100% of
apo (the documented Problem-2 degradation; experimental-apo and predicted-apo both
abstain). So promotion does **not** wait for more predicted structures. The working
lever is **cofactor restoration/fusion**: restoration recovers 22/22 lost primaries
(2026-06-04); the fused sequence→cofactor channel lifted heldout 23→37/45 (one-shot,
**spent** — do not re-run). Run the cofactor-fusion channel (locally, with backends)
over the promotion preview's chemistry-corroborated queue; resolve the **51
representation-loop review-outliers** (chemistry disagrees with the label) first.
Silver is earned per-row, never bulk-flipped.

### Stage 5 — A v2 benchmark, only when the atlas is broad
A 702-row benchmark over 8 families cannot validate a 10k atlas across many
families. When Stage 2 has matured the ontology, freeze a **new** expert-reviewed v2
benchmark (its own SHA; conjunctive win condition — mechanism prediction **and**
calibrated abstention on tail/hard-negative cases; cluster-bootstrapped, not
entry-bootstrapped). The current 702 stays frozen forever as the v1 anchor.

---

## The honest caveats (so we don't fool ourselves)

- **The cap math is the real story.** 10k forces ontology breadth (Stage 2). If we
  refuse to expand families, the honest ceiling is ~2k positives + diverse OOS, and
  padding to 10k with redundant OOS would violate the values. Say so rather than hit
  10k dishonestly.
- **Promotion may stay mostly bronze** until cofactor restoration is run at scale —
  and that is fine. Bronze is an honest tier; silver is earned, not assumed.
- **Beware the "receding horizon"** (`docs/MAP.md`): per-row deployment-blocker
  grinds (Lever 3/4 chores) that the framing can manufacture infinitely. This plan
  is sourcing-and-diversity-bound, not blocker-bound; if a lever turns into infinite
  per-row chores, stop feeding it.

---

## Assets already built (this plan's tooling)

All merged to `main`, all non-destructive, leakage-safe, with tests:

- `coverage_redundancy_audit.py` — the governor (balance/redundancy + acquisition
  targets). CLI `build-coverage-redundancy-audit`.
- `ser_his_triad_locator.py` — Ser-His-Asp triad corroborator + acquisition contract
  for the ser_his hole. CLI `build-ser-his-triad-locator-scan`.
- `novelty_admission_gate.py` — online near-dup/saturation filter feeding the apply
  path. CLI `build-novelty-admission-gate-audit`.
- `mechanism_representation_loop.py` — leakage-safe chemistry representation
  (cofactor/ligand + residue roles; LOO self-consistency 0.895); triages promotion,
  proposes hole candidates. CLI `build-mechanism-representation-loop`.
- `bronze_silver_promotion_preview.py` — promotion queue gated on **cofactor presence
  in coordinates** (not provenance). CLI `build-bronze-silver-promotion-preview`.

---

## One-line summary

**Unblock sourcing → close the holes → broaden the ontology → diverse
novelty-gated OOS → earn silver via cofactor fusion → freeze a v2 benchmark when
ready** — all behind the frozen-702 wall, the leakage wall, and the governor.
