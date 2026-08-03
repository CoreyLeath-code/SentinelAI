def test_inference_success(client, monkeypatch):
    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")
    headers = {"Authorization": "Bearer test-token"}
    payload = {"prompt": "Explain AI in one sentence."}

    response = client.post("/infer", json=payload, headers=headers)

    assert response.status_code == 200
    assert "response" in response.json()
