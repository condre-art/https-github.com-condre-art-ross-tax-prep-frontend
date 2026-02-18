import React from 'react';
import Card from '../shared/Card';

// Example props: refundAmount, status, lastUpdated
export default function ExpectedRefundWidget({ refundAmount, status, lastUpdated }) {
  return (
    <Card title="Expected Refund">
      <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2e7d32' }}>
        ${refundAmount?.toLocaleString() || '0.00'}
      </div>
      <div>Status: <b>{status || 'Pending'}</b></div>
      <div style={{ fontSize: '0.9rem', color: '#888' }}>
        Last updated: {lastUpdated ? new Date(lastUpdated).toLocaleString() : 'N/A'}
      </div>
    </Card>
  );
}
