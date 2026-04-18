'use client';
import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [models, setModels] = useState<any[]>([]);
  const [inferenceResult, setInferenceResult] = useState<string | null>(null);

  // Form states
  const [modelName, setModelName] = useState('');
  const [modelFramework, setModelFramework] = useState('PyTorch');

  // Load dummy models or fetch from control plane (mocked for visual interaction)
  useEffect(() => {
    setModels([
      { id: '1a2b-3c4d', spec: { name: 'fraud-detector-v1', framework: 'PyTorch' }, status: 'PRODUCTION' },
      { id: '9f8e-7d6c', spec: { name: 'llama-3-8b-instruct', framework: 'HuggingFace' }, status: 'STAGING' }
    ]);
  }, []);

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    const newModel = {
      id: Math.random().toString(36).substring(7),
      spec: { name: modelName, framework: modelFramework },
      status: 'REGISTERED'
    };
    setModels([...models, newModel]);
    setModelName('');
  };

  const handleSimulateInference = async () => {
    // Simulate RAG inference latency
    setInferenceResult('Running vector sequence... [L2 Metric]');
    setTimeout(() => {
      setInferenceResult(JSON.stringify({
        model_id: models[0]?.id || 'unknown',
        prediction: 'Anomaly',
        confidence: 0.9632,
        rag_context_results: 3,
        latency_ms: 84
      }, null, 2));
    }, 800);
  };

  return (
    <div className="container">
      <div className="header">
        <h1>AI Hub Control Center</h1>
        <p>High-Assurance AI Architecture Platform</p>
      </div>

      <div className="grid-2">
        {/* Registry Config Panel */}
        <div className="glass-panel">
          <h2>Register Model</h2>
          <form onSubmit={handleRegister}>
            <div className="input-block">
              <label>Model Identifier</label>
              <input 
                type="text" 
                placeholder="e.g. gpt-4-turbo" 
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                required
              />
            </div>
            <div className="input-block">
              <label>Framework Provider</label>
              <select value={modelFramework} onChange={(e) => setModelFramework(e.target.value)}>
                <option>PyTorch</option>
                <option>HuggingFace</option>
                <option>OpenAI API</option>
                <option>TensorFlow</option>
              </select>
            </div>
            <button className="btn" type="submit">Establish Connection</button>
          </form>
        </div>

        {/* Inference Testing Panel */}
        <div className="glass-panel">
          <h2>RAG Inference Simulator</h2>
          <p style={{marginBottom: '1.5rem'}}>Trigger vector embedding queries against the core AI serving plane.</p>
          <button className="btn" onClick={handleSimulateInference}>
            Execute Target Payload
          </button>
          
          {inferenceResult && (
            <div className="result-box">
              {inferenceResult}
            </div>
          )}
        </div>

        {/* Global Registry Viewer */}
        <div className="glass-panel" style={{ gridColumn: '1 / -1' }}>
          <h2>Live Topology (Control Plane Database)</h2>
          <div className="model-list">
            {models.map(m => (
              <div className="model-card" key={m.id}>
                <div>
                  <div className="model-card-title">{m.spec.name}</div>
                  <div style={{fontSize: '0.875rem', color: 'var(--text-muted)'}}>
                    {m.spec.framework} | ID: {m.id}
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
