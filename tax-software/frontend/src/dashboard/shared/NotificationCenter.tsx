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
      <div className="notification-list">
        {notifications.length === 0 ? (
          <div>No notifications.</div>
        ) : (
          notifications.map(n => (
            <div
              key={n.id}
              className={`notification-item${read.includes(n.id) || n.read ? ' read' : ''}`}
            >
              <b>{n.title}</b>
              <div>{n.body}</div>
              <div className="notification-time">{new Date(n.time).toLocaleString()}</div>
              {!read.includes(n.id) && !n.read && <button className="button" onClick={() => markAsRead(n.id)}>Mark as read</button>}
            </div>
          ))
        )}
      </div>
    </Card>
  );
}
