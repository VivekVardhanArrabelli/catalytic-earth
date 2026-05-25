# SaProt Representation Track Handoff

Run date: 2026-05-25
Branch: research/representation-saprot

## Decision

SaProt is no longer blocked at generic feasibility. A bounded public HF/Transformers SaProt-35M run was completed on the frozen current702 split using whole selected-structure Foldseek SA tokens and nearest-neighbor lookup over in-distribution embeddings.

This is not a full SaProt-650M result. The 650M repository was metadata-checked only and not downloaded because the public repo reports about 5.21 GB across duplicate `.pt` and `pytorch_model.bin` weight formats.

## New Artifacts

- `artifacts/representation_tracks/saprot/saprot_chain_token_policy_current702_20260525.json`
- `artifacts/representation_tracks/saprot/saprot_tokenization_coverage_current702_20260525.json`
- `artifacts/representation_tracks/saprot/saprot_sa_tokens_current702_20260525.jsonl`
- `artifacts/representation_tracks/saprot/saprot_embeddings_manifest_current702_20260525.json`
- `artifacts/representation_tracks/saprot/saprot_predictions_current702_20260525.jsonl`
- `artifacts/representation_tracks/saprot/saprot_metrics_current702_20260525.json`

Prior feasibility artifact retained:

- `artifacts/representation_tracks/saprot/saprot_feasibility_current702_20260525.json`

## Frozen Chain/Token Policy

- Use the selected structure provenance from the frozen current702 split artifact.
- For each selected coordinate, parse all Foldseek `structureto3didescriptor` records.
- If multiple records are emitted, choose the longest amino-acid/3Di record.
- Ties are resolved deterministically by Foldseek record id, then original Foldseek record index.
- Record all Foldseek alternatives with lengths and hashes.
- Do not use labels, EC, names, mechanism prose, expert notes, or model outcomes to choose chains.
- Pair Foldseek-emitted amino acid tokens with aligned Foldseek 3Di tokens lowercased for SaProt input.
- Whole-sequence/whole-structure mean pooling is the primary representation; active-site pooling remains a future ablation.

## Coverage

- Foldseek emitted 1,833 records across 672 staged coordinate files.
- 661 of 702 current rows are SaProt-token compatible.
- 41 rows are blocked before SaProt embedding:
  - 34 in-distribution
  - 7 held out
- The 41 blockers include the prior missing/un-staged selected coordinates plus model-token compatibility blockers:
  - 6 selected records exceed the HF model 1,024-residue limit.
  - 9 selected records contain unsupported Foldseek amino-acid token `X`.
- 414 rows had multiple Foldseek records; all alternatives are recorded, and longest-record selection was applied deterministically.

## Backend

- Model: `westlake-repl/SaProt_35M_AF2`
- Revision/SHA: `316cd4017d29f4657b959365f24b57f1ee278912`
- Embedding dimension: 480
- Pooling: mean last hidden state over non-special whole-sequence SA tokens
- Python: `/opt/homebrew/Caskroom/miniconda/base/bin/python`
- `torch`: 2.7.1
- `transformers`: 4.53.2
- `huggingface_hub`: 0.33.4
- Cache path: `/private/tmp/catalytic-saprot-hf-cache`
- Recorded cache size in metrics artifact: 766,366,756 bytes
- Recorded main weight size: `pytorch_model.bin` 136,862,061 bytes
- Foldseek: `/private/tmp/catalytic-foldseek-env/bin/foldseek`, version `718d42176d2f67d36a60866fedfb881f8d5a7ebf`

## Metrics

From `saprot_metrics_current702_20260525.json`:

- Primary macro-F1: 0.5134
- Primary supervised accuracy: 0.3333, 15/45
- Exact label accuracy, all heldout: 0.6357
- Exact label accuracy, in-scope heldout: 0.3125
- OOS false-positive rate without threshold: 0.1957, 18/92
- Embedded heldout rows: 133
- Heldout coordinate/tokenization abstentions: 7

Per-fingerprint top-1 accuracy:

- `flavin_dehydrogenase_reductase`: 0.4000, 4/10
- `heme_peroxidase_oxidase`: 0.5000, 2/4, underpowered
- `metal_dependent_hydrolase`: 0.0588, 1/17
- `plp_dependent_enzyme`: 0.8333, 5/6
- `ser_his_acid_hydrolase`: 0.3750, 3/8

OOS diagnostics by tier:

- `far_oos`: false-positive rate 0.0000, abstention rate 1.0000, 1 row
- `near_oos`: false-positive rate 0.3333, abstention rate 0.6667, 3 rows
- `unknown_oos`: false-positive rate 0.1932, abstention rate 0.8068, 88 rows

Comparator context:

- Sequence-NN current702 primary accuracy was 0.1556 and OOS FP rate was 0.2717; bounded SaProt-35M is +0.1777 primary accuracy with lower OOS FP rate.
- Foldseek 3Di current702 is represented here as tokenization coverage, not a predictive metric.
- ProtT5 current702 comparator is not available in this branch.
- ESM-2 150M exists only as the prior 12-row external-source sample artifact, not a current702 direct comparator.

## Verification

- JSON artifacts validated with `python -m json.tool`.
- JSONL artifacts parsed successfully:
  - 661 token rows
  - 140 heldout prediction rows
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed:
  - 12 source records
  - 8 mechanism fingerprints
  - 15 mechanism ontology families
  - 702 curated mechanism labels

## Caveats

- No labels, fingerprints, ontology, production scoring, thresholds, or main docs were edited.
- No large model was trained.
- No EC/name/prose/expert-note fields were used as predictive features.
- SaProt-650M remains uncomputed.
- The nearest-neighbor classifier has no calibrated abstention threshold; abstention is only nearest-train out-of-scope or explicit coordinate/tokenization blocker.
