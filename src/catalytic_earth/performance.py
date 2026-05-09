from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable

from .geometry_retrieval import load_json, run_geometry_retrieval
from .labels import evaluate_geometry_retrieval, load_labels, sweep_abstention_thresholds
from .v2 import build_mechanism_benchmark


def run_local_performance_suite(
    graph_path: Path,
    geometry_path: Path,
    retrieval_path: Path,
    iterations: int = 5,
) -> dict[str, Any]:
    if iterations < 1:
        raise ValueError("iterations must be positive")

    graph = load_json(graph_path)
    geometry = load_json(geometry_path)
    retrieval = load_json(retrieval_path)
    labels = load_labels()

    benchmarks = [
        _measure("load_v1_graph", lambda: load_json(graph_path), iterations),
        _measure("build_v2_benchmark", lambda: build_mechanism_benchmark(graph), iterations),
        _measure("run_geometry_retrieval", lambda: run_geometry_retrieval(geometry), iterations),
        _measure(
            "evaluate_geometry_labels",
            lambda: evaluate_geometry_retrieval(retrieval, labels),
            iterations,
        ),
        _measure(
            "sweep_abstention_thresholds",
            lambda: sweep_abstention_thresholds(retrieval, labels),
            iterations,
        ),
    ]
    return {
        "metadata": {
            "suite": "local_artifact_performance",
            "iterations": iterations,
            "validation_boundary": "local wall-clock timing for existing artifacts; not a scalability benchmark",
            "inputs": {
                "graph_path": str(graph_path),
                "graph_bytes": graph_path.stat().st_size,
                "geometry_path": str(geometry_path),
                "geometry_bytes": geometry_path.stat().st_size,
                "retrieval_path": str(retrieval_path),
                "retrieval_bytes": retrieval_path.stat().st_size,
            },
        },
        "benchmarks": benchmarks,
    }


def write_local_performance_suite(
    graph_path: Path,
    geometry_path: Path,
    retrieval_path: Path,
    out_path: Path,
    iterations: int = 5,
) -> dict[str, Any]:
    report = run_local_performance_suite(
        graph_path=graph_path,
        geometry_path=geometry_path,
        retrieval_path=retrieval_path,
        iterations=iterations,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _measure(name: str, func: Callable[[], Any], iterations: int) -> dict[str, Any]:
    durations: list[float] = []
    last_result: Any = None
    for _ in range(iterations):
        started = time.perf_counter()
        last_result = func()
        durations.append((time.perf_counter() - started) * 1000)
    return {
        "name": name,
        "iterations": iterations,
        "min_ms": round(min(durations), 3),
        "mean_ms": round(sum(durations) / len(durations), 3),
        "max_ms": round(max(durations), 3),
        "result_summary": _result_summary(last_result),
    }


def _result_summary(result: Any) -> dict[str, Any]:
    if not isinstance(result, dict):
        return {"type": type(result).__name__}
    metadata = result.get("metadata", {})
    if isinstance(metadata, dict):
        return {
            key: value
            for key, value in metadata.items()
            if key.endswith("_count")
            or key in {
                "entry_count",
                "record_count",
                "evaluated_count",
                "top1_accuracy_in_scope",
                "top3_accuracy_in_scope",
                "out_of_scope_abstention_rate",
                "selected_threshold",
            }
        }
    return {"keys": sorted(result.keys())}
