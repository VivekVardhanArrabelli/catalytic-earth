"""Compile offline source drafts and their wheel assets, or check exact bytes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from catalytic_earth.atlas_drafts import build_source_drafts, validate_source_drafts
from catalytic_earth.atlas_draft_batch import BATCHES, DEFAULT_BATCH, resolve_batch


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--batch", choices=sorted(BATCHES), default="default")
    args = parser.parse_args()
    batch = resolve_batch(args.batch)
    bundle = build_source_drafts(ROOT, batch=batch)
    summary = validate_source_drafts(bundle)
    payload = canonical_bytes(bundle)
    attribution = (ROOT / batch.attribution_path).read_bytes()
    expected = {
        "schema_version": "catalytic-earth.source-drafts-package.v1",
        "bundle_sha256": hashlib.sha256(payload).hexdigest(),
        "attribution_sha256": hashlib.sha256(attribution).hexdigest(),
    }
    stem = "source_drafts" if batch == DEFAULT_BATCH else batch.batch_id.replace("-", "_")
    outputs = {
        batch.records_path.as_posix(): payload,
        f"src/catalytic_earth/draft_data/{stem}.json": payload,
        f"src/catalytic_earth/draft_data/{stem}_attribution.md": attribution,
    }
    primary_source = ROOT / batch.gate_directory / "primary_evidence_annotations.json"
    primary_target = f"src/catalytic_earth/draft_data/{stem}_primary_evidence.json"
    primary = None
    if primary_source.is_file():
        from catalytic_earth.atlas_primary_evidence import validate_primary_evidence

        primary = json.loads(primary_source.read_text(encoding="utf-8"))
        validate_primary_evidence(primary, bundle=bundle, repo_root=ROOT)
        if any(
            annotation["annotation_kind"] == "primary_observed_state_context"
            for annotation in primary["annotations"]
        ):
            from catalytic_earth.atlas_primary_source_check import (
                audit_primary_structure_evidence,
            )

            audit_primary_structure_evidence(primary, ROOT)
        primary_raw = canonical_bytes(primary)
        expected["primary_evidence_sha256"] = hashlib.sha256(primary_raw).hexdigest()
        outputs[primary_target] = primary_raw
    elif (ROOT / primary_target).exists():
        raise SystemExit("packaged primary evidence exists without its reviewed repository input")
    reaction_source = ROOT / batch.gate_directory / "reaction_correspondence_annotations.json"
    reaction_target = f"src/catalytic_earth/draft_data/{stem}_reaction_correspondence.json"
    if reaction_source.is_file():
        from catalytic_earth.atlas_reaction_correspondence import validate_reaction_correspondence

        reaction_correspondence = json.loads(reaction_source.read_text(encoding="utf-8"))
        validate_reaction_correspondence(reaction_correspondence, bundle=bundle, repo_root=ROOT)
        reaction_raw = canonical_bytes(reaction_correspondence)
        expected["reaction_correspondence_sha256"] = hashlib.sha256(reaction_raw).hexdigest()
        outputs[reaction_target] = reaction_raw
        attribution_bindings = [item for item in reaction_correspondence["source_bindings"]
                                if item["artifact_kind"] == "attribution"]
        if len(attribution_bindings) != 1:
            raise SystemExit("reaction correspondence requires one source attribution")
        reaction_attribution = (ROOT / attribution_bindings[0]["path"]).read_bytes()
        expected["reaction_attribution_sha256"] = hashlib.sha256(reaction_attribution).hexdigest()
        outputs[f"src/catalytic_earth/draft_data/{stem}_reaction_attribution.md"] = reaction_attribution
    elif (ROOT / reaction_target).exists():
        raise SystemExit("packaged reaction correspondence exists without its reviewed repository input")
    step_source = ROOT / batch.gate_directory / "step_evidence_annotations.json"
    step_target = f"src/catalytic_earth/draft_data/{stem}_step_evidence.json"
    if step_source.is_file():
        from catalytic_earth.atlas_step_evidence import validate_step_evidence

        step_evidence = json.loads(step_source.read_text(encoding="utf-8"))
        validate_step_evidence(
            step_evidence, bundle=bundle, repo_root=ROOT,
            primary_evidence=(
                primary if step_evidence.get("primary_evidence_binding") is not None else None
            ),
        )
        step_raw = canonical_bytes(step_evidence)
        expected["step_evidence_sha256"] = hashlib.sha256(step_raw).hexdigest()
        outputs[step_target] = step_raw
    elif (ROOT / step_target).exists():
        raise SystemExit("packaged step evidence exists without its reviewed repository input")
    outputs[f"src/catalytic_earth/draft_data/{stem}_expected.json"] = canonical_bytes(expected)
    for relative, raw in outputs.items():
        path = ROOT / relative
        if args.check:
            if not path.is_file() or path.read_bytes() != raw:
                raise SystemExit(f"source draft output is stale: {relative}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
