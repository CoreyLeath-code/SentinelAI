# Contributing to SentinelAI

## Getting Started

The fastest way to get a working development environment is Docker Compose:

```bash
cp .env.example .env
docker compose up --build
```

This starts the full local stack (Postgres, ingestion service, drift engine, LLM guard,
Streamlit dashboard, Prometheus, and Grafana).  See [README.md](README.md) for service URLs
and example curl commands.

## How to Contribute
1. Fork the repo
2. Create a feature branch
3. Add tests
4. Submit PR

## Code Standards
- Black formatting
- Pytest required
- Type hints encouraged

## Local Dev Tips

- **Warehouse mode**: `WAREHOUSE_MODE=postgres` (default) uses the local Postgres container.
  Set `WAREHOUSE_MODE=snowflake` and fill in Snowflake credentials in `.env` to use a real warehouse.
- **LLM Guard**: the service works without Ollama — it falls back to a rule-based stub automatically.
- **Rebuild a single service**: `docker compose up --build <service-name>` (e.g. `docker compose up --build drift-engine`).
- **View logs**: `docker compose logs -f <service-name>`.

