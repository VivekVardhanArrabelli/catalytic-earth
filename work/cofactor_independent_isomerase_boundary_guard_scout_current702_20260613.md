# Cofactor-independent isomerase boundary guard scout

Run: 2026-06-13T01:26:19Z

Non-destructive EC co-annotation scout over 200 reviewed EC 5.3 + Isomerase rows. No registry write, no labels emitted.

## Summary

- `has_non_5_3_side_ec`: 77
- `only_ec_5_3`: 123
- `oxidoreductase_side_ec`: 34
- `peroxidase_side_ec`: 8
- `transferase_side_ec_2_5`: 11

## Non-5.3 side EC prefix counts

- `4.2`: 32
- `1.1`: 29
- `5.1`: 14
- `2.5`: 11
- `1.11`: 8
- `3.1`: 8
- `4.1`: 5
- `3.7`: 4
- `3.3`: 3
- `1.14`: 2
- `1.8`: 2
- `2.7`: 1

## Guard recommendation

- Hold non-5.3 side-EC rows unless a future rule explicitly assigns a separate subclass; especially hold 1.11 peroxidase/oxidoreductase and 2.5 transferase side rows. EC remains scope-only and cannot be counted.
