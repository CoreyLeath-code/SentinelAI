-- SentinelAI — minimal local schema
-- Mounted into Postgres via docker-entrypoint-initdb.d

CREATE TABLE IF NOT EXISTS inference_logs (
    id             BIGSERIAL PRIMARY KEY,
    model_id       TEXT        NOT NULL,
    model_version  TEXT,
    latency_ms     INTEGER,
    tokens_in      INTEGER,
    tokens_out     INTEGER,
    status         TEXT        NOT NULL DEFAULT 'ok',
    features       JSONB,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS drift_baselines (
    id                  BIGSERIAL PRIMARY KEY,
    model_id            TEXT    NOT NULL,
    feature_name        TEXT    NOT NULL,
    baseline_histogram  JSONB   NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (model_id, feature_name)
);

CREATE TABLE IF NOT EXISTS drift_scores (
    id             BIGSERIAL PRIMARY KEY,
    model_id       TEXT             NOT NULL,
    feature_name   TEXT             NOT NULL,
    psi            DOUBLE PRECISION,
    ks_stat        DOUBLE PRECISION,
    drift_detected BOOLEAN          NOT NULL DEFAULT FALSE,
    computed_at    TIMESTAMPTZ      NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incidents (
    id         BIGSERIAL PRIMARY KEY,
    type       TEXT    NOT NULL,
    severity   TEXT    NOT NULL DEFAULT 'medium',
    details    JSONB,
    resolved   BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incident_summaries (
    id          BIGSERIAL PRIMARY KEY,
    incident_id BIGINT      REFERENCES incidents (id),
    summary     TEXT        NOT NULL,
    model_used  TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
