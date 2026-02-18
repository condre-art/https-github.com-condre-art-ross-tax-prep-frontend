
import React, { useEffect, useState } from 'react';
import Card from '../shared/Card';
import NotificationCenter from '../shared/NotificationCenter';
import AuditLogViewer from '../admin/AuditLogViewer';
import ChatWidget from '../shared/ChatWidget';
import ExpectedRefundWidget from './ExpectedRefundWidget';

export default function ClientWidgets() {
  const [notifications, setNotifications] = useState([]);
  const [auditLog, setAuditLog] = useState([]);
  const [refund, setRefund] = useState(null);
  const [chat, setChat] = useState([]);

  useEffect(() => {
    fetch('/api/notifications').then(r => r.json()).then(setNotifications);
    fetch('/api/audit-log').then(r => r.json()).then(setAuditLog);
    fetch('/api/expected-refund').then(r => r.json()).then(setRefund);
    fetch('/api/chat').then(r => r.json()).then(setChat);
  }, []);

  return (
    <div className="client-widgets">
      {refund && <ExpectedRefundWidget {...refund} />}
      <NotificationCenter notifications={notifications} />
      <AuditLogViewer entries={auditLog} />
      <ChatWidget initialMessages={chat} />
    </div>
  );
}
