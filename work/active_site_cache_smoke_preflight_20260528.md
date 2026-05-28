# Active-Site Cache Smoke Preflight - 2026-05-28

Read-only preflight. No cache/tensor/model output was written.

## Decision

- safe cache CLI present: `False`
- next action: CLI implementation/preflight only: add or expose a small label-blind active-site cache writer, then run on these 10 rows. Do not train yet.

## Smoke Rows

- `m_csa:97` path_exists=True residues=4 roles=4 status=contract_ready_cli_missing_or_path_missing
- `m_csa:211` path_exists=True residues=3 roles=3 status=contract_ready_cli_missing_or_path_missing
- `m_csa:250` path_exists=True residues=4 roles=4 status=contract_ready_cli_missing_or_path_missing
- `m_csa:517` path_exists=True residues=5 roles=5 status=contract_ready_cli_missing_or_path_missing
- `m_csa:686` path_exists=True residues=6 roles=6 status=contract_ready_cli_missing_or_path_missing
- `m_csa:916` path_exists=True residues=6 roles=5 status=contract_ready_cli_missing_or_path_missing
- `m_csa:990` path_exists=True residues=4 roles=4 status=contract_ready_cli_missing_or_path_missing
- `m_csa:217` path_exists=True residues=6 roles=6 status=contract_ready_cli_missing_or_path_missing
- `m_csa:428` path_exists=True residues=7 roles=7 status=contract_ready_cli_missing_or_path_missing
- `m_csa:477` path_exists=True residues=5 roles=5 status=contract_ready_cli_missing_or_path_missing
