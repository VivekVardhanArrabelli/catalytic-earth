# Architecture boundary after the truth reset

The legacy research surface is preserved but frozen. Its size is provenance,
not a template for future work.

## Hard rules

- The five giant modules named in
  `data/governance/architecture_freeze.json` are byte-frozen. New behavior goes
  into bounded typed modules.
- The 47 grandfathered family sourcing modules remain historical. A new family
  is a `family-onboarding.v1` configuration processed by
  `family_onboarding.py`; adding another family-specific Python module fails
  validation.
- Family plans are proposal-only, require declared positive/counterevidence and
  an OOS contract, use an injected clock and seed, and cannot mutate a registry.
- The locked synthetic release fixture remains `mechanism-record.v1`.
  Biological Atlas compilation uses the richer, strict `mechanism-record.v2`
  plus the `atlas3-kernel.v1` wrapper. Unsupported counted objects, evidence
  references, site mappings, and provenance bindings fail instead of falling
  into prose.
- Every test module belongs to exactly one tier in `tests/test_tiers.json`.
- `catalytic-earth reproduce` remains the canonical locked fixture path;
  `catalytic-earth atlas3` reproduces the first biological kernel and query.
  `catalytic-earth-legacy` is deprecated and outside the locked-core guarantee.
- Tracked relative paths may not exceed 180 characters. The lean archive has a
  stricter observed ceiling and omits historical artifact/report trees.

Run:

```bash
python scripts/build_architecture_freeze.py --check
python scripts/build_atlas3_kernel.py --check
python scripts/run_test_tier.py --check
```

Changing a frozen hash is an architectural migration requiring a separate
decision and manifest update, not a casual edit hidden inside scientific work.
