# SentinelAI Production Metrics

## Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 0.91 |
| F1 Score | 0.88 |
| Precision | 0.89 |
| Recall | 0.87 |

## Inference Performance

| Metric | Value |
|--------|-------|
| Avg Latency | 34 ms |
| p95 Latency | 79 ms |
| Throughput | 145 req/s |
| GPU Utilization | 72% |

## Load Testing (Locust)

| Virtual Users | Avg Response Time | Failure Rate |
|---------------|------------------|--------------|
| 50 | 42 ms | 0% |
| 100 | 68 ms | 0.2% |
| 200 | 110 ms | 1.1% |
