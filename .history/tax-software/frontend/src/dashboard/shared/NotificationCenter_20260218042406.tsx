import React, { useState } from 'react';
import Card from '../shared/Card';

export default function NotificationCenter({ notifications = [] }) {
  const [read, setRead] = useState([]);
  function markAsRead(id) {
    fetch('/api/notifications/mark-read', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    }).then(() => setRead([...read, id]));
  }
  return (
    <Card title="Notifications">
      <div style={{ maxHeight: 200, overflowY: 'auto' }}>
        {notifications.length === 0 ? (
          <div>No notifications.</div>
        ) : (
          notifications.map(n => (
            <div key={n.id} style={{ background: read.includes(n.id) || n.read ? '#eee' : '#fff', padding: 8, marginBottom: 4 }}>
              <b>{n.title}</b>
              <div>{n.body}</div>
              <div style={{ fontSize: '0.8rem', color: '#888' }}>{new Date(n.time).toLocaleString()}</div>
              {!read.includes(n.id) && !n.read && <button onClick={() => markAsRead(n.id)}>Mark as read</button>}
            </div>
          ))
        )}
      </div>
    </Card>
  );
}
