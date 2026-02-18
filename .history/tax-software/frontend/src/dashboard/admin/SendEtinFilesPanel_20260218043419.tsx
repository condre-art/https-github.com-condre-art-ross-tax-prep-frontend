import React, { useState } from 'react';
import Card from '../shared/Card';

const PRESETS = [
  { etin: '12181', mode: 'production', label: '12181 (Production)' },
  { etin: '95409', mode: 'production', label: '95409 (Production)' },
  { etin: '95410', mode: 'test', label: '95410 (Test)' },
];

export default function SendEtinFilesPanel() {
  const [etin, setEtin] = useState('12181');
  const [mode, setMode] = useState('production');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  function handleSend() {
    setLoading(true);
    setError('');
    setResult('');
    fetch('/api/irs/send-etin-files', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ etin, mode })
    })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') setResult(data.message);
        else setError(data.message || 'Failed to send files.');
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to send files.');
        setLoading(false);
      });
  }

  return (
    <Card title="Send IRS ETIN Files">
      <div className="send-etin-files-panel">
        <div style={{ marginBottom: 8 }}>
          <label>Preset: </label>
          <select
            value={`${etin}|${mode}`}
            onChange={e => {
              const [eVal, mVal] = e.target.value.split('|');
              setEtin(eVal); setMode(mVal);
            }}
          >
            {PRESETS.map(p => (
              <option key={p.label} value={`${p.etin}|${p.mode}`}>{p.label}</option>
            ))}
          </select>
        </div>
        <input
          className="input"
          placeholder="ETIN"
          value={etin}
          onChange={e => setEtin(e.target.value)}
        />
        <select className="input" value={mode} onChange={e => setMode(e.target.value)}>
          <option value="production">Production</option>
          <option value="test">Test</option>
        </select>
        <button className="button" onClick={handleSend} disabled={loading || !etin}>
          Send Files
        </button>
        {loading && <div>Sending...</div>}
        {result && <div className="send-etin-files-success">{result}</div>}
        {error && <div className="send-etin-files-error">{error}</div>}
      </div>
    </Card>
  );
}
