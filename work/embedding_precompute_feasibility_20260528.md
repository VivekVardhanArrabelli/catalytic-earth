# Embedding Precompute Feasibility - 2026-05-28

Status: **blocked; no embedding precompute was run**.

The current disk guardrail is above the 10 GiB floor (19.5032 GiB free), but the current Hugging Face cache check reports no ESM-2 8M/35M/150M/650M weights. Existing Wave 1 artifacts are prediction/readout exports or bounded external sample summaries; they are not reusable raw embedding sidecars for the union surface.

## Candidate Surface

- Current702 M-CSA rows: 702 entries, 764 sequence records, 760 unique sequence accessions.
- Queued AMR rows: 0 sequence-addressable rows frozen; 18 AMR enzyme family classes are scoped only as a POC queue.
- External panel rows inventoried: 259 unique candidate IDs, 257 sequence-addressable, 143 UniProt IDs.
- Union estimate for vector storage: 826 accessions.

## Cache Inventory

- ESM-2 150M: standardized Wave 1 prediction/readout export exists, but `facebook/esm2_t30_150M_UR50D` is not cached now and no full-current raw vector sidecar exists.
- ESM-C corrected: standardized prediction/readout export exists; no local ESM-C backend/weights/raw sidecar were found.
- ProtT5: standardized prediction/readout export exists for covered rows; no local Swiss-Prot H5/raw sidecar or ProtT5 weights were found.
- SaProt: standardized prediction/readout export exists; no local SaProt raw sidecar or model weights were found.
- Foldseek: binary and current structural coordinate caches exist; current702 Foldseek readiness is present, all-materializable signal exists, and external 10/all30 structural cluster caches exist. No standardized Foldseek-pocket export exists.

## Disk Estimate

Vector storage is small relative to weights: all four sequence-vector tracks over the estimated accession union are about 9.781 MiB as float32 mean-pooled vectors. The blocker is model/backend cache, not vector sidecar size.

Representative missing model weights from metadata-only Hub inspection:

- ESM-2 150M primary `model.safetensors`: 0.5544 GiB.
- ESM-2 650M primary `model.safetensors`: 2.4303 GiB.
- ESM-C 300M primary `.pth`: 1.2406 GiB.
- ProtT5 half encoder primary `pytorch_model.bin`: 2.2504 GiB.
- Full ProtT5 XL single checkpoint: 10.5012 GiB.
- SaProt 35M primary `.pt`: 0.1256 GiB.

No download was performed. All listed downloads would currently remain above the 10 GiB floor if fetched one-at-a-time, but multi-GB fetches still require explicit authorization and artifacted justification.

## Decision

Do not use compute now for Wave 1.1/external embedding precompute. The already-cached condition is false, and running would either download missing model weights or create new model outputs beyond this feasibility scope.

## Exact Next Commands

```bash
df -h .
PYTHONPATH=src python -m catalytic_earth.cli build-external-source-representation-backend-sample --representation-backend-plan artifacts/v3_external_source_representation_backend_plan_1025.json --sequence-neighborhood-sample artifacts/v3_external_source_sequence_neighborhood_sample_1025.json --max-rows 100 --top-k 3 --embedding-backend esm2_t30_150m_ur50d --model-name facebook/esm2_t30_150M_UR50D --local-files-only --out artifacts/v3_external_source_representation_backend_esm2_t30_150m_ur50d_sample_1025.json
PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-representation-backend-sample --representation-backend-sample artifacts/v3_external_source_representation_backend_esm2_t30_150m_ur50d_sample_1025.json --out artifacts/v3_external_source_representation_backend_esm2_t30_150m_ur50d_sample_audit_1025.json
```

For full current702 embeddings, add a read-only sidecar builder first; the repo currently exposes interface-only learned retrieval manifests, not a full-current embedding writer. Keep vector generation label-blind, then join split/labels only for evaluation.
