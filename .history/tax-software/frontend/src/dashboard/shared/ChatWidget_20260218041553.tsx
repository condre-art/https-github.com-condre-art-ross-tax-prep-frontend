import React, { useState } from 'react';
import Card from '../shared/Card';

export default function ChatWidget() {
  const [messages, setMessages] = useState([
    { from: 'Staff', text: 'Welcome! How can we help you today?' }
  ]);
  const [input, setInput] = useState('');

  function sendMessage() {
    if (input.trim()) {
      setMessages([...messages, { from: 'You', text: input }]);
      setInput('');
      // TODO: Integrate with backend or chat service
    }
  }

  return (
    <Card title="Chat">
      <div style={{ minHeight: 100, maxHeight: 200, overflowY: 'auto', marginBottom: 8 }}>
        {messages.map((msg, i) => (
          <div key={i}><b>{msg.from}:</b> {msg.text}</div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && sendMessage()}
        placeholder="Type a message..."
        style={{ width: '80%' }}
      />
      <button onClick={sendMessage} style={{ marginLeft: 8 }}>Send</button>
    </Card>
  );
}
