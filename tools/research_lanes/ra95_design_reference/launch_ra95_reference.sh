#!/usr/bin/env bash
set -euo pipefail

# New development combination: the current public open-source inference setup
# plus the repository's author-maintained 5AN7 retroaldolase demo input. This is
# not a reproduction of the paper's historical RA95 run.

readonly EXPECTED_COMMIT="d365cbf4db3958814a9f8e4f6f94fa309dfebc2b"
readonly EXPECTED_DEMO_SHA256="6f62cc1d4faf790c8ed4582b3e28fea2fa9daa4677fa5af90bd68f145821c409"
readonly EXPECTED_INPUT_SHA256="6dc747dbb1840892ed1f2f05e44d544a888db09336f4bb9df8b7732ace663682"
readonly EXPECTED_CONFIG_SHA256="7385bbb347ff364ad4b2da4abe5957e1a96aefc3f1c0f1a111212f8737880f40"

mode="${1:---print}"
: "${RFD2_ROOT:?Set RFD2_ROOT to the pinned RFdiffusion2 checkout.}"
: "${RFD2_OUTDIR:?Set RFD2_OUTDIR to an absolute output directory.}"

if [[ "${RFD2_ROOT}" != /* || "${RFD2_OUTDIR}" != /* ]]; then
  printf '%s\n' 'RFD2_ROOT and RFD2_OUTDIR must be absolute paths.' >&2
  exit 2
fi
if [[ "${RFD2_ROOT}" =~ [[:space:]] || "${RFD2_OUTDIR}" =~ [[:space:]] ]]; then
  printf '%s\n' 'RFdiffusion2 upstream scripts do not safely support whitespace in these paths.' >&2
  exit 2
fi

readonly image="${RFD2_ROOT}/rf_diffusion/exec/bakerlab_rf_diffusion_aa.sif"
readonly model="${RFD2_ROOT}/rf_diffusion/model_weights/RFD_173.pt"
readonly pipeline="${RFD2_ROOT}/rf_diffusion/benchmark/pipeline.py"
readonly demo="${RFD2_ROOT}/rf_diffusion/benchmark/demo_enzymes.json"
readonly input="${RFD2_ROOT}/rf_diffusion/benchmark/input/ra_5an7_no_cov_ORI_cm1.pdb"
readonly config="${RFD2_ROOT}/rf_diffusion/benchmark/configs/open_source_demo.yaml"
readonly output_parent="$(dirname "${RFD2_OUTDIR}")"

readonly -a overrides=(
  '--config-name=open_source_demo'
  "sweep.command_args='--config-name=aa inference.deterministic=True inference.ckpt_path=${model} inference.seed_offset=43'"
  'sweep.benchmark_json=demo_enzymes.json'
  'sweep.benchmarks=retroaldolase'
  "outdir=${RFD2_OUTDIR}"
)

readonly -a command=(
  apptainer exec --nv
  --bind "${RFD2_ROOT}:${RFD2_ROOT}"
  --bind "${output_parent}:${output_parent}"
  "${image}"
  "${pipeline}"
  "${overrides[@]}"
)

print_command() {
  printf 'cd %q && ' "${RFD2_ROOT}"
  printf '%q ' "${command[@]}"
  printf '\n'
}

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

assert_equal() {
  local label="$1" expected="$2" actual="$3"
  if [[ "${actual}" != "${expected}" ]]; then
    printf '%s: expected %s, got %s\n' "${label}" "${expected}" "${actual}" >&2
    exit 3
  fi
}

preflight() {
  command -v apptainer >/dev/null 2>&1 || {
    printf '%s\n' 'apptainer is required.' >&2
    exit 4
  }
  command -v nvidia-smi >/dev/null 2>&1 || {
    printf '%s\n' 'An NVIDIA CUDA host visible through nvidia-smi is required.' >&2
    exit 4
  }
  nvidia-smi >/dev/null
  [[ -d "${output_parent}" ]] || {
    printf 'Output parent does not exist: %s\n' "${output_parent}" >&2
    exit 5
  }
  [[ ! -e "${RFD2_OUTDIR}" ]] || {
    printf 'Output path must be fresh: %s\n' "${RFD2_OUTDIR}" >&2
    exit 5
  }
  for required in "${image}" "${model}" "${pipeline}" "${demo}" "${input}" "${config}"; do
    [[ -s "${required}" ]] || {
      printf 'Missing required file: %s\n' "${required}" >&2
      exit 5
    }
  done
  assert_equal upstream_commit "${EXPECTED_COMMIT}" "$(git -C "${RFD2_ROOT}" rev-parse HEAD)"
  git -C "${RFD2_ROOT}" diff --quiet HEAD -- rf_diffusion setup.py || {
    printf '%s\n' 'Tracked RFdiffusion2 runtime/config files differ from the pinned commit.' >&2
    exit 3
  }
  assert_equal demo_enzymes_sha256 "${EXPECTED_DEMO_SHA256}" "$(sha256_file "${demo}")"
  assert_equal retroaldolase_input_sha256 "${EXPECTED_INPUT_SHA256}" "$(sha256_file "${input}")"
  assert_equal open_source_demo_sha256 "${EXPECTED_CONFIG_SHA256}" "$(sha256_file "${config}")"
}

resolve_config() {
  local resolved
  resolved="$(mktemp)"
  (
    cd "${RFD2_ROOT}"
    "${command[@]}" --cfg job --resolve >"${resolved}"
  )

  apptainer exec --nv "${image}" python -c '
import sys
from omegaconf import OmegaConf

c = OmegaConf.load(sys.stdin)
expected_args = " ".join("""
  --config-name=aa
  inference.deterministic=True
""".split()) + " inference.ckpt_path=" + sys.argv[2] + " inference.seed_offset=43"
checks = {
    "sweep.command_args": (" ".join(str(c.sweep.command_args).split()), expected_args),
    "sweep.benchmark_json": (c.sweep.benchmark_json, "demo_enzymes.json"),
    "sweep.benchmarks": (c.sweep.benchmarks, "retroaldolase"),
    "sweep.num_per_condition": (c.sweep.num_per_condition, 1),
    "sweep.num_per_job": (c.sweep.num_per_job, 1),
    "sweep.slurm.in_proc": (c.sweep.slurm.in_proc, True),
    "sweep.slurm.submit": (c.sweep.slurm.submit, True),
    "in_proc": (c.in_proc, True),
    "stop_step": (c.stop_step, "sweep"),
    "outdir": (c.outdir, sys.argv[1]),
    "sweep.out": (c.sweep.out, sys.argv[1] + "/run"),
}
bad = [f"{key}: expected {want!r}, got {got!r}" for key, (got, want) in checks.items() if got != want]
if bad:
    raise SystemExit("Resolved config mismatch:\n" + "\n".join(bad))
' "${RFD2_OUTDIR}" "${model}" <"${resolved}"

  rm -f "${resolved}"
  printf '%s\n' 'Resolved pipeline config contains the exact public one-design settings.'
}

case "${mode}" in
  --print)
    print_command
    ;;
  --check)
    preflight
    resolve_config
    ;;
  --execute)
    preflight
    resolve_config
    cd "${RFD2_ROOT}"
    exec "${command[@]}"
    ;;
  *)
    printf 'Usage: RFD2_ROOT=/abs/checkout RFD2_OUTDIR=/abs/output %s [--print|--check|--execute]\n' "$0" >&2
    exit 2
    ;;
esac
