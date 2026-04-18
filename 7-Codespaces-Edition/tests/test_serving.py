import pytest

def test_serving_health(serving_client):
    response = serving_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "model-serving-api"

def test_serving_predict_success(serving_client):
    payload = {
        "model_id": "test-model-123",
        "input_data": [0.1, 0.2, 0.3, 0.4]
    }
    response = serving_client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["model_id"] == "test-model-123"
    assert "prediction" in data
    assert "confidence" in data
    assert "rag_context_results" in data
    assert data["rag_context_results"] >= 1 # Assert mock RAG payload handling
    assert data["rag_context_results"] <= 5

def test_serving_predict_empty_data(serving_client):
    payload = {
        "model_id": "test-model-123",
        "input_data": []
    }
    response = serving_client.post("/predict", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Input data cannot be empty"

def test_serving_predict_invalid_data(serving_client):
    payload = {
        "model_id": "test-model-123",
        "input_data": ["not-a-float"]
    }
    response = serving_client.post("/predict", json=payload)
    assert response.status_code == 422 # Pydantic type validation
