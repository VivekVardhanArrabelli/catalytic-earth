# ProtT5 Representation Track Handoff

Run date: 2026-05-25
Branch: `research/representation-prott5`

## Output

- Feasibility/blocker artifact: `artifacts/representation_tracks/prott5/prott5_current702_swissprot_embedding_feasibility_20260525.json`
- Status: blocked before ProtT5 kNN/probe-free metrics.
- Blocking reasons: `h5py` is not installed, and no local UniProtKB/Swiss-Prot ProtT5 `per-protein.h5` file is present under the track download paths.

## Coverage Findings

- Current702 manifest rows: 702.
- Reference UniProt accessions probed: 760.
- Current UniProt accessions found through REST: 758.
- Reviewed Swiss-Prot accessions found: 721.
- Rows with at least one reviewed Swiss-Prot accession: 666.
- Rows without any reviewed Swiss-Prot accession: 36.
- Mixed rows with at least one supported reviewed accession and at least one unsupported accession: 2.
- Inactive/missing current UniProt accessions: `P03176`, `Q05489`.
- No accession exceeded UniProt's 12k-residue ProtT5 exclusion limit.

Unsupported rows are listed in the JSON artifact under
`coverage_feasibility.row_level_expected_swissprot_h5_feasibility_without_local_h5.unsupported_rows`.

## Required Citations Preserved

- Eval contract: `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
  SHA-256 `c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50`
- Sequence-NN baseline: `artifacts/v3_sequence_nn_metrics_current702_20260525.json`
  SHA-256 `22792684a943cd16987a73d048f801c3177a96c5967444d746a5aa768a0e6a26`
- Split artifact: `artifacts/v3_sequence_distance_holdout_eval_1025_current702_split_assignment_repaired_20260525.json`
  SHA-256 `dbed4d1a60c09e97403f6be26ae52a3de49284ba35b6d6c2fb4efebb55de7425`
- Sequence manifest: `artifacts/v3_sequence_manifest_current702_repaired_20260525.json`
  SHA-256 `b792e03276e5027975c323fb65068804ca7a7a70fa388fdf33e71e98434aeb4b`
- Model/source id: UniProtKB/Swiss-Prot ProtT5 per-protein embeddings, ProtT5/prottrans_t5_xl_u50 source vectors.
- Pooling mode: whole-sequence per-protein prepooled UniProt HDF5.
- Active-site pooling: not attempted; must remain a separate known-active-site-window ablation if run later.
- Input leakage contract: embedding vector only; no EC labels, entry names, mechanism prose, expert notes, Rhea identifiers, source prose, or review decisions as predictive inputs.

## Remote Source and Commands

Whole-sequence Swiss-Prot per-protein file:

```bash
python -m pip install h5py numpy
mkdir -p artifacts/representation_tracks/prott5/downloads
curl -L --fail --continue-at - --output artifacts/representation_tracks/prott5/downloads/uniprot_sprot_per-protein.h5 https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/embeddings/uniprot_sprot/per-protein.h5
```

Expected whole-sequence H5 size: 1,383,407,848 bytes, about 1.29 GiB.

Do not download the Swiss-Prot per-residue file for this track. Its current remote size is
426,737,506,536 bytes, about 397.43 GiB, and it would not be the whole-sequence baseline.

After download, run the exact H5 key coverage probe from the JSON artifact before any metrics.

## Metrics

No ProtT5 kNN/probe-free metrics were computed. The artifact only carries feasibility,
coverage, blocker state, baseline sequence-NN references, OOS diagnostic references, and
canary-summary references. When unblocked, compute macro-F1/accuracy, per-fingerprint
breakdown with underpowered-cell flags, OOS abstention/false-positive diagnostics by tier,
canary predictions, and a comparison to the cited sequence-NN baseline.
