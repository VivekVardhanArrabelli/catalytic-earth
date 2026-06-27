# Catalytic-residue-identity sidecar — separating the no-reaction families (2026-06-27)

User-directed ("go for sidecar", after "backfilling is a bit scary"). The reaction representation
recovered every cofactor-free family that carries a Rhea reaction, but two genuinely featureless
families remained collapsed — `cysteine_protease` and `ser_his_acid_hydrolase` — because they carry
**no Rhea reaction at all** (peptide-bond hydrolysis is unannotated in Rhea). In the cofactor +
bond-change space they are identical empty vectors. The discriminator is the **catalytic-residue
identity**: a cysteine protease attacks with a catalytic **Cys**, a Ser-His-Asp hydrolase with a
catalytic **Ser**.

## Why a sidecar (not a backfill)

Modifying ~9,800 curated bronze rows to add residue identity is risky. Instead the identity lives in
a **read-only, additive sidecar** — `artifacts/v3_catalytic_residue_identity_sidecar_current702.json`
— a plain `accession -> [amino acids at the annotated ACT_SITE positions]` map. The bronze registry
is **byte-for-byte unchanged** (sha verified identical before/after every step). The representation
attaches the identities to in-memory rows at load time and adds leakage-safe
`cat_res_{cys,ser,thr,tyr,his,lys,arg,asp_glu}` features; if the sidecar is absent the features are
simply 0 (graceful, reversible by deleting the file).

The residue identity is curated active-site structural evidence — the same leakage-safe category as
cofactor identity — never EC / name / prose / fingerprint. The sidecar is keyed by accession; the
feature is keyed by the residue letter, so perturbing EC/name/fingerprint cannot change it (unit
tested).

## Build (read-only)

`scripts/build_catalytic_residue_identity_sidecar.py` reads the ACT_SITE positions already stored in
the rows, batch-fetches each accession's sequence from UniProt (~50 batched queries), and records the
amino acid at each position. 4,931 active-site accessions, **0 missing sequences, 0 out-of-range
positions**. Writes only the sidecar.

## The design decision: weight, not just presence

At full weight the feature is a net win (LOO 0.733 -> 0.766) but **introduces regressions** where
families share a catalytic residue: peroxiredoxin's catalytic Cys collides with the protease Cys
(0.95 -> 0.81), and paps_sulfotransferase's catalytic His blurs against everything (0.93 -> 0.48).
The residue identity is a **secondary** structural feature — decisive where it is the only signal,
but it must not override families that already separate on cofactor or reaction. A weight sweep on
the live registry found the Pareto-safe operating point:

| weight | overall LOO | gains (>+0.03) | regressions (<-0.03) |
| --- | --- | --- | --- |
| off | 0.733 | – | – |
| **0.15 (chosen)** | **0.743** | **3** | **0** |
| 0.20 | 0.757 | 6 | 1 (zinc_lyase) |
| 1.00 | 0.766 | 13 | 8 |

`CATALYTIC_RESIDUE_WEIGHT = 0.15` is the no-regression point.

## Result (PYTHONHASHSEED 0/7/42, identical)

| fingerprint | before | after |
| --- | --- | --- |
| **ser_his_acid_hydrolase** | 0.0 | **0.67** ← recovered |
| cysteine_protease | 0.94 | 0.97 (sharpened) |
| metallo_amidohydrolase_deaminase | 0.70 | 0.73 |
| short_chain_dehydrogenase_reductase | 0.07 | 0.13 |
| **overall leave-one-out** | 0.733 | **0.743** |
| every other family | — | unchanged (zero regressions) |

`ser_his` — the last collapsed cofactor-free family — is recovered, and the two no-reaction families
(catalytic Cys protease vs catalytic Ser hydrolase) are now separated **without any fold/name
leakage and without touching the registry**.

## The honest limit (recorded, not hidden)

Higher weights additionally recover `metallopeptidase` (0.21 -> 0.93), but that gain is *coupled* to a
`zinc_lyase_hydratase` regression — both are metal+His families a **generic** catalytic-residue
feature cannot tell apart. Separating those would need a metal-ligand-specific or
residue-position/spacing feature, not the identity alone. Chosen point holds the no-regression line;
the metallopeptidase headroom is left as recorded future work.

## Verification

- 3 unit tests (attach adds the right classes; keyed by accession not EC; graceful without sidecar).
- Representation-loop test updated to the recovered ser_his baseline; full file green across
  PYTHONHASHSEED 0/7/42.
- Registry sha byte-identical before/after the entire sidecar build + feature wiring.
- Leakage guardrail `ec_name_prose_lane_used` stays False.

Cumulative across the session's representation work: overall LOO **0.699 -> 0.718 -> 0.733 -> 0.743**,
recovering three collapsed cofactor-free families (peroxiredoxin, metal-independent PDE, ser_his)
with zero net regressions, all leakage-safe and registry-clean.
