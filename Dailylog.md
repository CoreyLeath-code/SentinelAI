# Daily Log

## 2026-08-12 — Load-balancer gap recorded

An infrastructure audit found that the Compose stack exposes the ingestion service, drift engine, and LLM guard directly on host ports. Existing service health checks do not provide a stable proxy endpoint, multi-replica routing, or unhealthy-upstream handling.

Tracking issue: [#21 — add a health-aware load-balancing layer for API workers](https://github.com/CoreyLeath-code/SentinelAI/issues/21).

This record does **not** claim a load balancer, horizontal scaling, resilience test, or benchmark result has been implemented. The issue defines the required implementation and validation scope.
