import React from 'react';

interface HeaderProps {
  title: string;
}

export default function Header({ title }: HeaderProps) {
  return (
    <header className="dashboard-header ios-theme">
      <h1>{title}</h1>
    </header>
  );
}
