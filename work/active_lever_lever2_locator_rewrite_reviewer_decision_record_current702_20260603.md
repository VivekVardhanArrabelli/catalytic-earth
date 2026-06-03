# Active Lever 2 Source-Free Locator Rewrite — Reviewer Decision Record (current702)

Run: 2026-06-03

Human reviewer decision record for the 55 priority-1 current702 source-free
locator rewrites (Lever 2). It records the explicit per-row approve/reject
decision after a full per-row review, with candidate and planned-payload hashes
preserved unchanged from the committed review-only approval packet. It does not
copy locator sidecars, score heldout rows, or apply the frozen residual
threshold.

## Decision summary

- Reviewed rows: 55 (32 in-scope primaries, 23 out-of-scope negatives)
- **Approved: 53**
- **Rejected: 2** — `m_csa:723`, `m_csa:599`
- Integrity: 55/55 candidate hashes match; 0 forbidden-feature flags; all
  split-protected (review_only, not for training/threshold/import).

## What a source-free locator is

The Lever 2 heldout mechanism feature must be computed without leaking the
M-CSA label. A source-free locator picks active-site residues purely from **3D
proximity to a bound cofactor/metal in a PDB structure**, mapped to
UniProt-validated sequence positions (`struct_ref_seq`). No catalytic-role
annotation, mechanism text, EC/Rhea ID, name, or label is used.

## Review bar (in-scope vs out-of-scope)

The 55 heldout rows split by curated label type:

- **in-scope primary** (`seed_fingerprint`): the model must correctly *retain*
  the row, so the locator MUST land on the genuine catalytic center.
- **out-of-scope** (`out_of_scope`): the model must *abstain*; the locator only
  needs to be a faithful source-free pointer to the protein's real
  cofactor/metal site.

## The two rejections

Both are **in-scope `ser_his_acid_hydrolase`** rows. A Ser-His-Asp/Glu serine
hydrolase has **no cofactor or catalytic metal**, so the ligand-proximity method
cannot reach its catalytic triad and instead latched onto an adventitious metal:

- **m_csa:723** (P00782, subtilisin, 1S01) — anchored on the **structural Ca
  loop** (ILE186/ASP148/VAL188/ASN184/LEU182/GLN109, backbone carbonyls + surface
  side chains). The Ser-His-Asp triad is absent from the locator. Clear
  mis-anchor.
- **m_csa:599** (P36936, 1FY2) — anchored on a crystallographic **Cd** ion
  (His227/Glu224); the curated rationale states *"no metal required for target
  fingerprint."* Misses the Ser nucleophile and depends on a non-physiological
  metal.

These two are not just bad rows — they expose a **method gap**: ligand-proximity
locators structurally cannot locate cofactorless catalytic triads.
**Decision:** design a source-free catalytic-triad geometric locator (see below)
rather than force a ligand anchor for serine hydrolases.

## The 53 approvals

- **In-scope, catalytic center correctly anchored (30):** PLP rows capture the
  catalytic-Lys Schiff base at ~1.3-1.45 A (covalent internal aldimine);
  m_csa:115 captures the covalent 8a-His-FAD bond (1.30 A); m_csa:250 the
  Cys-ligated heme of chloroperoxidase; metal hydrolases show proper
  His/Asp/Glu-metal first shells at 1.7-2.5 A; m_csa:323 the four Cys ligating a
  4Fe-4S cluster.
- **Out-of-scope, faithful cofactor/metal anchor, abstention expected (23):**
  all point at a real ligand/metal site. Even structural-metal anchors
  (m_csa:370 KDM4A Cys3His zinc, m_csa:384 MetRS zinc knuckle) are truthful
  source-free sites and should still fall out-of-distribution.
- **Watch-items inside the approve set (approved, flagged for downstream
  sensitivity):** the 5 OOS minimum-locator rows (56/199/356/480/541, 2 contacts
  each, clean carboxylate/His metal ligands); m_csa:853 (B12 corrin periphery,
  not the Co axial center); m_csa:180 / m_csa:220 (backbone-carbonyl-heavy Mg
  shells).

## Per-row verdicts

