# Truth-governance data

- `claim_ledger.json` is the machine-readable source for current claim status.
- `exposure_ledger.jsonl` is append-only and records evaluation-surface state.
- `exposure_rows.jsonl` records immutable row/surface exposure facts and
  machine-computed development/independent-test eligibility.
- `exposure_rows_manifest.json` binds the row ledger and exact surface members.
- `preregistration-v1.schema.json` defines the mandatory signed evaluation
  contract.
- `expansion_freeze.json` mechanically blocks writes to the label,
  fingerprint, and ontology registries while CE-012 is active.
- `historical_lineage_quarantine.json` names genuine lineage mismatches that
  remain historical-only; embedded hashes are never refreshed merely to pass.
- `test_baseline.json` preserves the original full-suite failure counts, the
  corrected root-cause audit, the pinned green rerun, and compressed-log hashes.
- `architecture_freeze.json` binds the replacement architecture, legacy
  no-growth modules, test tiers, and cross-platform path ceiling.

Run the repository contract and core tier before committing:

```bash
python scripts/validate_repository_contracts.py
python scripts/run_test_tier.py "core/unit"
```

The truth validator rejects missing evidence paths, invalid claim statuses,
malformed exposure events, row-memory drift, chronological disorder, and any
attempt to turn an exposed or exhausted surface back into a fresh frozen
surface.

To add exposure, run `PYTHONPATH=src python scripts/record_exposure.py --help`
after freezing the row set and endpoint. Do not edit or reorder existing JSONL
lines. If an old line needs correction, append a `correction` event that leaves
an exhausted surface exhausted.
