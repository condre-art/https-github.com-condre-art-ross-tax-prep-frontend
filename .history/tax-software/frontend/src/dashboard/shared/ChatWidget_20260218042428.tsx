import React, { useState } from 'react';
import Card from '../shared/Card';

export default function ChatWidget({ initialMessages = [] }) {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState('');

  function sendMessage() {
    if (input.trim()) {
      const msg = { from: 'You', text: input };
      setMessages([...messages, msg]);
      fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(msg)
      });
      setInput('');
    }
  }

  return (
    <Card title="Chat">
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i}><b>{msg.from}:</b> {msg.text}</div>
        ))}
      </div>
      <input
        className="chat-input"
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && sendMessage()}
        placeholder="Type a message..."
      />
      <button className="button chat-send" onClick={sendMessage}>Send</button>
    </Card>
  );
}
