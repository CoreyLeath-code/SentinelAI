# Root directory audit

Reviewed on 2026-08-05. This record captures the reference searches and disposition of ambiguous root files.

## Moved

| Original file | Canonical location | Reason |
| --- | --- | --- |
| `FILE Structure` | `docs/reference/historical-repository-layout.md` | Unique, manually maintained historical layout reference; moved from a space-containing root filename. |
| `Prometheus ServiceMonitor (Metrics Credibility)` | `k8s/sentinelai-backend-servicemonitor.yaml` | Unique `ServiceMonitor` manifest; Kubernetes manifests belong under `k8s/`. |

## Removed duplicate

| Removed file | Canonical source | Verification |
| --- | --- | --- |
| `Test` | `tests/` directory | The root file was only a five-file snapshot of the existing test tree. Repository searches found no build, CI, Docker, script, documentation, or source reference to the root snapshot. |

## NEEDS HUMAN DECISION

| Filename | Why deletion is uncertain | Recommended action |
| --- | --- | --- |
| `bindings.cpp` | It is a unique pybind11 module declaration for `ingestion_cpp`; no `ingestion_cpp/` implementation or build reference was found, so its intended integration cannot be proven. | Identify or add the owning extension build and implementation; then either move it with that component or remove it in a dedicated, build-validated PR. |
| `drift_engine.cpp` | It is not identical to `drift-engine/drift_engine.cpp`: the root program is a PSI-only sample, while the service implementation parses JSON and computes PSI/KS. `docker/Dockerfile` explicitly compiles the root file. | Choose one supported drift-engine image/build path, update the Docker/build/documentation references, then remove the other implementation only after an image build and behavior test. |
