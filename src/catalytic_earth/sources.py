from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .models import RegistryError, SourceRecord


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_REGISTRY = PROJECT_ROOT / "data" / "registries" / "source_registry.json"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_sources(path: Path = SOURCE_REGISTRY) -> list[SourceRecord]:
    data = read_json(path)
    if not isinstance(data, list):
        raise RegistryError("source registry must be a list")

    records = [SourceRecord.from_dict(item, index) for index, item in enumerate(data)]
    ids = [record.id for record in records]
    duplicates = sorted(item for item, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise RegistryError(f"duplicate source ids: {', '.join(duplicates)}")
    return records


def build_source_ledger(records: list[SourceRecord]) -> dict[str, Any]:
    by_category: dict[str, list[str]] = defaultdict(list)
    by_role: dict[str, list[str]] = defaultdict(list)
    by_priority: dict[str, list[str]] = defaultdict(list)

    for record in records:
        by_category[record.category].append(record.id)
        by_priority[str(record.priority)].append(record.id)
        for role in record.roles:
            by_role[role].append(record.id)

    return {
        "source_count": len(records),
        "category_count": len(by_category),
        "by_category": {key: sorted(value) for key, value in sorted(by_category.items())},
        "by_role": {key: sorted(value) for key, value in sorted(by_role.items())},
        "by_priority": {key: sorted(value) for key, value in sorted(by_priority.items())},
        "sources": [record.to_dict() for record in sorted(records, key=lambda item: (item.priority, item.id))],
    }
