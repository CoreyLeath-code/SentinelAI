# SentinelAI Research Benchmark Report

## Executive summary

This report records a deterministic evaluation of the PSI/KS drift-decision rule used by SentinelAI. The committed baseline is a portable Python reference implementation that mirrors the thresholds and equations in `drift-engine/drift_engine.cpp`. It is intentionally reported separately from native C++ and end-to-end HTTP latency.

| Metric | Baseline |
|---|---:|
| Samples | 20,000 timed + 2,000 labeled |
| Mean latency | 41.706 µs |
| Median latency | 39.700 µs |
| P95 latency | 54.700 µs |
| P99 latency | 76.200 µs |
| Min / max latency | 23.700 / 319.200 µs |
| Throughput | 23,031.13 operations/s |
| Peak traced Python memory | 0.623 MiB |
| Precision / recall / F1 | 1.000 / 1.000 / 1.000 |
| Confusion matrix | TP 1000, TN 1000, FP 0, FN 0 |

## Protocol

- Fixed seed: `20260718`
- Runtime: CPython 3.12.13 on Windows 11
- Workload: 32-bin normalized gamma distributions
- Timing population: 20,000 evaluations after 100 warm-up evaluations
- Quality population: 2,000 balanced synthetic examples
- Positive class: strong seeded perturbation (`magnitude=1.8`)
- Negative class: weak seeded perturbation (`magnitude=0.05`)
- Decision rule: `PSI > 0.20 or KS > 0.10`
- Percentiles: linear interpolation over ordered observations
- Memory: peak allocations reported by Python `tracemalloc`

Reproduce with:

```bash
python benchmarks/run_benchmark.py --output benchmarks/latest.json
```

## Interpretation

The baseline demonstrates that the reference decision rule is inexpensive and perfectly separates the deliberately distinct synthetic classes in this controlled experiment. The quality result is a pipeline regression check, not a claim of production model accuracy. Native C++ service latency, network latency, database effects, concurrency, and real-world drift labels remain separate evaluation domains.

## Regression policy

CI fails when the benchmark cannot execute or its artifact is invalid. Performance changes are surfaced by the checked-in JSON diff and uploaded artifact. A performance regression should be investigated when median or P95 latency increases by more than 15% on comparable hardware and runtime; update the baseline only with an explanation of the environment and cause.

## Evidence and limitations

Raw machine-readable evidence is stored in [latest.json](latest.json). The harness and seed are versioned in [run_benchmark.py](run_benchmark.py).

- The benchmark measures the Python reference implementation, not the native C++ binary or HTTP service.
- Synthetic labels validate repeatability and decision behavior; they do not replace production ground truth.
- Cross-host microbenchmark comparisons require comparable CPU, OS, Python version, power policy, and background load.