| row | acc | PDB | ligand | locs | warn | scope | fingerprint | verdict |
| --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| m_csa:3 | P15559 | 1D4A | FAD | 8 | 0 | in-scope | flavin_dehydrogenase_reductase | approve |
| m_csa:9 | P31153 | 5A1I | SAM | 8 | 0 | OOS | — | approve |
| m_csa:32 | Q04760 | 1QIN | ZN | 3 | 0 | OOS | — | approve |
| m_csa:43 | P80366 | 4KBP | FE | 4 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:44 | P00634 | 1ALK | ZN | 4 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:45 | P43379 | 1CDG | CA | 6 | 0 | OOS | — | approve |
| m_csa:46 | P14385 | 2ADM | SAM | 8 | 0 | OOS | — | approve |
| m_csa:97 | P0ABF6 | 1CTT | ZN | 3 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:109 | Q02127 | 1D3G | FMN | 8 | 0 | in-scope | flavin_dehydrogenase_reductase | approve |
| m_csa:115 | Q9T0N8 | 1W1O | FAD | 8 | 0 | in-scope | flavin_dehydrogenase_reductase | approve |
| m_csa:121 | P07850 | 1SOX | HEM | 8 | 0 | OOS | — | approve |
| m_csa:131 | P20586 | 1DOC | FAD | 8 | 0 | in-scope | flavin_monooxygenase | approve |
| m_csa:159 | P0A434 | 1HZY | ZN | 3 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:163 | P0A7Y4 | 1RDD | MG | 3 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:171 | P00730 | 1M4L | ZN | 3 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:180 | P35505 | 1HYO | MG | 5 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:188 | P09147 | 1XEL | NAD | 8 | 0 | OOS | — | approve |
| m_csa:211 | P38489 | 1IDT | FMN | 8 | 0 | in-scope | flavin_dehydrogenase_reductase | approve |
| m_csa:220 | P20906 | 1MCZ | MG | 3 | 0 | OOS | — | approve |
| m_csa:239 | P00433 | 7ATJ | HEM | 8 | 0 | in-scope | heme_peroxidase_oxidase | approve |
| m_csa:242 | Q8I914 | 2F9R | MG | 3 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:250 | P04963 | 2CPO | HEM | 8 | 0 | in-scope | heme_peroxidase_oxidase | approve |
| m_csa:311 | P00924 | 7ENL | MG | 3 | 0 | OOS | — | approve |
| m_csa:321 | P09155 | 1YT3 | ZN | 4 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:323 | P05314 | 2AKJ | SF4 | 8 | 0 | OOS | — | approve |
| m_csa:333 | Q9RUB5 | 2O1X | MG | 3 | 0 | OOS | — | approve |
| m_csa:352 | P00949 | 3PMG | MG | 3 | 0 | OOS | — | approve |
| m_csa:370 | O75164 | 2YBP | ZN | 4 | 0 | OOS | — | approve |
| m_csa:384 | P23395 | 1A8H | ZN | 4 | 0 | OOS | — | approve |
| m_csa:392 | P07801 | 1AF7 | SAH | 8 | 0 | OOS | — | approve |
| m_csa:397 | P04063 | 1AMY | CA | 5 | 0 | OOS | — | approve |
| m_csa:403 | P07584 | 1AST | ZN | 4 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:418 | P37821 | 1B8G | PLP | 8 | 0 | in-scope | plp_dependent_enzyme | approve |
| m_csa:419 | O52552 | 1B9H | PLP | 8 | 0 | in-scope | plp_dependent_enzyme | approve |
| m_csa:497 | Q9FDN7 | 1YCF | FMN | 8 | 0 | OOS | — | approve |
| m_csa:517 | P61517 | 1I6P | ZN | 4 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:526 | P11708 | 4MDH | NAD | 8 | 0 | OOS | — | approve |
| m_csa:545 | Q7M523 | 1F2D | PLP | 8 | 0 | in-scope | plp_dependent_enzyme | approve |
| m_csa:551 | P15245 | 1FOH | FAD | 8 | 0 | in-scope | flavin_dehydrogenase_reductase | approve |
| m_csa:709 | P00431 | 1DJ1 | HEM | 8 | 0 | in-scope | heme_peroxidase_oxidase | approve |
| m_csa:710 | P25524 | 1RA0 | FE | 4 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:714 | P0ABI8 | 1FFT | HEO | 8 | 0 | in-scope | heme_peroxidase_oxidase | approve |
| m_csa:723 | P00782 | 1S01 | CA | 6 | 0 | in-scope | ser_his_acid_hydrolase | REJECT |
| m_csa:750 | P55792 | 1U8V | FAD | 8 | 0 | OOS | — | approve |
| m_csa:853 | P31570 | 1G64 | B12 | 8 | 0 | in-scope | cobalamin_radical_rearrangement | approve |
| m_csa:854 | P80147 | 1OHV | PLP | 8 | 0 | in-scope | plp_dependent_enzyme | approve |
| m_csa:916 | P9WI55 | 4Z71 | MG | 3 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:990 | Q8GS60 | 5DQR | FAD | 8 | 0 | in-scope | flavin_dehydrogenase_reductase | approve |
| m_csa:994 | Q9Y3Z3 | 4BZC | MN | 4 | 0 | in-scope | metal_dependent_hydrolase | approve |
| m_csa:56 | Q9WZW0 | 1ZE1 | MG | 2 | 1 | OOS | — | approve |
| m_csa:199 | P04425 | 1GSA | MG | 2 | 1 | OOS | — | approve |
| m_csa:356 | P14769 | 1VZX | MN | 2 | 1 | OOS | — | approve |
| m_csa:480 | P26214 | 1CZF | ZN | 2 | 1 | OOS | — | approve |
| m_csa:541 | P75430 | 1U3F | MG | 2 | 1 | OOS | — | approve |
| m_csa:599 | P36936 | 1FY2 | CD | 2 | 1 | in-scope | ser_his_acid_hydrolase | REJECT |

