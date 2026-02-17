import React from 'react';

interface CardProps {
  title: string;
  children: React.ReactNode;
}

export default function Card({ title, children }: CardProps) {
  return (
    <div className="dashboard-card ios-theme">
      <h2>{title}</h2>
      <div>{children}</div>
    </div>
  );
}
