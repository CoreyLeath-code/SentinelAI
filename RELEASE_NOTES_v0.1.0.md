# SentinelAI v0.1.0

SentinelAI v0.1.0 is the first formal portfolio release of the repository's reproducible drift-monitoring reference system.

## Release scope

The directly implemented statistical path compares expected and observed histograms with Population Stability Index (PSI) and a Kolmogorov-Smirnov CDF distance, then flags drift when the configured thresholds are crossed. The repository's benchmark evidence is synthetic and reproducible; it is not presented as production drift-detection accuracy, native C++ service latency, or fleet-scale throughput.

## Verified repository surface

The release candidate is gated by:

- the Python test suite;
- Go tests for the ingestion service;
- a container build for the ingestion service;
- the repository's existing CI, benchmark, schema-validation, and security workflows.

The existing CI also exercises the ingestion path behind NGINX with three replicas and verifies readiness survives loss of one backend.

## Release artifacts

A successful `v0.1.0` tag publishes:

- a deterministic source archive and SHA-256 checksum on the GitHub Release;
- the validated Go ingestion-service container at `ghcr.io/coreyleath-code/sentinelai-ingestion:0.1.0`;
- additional GHCR tags for `0.1` and `latest`.

## Reproducibility

The statistical benchmark can be regenerated with:

```bash
python benchmarks/run_benchmark.py --output benchmarks/latest.json
```

The release does not add or imply production authorization, calibrated statistical significance, production model-quality guarantees, or cross-hardware performance guarantees.
