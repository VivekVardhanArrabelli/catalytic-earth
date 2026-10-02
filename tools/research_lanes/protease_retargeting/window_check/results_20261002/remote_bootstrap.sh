#!/usr/bin/env bash
# Prepared for the authorized disposable remote GPU only; never run locally.
# The owner must terminate the rental within the shared 45-minute / $5 cap.
# This installs and checks the runtime, then downloads and pins one checkpoint.
# It does NOT launch predictions or provision/terminate a rental.
set -euo pipefail
: "${CE_RF3_BOOT_ROOT:?Fresh absolute remote bootstrap directory required}"
: "${CE_RF3_DRIVER:?Absolute path to the reviewed native gate required}"
: "${CE_RF3_INPUT_DIR:?Absolute directory containing the two reviewed inputs required}"
CE_RF3_COMMIT=0932f1cb165ae7d413c11b1a7acc04ee31758817
test ! -e "$CE_RF3_BOOT_ROOT"
mkdir -p "$CE_RF3_BOOT_ROOT"
export CE_RF3_FOUNDRY="$CE_RF3_BOOT_ROOT/foundry"
export CE_RF3_CKPT="$CE_RF3_BOOT_ROOT/checkpoints/rf3_foundry_01_24_latest_remapped.ckpt"
export CE_RF3_VENV="$CE_RF3_BOOT_ROOT/venv"
date -u +%FT%TZ > "$CE_RF3_BOOT_ROOT/bootstrap_started_utc.txt"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv > "$CE_RF3_BOOT_ROOT/gpu.csv"

# Isolated Python 3.12. uv is an installation accelerator, not model code.
# Its managed-Python download is needed only when a suitable Python is absent.
if command -v uv >/dev/null 2>&1; then
  CE_UV=$(command -v uv)
else
  python3 -m pip install --user uv
  CE_USER_BASE=$(python3 -m site --user-base)
  CE_UV="$CE_USER_BASE/bin/uv"
fi
"$CE_UV" --version > "$CE_RF3_BOOT_ROOT/uv_version.txt"
"$CE_UV" venv --python 3.12 "$CE_RF3_VENV"
export PATH="$CE_RF3_VENV/bin:$PATH"

# Fetch exactly the reviewed official source commit; do not follow a moving branch.
git init "$CE_RF3_FOUNDRY"
git -C "$CE_RF3_FOUNDRY" remote add origin https://github.com/RosettaCommons/foundry.git
git -C "$CE_RF3_FOUNDRY" fetch --depth 1 origin "$CE_RF3_COMMIT"
git -C "$CE_RF3_FOUNDRY" checkout --detach FETCH_HEAD
test "$(git -C "$CE_RF3_FOUNDRY" rev-parse HEAD)" = "$CE_RF3_COMMIT"
# Official RF3 extra, installed from the pinned checkout instead of a moving PyPI release.
"$CE_UV" pip install --torch-backend=cu128 --python "$CE_RF3_VENV/bin/python" -e "$CE_RF3_FOUNDRY[rf3]"
"$CE_UV" pip freeze --python "$CE_RF3_VENV/bin/python" > "$CE_RF3_BOOT_ROOT/runtime_freeze.txt"
python - <<'PY' > "$CE_RF3_BOOT_ROOT/runtime_gpu_check.json"
import json, sys, torch
assert sys.version_info >= (3, 12), 'RF3 requires Python >=3.12'
assert torch.cuda.is_available(), 'Installed torch cannot use the remote GPU'
assert torch.version.cuda and torch.version.cuda.split('.')[0] == '12', 'RF3 extra declares CUDA12 cuequivariance; inspect an incompatible torch build before proceeding'
print(json.dumps({'python':sys.version, 'torch':torch.__version__, 'torch_cuda':torch.version.cuda,
                  'device':torch.cuda.get_device_name(0)}, indent=2))
PY

# Run the actual native component parser and bond/charge gate before acquiring weights.
unset LOCAL_MSA_DIRS
python "$CE_RF3_DRIVER" --foundry-root "$CE_RF3_FOUNDRY" --input-dir "$CE_RF3_INPUT_DIR" --out-dir "$CE_RF3_BOOT_ROOT/native-input-gate"

# RF3 README names this file on the official IPD host. Use TLS; stop if unavailable.
# The retained README gives no vendor SHA256: this records content identity, not an
# independent cryptographic attestation of upstream weights. No HTTP fallback.
mkdir "$CE_RF3_BOOT_ROOT/checkpoints"
CE_RF3_CKPT_URL=https://files.ipd.uw.edu/pub/rf3/rf3_foundry_01_24_latest_remapped.ckpt
curl --fail --location --proto '=https' --proto-redir '=https' --connect-timeout 20 --max-time 600 --retry 0 --dump-header "$CE_RF3_BOOT_ROOT/checkpoint_http_headers.txt" --output "$CE_RF3_CKPT.part" "$CE_RF3_CKPT_URL"
test -s "$CE_RF3_CKPT.part"
mv "$CE_RF3_CKPT.part" "$CE_RF3_CKPT"
export CE_RF3_CKPT_URL
python - <<'PY'
import datetime, hashlib, json, os, pathlib, shlex
root=pathlib.Path(os.environ['CE_RF3_BOOT_ROOT'])
path=pathlib.Path(os.environ['CE_RF3_CKPT'])
h=hashlib.sha256()
with path.open('rb') as f:
    for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
pin=h.hexdigest()
receipt={'url':os.environ['CE_RF3_CKPT_URL'], 'path':str(path), 'bytes':path.stat().st_size,
         'sha256':pin, 'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'vendor_hash_available_in_retained_source':False, 'model_loaded':False}
(root/'checkpoint_download_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
names=['CE_RF3_FOUNDRY','CE_RF3_CKPT','CE_RF3_DRIVER','CE_RF3_INPUT_DIR']
lines=['export '+n+'='+shlex.quote(os.environ[n]) for n in names]
lines += ['export CE_RF3_CKPT_SHA256='+shlex.quote(pin),
          'export PATH='+shlex.quote(os.environ['CE_RF3_VENV']+'/bin')+':"$PATH"']
(root/'runtime.env').write_text('\n'.join(lines)+'\n')
print(json.dumps(receipt,indent=2))
PY
date -u +%FT%TZ > "$CE_RF3_BOOT_ROOT/bootstrap_finished_utc.txt"
# Next, source runtime.env, set a fresh CE_RF3_OUT, and run rf3_remote_commands.sh.
# Native gate failures or installation failures stop this script; do not bypass them.
