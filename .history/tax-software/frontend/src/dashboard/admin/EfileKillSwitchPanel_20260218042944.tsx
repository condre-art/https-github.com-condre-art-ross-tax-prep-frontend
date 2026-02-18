import React, { useState, useEffect } from 'react';
import Card from '../shared/Card';

export default function EfileKillSwitchPanel() {
  const [enabled, setEnabled] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/efile/kill-switch')
      .then(r => r.json())
      .then(data => setEnabled(data.enabled))
      .catch(() => setError('Failed to fetch kill switch status.'));
  }, []);

  function toggleKillSwitch() {
    setLoading(true);
    setError('');
    fetch('/api/efile/kill-switch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled: !enabled })
    })
      .then(r => r.json())
      .then(data => {
        setEnabled(data.enabled);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to update kill switch.');
        setLoading(false);
      });
  }

  return (
    <Card title="E-file Transmission Kill Switch">
      <div className="efile-kill-switch-panel">
        <div>Status: <b style={{ color: enabled ? 'green' : 'red' }}>{enabled ? 'ENABLED' : 'DISABLED'}</b></div>
        <button className="button" onClick={toggleKillSwitch} disabled={loading}>
          {enabled ? 'Disable E-file Transmission' : 'Enable E-file Transmission'}
        </button>
        {loading && <div>Updating...</div>}
        {error && <div className="efile-kill-switch-error">{error}</div>}
      </div>
    </Card>
  );
}
