# drift-engine — multi-stage: build C++ binary, then run Python HTTP server
FROM gcc:12 AS cpp-builder
WORKDIR /app
COPY drift_engine.cpp .
RUN g++ -O2 -std=c++17 -o drift_engine drift_engine.cpp

# ── Python runtime ──────────────────────────────────────────────────────────
FROM python:3.11-slim
WORKDIR /app
COPY --from=cpp-builder /app/drift_engine ./drift_engine
COPY server.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7070
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7070/health')"

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7070"]
