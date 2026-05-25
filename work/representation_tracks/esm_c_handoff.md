# ESM-C Representation Track Handoff

Run timestamp: 2026-05-25T17:13:06Z

Branch: `research/representation-esm-c`

## Status

ESM-C 300M remains blocked at backend feasibility, now with a bounded package/model preflight. No embeddings, predictions, metrics, labels, fingerprints, ontology entries, thresholds, or production scoring were changed.

Track artifacts:

- `artifacts/representation_tracks/esm_c/esm_c_feasibility_backend_blocker_current702_20260525.json`
- SHA-256: `d533c3378a85da024ff349e94eaa9f77197e1a02ef5bc87388f94addfe114ae9`
- `artifacts/representation_tracks/esm_c/esm_c_bounded_backend_preflight_current702_20260525.json`
- SHA-256: `6f8be06cc4c207bb8b18716231777336a4375582c3cafc6c56c0bc3aa80ce109`

## What Was Checked

- Shared baseline: `origin/main` is `8e69bf002097d5cf55521a13764e096908d8e0af`, satisfying the requested baseline.
- Eval contract SHA: `c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50`.
- Sequence manifest SHA: `b792e03276e5027975c323fb65068804ca7a7a70fa388fdf33e71e98434aeb4b`.
- Repaired split SHA: `dbed4d1a60c09e97403f6be26ae52a3de49284ba35b6d6c2fb4efebb55de7425`.
- Sequence-NN metrics SHA: `22792684a943cd16987a73d048f801c3177a96c5967444d746a5aa768a0e6a26`.
- Repaired current702 FASTA SHA: `f151bcf8e3e9b7ca7adfd6bbf1da119e3d486228f3dad19f92dc4b9f20c42a3e`.

Backend probe:

- `esm` package: unavailable.
- `torch`: available, version `2.7.1`.
- `transformers`: available, version `4.53.2`.
- `huggingface_hub`: available, version `0.33.4`.
- PyPI `esm` latest version: `3.2.3`, requiring Python `<3.13,>=3.12` and `transformers<4.48.2`.
- Local runtime conflict: installed `transformers` is `4.53.2`, so installing `esm` into the shared interpreter would require a downgrade.
- Missing local ESM-C runtime dependencies include `torchtext`, `einops`, `biotite`, `msgpack-numpy`, `biopython`, `cloudpathlib`, `tenacity`, `zstd`, `pydssp`, `pygtrie`, and `dna_features_viewer`.
- CUDA and MPS: unavailable.
- Default Hugging Face cache path checked: `/Users/vivekvardhanarrabelli/.cache/huggingface/hub`; directory absent.
- Default Torch cache path checked: `/Users/vivekvardhanarrabelli/.cache/torch`; directory absent.
- Local-only probes for `EvolutionaryScale/esmc-300m-2024-12`, `esmc_300m`, and `facebook/esm2_t6_8M_UR50D` found no cached files.
- Hugging Face model metadata resolved `EvolutionaryScale/esmc-300m-2024-12` to `biohub/esmc-300m-2024-12`, public and ungated at commit `c309e1f43e775c1a513826dba9f1fe04622e96a1`.
- Remote metadata reports `data/weights/esmc_300m_2024_12_v0.pth` at `1,332,095,738` bytes. No model file was downloaded.
- The repaired FASTA has 760 records totaling 318,251 amino acids; max sequence length is 3,011. CPU-only full embedding may exceed a short automation window.

## Contract State

Prepared ESM-C settings:

- Model id: `esmc_300m`.
- Pooling mode: `whole_sequence`.
- Active-site pooling: not run; remains separate as `known_active_site_window_ablation`.
- Allowed predictive input: amino-acid sequence only.
- Forbidden predictive inputs: EC labels, entry names, mechanism prose, expert notes, review text, and source identifiers as features.

No ESM-C metrics were computed. The artifact explicitly marks primary macro-F1, accuracy, per-fingerprint breakdown, OOS tier diagnostics, canary predictions, and underpowered-cell flags as blocked because no embeddings or predictions exist.

## Next Exact Step

Create an isolated ESM-C runtime rather than mutating the shared interpreter, pin `esm==3.2.3` with `transformers<4.48.2`, set a recorded `HF_HOME` or `HUGGINGFACE_HUB_CACHE`, and download only `biohub/esmc-300m-2024-12/data/weights/esmc_300m_2024_12_v0.pth` after accepting the 1.33 GB size budget. Run a two-record smoke embedding first; if CPU wall time is acceptable, compute whole-sequence frozen embeddings for the repaired current702 FASTA. Write all embeddings, predictions, and metrics only under `artifacts/representation_tracks/esm_c/`.
