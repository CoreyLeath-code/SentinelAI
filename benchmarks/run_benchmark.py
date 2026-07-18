#!/usr/bin/env python3
"""Deterministic SentinelAI drift-detector research benchmark.

The benchmark mirrors the PSI/KS decision rule in drift-engine/drift_engine.cpp.
It measures the portable reference implementation, not native C++ service latency.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
import random
import statistics
import sys
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path

SEED = 20260718
PSI_THRESHOLD = 0.2
KS_THRESHOLD = 0.1


def score(expected: list[float], actual: list[float]) -> tuple[float, float, bool]:
    psi = sum((a - e) * math.log(a / e) for e, a in zip(expected, actual) if e > 0 and a > 0)
    exp_total, act_total = sum(expected), sum(actual)
    exp_cdf = act_cdf = ks = 0.0
    for e, a in zip(expected, actual):
        exp_cdf += e / exp_total if exp_total else 0.0
        act_cdf += a / act_total if act_total else 0.0
        ks = max(ks, abs(exp_cdf - act_cdf))
    return psi, ks, psi > PSI_THRESHOLD or ks > KS_THRESHOLD


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lo, hi = math.floor(position), math.ceil(position)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - position) + ordered[hi] * (position - lo)


def distribution(rng: random.Random, bins: int = 32) -> list[float]:
    raw = [rng.gammavariate(2.0, 1.0) + 1e-9 for _ in range(bins)]
    total = sum(raw)
    return [value / total for value in raw]


def perturb(values: list[float], magnitude: float, rng: random.Random) -> list[float]:
    shifted = [max(1e-9, value * (1.0 + rng.uniform(-magnitude, magnitude))) for value in values]
    total = sum(shifted)
    return [value / total for value in shifted]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=20_000)
    parser.add_argument("--evaluation-samples", type=int, default=2_000)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/latest.json"))
    args = parser.parse_args()
    if args.iterations < 100 or args.evaluation_samples < 100:
        parser.error("iterations and evaluation samples must be at least 100")

    rng = random.Random(SEED)
    pairs = [(distribution(rng), None) for _ in range(args.iterations)]
    pairs = [(baseline, perturb(baseline, 0.15, rng)) for baseline, _ in pairs]

    for expected, actual in pairs[:100]:
        score(expected, actual)

    timings_us: list[float] = []
    tracemalloc.start()
    started = time.perf_counter_ns()
    for expected, actual in pairs:
        sample_start = time.perf_counter_ns()
        score(expected, actual)
        timings_us.append((time.perf_counter_ns() - sample_start) / 1_000)
    elapsed_s = (time.perf_counter_ns() - started) / 1_000_000_000
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tp = tn = fp = fn = 0
    eval_rng = random.Random(SEED + 1)
    for index in range(args.evaluation_samples):
        expected = distribution(eval_rng)
        positive = index % 2 == 0
        actual = perturb(expected, 1.8 if positive else 0.05, eval_rng)
        predicted = score(expected, actual)[2]
        if positive and predicted: tp += 1
        elif positive: fn += 1
        elif predicted: fp += 1
        else: tn += 1
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    result = {
        "schema_version": 1,
        "benchmark": "python-reference-drift-decision",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "protocol": {"iterations": args.iterations, "warmup": 100, "bins": 32, "evaluation_samples": args.evaluation_samples},
        "latency_us": {
            "mean": statistics.fmean(timings_us), "median": statistics.median(timings_us),
            "p95": percentile(timings_us, 0.95), "p99": percentile(timings_us, 0.99),
            "min": min(timings_us), "max": max(timings_us),
        },
        "throughput_ops_s": args.iterations / elapsed_s,
        "peak_tracemalloc_mib": peak_bytes / 1_048_576,
        "quality": {"precision": precision, "recall": recall, "f1": f1, "confusion_matrix": {"tp": tp, "tn": tn, "fp": fp, "fn": fn}},
        "limitations": ["Measures the Python reference implementation, not native C++ or HTTP latency.", "Quality labels use seeded synthetic perturbation classes, not production ground truth."],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

