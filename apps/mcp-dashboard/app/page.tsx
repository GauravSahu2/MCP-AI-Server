'use client';
import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [models, setModels] = useState<any[]>([]);
  const [inferenceResult, setInferenceResult] = useState<string | null>(null);
  const [modelName, setModelName] = useState('');
  const [modelFramework, setModelFramework] = useState('PyTorch');

  // In production, this token comes from NextAuth/Zitadel login
  // For development, use the token from bootstrap_token.txt
  const DEV_TOKEN = process.env.NEXT_PUBLIC_DEV_TOKEN || "PASTE_YOUR_BOOTSTRAP_TOKEN_HERE";
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

  const fetchModels = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/models`, {
        headers: { 'Authorization': `Bearer ${DEV_TOKEN}` }
      });
      if (res.ok) {
        const data = await res.json();
        setModels(data.models || []);
      }
    } catch (err) {
      console.error("Failed to fetch models:", err);
    }
  };

  useEffect(() => {
    fetchModels();
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      name: modelName,
      version: "v1.0",
      description: "Deployed via Aegis Dashboard",
      framework: modelFramework,
      s3_uri: `s3://aegis-models/${modelName.toLowerCase().replace(/ /g, '-')}`
    };

    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/models`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${DEV_TOKEN}`
        },
        body: JSON.stringify(payload)
      });
      
      if (res.ok) {
        setModelName('');
        fetchModels(); // Refresh live topology
      }
    } catch (err) {
      console.error("Registration failed:", err);
    }
  };

  const handleSimulateInference = async () => {
    setInferenceResult('Calling Sovereign Serving Plane... [RED Metrics Active]');
    try {
      // Simulate real inference through the serving API
      const res = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model_id: models[0]?.id || 'aegis-default-v1',
          prompt: "Verify the high-assurance state of the current cluster."
        })
      });
      const data = await res.json();
      setInferenceResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setInferenceResult("Inference failed: Ensure Serving API is running.");
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Aegis AI Control Center</h1>
        <p>100% Metric Compliance Dashboard</p>
      </div>

      <div className="grid-2">
        <div className="glass-panel">
          <h2>Register Model</h2>
          <form onSubmit={handleRegister}>
            <div className="input-block">
              <label>Model Name</label>
              <input 
                type="text" 
                placeholder="e.g. Fraud Detection 4.0" 
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                required
              />
            </div>
            <div className="input-block">
              <label>Engine Framework</label>
              <select value={modelFramework} onChange={(e) => setModelFramework(e.target.value)}>
                <option>PyTorch</option>
                <option>HuggingFace</option>
                <option>OpenAI API</option>
                <option>TensorFlow</option>
              </select>
            </div>
            <button className="btn" type="submit">Deploy to Registry</button>
          </form>
        </div>

        <div className="glass-panel">
          <h2>RAG Inference Plane</h2>
          <p style={{marginBottom: '1.5rem'}}>Trigger high-assurance vector retrieval against the serving API.</p>
          <button className="btn" onClick={handleSimulateInference}>
            Execute Request
          </button>
          
          {inferenceResult && (
            <div className="result-box" style={{ whiteSpace: 'pre-wrap' }}>
              {inferenceResult}
            </div>
          )}
        </div>

        <div className="glass-panel" style={{ gridColumn: '1 / -1' }}>
          <h2>Global Topology (Live PostgreSQL State)</h2>
          <div className="model-list">
            {models.length === 0 && <p style={{color: 'var(--text-muted)'}}>No models detected. Register your first model to begin.</p>}
            {models.map(m => (
              <div className="model-card" key={m.id}>
                <div>
                  <div className="model-card-title">{m.name || m.spec?.name}</div>
                  <div style={{fontSize: '0.875rem', color: 'var(--text-muted)'}}>
                    {m.framework || m.spec?.framework} | {m.id}
                  </div>
                </div>
                <div className="model-badge">{m.status}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
