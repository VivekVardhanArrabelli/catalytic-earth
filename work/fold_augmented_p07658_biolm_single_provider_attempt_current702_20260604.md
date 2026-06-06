# Fold-Augmented P07658 BioLM Single Provider Attempt - current702

Run: 2026-06-04T18:11:36.655809Z

Single approved full-length provider attempt for the exact Lever 3 P07658 715-residue sequence. It records request/response provenance only; it stages no coordinates, scores no rows, and changes no thresholds.

## Status

- fold_augmented_p07658_biolm_single_provider_attempt_no_coordinate
- Provider: BioLM ESMFold
- HTTP status: 401
- Coordinate returned: False
- Sequence length: 715
- Selenocysteine positions: [140]

## Decision

- Coordinate blocker cleared now: False
- Response: {"detail":"Authentication credentials were not provided."}
- Next gate: Rerun acceptance preflight only if a coordinate plus filled provider/model/version/path/checksum provenance exists.
