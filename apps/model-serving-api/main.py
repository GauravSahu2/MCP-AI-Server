from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import os
from rag_engine import rag_engine

app = FastAPI(title="Aegis Serving API", description="High-throughput AI Inference with dynamic RAG")

class PredictionRequest(BaseModel):
    model_id: str
    prompt: str
    prompt_tokens: int = 100 # Default to 100 if not provided

class IngestRequest(BaseModel):
    document_text: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "model-serving-api"}

@app.post("/api/v1/knowledge-base/ingest")
async def ingest_document(req: IngestRequest):
    try:
        chunk_count = rag_engine.ingest(req.document_text)
        return {"status": "success", "chunks_indexed": chunk_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict(req: PredictionRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
    # ── RAG Step: Context-Aware Retrieval (Phase 5/6) ─────────────────────
    context, distances = rag_engine.retrieve(req.prompt, req.prompt_tokens)
    
    # ── Inference Step (Simulated) ────────────────────────────────────────
    confidence = round(random.uniform(0.92, 0.99), 4)
    prediction_class = "Success" if context else "Inferred"
    
    return {
        "model_id": req.model_id,
        "prediction": prediction_class,
        "confidence": confidence,
        "context_retrieved": context,
        "semantic_distances": distances,
        "latency_ms": random.randint(45, 120)
    }
