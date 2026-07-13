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
- Mechanism interchange uses `mechanism-record.v1` typed objects and JSON
  Schema. Unsupported counted objects fail instead of falling into prose.
- Every test module belongs to exactly one tier in `tests/test_tiers.json`.
- `catalytic-earth reproduce` is the canonical installed path.
  `catalytic-earth-legacy` is deprecated and outside the locked-core guarantee.
- Tracked relative paths may not exceed 180 characters. The lean archive has a
  stricter observed ceiling and omits historical artifact/report trees.

Run:

```bash
python scripts/build_architecture_freeze.py --check
python scripts/run_test_tier.py --check
```

Changing a frozen hash is an architectural migration requiring a separate
decision and manifest update, not a casual edit hidden inside scientific work.
