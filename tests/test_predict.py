from api import main


def test_predict_accepts_exact_model_feature_dimension(client, monkeypatch):
    monkeypatch.setattr(main, "run_inference", lambda features: [0.42])

    response = client.post("/predict", json={"features": [0.0] * 16})

    assert response.status_code == 200
    assert response.json() == {"prediction": [0.42]}


def test_predict_rejects_feature_vectors_with_the_wrong_dimension(client):
    response = client.post("/predict", json={"features": [0.0] * 15})

    assert response.status_code == 422
    assert any(error["loc"] == ["body", "features"] for error in response.json()["detail"])
