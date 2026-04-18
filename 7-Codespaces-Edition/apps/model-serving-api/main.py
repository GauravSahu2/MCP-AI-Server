from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import os
# from pymilvus import connections, Collection # Commented out so it doesn't crash if Milvus is down locally

app = FastAPI(title="Model Serving API", description="High-throughput API for AI Inference with RAG")

class PredictionRequest(BaseModel):
    model_id: str
    input_data: list[float]

@app.on_event("startup")
def startup_event():
    # Example connection snippet for Milvus
    # milvus_host = os.getenv("MILVUS_HOST", "milvus-standalone.default.svc.cluster.local")
    # connections.connect("default", host=milvus_host, port="19530")
    print("Mock Milvus connected successfully.")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "model-serving-api", "ready_for_inference": True, "vector_db": "connected"}

@app.post("/predict")
def predict(req: PredictionRequest):
    if len(req.input_data) == 0:
        raise HTTPException(status_code=400, detail="Input data cannot be empty")
        
    # [NEW] Mock Vector Database Query (RAG Step)
    # Search for similar embeddings in Milvus
    # results = collection.search(data=[req.input_data], anns_field="embedding", param={"metric_type": "L2", "params": {"nprobe": 10}}, limit=3)
    mock_rag_context_retrieved = random.randint(1, 5)
    
    # Simulate processing time and result (Augmented by Vector DB)
    confidence = round(random.uniform(0.85, 0.99), 4) # Higher confidence due to RAG
    prediction_class = random.choice(["Fraud", "Not Fraud", "Anomaly", "Normal"])
    
    return {
        "model_id": req.model_id,
        "prediction": prediction_class,
        "confidence": confidence,
        "rag_context_results": mock_rag_context_retrieved,
        "latency_ms": random.randint(20, 200) # Slightly higher latency due to RAG
    }
