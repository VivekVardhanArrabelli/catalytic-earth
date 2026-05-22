# M-CSA PyMOL Expert Review Cockpit Plan

## Purpose

Build a human review tool that turns M-CSA review debt into focused active-site
visual inspections. The goal is to help the human expert decide whether a
pending row should be accepted, rejected, skipped, or marked as needing more
evidence.

This is a review cockpit, not a label importer. Accepted decisions must still
flow through the existing expert-review import previews and label-factory gates
before any countable label changes.

## Priority

After the current main-loop dirty work is finished, validated, committed, and
pushed, implement this before starting another broad external mini-campaign.
This tool is allowed to support M-CSA expert review even though M-CSA-only
count growth remains stopped without expert decisions.

## Required Inputs

Use the current review artifacts, starting with:

- `artifacts/v3_expert_label_decision_review_export_1000.json`
- `artifacts/v3_review_debt_summary_1025_preview.json`
- `artifacts/v3_review_evidence_gaps_1025_preview.json`
- relevant geometry/retrieval artifacts that contain residue, atom, distance,
  structure, or local active-site failure evidence
- local mmCIF/PDB/AlphaFold coordinate sidecars already present in the repo or
  cache

Do not invent missing residue pairs. If an artifact does not contain an exact
failed atom pair or exact measured distance, mark that row as not yet
PyMOL-ready and record the missing fields.

## Backend Extractor

Add a bounded extractor that emits a machine-readable queue such as:

```text
artifacts/v3_mcsa_pymol_expert_review_queue_1025.json
```

Each queue row should contain:

- `entry_id`, for example `m_csa:1004`
- `entry_name`
- `structure_id` and `structure_path`
- `target_fingerprint_id` or target mechanism/family
- `review_reason` and source artifact path
- catalytic or failed residues with chain, residue name, residue number,
  atom name when known, and role when known
- exact measured distance in Angstroms when available
- heuristic threshold that was violated when available
- `pymol_ready=true|false`
- `missing_fields` for rows that cannot safely generate a focused scene
- provenance pointers to the artifacts/fields used

The extractor should report counts:

- total review rows scanned
- rows with structure paths
- rows with exact residue/atom pairs
- rows with exact distances
- rows PyMOL-ready
- rows blocked by missing structure, missing atom pair, missing distance, or
  ambiguous residue mapping

## PyMOL Script Generator

Generate one `.pml` script per PyMOL-ready row, preferably on demand or under a
dedicated small directory such as:

```text
artifacts/review_pymol/mcsa_1025/
```

Each script must:

1. Load the mmCIF/PDB structure.
2. Hide the default representation.
3. Show the protein as a faint context surface or cartoon, around 80 percent
   transparent where PyMOL supports it.
4. Highlight catalytic/failed residues as bright sticks.
5. Draw a dashed line between the exact failed atoms.
6. Label the distance, for example `4.1 A`.
7. Zoom and center directly on the failed atom pair.

If PyMOL is not installed, generation should still work and the launcher should
fail closed with a clear message.

## Terminal Review UI

Add a simple terminal review loop. A CLI or script name like the following is
acceptable:

```bash
PYTHONPATH=src python -m catalytic_earth.cli launch-mcsa-pymol-review \
  --queue artifacts/v3_mcsa_pymol_expert_review_queue_1025.json \
  --out artifacts/v3_expert_review_decision_batch_pymol_manual.json
```

Required behavior:

- Supports `--dry-run`, `--max-rows`, `--start-index`, `--no-launch`, and
  `--pymol-bin`.
- Opens one PyMOL scene at a time when launch is enabled.
- Prints concise context in the terminal:
  - row index
  - M-CSA id
  - target fingerprint/family
  - failed distance and threshold
  - review reason
- Prompts for:
  - accept
  - reject
  - skip
  - needs_more_evidence
  - quit and save
- Allows an optional expert note.
- Saves incrementally so a crash does not lose completed decisions.
- Closes or asks PyMOL to quit before opening the next row where possible.

## Output Manifest

Write an output artifact such as:

```text
artifacts/v3_expert_review_decision_batch_pymol_manual.json
```

Use a schema that can be converted into the existing expert-review import
workflow. Include at minimum:

- reviewer
- reviewed_at
- input_queue_path
- M-CSA entry id
- structure id/path
- decision: `accepted`, `rejected`, `skipped`, or `needs_more_evidence`
- expert note
- exact visual evidence pointers
- whether the decision is countable-import-ready under existing gates

Default `countable_import_ready` must be false. This review output should be
fed into the existing `import-label-review` or `import-countable-label-review`
preview path only after validation.

## Tests And Safety

Add targeted tests for:

- queue extraction from a small fixture or a small real artifact subset
- fail-closed behavior when exact atom pairs are missing
- `.pml` generation with correct load, selection, distance, label, and zoom
  commands
- launcher dry-run/no-launch behavior
- output decision schema validation
- no mutation of `data/registries/curated_mechanism_labels.json`

Required verification:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m catalytic_earth.cli validate
git diff --check
```

No artifact upload, deletion, externalization, Git-LFS migration, history
rewrite, label import, production fingerprint edit, or countable registry
change is allowed for this tool.

## Acceptance Criteria

The first implementation is successful when:

- a review queue can be built from current M-CSA review artifacts
- all non-PyMOL-ready rows are explicitly explained instead of guessed
- at least one real PyMOL-ready row or a clear zero-ready blocker report exists
- `.pml` scripts are generated for ready rows
- the terminal review loop can run in dry-run/no-launch mode
- a manual decision output artifact can be written and parsed
- docs/handoff explain how the human should use it
- all tests and validation pass
