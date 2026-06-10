# Ser/Cys-His-Asp Catalytic-Triad Locator For The ser_his Hole

Run: 2026-06-10T05:04:59Z

`ser_his_acid_hydrolase` is the one seed fingerprint the cofactor-anchored engine cannot reach -- it is cofactorless. This supplies the missing corroborator: a coordinate Ser/Cys/Thr-His-Asp/Glu triad that must coincide with the annotated catalytic ACT_SITE of a serine-hydrolase EC family. Non-destructive: no registry is written, no label emitted.

## ser_his standing

- Combined 42 (42 frozen + 0 expansion); floor 100; deficit 58.

## Control panel -- why corroboration is required

- Raw geometric triad resolves on 31/120 local structures (rate 0.2583) -- the incidental-trigger surface that ACT_SITE corroboration suppresses.

## Recovery scan (coordinate-bearing registry rows)

- Serine-hydrolase-EC rows in expansion: 13.
- Decisions: {'hold': 13}.
- Confirmed ser_his recoveries (apply-ready): 0.

## Acquisition contract (ready to run when sourcing is authorized)

- Blocked here: pools drained; UniProt blocked_http_403; local serine-hydrolase candidate rows 13.
- Scope EC families: ['3.4.21', '3.4.16', '3.1.1'] (excluding ['3.1.11', '3.1.13', '3.1.16']); EC scope_assignment_only_never_predictive_feature.
- Cofactor: no_catalytic_cofactor_annotated; structural corroboration: coordinate Ser/Cys/Thr-His-Asp/Glu triad must coincide with the annotated catalytic ACT_SITE residues (>=2 overlap).
- Dedup: against BOTH registries (accession + sequence-SHA); tiering: tier=bronze, review_status=automation_curated, uniprot namespace.

## Guardrails

- Frozen benchmark written: False.
- Registry labels emitted: 0.
- EC used for scope assignment only, never predictive; triad confirmation uses coordinates only; no network.
