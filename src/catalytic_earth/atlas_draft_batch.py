"""Declarative repository paths for immutable source-draft batches."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class DraftBatchPaths:
    """Repository-relative source and review paths for one draft batch."""

    batch_id: str
    source_directory: Path
    probe_spec_path: Path
    probe_report_path: Path
    gate_directory: Path
    challenge_path: Path
    predecessor_batch_id: str | None = None

    def __post_init__(self) -> None:
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", self.batch_id) is None:
            raise ValueError("batch_id must be a lowercase hyphenated identifier")
        for field_name in (
            "source_directory",
            "probe_spec_path",
            "probe_report_path",
            "gate_directory",
            "challenge_path",
        ):
            path = getattr(self, field_name)
            if not isinstance(path, Path) or path.is_absolute() or ".." in path.parts:
                raise ValueError(f"{field_name} must be a repository-relative Path")

    @property
    def manifest_path(self) -> Path:
        return self.source_directory / "source_manifest.json"

    @property
    def sources_directory(self) -> Path:
        return self.source_directory / "sources"

    @property
    def attribution_path(self) -> Path:
        return self.source_directory / "SOURCE_ATTRIBUTION.md"

    @property
    def records_path(self) -> Path:
        return self.source_directory / "records.json"

    @property
    def adjudications_path(self) -> Path:
        return self.gate_directory / "adjudications.json"

    @property
    def review_bindings_path(self) -> Path:
        return self.gate_directory / "review_bindings.json"

    @property
    def status_path(self) -> Path:
        return self.gate_directory / "status.json"


DEFAULT_BATCH = DraftBatchPaths(
    batch_id="default",
    source_directory=Path("data/atlas/source_drafts"),
    probe_spec_path=Path("data/atlas/atlas50/state_probe/spec.json"),
    probe_report_path=Path("data/atlas/atlas50/state_probe/report.json"),
    gate_directory=Path("data/atlas/atlas50/development_gate"),
    challenge_path=Path(
        "data/atlas/atlas50/computational_review/source_challenge_20260905.json"
    ),
)

_ALDOLASE_ROOT = Path(
    "data/atlas/source_drafts/batches/aldolase-transketolase"
)
ALDOLASE_TRANSKETOLASE_BATCH = DraftBatchPaths(
    batch_id="aldolase-transketolase",
    source_directory=_ALDOLASE_ROOT,
    probe_spec_path=_ALDOLASE_ROOT / "review/spec.json",
    probe_report_path=_ALDOLASE_ROOT / "review/probe.json",
    gate_directory=_ALDOLASE_ROOT / "review",
    challenge_path=_ALDOLASE_ROOT / "review/challenge.json",
    predecessor_batch_id="default",
)

_PLP_ROOT = Path("data/atlas/source_drafts/batches/plp-pyruvoyl")
PLP_PYRUVOYL_BATCH = DraftBatchPaths(
    batch_id="plp-pyruvoyl",
    source_directory=_PLP_ROOT,
    probe_spec_path=_PLP_ROOT / "review/spec.json",
    probe_report_path=_PLP_ROOT / "review/probe.json",
    gate_directory=_PLP_ROOT / "review",
    challenge_path=_PLP_ROOT / "review/challenge.json",
    predecessor_batch_id="aldolase-transketolase",
)

BATCHES: Mapping[str, DraftBatchPaths] = MappingProxyType(
    {
        DEFAULT_BATCH.batch_id: DEFAULT_BATCH,
        ALDOLASE_TRANSKETOLASE_BATCH.batch_id: ALDOLASE_TRANSKETOLASE_BATCH,
        PLP_PYRUVOYL_BATCH.batch_id: PLP_PYRUVOYL_BATCH,
    }
)


def resolve_batch(name: str | None) -> DraftBatchPaths:
    """Resolve a supported declarative batch name; ``None`` means legacy default."""

    key = DEFAULT_BATCH.batch_id if name is None else name
    try:
        return BATCHES[key]
    except (KeyError, TypeError) as exc:
        choices = ", ".join(BATCHES)
        raise ValueError(f"unknown source-draft batch {name!r}; choose {choices}") from exc


def predecessor_batch(batch: DraftBatchPaths) -> DraftBatchPaths:
    """Return the configured predecessor; source data cannot select its own base."""

    if batch.predecessor_batch_id is None:
        raise ValueError("source-draft batch has no configured predecessor")
    predecessor = resolve_batch(batch.predecessor_batch_id)
    if predecessor.batch_id == batch.batch_id:
        raise ValueError("source-draft batch cannot inherit itself")
    return predecessor
