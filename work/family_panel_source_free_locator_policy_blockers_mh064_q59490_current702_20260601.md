# Source-Free Locator Policy Blockers: mh_064/Q59490

## Summary

This packet isolates the final two no-ligand/metal locator blockers after the
validation reviews. Neither can be cleared by local automation without a policy
decision.

## Result

| Row | Blocker | Current safe action |
| --- | --- | --- |
| `mh_064` | selected `3PG4` has no detected non-water ligand or metal site | approve or reject five frozen alternate-coordinate fetches |
| `secondary_probe::cobalamin_radical_rearrangement` | selected `1L1L` has no detected ligand/metal site and no frozen alternate PDB IDs | design a nonlabel locator strategy or approve an alternate source row |

No coordinates were fetched, no locator sidecars were copied, and no
predicted-geometry scoring was run.

## Guardrails

- Kept both rows review-only and non-countable.
- Did not fetch alternate coordinates.
- Did not use source prose, labels, EC/Rhea IDs, panel IDs, or fingerprint IDs
  as predictive features.
- Did not change labels, registries, ontologies, splits, thresholds, or model
  weights.

## Next Action

Human decision required: approve the `mh_064` alternate-coordinate fetches,
reject them, or authorize/design a Q59490 nonlabel locator strategy. After any
approval, rerun coordinate-only candidate extraction plus integrity/schema audit
before copying a locator sidecar or scoring source-free predicted geometry.
