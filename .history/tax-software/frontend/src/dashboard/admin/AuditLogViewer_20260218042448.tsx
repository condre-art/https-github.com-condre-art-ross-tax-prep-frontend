import React from 'react';
import Card from '../shared/Card';

// Example: Pass audit log entries as props
export default function AuditLogViewer({ entries = [] }) {
  return (
    <Card title="Audit Log">
      <div className="audit-log-list">
        {entries.length === 0 ? (
          <div>No audit log entries.</div>
        ) : (
          <table className="audit-log-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>User</th>
                <th>Action</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((e, i) => (
                <tr key={i}>
                  <td>{new Date(e.time).toLocaleString()}</td>
                  <td>{e.user}</td>
                  <td>{e.action}</td>
                  <td>{e.details}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </Card>
  );
}
