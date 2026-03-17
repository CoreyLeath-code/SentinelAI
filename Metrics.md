# SentinelAI — Performance & Evaluation Metrics

## Drift Detection Metrics

| Metric | Description |
|--------|------------|
| PSI | Population Stability Index |
| KS Statistic | Kolmogorov-Smirnov test |
| Drift Threshold | Configurable alert threshold |

---

## Model Performance

| Metric | Value |
|--------|-------|
| Precision | TBD |
| Recall | TBD |
| ROC-AUC | TBD |
| F1 Score | TBD |

---

## LLM Monitoring

| Metric | Description |
|--------|------------|
| Hallucination Score | Confidence-based hallucination probability |
| Token Usage | Tokens per request |
| Latency | Response time per inference |

---

## Infrastructure

| Metric | Description |
|--------|------------|
| P95 Latency | 95th percentile response time |
| Throughput | Requests per second |
| Cost per 1k requests | Cloud compute estimate |


## Performance Benchmarks

| Component | Metric | Result |
|------------|--------|--------|
| C++ Drift Engine | PSI calculation time | < 2ms |
| Go Ingestion API | P95 latency | 180ms |
| LLM Guard | Avg summarization time | 1.2s |
| Throughput | Requests/sec | 150 RPS |
| Docker container startup | Cold start | < 3s |
