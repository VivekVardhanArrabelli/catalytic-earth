# Packet 1 TM Verification and m_csa:497 Review - 2026-05-27

This is a review-only follow-up to the Packet 1 disposition. It records expert
review of `m_csa:497` and TM-pair verification for `m_csa:428`, `m_csa:440`,
and `m_csa:477`. No label registry, ontology, fingerprint registry, import,
threshold, production scorer, or model output changed.

## m_csa:497

Recommendation: relabel `m_csa:497` from
`flavin_dehydrogenase_reductase` to `out_of_scope`.

Rationale: the curated M-CSA mechanism describes nitric oxide reduction at a
non-heme Fe(II)Fe(II) center. FMNH2 donates electrons to the di-iron nitrosyl
complex, but the catalytic locus is the di-iron center rather than a flavin
hydride-transfer locus. This does not match the v1
`flavin_dehydrogenase_reductase` semantics and does not fit the other four v1
primary fingerprints.

Eval consequence: pull `m_csa:497` from the Wave 1 near-orphan primary eval
cell and from any `geometry-correct, Foldseek-wrong` anchor role until an
explicit gated label-state revision is accepted. Also drop its proposed
`flavin.dehydrogenase_oxidase_hydride_transfer` child label.

Implementation state: not applied to the canonical registry. This needs an
explicit relabel gate if Vivek accepts it.

## TM Verification

Foldseek TM-pair verification was run for `m_csa:428`, `m_csa:440`, and
`m_csa:477` against train-partition-only structures.

Updated dispositions:

- `m_csa:477`: strongly verified fold-conflict OOS hard negative. It has nine
  primary hits at TM >= 0.70, including six distinct primary M-CSA entries. It
  is now the cleanest Packet 1 adversarial fold-conflict anchor.
- `m_csa:217`: remains verified fold-conflict OOS hard negative with three
  primary neighbors.
- `m_csa:428`: partially verified with caveat. It has three incidental primary
  TIM-barrel hits, but most TM>=0.70 neighbors are OOS glycosidase-like rows.
  Use cautiously as a TIM-barrel false-positive / structural-similarity caveat
  case, not as cleanly as `217` or `477`.
- `m_csa:440`: not verified. It had zero Foldseek hits under the TM-pair run
  and should move from fold-conflict candidate to near-orphan OOS /
  Foldseek-router-abstention diagnostic.

## Corrected Test Cells

| Cell | Rows | Use |
| --- | --- | --- |
| Verified fold-conflict OOS hard negatives | `m_csa:217`, `m_csa:477` | Primary fold-conflict anchors |
| Verified with caveat | `m_csa:428` | TIM-barrel incidental-primary-hit caveat |
| Near-orphan OOS | `m_csa:440` | Router abstention / no-neighbor diagnostic |
| Pull pending relabel | `m_csa:497` | Do not use in primary eval until label-state resolved |

## Next Steps

1. If Vivek accepts the relabel recommendation, run a gated canonical label
   revision for `m_csa:497`.
2. Recompute or annotate Wave 1 metrics with `m_csa:497` excluded from primary
   flavin support before locking claims.
3. Use `m_csa:477` and `m_csa:217` as the clean verified fold-conflict anchors.

## Flavin Fe-S Follow-Up

The Fe-S plus flavin population review adds two caveats to this disposition:

- `m_csa:990` is not analogous to `m_csa:497`; keep its v1 flavin label with
  Fe-S plus flavin / coupled dehydration-reduction metadata.
- `m_csa:428` should be treated even more cautiously because its apparent
  primary TM-neighbor set includes `m_csa:750`, whose v1 flavin label is now
  contested.

See:

```text
artifacts/v3_flavin_fe_s_population_expert_disposition_702_20260527.json
work/flavin_fe_s_population_expert_disposition_20260527.md
```
