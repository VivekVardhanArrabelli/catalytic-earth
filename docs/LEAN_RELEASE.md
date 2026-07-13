# Lean release and restore

The canonical release is the wheel plus the deterministic lean source archive.
Neither contains the 5.1 GB historical artifact tree or 1,316 historical
`work/` reports.

## Fast Git entry

Sparse checkout alone still downloads historical blobs. Use a blob-filtered
public HTTPS clone:

```bash
git clone --filter=blob:none --sparse \
  https://github.com/VivekVardhanArrabelli/catalytic-earth.git
cd catalytic-earth
git sparse-checkout set .github config data/governance docs environments \
  release requirements scripts src tests
```

Git history remains authoritative. This does not rewrite or discard old
provenance; blobs are fetched only if requested.

## Deterministic assets

```bash
python -m pip install -r requirements/build.lock
python scripts/build_canonical_release_assets.py \
  --source-commit <release_manifest.source_commit>
python scripts/verify_core_release.py \
  --wheel dist \
  --source-archive dist/catalytic-earth-0.1.0-lean-source.zip
python scripts/build_release_manifest.py --check
```

The asset builder first creates the deterministic lean archive from exact Git
blobs, extracts it into a temporary directory, sets `SOURCE_DATE_EPOCH` from
the source commit, and builds the wheel there with the locked tools and
`--no-isolation`. It does not accidentally build from later release-metadata
commits or from uncommitted working-tree files.

The verifier creates empty temporary directories and a fresh virtual
environment, installs the wheel with `--no-deps`, runs the golden command from
an unrelated working directory, checks the result hash, safely extracts the
source archive, and repeats the command from source.

Linux and Windows, Python 3.10 and 3.12, run this exact path in CI. A release is
not called cross-platform verified until all four jobs pass for its exact
commit.

## Historical bundles

`release/report_archive_index.json` maps every historical `work/` report to an
exact Git blob and deterministic bundle group. The deterministic report bundle
is a canonical release asset. Build it with:

```bash
python scripts/build_report_archive.py --check --build-bundle
```

The 5.1 GB historical `artifacts/` surface remains in exact Git objects and is
bound by `release/live_artifact_manifest.json`; it is not part of the lean
release. Copying it to another service is a separate rights-sensitive
migration, not a prerequisite for using the canonical core. No large file may
be removed until its external URI, SHA-256, source rights, and empty-directory
restore test are recorded. The old Git commit remains citable even after a
future migration.
