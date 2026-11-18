from api import main


def test_predict_accepts_exact_model_feature_dimension(client, monkeypatch):
    monkeypatch.setattr(main, "run_inference", lambda features: [0.42])
    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")

    response = client.post(
        "/predict",
        json={"features": [0.0] * 16},
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 200
    assert response.json() == {"prediction": [0.42]}


def test_predict_rejects_feature_vectors_with_the_wrong_dimension(client, monkeypatch):
    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")
    response = client.post(
        "/predict",
        json={"features": [0.0] * 15},
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 422
    assert any(error["loc"] == ["body", "features"] for error in response.json()["detail"])


def test_predict_rejects_non_finite_features(client, monkeypatch):
    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")

    response = client.post(
        "/predict",
        json={"features": ["NaN"] * 16},
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 422


def test_predict_fails_closed_when_model_checkpoint_is_unavailable(client, monkeypatch):
    from api import inference

    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")
    monkeypatch.delenv("SENTINEL_MODEL_CHECKPOINT", raising=False)
    monkeypatch.delenv("SENTINEL_MODEL_SHA256", raising=False)
    monkeypatch.setattr(main, "run_inference", inference.run_inference)
    monkeypatch.setattr(inference, "_model", None)

    response = client.post(
        "/predict",
        json={"features": [0.0] * 16},
        headers={"Authorization": "Bearer test-token"},
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "Verified model unavailable"


def test_inference_rejects_bad_checkpoint_digest_before_model_load(monkeypatch, tmp_path):
    from api import inference

    artifact = tmp_path / "model.pt"
    artifact.write_bytes(b"not a verified model")
    monkeypatch.setenv("SENTINEL_MODEL_CHECKPOINT", str(artifact))
    monkeypatch.setenv("SENTINEL_MODEL_SHA256", "0" * 64)
    monkeypatch.setattr(inference, "_model", None)
    try:
        inference._get_model()
    except RuntimeError as exc:
        assert "fingerprint verification failed" in str(exc)
    else:
        raise AssertionError("unverified checkpoint unexpectedly loaded")
