import pytest

def test_mcp_health(mcp_client):
    response = mcp_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "model-control-plane"}

def test_mcp_register_model_success(mcp_client):
    payload = {
        "name": "fraud-detector-v1",
        "version": "1.0",
        "description": "Initial model",
        "framework": "PyTorch",
        "s3_uri": "s3://models/fraud-detector-v1/model.pt"
    }
    response = mcp_client.post("/api/v1/models", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "id" in data["data"]
    assert data["message"] == "Model registered successfully"

def test_mcp_register_model_invalid_payload(mcp_client):
    payload = {
        "name": "fraud-detector-v1"
        # Missing required fields like version, description, etc.
    }
    response = mcp_client.post("/api/v1/models", json=payload)
    assert response.status_code == 422 # Pydantic type blocking

def test_mcp_get_nonexistent_model(mcp_client):
    response = mcp_client.get("/api/v1/models/non-existent-uuid")
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found"
