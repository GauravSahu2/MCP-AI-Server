# apps/model-serving-api/rag_engine.py
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RagEngine:
    def __init__(self):
        # Using BGE-M3 (small-en-v1.5) for high-performance embeddings
        self.model = SentenceTransformer('BAAI/bge-small-en-v1.5')
        self.dimension = 384
        self.use_milvus = os.getenv("USE_MILVUS", "false").lower() == "true"
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )
        
        # Local FAISS as high-assurance fallback
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        
        # Initial seeding
        self.ingest("Aegis system is a high-assurance AI orchestration platform.")
        print("RagEngine initialized with BGE-M3 and FAISS fallback.")

    def ingest(self, raw_text: str):
        chunks = self.text_splitter.split_text(raw_text)
        embeddings = self.model.encode(chunks)
        self.index.add(np.array(embeddings).astype('float32'))
        self.metadata.extend(chunks)
        return len(chunks)

    def retrieve(self, query: str, prompt_tokens: int, model_limit: int = 4000):
        # ── Phase 6: Dynamic Intelligence Optimization ───────────────────────
        # Prevent token overflow by calculating safe allowance
        safe_token_allowance = model_limit - prompt_tokens - 500 # 500 buffer for output
        max_safe_k = max(1, int(safe_token_allowance / 125)) # Approx 125 tokens per chunk
        
        query_vector = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vector, max_safe_k)
        
        # Filter out invalid indices and map to metadata
        results = [self.metadata[i] for i in indices[0] if i != -1 and i < len(self.metadata)]
        return results, distances[0].tolist()

rag_engine = RagEngine()
