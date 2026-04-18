from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import datetime

app = FastAPI(title="Model Control Plane (MCP) API", description="Centralized Model Registry and Lifecycle Manager")

# In-memory database for demonstration purposes
# In a real FAANG environment, this would be PostgreSQL/DynamoDB and connected to MLflow
models_db = {}

class ModelSpec(BaseModel):
    name: str
    version: str
    description: str
    framework: str # e.g., PyTorch, TensorFlow, Scikit-learn
    s3_uri: str

class ModelStatusUpdate(BaseModel):
    status: str # e.g., STAGING, PRODUCTION, ARCHIVED

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "model-control-plane"}

@app.post("/api/v1/models")
def register_model(spec: ModelSpec):
    model_id = str(uuid.uuid4())
    models_db[model_id] = {
        "id": model_id,
        "spec": spec.dict(),
        "status": "REGISTERED",
        "registered_at": datetime.datetime.utcnow().isoformat()
    }
    return {"message": "Model registered successfully", "data": models_db[model_id]}

@app.get("/api/v1/models")
def list_models():
    return {"models": list(models_db.values())}

@app.get("/api/v1/models/{model_id}")
def get_model(model_id: str):
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    return models_db[model_id]

@app.put("/api/v1/models/{model_id}/status")
def update_model_status(model_id: str, update: ModelStatusUpdate):
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Model not found")
    
    valid_statuses = ["REGISTERED", "STAGING", "PRODUCTION", "ARCHIVED"]
    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
    models_db[model_id]["status"] = update.status
    models_db[model_id]["updated_at"] = datetime.datetime.utcnow().isoformat()
    return {"message": "Status updated", "data": models_db[model_id]}
