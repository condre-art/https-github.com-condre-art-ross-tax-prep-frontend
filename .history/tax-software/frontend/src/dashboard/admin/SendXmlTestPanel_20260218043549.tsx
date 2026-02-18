import React, { useState } from 'react';
import Card from '../shared/Card';

export default function SendXmlTestPanel() {
  const [xml, setXml] = useState('<Return><TaxYear>2025</TaxYear></Return>');
  const [year, setYear] = useState('2025');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  function handleSend() {
    setLoading(true);
    setError('');
    setResult('');
    fetch('/api/irs/send-xml-test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ xml, year })
    })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') setResult(data.message);
        else setError(data.message || 'Failed to send XML.');
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to send XML.');
        setLoading(false);
      });
  }

  return (
    <Card title="Send IRS Test XML (2025)">
      <div className="send-xml-test-panel">
        <textarea
          className="input"
          rows={6}
          value={xml}
          onChange={e => setXml(e.target.value)}
          placeholder="Paste XML here"
        />
        <input
          className="input"
          placeholder="Tax Year"
          value={year}
          onChange={e => setYear(e.target.value)}
        />
        <button className="button" onClick={handleSend} disabled={loading || !xml || !year}>
          Send Test XML
        </button>
        {loading && <div>Sending...</div>}
        {result && <div className="send-xml-test-success">{result}</div>}
        {error && <div className="send-xml-test-error">{error}</div>}
      </div>
    </Card>
  );
}
