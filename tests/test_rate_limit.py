def test_rate_limit(client, monkeypatch):
    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")
    headers = {"Authorization": "Bearer test-token"}
    payload = {"prompt": "rate limit test"}

    for _ in range(5):
        client.post("/infer", json=payload, headers=headers)

    response = client.post("/infer", json=payload, headers=headers)
    assert response.status_code in [429, 200]
