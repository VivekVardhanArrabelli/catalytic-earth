#!/usr/bin/env bash
# Remote disposable GPU setup only. Does not provision or launch inference.
# Provider termination is owned by the lead under the approved rental cap.
set -euo pipefail
: "${CE_P8_RUNTIME:?Fresh absolute remote runtime directory}"
: "${CE_P8_PACKAGE:?Absolute path to reviewed experiment package}"
test ! -e "$CE_P8_RUNTIME"
mkdir -p "$CE_P8_RUNTIME"
CE_P8_COMMIT=0932f1cb165ae7d413c11b1a7acc04ee31758817
date -u +%FT%TZ > "$CE_P8_RUNTIME/started_utc.txt"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv > "$CE_P8_RUNTIME/gpu.csv"
if command -v uv >/dev/null 2>&1; then
  CE_P8_UV=$(command -v uv)
else
  python3 -m pip install --user uv
  CE_P8_USER_BASE=$(python3 -m site --user-base)
  CE_P8_UV="$CE_P8_USER_BASE/bin/uv"
fi
"$CE_P8_UV" venv --python 3.12 "$CE_P8_RUNTIME/venv"
export PATH="$CE_P8_RUNTIME/venv/bin:$PATH"
git init "$CE_P8_RUNTIME/foundry"
git -C "$CE_P8_RUNTIME/foundry" remote add origin https://github.com/RosettaCommons/foundry.git
git -C "$CE_P8_RUNTIME/foundry" fetch --depth 1 origin "$CE_P8_COMMIT"
git -C "$CE_P8_RUNTIME/foundry" checkout --detach FETCH_HEAD
test "$(git -C "$CE_P8_RUNTIME/foundry" rev-parse HEAD)" = "$CE_P8_COMMIT"
"$CE_P8_UV" pip install --torch-backend=cu128 --python "$CE_P8_RUNTIME/venv/bin/python" \
  -e "$CE_P8_RUNTIME/foundry[rfd3,rf3,rfo]" torch==2.11.0 atomworks==2.2.1 biotite==1.4.0 rdkit==2026.3.6
"$CE_P8_UV" pip freeze --python "$CE_P8_RUNTIME/venv/bin/python" > "$CE_P8_RUNTIME/runtime_freeze.txt"
python - <<'PY' > "$CE_P8_RUNTIME/runtime_gpu_check.json"
import json,sys,torch
assert sys.version_info >= (3,12)
assert torch.cuda.is_available()
assert torch.version.cuda and torch.version.cuda.split('.')[0]=='12'
print(json.dumps({'python':sys.version,'torch':torch.__version__,'cuda':torch.version.cuda,
                  'device':torch.cuda.get_device_name(0)},indent=2))
PY
unset LOCAL_MSA_DIRS
python "$CE_P8_PACKAGE/native_context_gate.py" \
  --foundry-root "$CE_P8_RUNTIME/foundry" \
  --scaffold "$CE_P8_PACKAGE/selected_scaffold.cif.gz" \
  --output "$CE_P8_RUNTIME/native_context_verified.json"
mkdir "$CE_P8_RUNTIME/checkpoints"
for CE_P8_WEIGHT in ligandmpnn/ligandmpnn_v_32_010_25.pt rf3/rf3_foundry_01_24_latest_remapped.ckpt; do
  CE_P8_FILE=${CE_P8_WEIGHT#*/}
  curl --fail --location --proto '=https' --proto-redir '=https' --connect-timeout 20 --max-time 600 --retry 0 \
    --dump-header "$CE_P8_RUNTIME/checkpoints/$CE_P8_FILE.headers" \
    --output "$CE_P8_RUNTIME/checkpoints/$CE_P8_FILE.part" "https://files.ipd.uw.edu/pub/$CE_P8_WEIGHT"
  mv "$CE_P8_RUNTIME/checkpoints/$CE_P8_FILE.part" "$CE_P8_RUNTIME/checkpoints/$CE_P8_FILE"
done
export CE_P8_RUNTIME
python - <<'PY'
import os,pathlib,hashlib,json,datetime
root=pathlib.Path(os.environ['CE_P8_RUNTIME'])
expected={'ligandmpnn_v_32_010_25.pt':10541943,
          'rf3_foundry_01_24_latest_remapped.ckpt':3038876446}
rows=[]
for name,size in expected.items():
 p=root/'checkpoints'/name
 assert p.stat().st_size==size, f'Checkpoint size changed: {name}'
 h=hashlib.sha256()
 with p.open('rb') as f:
  for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
 if name.startswith('ligandmpnn_'):assert h.hexdigest()=='161cd264061fda9680cbb940255522ae42f2966c552d045d87913d9452a80970'
 if name.startswith('rf3_'):assert h.hexdigest()=='364ef592fd8042a9cf4176d045015190f8322f961ccca38d891b20ca578d3bb0'
 rows.append({'file':name,'bytes':size,'sha256':h.hexdigest(),
              'source':'official IPD server; hashes match previous completed run, not independent vendor attestations'})
(root/'checkpoint_receipts.json').write_text(json.dumps({'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkpoints':rows},indent=2)+'\n')
PY
date -u +%FT%TZ > "$CE_P8_RUNTIME/finished_utc.txt"
