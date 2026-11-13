def test_inference_success(client, monkeypatch):
    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")
    headers = {"Authorization": "Bearer test-token"}
    payload = {"prompt": "Explain AI in one sentence."}

    response = client.post("/infer", json=payload, headers=headers)

    assert response.status_code == 200
    assert "response" in response.json()


def test_inference_rejects_empty_or_oversized_prompts(client, monkeypatch):
    monkeypatch.setenv("API_BEARER_TOKEN", "test-token")
    headers = {"Authorization": "Bearer test-token"}

    assert client.post("/infer", json={"prompt": ""}, headers=headers).status_code == 422
    assert client.post(
        "/infer",
        json={"prompt": "x" * 4_001},
        headers=headers,
    ).status_code == 422
