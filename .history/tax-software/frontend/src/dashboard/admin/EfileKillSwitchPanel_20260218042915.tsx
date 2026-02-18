import React, { useState } from 'react';
import Card from '../shared/Card';

export default function EfileKillSwitchPanel() {
  const [enabled, setEnabled] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');

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
        setStatus(data.message || '');
        setLoading(false);
      })
      .catch(e => {
        setError('Failed to update kill switch.');
        setLoading(false);
      });
  }

  // On mount, fetch current state
  React.useEffect(() => {
    fetch('/api/efile/kill-switch')
      .then(r => r.json())
      .then(data => setEnabled(data.enabled))
      .catch(() => setEnabled(true));
  }, []);

  return (
    <Card title="E-file Transmission Kill Switch">
      <div className="efile-kill-switch-panel">
        <div className="efile-kill-switch-status">
          <b>Status:</b> {enabled ? <span className="efile-enabled">E-file Transmission ENABLED</span> : <span className="efile-disabled">E-file Transmission DISABLED</span>}
        </div>
        <button className="button efile-kill-switch-btn" onClick={toggleKillSwitch} disabled={loading}>
          {enabled ? 'Disable E-file Transmission' : 'Enable E-file Transmission'}
        </button>
        {loading && <div>Updating...</div>}
        {error && <div className="efile-kill-switch-error">{error}</div>}
        {status && <div className="efile-kill-switch-status-msg">{status}</div>}
      </div>
    </Card>
  );
}
