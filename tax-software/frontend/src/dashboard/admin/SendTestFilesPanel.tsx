import React, { useState } from 'react';
import Card from '../shared/Card';

export default function SendTestFilesPanel() {
  const [efin, setEfin] = useState('748335');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  function handleSend() {
    setLoading(true);
    setError('');
    setResult('');
    fetch('/api/irs/send-test-files', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ efin })
    })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') setResult(data.message);
        else setError(data.message || 'Failed to send test files.');
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to send test files.');
        setLoading(false);
      });
  }

  return (
    <Card title="Send IRS Test Files">
      <div className="send-test-files-panel">
        <input
          className="input"
          placeholder="EFIN"
          value={efin}
          onChange={e => setEfin(e.target.value)}
        />
        <button className="button" onClick={handleSend} disabled={loading || !efin}>
          Send Test Files
        </button>
        {loading && <div>Sending...</div>}
        {result && <div className="send-test-files-success">{result}</div>}
        {error && <div className="send-test-files-error">{error}</div>}
      </div>
    </Card>
  );
}
