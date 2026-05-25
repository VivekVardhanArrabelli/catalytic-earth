# ESM-C Representation Track Handoff

Run timestamp: 2026-05-25T16:12:19Z

Branch: `research/representation-esm-c`

## Status

ESM-C 300M is blocked at backend feasibility. No embeddings, predictions, metrics, labels, fingerprints, ontology entries, thresholds, or production scoring were changed.

Track artifact:

- `artifacts/representation_tracks/esm_c/esm_c_feasibility_backend_blocker_current702_20260525.json`
- SHA-256: `d533c3378a85da024ff349e94eaa9f77197e1a02ef5bc87388f94addfe114ae9`

## What Was Checked

- Shared baseline: `origin/main` is `8e69bf002097d5cf55521a13764e096908d8e0af`, satisfying the requested baseline.
- Eval contract SHA: `c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50`.
- Sequence manifest SHA: `b792e03276e5027975c323fb65068804ca7a7a70fa388fdf33e71e98434aeb4b`.
- Repaired split SHA: `dbed4d1a60c09e97403f6be26ae52a3de49284ba35b6d6c2fb4efebb55de7425`.
- Sequence-NN metrics SHA: `22792684a943cd16987a73d048f801c3177a96c5967444d746a5aa768a0e6a26`.

Backend probe:

- `esm` package: unavailable.
- `torch`: available, version `2.7.1`.
- `transformers`: available, version `4.53.2`.
- `huggingface_hub`: available, version `0.33.4`.
- CUDA and MPS: unavailable.
- Default Hugging Face cache path checked: `/Users/vivekvardhanarrabelli/.cache/huggingface/hub`; directory absent.
- Default Torch cache path checked: `/Users/vivekvardhanarrabelli/.cache/torch`; directory absent.
- Local-only probes for `EvolutionaryScale/esmc-300m-2024-12`, `esmc_300m`, and `facebook/esm2_t6_8M_UR50D` found no cached files.

## Contract State

Prepared ESM-C settings:

- Model id: `esmc_300m`.
- Pooling mode: `whole_sequence`.
- Active-site pooling: not run; remains separate as `known_active_site_window_ablation`.
- Allowed predictive input: amino-acid sequence only.
- Forbidden predictive inputs: EC labels, entry names, mechanism prose, expert notes, review text, and source identifiers as features.

No ESM-C metrics were computed. The artifact explicitly marks primary macro-F1, accuracy, per-fingerprint breakdown, OOS tier diagnostics, canary predictions, and underpowered-cell flags as blocked because no embeddings or predictions exist.

## Next Exact Step

After explicit approval for bounded install/download, expose a pinned EvolutionaryScale ESM-C backend with local `esmc_300m` weights, record checkpoint cache path and weight size, then compute whole-sequence frozen embeddings for the repaired current702 FASTA. Write all embeddings, predictions, and metrics only under `artifacts/representation_tracks/esm_c/`.
