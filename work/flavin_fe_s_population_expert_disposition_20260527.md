# Flavin Fe-S Population Expert Disposition - 2026-05-27

This is a review-only follow-up to Packet 1 and the v2 sublabel audit. It does
not change labels, ontology, fingerprints, imports, thresholds, model outputs,
or production policy.

## Core Finding

`m_csa:990` is defensible as a v1 `flavin_dehydrogenase_reductase` row, but the
current v2 child label `flavin.dehydrogenase_oxidase_hydride_transfer` is not
ready for evaluation use as written.

The reason is population-level heterogeneity. The flavin bucket has 50 rows:

- 34 flavin-only rows
- 9 flavin plus Fe-S cluster rows
- 4 flavin plus metal-ion rows
- 3 flavin plus heme rows

The 9 Fe-S plus flavin rows alone contain at least three distinct mechanism
classes: clean flavin hydride-transfer, FAD electron-transfer/coupled chemistry,
and mechanistically distinct covalent or radical flavin chemistry.

## Row-Level Decisions

### m_csa:990

Keep the v1 `flavin_dehydrogenase_reductase` label. The catalytic locus is the
FAD-substrate interface. The two 4Fe-4S clusters relay electrons from
ferredoxin to FAD; FAD reduces the substrate, while Asp237 supports the
dehydration portion.

Do not treat it as a plain hydride-transfer child-label example. Carry:

```text
cofactor_complexity = fe_s_plus_flavin
mechanism_class = coupled_dehydration_and_reduction
fe_s_role = electron_relay
flavin_role = catalytic_substrate_reduction_locus
```

### m_csa:750

Pull from current evaluation until v1 label review. It appears to be flavin
radical dehydratase chemistry with flavin semiquinone and Fe-S involvement, not
a straightforward flavin reductase. This matters because Wave 1 currently uses
`m_csa:750` as a learned-representation failure canary. If its ground truth is
contested, it is unsafe as a canary.

### m_csa:123

Keep as v1 flavin with boundary metadata. FAD is central, but the mechanism is
covalent FAD-substrate adduct chemistry rather than classical hydride transfer.

### m_csa:497

The prior recommendation to relabel `m_csa:497` to `out_of_scope` is reinforced.
It belongs to the broader issue that flavin/metal cofactor presence is not
enough to define a flavin hydride-transfer mechanism.

## V2 Sublabel Decision

Move `flavin.dehydrogenase_oxidase_hydride_transfer` from ready-for-future-eval
to expert-review-needed until the heterogeneity is resolved.

Immediate practical fix: keep the broad v1 flavin bucket for statistical power,
but add diagnostic axes:

```text
cofactor_complexity:
  flavin_only
  fe_s_plus_flavin
  flavin_plus_metal_ion
  flavin_plus_heme

mechanism_class:
  clean_hydride_transfer
  electron_transfer_coupled
  covalent_fad_adduct
  flavin_radical_dehydratase
  boundary_or_unresolved
```

Eventual goal: split into mechanism-typed v2 strata once support is sufficient.
Likely future children include simple hydride transfer, hydride transfer with
Fe-S relay, electron transfer with Fe-S relay, covalent FAD-adduct chemistry,
and flavin radical dehydratase chemistry.

## Packet 1 Implications

- `m_csa:990` remains usable in the near-orphan primary cell, with cofactor and
  coupled-chemistry caveat metadata.
- `m_csa:750` should be pulled from learned-representation canary use until
  reviewed.
- `m_csa:428` gets a stronger caveat because one of its apparent primary TM
  neighbors is `m_csa:750`, whose v1 label is now contested.
- `m_csa:497` remains recommended for out-of-scope relabel through a separate
  explicit gated change.

