import React, { useState } from 'react';
import Card from '../shared/Card';

export default function IRSEfileWidget() {
  const [eroId, setEroId] = useState('');
  const [cert, setCert] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function handleGenerate() {
    setLoading(true);
    setError('');
    fetch('/api/irs/generate_cert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ero_id: eroId })
    })
      .then(r => r.json())
      .then(data => {
        setCert(data);
        setLoading(false);
      })
      .catch(e => {
        setError('Failed to generate certificate.');
        setLoading(false);
      });
  }

  function handleGet() {
    setLoading(true);
    setError('');
    fetch(`/api/irs/get_cert?ero_id=${encodeURIComponent(eroId)}`)
      .then(r => r.json())
      .then(data => {
        setCert(data);
        setLoading(false);
      })
      .catch(e => {
        setError('Failed to retrieve certificate.');
        setLoading(false);
      });
  }

  return (
    <Card title="IRS E-file Certificate">
      <div style={{ marginBottom: 12 }}>
        <input
          className="input"
          placeholder="ERO ID"
          value={eroId}
          onChange={e => setEroId(e.target.value)}
        />
        <button className="button" onClick={handleGenerate} disabled={loading || !eroId}>
          Generate Cert
        </button>
        <button className="button" onClick={handleGet} disabled={loading || !eroId} style={{ marginLeft: 8 }}>
          Get Cert
        </button>
      </div>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {cert && (
        <pre style={{ background: '#eee', padding: 8, borderRadius: 8, color: '#222' }}>{JSON.stringify(cert, null, 2)}</pre>
      )}
    </Card>
  );
}
