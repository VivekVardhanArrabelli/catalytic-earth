# Truth-governance data

- `claim_ledger.json` is the machine-readable source for current claim status.
- `exposure_ledger.jsonl` is append-only and records evaluation-surface state.
- `expansion_freeze.json` mechanically blocks writes to the label,
  fingerprint, and ontology registries while CE-012 is active.

Run both validation commands before committing:

```bash
PYTHONPATH=src python scripts/validate_truth_governance.py
PYTHONPATH=src python -m catalytic_earth.cli validate
```

The truth validator rejects missing evidence paths, invalid claim statuses,
malformed exposure events, chronological disorder, and any attempt to turn an
exposed or exhausted surface back into a fresh frozen surface.

To add exposure, run `PYTHONPATH=src python scripts/record_exposure.py --help`
after freezing the row set and endpoint. Do not edit or reorder existing JSONL
lines. If an old line needs correction, append a `correction` event that leaves
an exhausted surface exhausted.
