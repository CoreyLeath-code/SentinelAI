def test_infer_fails_closed_when_bearer_token_is_unconfigured(client, monkeypatch):
    monkeypatch.delenv("API_BEARER_TOKEN", raising=False)

    response = client.post("/infer", json={"prompt": "Hello"})
    predict_response = client.post("/predict", json={"features": [0.0] * 16})

    assert response.status_code == 503
    assert predict_response.status_code == 503


def test_infer_rejects_missing_and_invalid_bearer_tokens(client, monkeypatch):
    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")

    assert client.post("/infer", json={"prompt": "Hello"}).status_code == 401
    assert client.post(
        "/infer",
        json={"prompt": "Hello"},
        headers={"Authorization": "Bearer wrong-token"},
    ).status_code == 401
    assert client.post("/predict", json={"features": [0.0] * 16}).status_code == 401
    assert client.post(
        "/predict",
        json={"features": [0.0] * 16},
        headers={"Authorization": "Bearer wrong-token"},
    ).status_code == 401
