# Non-Heme Iron 2OG Next-Lane Scout

Run: 2026-06-13T00:12:35Z

P450 is now applied to the floor, so this focused scout checks the next likely 10k-path lane without
creating labels or writing either registry.

## Result

- Candidate: `non_heme_iron_2og_dioxygenase`.
- Recommendation: wire as the next deliberate fingerprint-universe change.
- Reviewed Swiss-Prot supply:
  - EC 1.14.11 + iron/dioxygenase handle: **870**.
  - EC 1.14.11 + Dioxygenase keyword: **825**.
  - EC 1.14.11 + iron-only handle: **854**.
  - Broad EC 1.14.11: **874**.
- EC-diversity sample: **200** rows, **36** distinct specific ECs; top sample ECs were
  `1.14.11.67` (13), `1.14.11.66` (13), `1.14.11.27` (13), `1.14.11.29` (12),
  `1.14.11.33` (11), `1.14.11.65` (11), `1.14.11.53` (10), and `1.14.11.2` (10).

## Guardrails

- No labels emitted; no registry written.
- EC 1.14.11 is a scope/fetch selector only.
- Counted mechanism handles for a future import should be Fe(II)/non-heme binding evidence,
  2-oxoglutarate/succinate/CO2 Rhea participants, Dioxygenase keyword/domain evidence, and
  active-site/facial-triad residue roles.
- Heme P450, flavin oxygenase, peroxide/peroxidase, and generic iron proteins must stay held or
  route off-target.

## Next Action

Wire `non_heme_iron_2og_dioxygenase` as a 17fp universe change: fingerprint spec, ontology node,
mechanism corroborator, offline leakage/trust-tier tests, 17fp OOS preregistration, then
non-destructive preview and apply only if gates pass.