## Verification (read-only, no writes)

Validated the recorded decisions against the materialization gate and intake
preflight in-memory, with no sidecar writes and no heldout read:

- Materialization gate: 53 `approved_ready_for_materialization`, 0 invalid
  approval records, 0 unmatched, **0 critical violations**, 0 sidecars written.
  Remaining blockers are only `approved_locator_sidecar_write_flag_not_enabled`
  and `approved_locator_sidecars_not_materialized` (cleared by the separate
  write-enabled materialization step).
- Source-decision intake preflight: status `...ready`; 55 explicit Lever 2
  decisions, 53 locator-materialization-ready approvals, 2 rejections, 0 invalid,
  0 source-edit-contract violations; `locator_materialization_gate_ready: True`.
  (23 Lever 3/4 rows remain pending — out of scope for this decision.)

## Serine-hydrolase method gap — triad-geometry locator (decision: design)

The ligand-proximity locator cannot serve cofactorless Ser-His-Asp/Glu
hydrolases. Proposed source-free catalytic-triad geometric locator:

1. **Candidate nucleophile detection** — scan the structure for Ser/Cys/Thr OG/SG
   within H-bond distance (~2.6-3.2 A) of a His ND1/NE2.
2. **Acid completion** — require an Asp/Glu carboxylate O within ~2.6-3.2 A of the
   His's other imidazole nitrogen, giving a closed nucleophile-His-acid triad.
3. **Source-free guardrails** — derive everything from coordinates + residue
   identity only; forbid mechanism text, roles, EC/Rhea, names, labels, panel IDs
   (same `forbidden_feature_audit` contract as the ligand locator).
4. **Schema reuse** — emit the same `residue_locators` shape (>=2 sequence
   positions, UniProt-validated) with `locator_evidence_class:
   structure_local_catalytic_triad_geometry_without_source_text`, so the
   downstream geometry channel consumes it unchanged.
5. **Scope** — apply to ser_his_acid_hydrolase heldout rows (m_csa:723, m_csa:599
   here) and validate it reproduces the known triad before any approval.

Implementation is a new fail-closed gate, to be built and reviewed separately
before any heldout read.

## Guardrails (this record)

No labels, registries, ontologies, imports, production thresholds, or model
weights changed. No locator sidecars copied. No heldout rows evaluated. The
committed review-only approval packet and materialization gate are unchanged;
decisions are recorded in the separate approval-decisions artifact.
